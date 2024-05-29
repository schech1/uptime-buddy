FROM --platform=linux/amd64 python:3.9-slim

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

ENV FLASK_APP=app.py

CMD ["python", "app.py"]
