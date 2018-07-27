FROM ubuntu:18.04

LABEL maintainer "Atsushi Yamaguchi <libertyrh@gmail.com>"

# RUN echo 'Acquire::HTTP::Proxy "http://172.17.0.1:3142";' >> /etc/apt/apt.conf.d/01proxy \
# && echo 'Acquire::HTTPS::Proxy "false";' >> /etc/apt/apt.conf.d/01proxy

RUN apt-get update -qq \
  && apt-get install -y \
    python3 \
    python3-pip \
    redis-server \
    jq \
    git \
    nginx \
    lua-nginx-redis \
  && apt-get clean

RUN pip3 install \
  redis \
  yq

COPY redis/regist.py /usr/sbin/regist.py
RUN chmod +x  /usr/sbin/regist.py

ADD nginx/default /etc/nginx/sites-available/
ADD nginx/rewrite.lua /etc/nginx/sites-available/

ADD bin/entrypoint /usr/bin/entrypoint
RUN chmod +x /usr/bin/entrypoint

CMD ["/usr/bin/entrypoint"]