FROM python:3.10.10

RUN useradd --create-home --shell /bin/bash bananabot

USER bananabot
WORKDIR /home/bananabot/

RUN pip install \
    anyio==3.6.2 \
    attrs==22.2.0 \
    bcrypt==4.0.1 \
    certifi==2022.12.7 \
    charset-normalizer==3.1.0 \
    click==8.1.3 \
    exceptiongroup==1.1.0 \
    fastapi==0.92.0 \
    h11==0.14.0 \
    httpcore==0.16.3 \
    idna==3.4 \
    iniconfig==2.0.0 \
    Jinja2==3.1.2 \
    MarkupSafe==2.1.2 \
    packaging==23.0 \
    pluggy==1.0.0 \
    pydantic==1.10.5 \
    requests==2.28.2 \
    rfc3986==1.5.0 \
    sniffio==1.3.0 \
    starlette==0.25.0 \
    tomli==2.0.1 \
    typing_extensions==4.5.0 \
    urllib3==1.26.14 \
    uvicorn==0.20.0

COPY bananabot.py announcement.py logging.conf /home/bananabot/
COPY templates /home/bananabot/templates/
COPY static /home/bananabot/static/

# Change this to your timezone
ENV TZ=Australia/Sydney

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f localhost:8000/healthcheck 

EXPOSE 8000
CMD [ "python3", "-m", "uvicorn", "bananabot:app", "--host", "0.0.0.0", "--port", "8000"]