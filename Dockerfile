FROM python:3.8.10-slim

WORKDIR /server

COPY . /server

RUN pip install -r requirements.txt

EXPOSE 8000

# Use uvicorn to run your FastAPI application (replace 'main:app' if different)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
