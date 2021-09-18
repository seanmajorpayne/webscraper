FROM ubuntu:20.04
RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt-get update && apt-get install -y python3-pip
RUN mkdir /usr/src/app
COPY requirements.txt /usr/src/app
WORKDIR /usr/src/app
RUN mkdir ./fetch
RUN python3 -m pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python3"]