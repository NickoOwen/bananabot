FROM python:3.10.8

RUN useradd --create-home --shell /bin/bash bananabot

USER bananabot
COPY requirements.txt /home/bananabot/requirements.txt
RUN pip install -r /home/bananabot/requirements.txt

COPY bananabot.py announcements.py /home/bananabot/
COPY templates /home/bananabot/templates/
COPY static /home/bananabot/static/

# Change this to your timezone
ENV TZ=Australia/Sydney

EXPOSE 8000
CMD [ "python3", "/home/bananabot/bananabot.py" ]