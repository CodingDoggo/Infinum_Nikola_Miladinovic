FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements_backend.txt .
RUN pip install --no-cache-dir -r requirements_backend.txt

# Copy the backend directory preserving structure
COPY backend/ ./backend/

# Set Python path to include app directory
ENV PYTHONPATH=/app

EXPOSE 8000

# Updated to use the module inside backend directory
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]