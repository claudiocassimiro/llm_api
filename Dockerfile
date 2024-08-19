FROM python:3.12.5

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 --timeout 300 app:app"]
