FROM python:3.11-slim

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the current build context to /app
COPY backend /app
COPY VERSION /app/VERSION

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 5005

# Set FLASK_APP environment variable
ENV FLASK_APP=app.py

# Command to run the Flask app
CMD ["python", "app.py"]
