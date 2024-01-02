# BananaBot

## Table of Contents

- [About The Project](#about-the-project)
    - [Built With](#built-with)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
    - [Building](#building)
    - [Deploying](#deploying)
- [Contributing](#contributing)
    - [Development Tips](#development-tips)
- [License](#license)
- [Changelog](#changelog)

## About The Project

BananaBot (BB for short) is a good little bot created to help make sure everyone has their daily banana on time. It provides a user-friendly admin page where an administrator can configure the bot's messages and banana time. It also features a home page with a timer that counts down to banana time.

BananaBot is designed to send a `POST` request to a given endpoint, allowing it to work with many popular chat platforms (e.g. Slack) via [incoming webhooks](https://api.slack.com/messaging/webhooks). The `send_message()` function can be found in [app/utilities/utilities.py](./app/utilities/utilities.py) and can be modified to suit your needs if required.

### Built With

* [FastAPI](https://fastapi.tiangolo.com/)
* [Bootstrap](https://getbootstrap.com/)
* [JQuery](https://jquery.com/)

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

3. From the `app` directory, run the following command to run the app
    ```bash
    python3 -m uvicorn main:app
    ```

## Usage

1. Set the `url` class variable in [app/models/app_state.py](./app/models/app_state.py) to your [webhook](https://api.slack.com/messaging/webhooks). (Note this is hard coded intentionally to avoid the potential for misuse)

2. [Build](#building) and [deploy](#deploying) the app

3. Go to the admin page at `hostname:port/admin`

4. Login with the username `admin` and the password shown in the server logs

5. Configure banana time and the announcements however you want

6. Click the switch to turn on BananaBot. BB is now active and will send the messages you configured at the set times

7. You can add, remove, and reconfigure BananaBot without needing to turn it off

### Building

BananaBot is intended to be deployed in a container, but can also be ran locally if desired (see [Installation](#installation))

1. Install Docker on your target platform (https://www.docker.com/)

2. Build the BananaBot Docker image by running the following command
    ```bash
    docker build -t bananabot .
    ```

### Deploying

1. To run the BananaBot container built above, run the following command
    ```bash
    docker run --name bananabot -p 8000:8000 -d bananabot
    ```

## Contributing

BananaBot has been a team effort since the very beginning and we absolutely love it when more people want to contribute. Any contributions you make are **greatly appreciated**.

If you have a suggestion that you think would improve BananaBot, please fork the repo and create a pull request. You can also simply open an issue with the tag `enhancement`. Don't forget to give the project a star! Thanks again for your contribution!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

### Development Tips

1. To utilise FastAPI's automatic change detection when developing, add the `--reload` flag to the command as shown below
    ```bash
    python3 -m uvicorn main:app --reload
    ```

2. To run the unit tests, run the following command from within the `app` directory
    ```
    python3 -m pytest ./tests
    ```

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.

## Changelog

[Link to CHANGELOG.md](./CHANGELOG.md)
