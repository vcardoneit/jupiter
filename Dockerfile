FROM python:3.12-slim-bullseye

RUN addgroup --system jupiter && adduser --system --group jupiter

ENV APP_HOME=/home/jupiter/web

RUN mkdir -p $APP_HOME/staticfiles

WORKDIR $APP_HOME

COPY . $APP_HOME

RUN apt-get update && apt-get install -y --no-install-recommends netcat
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

RUN chown -R jupiter:jupiter $APP_HOME

RUN python manage.py collectstatic --no-input --clear

USER jupiter

ENTRYPOINT ["/home/jupiter/web/entrypoint.sh"]