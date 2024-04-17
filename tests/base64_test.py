import requests
import pathlib

from datetime import datetime
from time import sleep


URL: str = 'http://localhost:8000/api/v1/base64/'
TEXT: str = 'hano world'
OPTIONS: dict = {
    "name": "Base64 List",
    "description": "",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "POST": {
            "base64": {
                "type": "string",
                "required": True,
                "read_only": False,
                "label": "Base64"
            }
        }
    }
}
WRONG_FILE: pathlib.Path = pathlib.Path('tests', 'data', 'audio', 'audio.wav')
WRONG_PAYLOAD: dict = {'file': open(WRONG_FILE, 'rb')}


def payload(name: str):
    file: pathlib.Path = pathlib.Path('tests', 'data', 'base64', name)
    payload: dict = {'base64': open(file, 'r', encoding='utf-8')}

    return payload


def test_get_405() -> None:
    response: requests.Response = requests.get(URL)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "GET" not allowed.'


def test_head_405() -> None:
    response: requests.Response = requests.head(URL)

    assert response.status_code == 405


def test_post_caching() -> None:
    sleep(5)

    uncached_start: datetime = datetime.now()
    requests.post(URL, payload('base64_wav.txt'))
    uncached_end: datetime = datetime.now()
    uncached_time: int = (uncached_end - uncached_start).microseconds

    cached_start: datetime = datetime.now()
    requests.post(URL, payload('base64_wav.txt'))
    cached_end: datetime = datetime.now()
    cached_time: int = (cached_end - cached_start).microseconds

    assert cached_time < (uncached_time * 0.65)


def test_post_201_aac() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_aac.txt')
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == 'hano world'


def test_post_201_aiff() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_aiff.txt')
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == 'hano world'


def test_post_201_flac() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_flac.txt')
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == 'hano world'


def test_post_201_m4a() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_m4a.txt')
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == 'hano world'


def test_post_201_mp3() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_mp3.txt')
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == 'hano world'


def test_post_201_ogg() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_ogg.txt')
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == 'hano world'


def test_post_201_opus() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_opus.txt')
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == 'hano world'


def test_post_201_wav() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_wav.txt')
    )
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == 'hano world'


def test_post_400_missing_field() -> None:
    response: requests.Response = requests.post(URL, files=WRONG_PAYLOAD)
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'base64': ['This field is required.']}


def test_post_400_malformed_data() -> None:
    file: pathlib.Path = pathlib.Path(
        'tests', 'data', 'base64', 'base64_wav.txt'
    )

    payload_: dict = {
        'base64': str(open(file, 'r', encoding='utf-8')) + 'a'
    }

    response: requests.Response = requests.post(URL, payload_)
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'base64': ['Malformed base64 data.']}


def test_post_400_not_an_audio() -> None:
    file: pathlib.Path = pathlib.Path('tests', 'data', 'base64', 'image.txt')
    payload_: dict = {'base64': open(file, 'r', encoding='utf-8')}

    response: requests.Response = requests.post(URL, payload_)
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'base64': ['Not an audio.']}


def test_put_405() -> None:
    response: requests.Response = requests.put(URL)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "PUT" not allowed.'


def test_patch_405() -> None:
    response: requests.Response = requests.patch(URL)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "PATCH" not allowed.'


def test_delete_405() -> None:
    response: requests.Response = requests.delete(URL)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "DELETE" not allowed.'


def test_options_200() -> None:
    response: requests.Response = requests.options(URL)
    data: dict = response.json()

    assert response.status_code == 200
    assert data == OPTIONS
