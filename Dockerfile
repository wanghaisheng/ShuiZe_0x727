FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY . /app


RUN apt-get update
RUN apt install git --fix-missing
RUN rm /usr/bin/python3
RUN ln -s /usr/local/bin/python3.8 /usr/bin/python3
RUN python3 -m pip install --upgrade pip
RUN chmod 777 docker_build.sh
RUN ./docker_build.sh
