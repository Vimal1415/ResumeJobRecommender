# 🧠 Automated Job Recommendation System (Serverless on AWS)

A **fully serverless backend system** that parses resumes, extracts candidate skills, and automatically generates **top 5 personalized job recommendations** in real-time.  
Built using **AWS Lambda, S3, DynamoDB, and Python**, this system is designed for scalability and automation — no manual intervention required.

---

## 🚀 Features
- 📂 **Resume Upload Pipeline**: Upload resumes to S3 and trigger an automated workflow.
- 🔍 **Resume Text Extraction**: Extract raw text from uploaded PDF or DOCX files using AWS Lambda.
- 📝 **Resume Parsing**: Parse candidate details (name, email, phone, skills, education, projects, seniority estimate) and save structured data to DynamoDB.
- 🤖 **Job Recommendation Engine**: Match candidate skills with job listings and store top 5 recommendations in DynamoDB.
- 🔗 **Lambda-to-Lambda Automation**: Serverless orchestration of multiple Lambda functions for full automation.
- ☁️ **AWS-Native Architecture**: Scalable, event-driven design using S3 triggers, Lambda, and DynamoDB.

---

## 🛠️ Tech Stack
| Component            | Technology Used                        |
|----------------------|---------------------------------------|
| **Language**         | Python 3.11                           |
| **Cloud Platform**   | AWS                                   |
| **Compute**          | AWS Lambda                           |
| **Storage**          | Amazon S3, Amazon DynamoDB           |
| **Orchestration**    | Lambda-to-Lambda Invocation          |
| **Data Processing**  | Regex, NLP-based skill extraction     |

---

## 📦 Project Structure
```bash
automated-job-recommendation/
│
├── lambdas/
│   ├── resume-upload-function/        # Handles resume uploads and stores them in S3
│   │   └── lambda_function.py
│   ├── resume-extract-function/       # Extracts text from resumes
│   │   └── lambda_function.py
│   ├── ResumeParserFunction/          # Parses resume and stores data in DynamoDB
│   │   └── lambda_function.py
│   └── JobRecommenderLambda/          # Generates job recommendations
│       └── lambda_function.py
│
├── dynamodb-tables/
│   ├── ResumeData.json                # Sample ResumeData table schema
│   ├── JobListings.json               # Sample JobListings table schema
│   └── JobRecommendations.json        # Sample JobRecommendations schema
│
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
