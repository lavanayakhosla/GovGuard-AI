# Use stable Python
FROM python:3.11.9-slim

# Working directory inside container
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Use Render's assigned port automatically
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
