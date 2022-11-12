FROM python:3.10.8

RUN useradd --create-home --shell /bin/bash bananabot

USER bananabot
RUN pip install Flask Flask-HTTPAuth requests

COPY bananabot.py announcements.py /home/bananabot/
COPY templates /home/bananabot/templates/
COPY static /home/bananabot/static/

# Change this to your timezone
ENV TZ=Australia/Sydney

EXPOSE 8000
CMD [ "python3", "/home/bananabot/bananabot.py" ]