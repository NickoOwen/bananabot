FROM python:3.10.8

RUN useradd --create-home --shell /bin/bash bananabot

USER bananabot
RUN pip install Flask==2.2.2 Flask-HTTPAuth==4.7.0 requests==2.25.1

COPY bananabot.py announcements.py /home/bananabot/
COPY templates /home/bananabot/templates/
COPY static /home/bananabot/static/

# Change this to your timezone
ENV TZ=Australia/Sydney

EXPOSE 8000
CMD [ "python3", "/home/bananabot/bananabot.py" ]