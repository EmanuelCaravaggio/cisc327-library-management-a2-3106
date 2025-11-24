FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_APP_HOST=0.0.0.0
ENV FLASK_APP_PORT=5000

EXPOSE 5000

CMD [ "flask","run", "--host=0.0.0.0", "--port=5000"]
