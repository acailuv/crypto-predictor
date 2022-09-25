FROM python:3.8-slim-buster

COPY . .

RUN python3 -m pip install -r requirements.txt --timeout=1000

CMD ["python3", "server.py"]
