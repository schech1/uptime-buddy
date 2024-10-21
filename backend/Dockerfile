FROM python:3.11-slim
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY backend /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5005
ENV FLASK_APP=app.py
ENV APP_VERSION=$(cat /app/VERSION)
CMD ["python", "app.py"]
