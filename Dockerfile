FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY . /app

RUN chmod -R 777 /app
RUN apt-get update
RUN apt install git --fix-missing 
RUN apt-get install -y libpcap-dev sudo policykit-1
RUN rm /usr/bin/python3
RUN ln -s /usr/local/bin/python3.8 /usr/bin/python3
RUN python3 -m pip install --upgrade pip
RUN chmod 777 docker_build.sh
RUN ./docker_build.sh
User root:root
# RUN apt-get update \
#     && apt-get install flex bison -y \
#     && apt-get clean

# RUN wget http://www.tcpdump.org/release/libpcap-1.10.1.tar.gz && tar xzf libpcap-1.10.1.tar.gz \
#     && cd libpcap-1.10.1 \
#     && ./configure && make install
# RUN pkexec chown root: /usr/bin/sudo 
# RUN pkexec chmod 4755 /usr/bin/sudo



# https://stackoverflow.com/questions/30663245/tcpdump-reports-error-in-docker-container-thats-started-with-privileged
# RUN chmod 777 /usr/bin/tcpdump && tcpdump -i eth0


RUN chown root:root /usr/bin/sudo

RUN chmod 4755 /usr/bin/sudo
RUN apt-get -y install tcpdump
