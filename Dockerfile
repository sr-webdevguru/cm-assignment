FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
	nginx \
  && rm -rf /var/lib/apt/lists/*

COPY docker-nginx-conf/nginx_backend.conf /etc/nginx/sites-enabled/
COPY docker-nginx-conf/nginx_frontend.conf /etc/nginx/sites-enabled/

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r /code/project/requirements/base.txt
RUN python /code/project/manage.py collectstatic --noinput
