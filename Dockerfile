FROM python:3.11.9-slim

WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend .

# Use Render's assigned port
ENV PORT=10000  # default if not set
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
