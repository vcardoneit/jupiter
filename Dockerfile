FROM python:3.13.0rc1-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /home/jupiter/web

WORKDIR /home/jupiter/web

COPY . /home/jupiter/web

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  /home/jupiter/web/entrypoint.sh
RUN chmod +x  /home/jupiter/web/entrypoint.sh

RUN python manage.py collectstatic --no-input --clear

ENTRYPOINT ["/home/jupiter/web/entrypoint.sh"]