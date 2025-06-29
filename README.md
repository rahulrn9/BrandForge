# BrandForge

A scalable, brand-tailored, customer-facing content generation platform leveraging AWS Bedrock, LlamaIndex, DynamoDB, React, Docker, Jenkins, and Power BI.

---

## Features

- **Secure User Management** (JWT, role-based admin)
- **Retrieval-Augmented Generation** with LlamaIndex
- **AWS Bedrock** LLM content generation
- **A/B Testing & Analytics** with DynamoDB and Power BI
- **Automated CI/CD** with Docker and Jenkins
- **React Frontend** with admin dashboard
- **Extensive Backend & Frontend Tests**

---

## Architecture

content-platform/
├── backend/
│ ├── main.py
│ ├── auth.py
│ ├── bedrock_client.py
│ ├── llamaindex_client.py
│ ├── dynamo_client.py
│ ├── create_user.py
│ ├── requirements.txt
│ ├── test_feedback.py
│ ├── test_main.py
│ └── Dockerfile
├── frontend/
│ ├── src/
│ │ ├── App.js
│ │ ├── App.test.js
│ │ └── AdminPanel.js
│ └── package.json
├── rag_docs/
│ ├── brand_guidelines.txt
│ └── faq.txt
└── README.md

yaml
Copy
Edit

---

## Prerequisites

- **AWS Account** (Bedrock, DynamoDB access)
- **Python 3.10+**
- **Node.js (React)**
- **Docker (for containerization)**
- **Git, GitHub Account**
- (Optional) **Jenkins** for CI/CD

---

## 1. Backend Setup (FastAPI)

### **Install dependencies:**

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
AWS Credentials:
Configure credentials via aws configure or environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION).

DynamoDB Setup:
Create required tables (example with AWS CLI):

bash
Copy
Edit
aws dynamodb create-table \
    --table-name UsersTable \
    --attribute-definitions AttributeName=user_id,AttributeType=S \
    --key-schema AttributeName=user_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb create-table \
    --table-name ContentTable \
    --attribute-definitions AttributeName=user_id,AttributeType=S AttributeName=timestamp,AttributeType=S \
    --key-schema AttributeName=user_id,KeyType=HASH AttributeName=timestamp,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb create-table \
    --table-name AnalyticsTable \
    --attribute-definitions AttributeName=user_id,AttributeType=S AttributeName=timestamp,AttributeType=S \
    --key-schema AttributeName=user_id,KeyType=HASH AttributeName=timestamp,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
Create Admin/User Accounts:
Edit and run create_user.py to add users (see file for usage).

Run the Backend:
bash
Copy
Edit
uvicorn main:app --reload
# or with Docker
docker build -t content-backend .
docker run -p 8000:8000 content-backend
2. Frontend Setup (React)
bash
Copy
Edit
cd frontend
npm install
npm start
The app will run at http://localhost:3000 (default).

Adjust backend URL in App.js if needed.

3. Adding/Retrieving Brand Documents
Place .txt/.md/.pdf files into rag_docs/ for LlamaIndex RAG context.

These will be indexed on backend startup.

4. Running Tests
Backend:
bash
Copy
Edit
cd backend
pytest
Frontend:
bash
Copy
Edit
cd frontend
npm test
5. CI/CD Pipeline (Jenkins, Docker)
Use the provided Dockerfile for backend containerization.

Sample Jenkinsfile for automated build/test/deploy (not included by default).

Push code to GitHub for remote builds and collaboration.

6. Power BI Analytics
Export DynamoDB analytics as CSV for Power BI dashboarding.

Example visuals: variant engagement, feedback scores, usage trends.

See Power BI Starter Template for rapid setup.

7. Admin Features
Admin users can download all feedback as CSV from /admin/feedback (see AdminPanel.js).

Only users with is_admin: true in DynamoDB can access admin routes.

8. API Endpoints
POST /token — JWT login

POST /generate — Generate brand-aligned content

POST /feedback — Submit user feedback (A/B analytics)

GET /admin/feedback — (Admin only) Download all feedback as CSV

9. Security & Notes
Store secret keys securely.

Use HTTPS in production.

Limit IAM permissions on AWS credentials.

Rate limit API endpoints in production.

