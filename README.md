# BananaBot

## Table of Contents

- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Build](#build)
- [Deploy](#deploy)
- [Contributing](#contributing)
- [License](#license)
- [Changelog](#changelog)

## About The Project

BananaBot (BB for short) is a good little bot created to help make sure everyone has their daily banana on time. It provides a user-friendly admin page where an administrator can configure the bot's messages and banana time. It also features a home page with a timer that counts down to banana time.

BananaBot is designed to send a `POST` request to a given endpoint, allowing it to work with many popular chat platforms (e.g. Slack) via [incoming webhooks](https://api.slack.com/messaging/webhooks). The logic for sending a request can be found in [src/announcement.py](./src/announcement.py) and can be modified to suit your needs if required.

## Getting Started

To get a local copy of BananaBot up and running follow the steps below.

### Prerequisites

Download and install Python `v3.10.10`
* https://www.python.org/downloads/release/python-31010/

### Installation

1. Clone the repository
    ```bash
    git clone https://github.com/NickoOwen/bananabot.git
    ```

2. Install the requirements using `pip`
    ```bash
    pip install -r requirements.txt
    ```

3. From the `src` directory, run the following command to run the app
    ```bash
    python3 -m uvicorn bananabot:app
    ```

To utilise FastAPI's automatic change detection when developing, add the `--reload` flag to the command as shown below
```bash
python3 -m uvicorn bananabot:app --reload
```

## Usage

1. Set the `url` class variable in [src/announcement.py](./src/announcement.py) to the [incoming webhook](https://api.slack.com/messaging/webhooks)

2. 

## Build

To build the BananaBot Docker image, run the following command from within the `src` directory
```
docker build -t bananabot .
```

## Deploy

BananaBot is intended to be deployed in a container, but can also be ran locally using Python `v3.10.8` or later.

### Deploy a Container

To run the BananaBot container built above, run the following command
```
docker run --name bananabot -p 8000:8000 -d bananabot
```

## Contributing

BananaBot has been a team effort since the very beginning and we absolutely love it when more people want to contribute. Any contributions you make are **greatly appreciated**.

If you have a suggestion that you think would improve BananaBot, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star, and thanks again for your contribution!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

### Development Environment Setup

Setup your development environment by running the following command
```
pip install -r requirements.txt
```

### Running Tests

To run the unit tests, run the following command from within the `src` directory
```
python3 -m pytest ./tests
```

### Running BananaBot

To run the BananaBot app, run the following command from within the `src` directory
```
python3 -m uvicorn bananabot:app --reload
```

The `--reload` flag causes new changes to be automatically detected and reloads the app.

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.

## Changelog

[Link to CHANGELOG.md](./CHANGELOG.md)
