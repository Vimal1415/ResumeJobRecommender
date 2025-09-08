import json
import re
import uuid
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('ResumeData')
lambda_client = boto3.client('lambda')

# Job Recommender Lambda name
JOB_RECOMMENDER = "JobRecommenderLambda"

SKILL_TOKENS = [
    "python","c++","java","javascript","html","css","react","node.js","node","express",
    "scikit-learn","tensorflow","keras","pytorch","xgboost","opencv","numpy","pandas",
    "matplotlib","mongodb","rest","api","oauth","jwt","linux","arduino","git","github",
    "tailwind","esp32","nlp","tf-idf","docker","aws","sql","mern","react.js","express.js"
]

def extract_email(text):
    m = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return m.group(0) if m else None

def extract_phone(text):
    m = re.search(r'(\+?\d{1,3}[-\s]?)?(\d{10}|\d{5}[-\s]\d{5})', text)
    return m.group(0) if m else None

def extract_education(text):
    lines = text.splitlines()
    return [L.strip() for L in lines if re.search(
        r'\b(b\.?tech|bachelor|m\.?tech|master|high school|class 12|class 10)\b', L, re.I)]

def extract_projects(text):
    lines = text.splitlines()
    projects = []
    for i, L in enumerate(lines):
        if re.search(r'\b(project|research|intern)\b', L, re.I):
            window = " ".join(lines[i:i+3]).strip()
            projects.append(window)
    return projects

def extract_skills(text):
    tl = text.lower()
    return sorted(set(token for token in SKILL_TOKENS if token in tl))

def estimate_seniority(text):
    t = text.lower()
    if re.search(r'\b(final-?year|student|intern)\b', t):
        return "Entry / New Graduate / Intern"
    if re.search(r'\b(years? of experience|experienced|senior)\b', t):
        return "Mid / Senior"
    return "Not specified"

def lambda_handler(event, context):
    print("Parser Lambda triggered. Event:", json.dumps(event))

    try:
        resume_text = event.get('resume_text') or ""
        filename = event.get('filename', "unknown_file")

        if not resume_text:
            return {"statusCode": 400, "body": "No resume_text found in event."}

        lines = [L.strip() for L in resume_text.splitlines() if L.strip()]
        name = lines[0] if lines else "Unknown"

        resume_id = str(uuid.uuid4())
        item = {
            "resume_id": resume_id,
            "filename": filename,
            "name": name,
            "email": extract_email(resume_text),
            "phone": extract_phone(resume_text),
            "skills": extract_skills(resume_text),
            "education": extract_education(resume_text),
            "projects": extract_projects(resume_text),
            "seniority_estimate": estimate_seniority(resume_text),
            "raw_text_snippet": resume_text[:200],
            "raw_text_full": resume_text,
            "created_at": datetime.utcnow().isoformat()
        }

        # Save resume data to DynamoDB
        table.put_item(Item=item)
        print(f"✅ Saved resume {resume_id} to DynamoDB.")

        # Call JobRecommenderLambda to get recommendations
        print(f"🔹 Invoking JobRecommenderLambda for resume_id {resume_id}...")
        response = lambda_client.invoke(
            FunctionName=JOB_RECOMMENDER,
            InvocationType="RequestResponse",
            Payload=json.dumps({"resume_id": resume_id})
        )

        recommender_payload = json.loads(response['Payload'].read())
        recommendations = json.loads(recommender_payload.get("body", "{}")).get("recommendations", [])

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Resume parsed and recommendations generated.",
                "resume_id": resume_id,
                "recommendations": recommendations
            })
        }

    except Exception as e:
        print(f"❌ ERROR in Parser Lambda: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
