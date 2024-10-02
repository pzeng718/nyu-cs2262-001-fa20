FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install Flask requests

EXPOSE 53533

CMD ["python", "run.py"]