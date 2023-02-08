FROM python:3.9-slim
COPY . ./
RUN pip3 install -r ./requirements.txt
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 flaskapp:app
