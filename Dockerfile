FROM python:3.8.10-slim

WORKDIR /server

COPY . /server

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["fastapi","dev","main.py"]