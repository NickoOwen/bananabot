FROM python:3.10.10

RUN useradd --create-home --shell /bin/bash bananabot

USER bananabot
WORKDIR /home/bananabot/

COPY requirements.txt /home/bananabot/requirements.txt

RUN pip install -r /home/bananabot/requirements.txt

COPY app/ /home/bananabot/app

# Change this to your timezone
ENV TZ=Australia/Sydney

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f localhost:8000/healthcheck 

USER root
RUN chown -R bananabot /home/bananabot
USER bananabot

WORKDIR /home/bananabot/app

EXPOSE 8000
CMD [ "python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
