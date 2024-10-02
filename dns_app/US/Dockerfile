FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install Flask requests

EXPOSE 8080

CMD ["python", "run.py"]