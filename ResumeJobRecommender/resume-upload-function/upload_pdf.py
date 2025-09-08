import requests
import base64

# 1️⃣ Replace with your API endpoint
API_URL = "https://pyiq63ob4k.execute-api.ap-south-1.amazonaws.com/prod/upload"

# 2️⃣ Replace with the path to your PDF
pdf_file_path = r"C:\Users\chees\OneDrive\Desktop\project_cloud\Vimal_Resume.pdf"

# 3️⃣ Read PDF and encode to base64
with open(pdf_file_path, "rb") as f:
    encoded_pdf = base64.b64encode(f.read()).decode("utf-8")

# 4️⃣ Prepare JSON payload
payload = {
    "body": encoded_pdf
}

# 5️⃣ Send POST request
response = requests.post(API_URL, json=payload)

# 6️⃣ Print response
print("Status Code:", response.status_code)
print("Response Body:", response.text)
