FROM python:3.11-slim

WORKDIR /app

COPY web_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_app:app"]
