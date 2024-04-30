# Acuity

A simple and reliable REST API service for audio recognition

# Features

🎙️ Recognizes English with `wav2vec2-large-xlsr-53-english`

🧩 Accepts `files` and `base64`

📄 Has support for `Swagger` and `Redoc`

💾 Logs `hashes` instead of sensitive information

🔥 Uses `caching`, `queues` and `data validation`

🔐 Uses `JWT` for authentication

🛡️ `DOS` protected

🏎️ `GPU` accelerated

# Run

Steps:
1. Make sure you have [docker](https://www.docker.com/) installed
2. Download [xlsr-53](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english/tree/main) and put in `./nn_model` folder
3. Run `docker compose up --build` in the terminal

# GPU acceleration

Steps:
1. Make sure that the nvidia graphics card is physically installed on your
device
2. Run `docker compose -f .\docker-compose-gpu.yml up --build`

# Endpoints

* `api/token/` - JWT
* `api/v1/schema/swagger/` or `api/v1/schema/redoc/` - Documentation
* `api/v1/` - DRF browsable API

# Develop

Steps:
1. Make sure you have [python 3.12](https://www.python.org/) installed
2. Make sure you have [docker](https://www.docker.com/) installed
3. Download [xlsr-53](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english/tree/main) and put in `./nn_model` folder
4. Run `python -m pip install -r .\src\requirements\dev.txt` in the terminal to install dependencies
5. Write some new code
6. Run `python manage.py migrate` in the terminal from `src` folder to apply migrations
7. Run `python manage.py createsuperuser` in the terminal from `src` folder to create user
8. Run `python manage.py runserver` in the terminal from `src` folder to start django dev server
9. Run `python manage.py celery dev` in the terminal from `src` folder to start celery dev server
10. Run `python -m pytest .` in the terminal from `.` folder to run tests

# Customize

Change the values in the `./prod.env` file

**PostgreSQL**
* `POSTGRES_HOST` - Host
* `POSTGRES_NAME`- Table prefixes
* `POSTGRES_PASSWORD` - Password
* `POSTGRES_USER` - User
* `POSTGRES_DB` - Database name
* `POSTGRES_PORT` - Port

**Redis**
* `REDIS_ADDRESS` - Address
* `REDIS_TIMEOUT` - Cache lifetime in seconds

**RabbitMQ**
* `RABBITMQ_ADDRESS` - Address including vhost
* `RABBITMQ_DEFAULT_USER` - User
* `RABBITMQ_DEFAULT_PASS` - Password
* `RABBITMQ_DEFAULT_VHOST` - VHost

**Neural Network Model**
* `NN_CONVERTER_FORMAT` - Format to which the audio will be converted
* `NN_CONVERTER_BITRATE` - Bitrate of converted audio
* `NN_CONVERTER_MONO` - Convert audio to mono
* `NN_MODEL_PATH` - Path to the neural network model inside docker
* `NN_MAX_LENGTH` - Maximum length of audio to be processed
* `NN_SAMPLE_RATE` - Sample rate of audio coming into the neural network

**Django**
* `DJANGO_SUPERUSER_USERNAME` - Username
* `DJANGO_SUPERUSER_PASSWORD` - Password
* `DJANGO_SUPERUSER_EMAIL` - Email
* `DJANGO_SECRET_KEY` - Secret Key
* `DJANGO_ALLOWED_HOSTS` - Allowed hosts

# Example

``` Python
from pathlib import Path
from requests import get, post, Response
from time import sleep


def authenticate(url: str, login: str, password: str) -> dict[str, str]:
    response: Response = post(
        url, data={'username': login, 'password': password}
    )

    data: dict = response.json()
    jwt: str = data.get('access', '')
    headers: dict[str, str] = {'Authorization': f'Bearer {jwt}'}

    return headers


def recognize(
    url: str, file: Path, wait: float, headers: dict[str, str],
) -> str:
    response: Response = post(
        url, files={'file': open(file, 'rb')}, headers=headers
    )

    data: dict = response.json()
    link_to_recognized_text: str = data.get('link', '')

    while True:
        redirect: Response = get(link_to_recognized_text, headers=headers)
        redirect_data: dict = redirect.json()
        ready: bool = redirect_data.get('ready', False)

        if ready:
            text: str = redirect_data.get('text', '')
            return text

        else:
            sleep(wait)


auth_url: str = 'http://localhost:8000/api/token/'
recognition_url: str = 'http://localhost:8000/api/v1/file/'
login: str = 'admin'
password: str = 'admin'


headers = authenticate(auth_url, login, password)
file: Path = Path('tests', 'data', 'audio', 'audio.wav')
recognized_text: str = recognize(recognition_url, file, 0.2, headers)

print(recognized_text)
```
