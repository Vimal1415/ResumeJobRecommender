import boto3
import json
from decimal import Decimal
from datetime import datetime

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
resume_table = dynamodb.Table('ResumeData')
jobs_table = dynamodb.Table('JobListings')
recommendations_table = dynamodb.Table('JobRecommendations')

def calculate_score(resume_data, job):
    """Calculate weighted score between a resume and job posting."""
    resume_skills = set([s.lower() for s in resume_data.get("skills", [])])
    job_skills = set([s.lower() for s in job.get("skills_required", [])])
    domain = job.get("domain", "").lower()
    seniority = job.get("seniority", "").lower()
    location = job.get("location", "").lower()
    
    # Extract relevant resume info
    resume_text = (resume_data.get("raw_text_full", "")).lower()
    resume_seniority = (resume_data.get("seniority_estimate", "")).lower()

    # ---- Weight Config ----
    WEIGHT_SKILLS = 60
    WEIGHT_DOMAIN = 20
    WEIGHT_SENIORITY = 10
    WEIGHT_LOCATION = 10

    # ---- Skills Matching ----
    skill_score = (len(resume_skills & job_skills) / len(job_skills) * WEIGHT_SKILLS) if job_skills else 0

    # ---- Domain Match ----
    domain_score = WEIGHT_DOMAIN if domain and domain in resume_text else 0

    # ---- Seniority Match ----
    seniority_score = WEIGHT_SENIORITY if seniority and seniority in resume_seniority else 0

    # ---- Location Match ----
    location_score = WEIGHT_LOCATION if location and location in resume_text else 0

    total_score = skill_score + domain_score + seniority_score + location_score
    return total_score

def lambda_handler(event, context):
    try:
        # Get resume_id
        resume_id = event.get("resume_id")
        if not resume_id:
            return {"statusCode": 400, "body": "Missing resume_id in event"}

        # Fetch resume data
        resume_resp = resume_table.get_item(Key={"resume_id": resume_id})
        resume_data = resume_resp.get("Item")
        if not resume_data:
            return {"statusCode": 404, "body": f"No resume found for {resume_id}"}

        # Fetch all jobs
        job_resp = jobs_table.scan()
        job_list = job_resp.get("Items", [])

        # Score and rank jobs
        scored_jobs = []
        for job in job_list:
            score = calculate_score(resume_data, job)
            scored_jobs.append((score, job))

        # Sort and pick top 5
        scored_jobs.sort(key=lambda x: x[0], reverse=True)
        top_jobs = [{"score": Decimal(str(round(score, 2))), **job} for score, job in scored_jobs[:5]]

        # Store recommendations in DynamoDB
        recommendations_table.put_item(
            Item={
                "resume_id": resume_id,
                "recommendations": top_jobs,
                "generated_at": datetime.utcnow().isoformat()
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "resume_id": resume_id,
                "recommendations": top_jobs
            }, default=str)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": str(e)}
