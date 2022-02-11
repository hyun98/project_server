FROM python:3.9.0

COPY ./ /home/ubuntu/backend-msa/apigateway-auth-service

WORKDIR /home/ubuntu/backend-msa/apigateway-auth-service/

RUN apt-get upgrade && \
    pip3 install --upgrade pip \
    pip install -r requirements.txt && \
    pip install gunicorn && \
    pip install mysqlclient

EXPOSE 8000
