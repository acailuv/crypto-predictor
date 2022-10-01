FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY . .

RUN python3 -m pip install -r requirements.txt --timeout=1000 --retries=1000

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
