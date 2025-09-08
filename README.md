# Automated Resume Job Recommendation System

A serverless AWS-powered project that extracts resume data, parses job listings, and provides **automated job recommendations** based on resume content.  
Built entirely on AWS Lambda, DynamoDB, and S3, this backend system demonstrates cloud-native architecture for intelligent automation.

---

## Features
- 🔹 Upload resumes via API – automatically stored in **Amazon S3**
- 🔹 Text extraction from PDFs using **AWS Lambda**
- 🔹 Resume parsing and structured storage in **DynamoDB**
- 🔹 Automated job recommendations using **JobRecommenderLambda**
- 🔹 Recommendations saved in a separate **JobRecommendations** table
- 🔹 Fully serverless – scales with AWS Lambda

---

## Tech Stack
- **Backend:** AWS Lambda (Python 3.11)
- **Database:** Amazon DynamoDB
- **Storage:** Amazon S3
- **Orchestration:** Lambda-to-Lambda invocation
- **Infrastructure:** IAM Roles & Policies
- **Language:** Python

---

## 📂 Project Structure
