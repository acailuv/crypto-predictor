FROM python:3.8-slim-buster

COPY . .

RUN python3 -m pip install -r requirements.txt --timeout=1000
RUN pip install "uvicorn[standard]"

CMD ["uvicorn", "server:app"]

EXPOSE 8000
