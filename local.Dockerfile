FROM python:3.9.0

WORKDIR /home/

COPY ./ /home/ubuntu/project_server/

WORKDIR /home/ubuntu/project_server/

RUN apt-get upgrade && pip3 install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000
