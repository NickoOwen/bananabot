# BananaBot

## Description
BananaBot (BB for short) is a good little bot created to help make sure everyone has their daily banana on time. It provides a user-friendly admin page where an administrator can easily add and remove announcements and configure banana time itself.

BananaBot is designed to send a `POST` request to a given endpoint, allowing it to work with many popular chat platforms (e.g. Slack) via [incoming webhooks](https://api.slack.com/messaging/webhooks). The logic for sending a request can be found in [announcements.py](./announcements.py) and can be modified to suit your needs if required.

## Configure

Set the `url` variable in [announcements.py](./announcements.py) so that it points to the desired endpoint.

## Build

To build the BananaBot Docker image, run the following command from within this directory
```
docker build -t bananabot .
```

## Deploy

BananaBot is intended to be deployed in a container, but can also be ran locally using Python `v3.10.8` or later.

### Deploy a Container

To run the BananaBot container built above, run the following command
```
docker run --name bananabot -p 8000:8000 bananabot
```

### Running with Python3

To run BananaBot using Python, first install the required dependencies
```
pip install -r requirements.txt
```

Then run `bananabot.py`
```
python3 bananabot.py
```

## Changelog

[Link to CHANGELOG.md](./CHANGELOG.md)