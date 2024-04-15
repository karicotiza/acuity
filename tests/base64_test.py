import requests
import pathlib


URL: str = 'http://localhost:8000/api/v1/base64/'
FILE: pathlib.Path = pathlib.Path('tests', 'base64.txt')
PAYLOAD: dict = {'base64': open(FILE, 'r', encoding='utf-8')}
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
WRONG_FILE: pathlib.Path = pathlib.Path('tests', 'audio.wav')
WRONG_PAYLOAD: dict = {'file': open(WRONG_FILE, 'rb')}


def test_get_405() -> None:
    response: requests.Response = requests.get(URL)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "GET" not allowed.'


def test_head_405() -> None:
    response: requests.Response = requests.head(URL)

    assert response.status_code == 405


def test_post_201() -> None:
    response: requests.Response = requests.post(URL, PAYLOAD)
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('text', '') == TEXT


def test_post_400() -> None:
    response: requests.Response = requests.post(URL, files=WRONG_PAYLOAD)
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'base64': ['This field is required.']}


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
