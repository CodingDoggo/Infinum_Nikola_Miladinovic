FROM python:3.11-slim

WORKDIR /app

COPY frontend/requirements_frontend.txt .
RUN pip install --no-cache-dir -r requirements_frontend.txt

# Copy the frontend directory preserving structure
COPY frontend/ ./frontend/

EXPOSE 8501

# Updated path to the app.py file
CMD ["streamlit", "run", "frontend/app_docker.py", "--server.port=8501", "--server.address=0.0.0.0"]