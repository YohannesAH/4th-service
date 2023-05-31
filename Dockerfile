# Base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code
COPY app4.py .

# Expose the necessary port
EXPOSE 5004

# Set environment variables
ENV SPEECH_KEY your_speech_key
ENV SPEECH_REGION your_speech_region

# Run the Flask app
CMD ["python", "app4.py"]
