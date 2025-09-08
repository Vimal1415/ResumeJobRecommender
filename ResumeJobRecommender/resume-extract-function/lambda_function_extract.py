import boto3
import json

REGION = "ap-south-1"
textract = boto3.client('textract', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)

PARSER_LAMBDA_NAME = "ResumeParserFunction"  
def lambda_handler(event, context):
    print("Extract Lambda triggered. Event:", json.dumps(event))

    try:
        record = event['Records'][0]['s3']
        bucket_name = record['bucket']['name']
        object_key = record['object']['key']
        print(f"Processing file: {object_key} from bucket: {bucket_name}")

        # Textract
        response = textract.detect_document_text(
            Document={'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
        )
        print("Textract response received.")

        # Extract text
        extracted_text = ""
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                extracted_text += block['Text'] + "\n"
        print(f"Extracted {len(extracted_text)} characters of text.")

        # Save extracted text in S3
        text_key = object_key.replace("resumes/", "text/") + ".txt"
        s3.put_object(
            Bucket=bucket_name,
            Key=text_key,
            Body=extracted_text.encode('utf-8')
        )
        print(f"Text saved to: {text_key}")

        # Call Parser Lambda
        payload = {
            "resume_text": extracted_text,
            "filename": object_key
        }
        print("Invoking Parser Lambda...")
        parser_response = lambda_client.invoke(
            FunctionName=PARSER_LAMBDA_NAME,
            InvocationType='RequestResponse',  # Wait for Parser response
            Payload=json.dumps(payload)
        )

        parser_result = json.loads(parser_response['Payload'].read().decode('utf-8'))
        print("Parser Lambda response:", parser_result)

        return {
            "statusCode": 200,
            "body": f"Extracted text saved as {text_key}, Parser response: {parser_result}"
        }

    except Exception as e:
        print(f"ERROR in Extract Lambda: {str(e)}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
