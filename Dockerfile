FROM python:3-alpine AS builder
 
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
 
CMD ["gunicorn", "--worker-class" , "eventlet", "-w", "1", "app:app"]