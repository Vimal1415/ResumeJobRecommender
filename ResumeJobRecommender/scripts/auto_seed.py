import boto3
import uuid
import random
import sys
print("Starting")
# --------------------------
# DynamoDB setup
# --------------------------
REGION = "ap-south-1"
TABLE_NAME = "JobListings"

try:
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table(TABLE_NAME)
    print(f"✅ Connected to DynamoDB table: {TABLE_NAME} in region {REGION}")
except Exception as e:
    print(f"❌ Failed to connect to DynamoDB: {e}")
    sys.exit(1)

# --------------------------
# Sample data pools
# --------------------------
job_titles = [
    "Machine Learning Engineer", "Data Scientist", "Backend Developer", 
    "Frontend Developer", "Full Stack Engineer", "Cloud Engineer", 
    "IoT Engineer", "DevOps Engineer", "Security Analyst", 
    "AI Researcher", "Software Engineer", "Mobile App Developer",
    "Database Administrator", "Cybersecurity Specialist", "Data Engineer"
]

companies = [
    "TechCorp", "Webify", "DataWorks", "InsightAI", "SmartEdge", 
    "CloudNet", "SecureX", "Innovatech", "CodeCrafters", "AI Labs"
]

domains = [
    "AI/ML", "Data Science", "Web Development", "Cloud Computing", 
    "IoT", "Cybersecurity", "Mobile Development", "DevOps"
]

skills_pool = [
    "python", "java", "c++", "javascript", "typescript", "react", "angular", 
    "node", "express", "mongodb", "sql", "aws", "docker", "kubernetes", 
    "tensorflow", "pytorch", "linux", "html", "css", "tailwind", 
    "arduino", "esp32", "spark", "hadoop", "flask", "django"
]

seniority_levels = [
    "Entry / New Graduate / Intern",
    "Mid / Senior (has experience)"
]

locations = [
    "Bangalore", "Hyderabad", "Chennai", "Pune", "Remote", 
    "Delhi", "Mumbai", "Kolkata"
]

# --------------------------
# Functions
# --------------------------
def generate_random_job():
    """Generate a random job item."""
    return {
        "job_id": str(uuid.uuid4()),
        "title": random.choice(job_titles),
        "company": random.choice(companies),
        "domain": random.choice(domains),
        "location": random.choice(locations),
        "seniority": random.choice(seniority_levels),
        "skills_required": random.sample(skills_pool, random.randint(4, 7))
    }

def seed_jobs(count=100):
    """Seed DynamoDB with random jobs and log success/failure."""
    success_count = 0
    failure_count = 0

    for i in range(count):
        job = generate_random_job()
        try:
            table.put_item(Item=job)
            print(f"✅ [{i+1}/{count}] Added job: {job['title']} at {job['company']}")
            success_count += 1
        except Exception as e:
            print(f"❌ [{i+1}/{count}] Failed to add job: {e}")
            failure_count += 1

    print("\n---------------------------")
    print(f"✅ Jobs successfully added: {success_count}")
    print(f"❌ Jobs failed to add: {failure_count}")
    print("---------------------------")

# --------------------------
# Main
# --------------------------
if __name__ == "__main__":
    try:
        seed_jobs(100)  # You can change the number here
    except Exception as e:
        print(f"❌ Fatal error during seeding: {e}")
