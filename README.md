# Legal Advisor Chatbot

![Legal Advisor Interface](https://i.imgur.com/IDbnAii.jpeg)

## Overview

Legal Advisor Chatbot is a custom legal consulting application that provides an AI-powered chat interface similar to ChatGPT, specifically designed for legal consultation. The application is built with a Python backend, Streamlit frontend, and uses PostgreSQL for data storage.

## Branches

- **master**: Stable version with Langchain integration
- **stable-no-langchain**: Stable version without Langchain dependency

Both branches can be run using the same methods described below.

## Requirements

- Docker and Docker Compose (for containerized deployment - recommended)
- PostgreSQL 17 (for local deployment - optional)
- OpenAI API key
- Python 3.11.4 (recommended for local deployment - optional)

## Environment Setup

1. Create a `.env` file in the root directory (same location as `.env.example`)
2. Configure the following environment variables:
   - For variables with "your_" prefix: Replace with your actual credentials
   - For other variables: Keep the default values as shown

```
FRONTEND_TARGET="localhost"
OPENAI_API_KEY="your_openai_api_key"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
DATABASE_USER="postgres"
DATABASE_PASSWORD="your_database_password"
DATABASE_NAME="legalchatbot"
```

## Running with Docker (Recommended)

1. Ensure Docker and Docker Compose are installed
2. Make sure Docker Desktop is open and running before proceeding
3. Navigate to the root directory of the project
4. Run the following command:

```bash
docker-compose up --build
```

5. Once the containers are built and running, access:
   - Frontend: [http://127.0.0.1:8501](http://127.0.0.1:8501)
   - Backend API: [http://127.0.0.1:8000](http://127.0.0.1:8000)

The application will be visible in Docker Desktop once successfully built.

**Note about API Testing**: If you use Postman to test the backend API while running in Docker, be aware that Postman will have a different IP address compared to the frontend. This means that chats created via Postman will be associated with a different user and will not appear in the frontend interface. This is by design as the application uses IP addresses for user identification.

## Running Locally

### Prerequisites
- PostgreSQL 17 installed and running
- Python 3.11.4 (other versions above 3.8 have not been tested for compatibility)

### Database Setup

Before running the application locally, you need to create the database:

1. Open Command Prompt and connect to PostgreSQL:
```bash
psql -U postgres
```

2. Create the database:
```sql
CREATE DATABASE legalchatbot;
```

3. Exit PostgreSQL:
```
\q
```

To remove the database if needed:
```sql
DROP DATABASE legalchatbot;
```

### Application Setup

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Start the backend server (in one terminal):
```bash
uvicorn backend.main:app --reload
```

3. Start the frontend (in another terminal):
```bash
streamlit run frontend/app.py
```

4. Access the application:
   - Frontend: [http://127.0.0.1:8501](http://127.0.0.1:8501)
   - Backend API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
