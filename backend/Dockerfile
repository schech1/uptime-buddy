FROM python:3.11-slim

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set the working directory inside the container
WORKDIR /app

# Copy the entire application directory to the Docker image
COPY . /app

# Copy the VERSION file into the image
COPY ../VERSION /app/VERSION

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 5005

# Set FLASK_APP environment variable
ENV FLASK_APP=app.py

# Use RUN to read the VERSION file and set the APP_VERSION as an environment variable
RUN export APP_VERSION=$(cat /app/VERSION) && echo "App Version is $APP_VERSION"

# Command to run the Flask app
CMD ["python", "app.py"]
