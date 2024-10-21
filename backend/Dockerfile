FROM python:3.11-slim

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY . /app
COPY ../VERSION /app/VERSION

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

ENV FLASK_APP=app.py

CMD ["python", "app.py"]
