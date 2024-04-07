FROM python:3.12.2-alpine3.19 AS builder
 
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
 
CMD ["gunicorn", "--worker-class" , "eventlet", "-w", "1", "app:app"]