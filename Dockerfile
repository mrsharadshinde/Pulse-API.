# 1. Pull the official, lightweight Python 3.11 image from Docker Hub
FROM python:3.11-slim

# 2. Tell Docker to do all future work inside this specific folder
WORKDIR /usr/src/app

COPY requirement.txt ./

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. The default command to start your server when the container boots up
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
