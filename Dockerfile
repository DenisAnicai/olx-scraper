FROM python:3.11-alpine

COPY . /app
WORKDIR /app

EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["python", "api.py"]