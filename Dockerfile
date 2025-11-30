# Dockerfile
# Use a Python base image (slim avoids unnecessary OS files)
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This is done in a separate step to leverage Docker caching
COPY requirements.txt .
# Use the image's Python to install requirements to ensure pip targets the correct interpreter
RUN python -m pip install --no-cache-dir -r requirements.txt \
	&& python -c "import pandas as _p; print('pandas==%s' % _p.__version__)"

# Copy the rest of the application code, including src/ and app.py
COPY . .

# Set a default command to run the application
# We use the sample data for the container's default run
ENV PYTHONUNBUFFERED=1
CMD ["python", "app.py", "-i", "data/sample_emails.csv"]