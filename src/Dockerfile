FROM python:3.10.8

RUN useradd --create-home --shell /bin/bash bananabot

USER bananabot

RUN pip install \
    anyio==3.6.2 \
    attrs==22.2.0 \
    bcrypt==4.0.1 \
    certifi==2022.12.7 \
    charset-normalizer==3.0.1 \
    click==8.1.3 \
    colorama==0.4.6 \
    dnspython==2.3.0 \
    email-validator==1.3.1 \
    exceptiongroup==1.1.0 \
    fastapi==0.92.0 \
    h11==0.14.0
    httpcore==0.16.3 \
    httptools==0.5.0 \
    httpx==0.23.3 \
    idna==3.4
    iniconfig==2.0.0 \
    itsdangerous==2.1.2 \
    Jinja2==3.1.2 \
    MarkupSafe==2.1.2 \
    orjson==3.8.7 \
    packaging==23.0 \
    pluggy==1.0.0 \
    pydantic==1.10.5 \
    python-dotenv==1.0.0 \
    python-multipart==0.0.6 \
    PyYAML==6.0
    requests==2.28.2 \
    rfc3986==1.5.0 \
    sniffio==1.3.0 \
    starlette==0.25.0 \
    tomli==2.0.1 \
    typing_extensions==4.5.0 \
    ujson==5.7.0 \
    urllib3==1.26.14 \
    uvicorn==0.20.0 \
    watchfiles==0.18.1 \
    websockets==10.4

COPY bananabot.py announcement.py /home/bananabot/
COPY templates /home/bananabot/templates/
COPY static /home/bananabot/static/

# Change this to your timezone
ENV TZ=Australia/Sydney

EXPOSE 8000
CMD [ "python3", "/home/bananabot/bananabot.py" ]