import requests
import pathlib

from time import sleep


URL: str = 'http://localhost:8000/api/v1/file/'
TEXT: str = 'hano world'
OPTIONS: dict = {
    "name": "File List",
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
            "file": {
                "type": "file upload",
                "required": True,
                "read_only": False,
                "label": "File"
            }
        }
    }
}
WRONG_FILE: pathlib.Path = pathlib.Path(
    'tests', 'data', 'base64', 'base64_wav.txt'
)

WRONG_PAYLOAD: dict = {'base64': open(WRONG_FILE, 'r', encoding='utf-8')}


def payload(name: str):
    file: pathlib.Path = pathlib.Path('tests', 'data', 'audio', name)
    payload: dict = {'file': open(file, 'rb')}

    return payload


def wait(link: str) -> None:
    while True:
        redirect: requests.Response = requests.get(link)
        redirect_data: dict = redirect.json()

        assert redirect.status_code == 200

        if redirect_data.get('ready'):
            assert redirect_data.get('text') == TEXT
            break

        else:
            sleep(0.2)


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

    response: requests.Response = requests.post(
        URL, files=payload('audio.wav')
    )
    data: dict = response.json()
    link: str = data.get('link', '')
    redirect: requests.Response = requests.get(link)

    assert redirect.status_code == 200

    sleep(2)

    redirect_: requests.Response = requests.get(link)
    redirect_data: dict = redirect_.json()

    assert redirect_.status_code == 200
    assert redirect_data.get('ready') is True
    assert redirect_data.get('text') == TEXT


def test_post_201_aac() -> None:
    response: requests.Response = requests.post(
        URL, files=payload('audio.aac')
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_aiff() -> None:
    response: requests.Response = requests.post(
        URL, files=payload('audio.aiff')
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_flac() -> None:
    response: requests.Response = requests.post(
        URL, files=payload('audio.flac')
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_m4a() -> None:
    response: requests.Response = requests.post(
        URL, files=payload('audio.m4a')
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_mp3() -> None:
    response: requests.Response = requests.post(
        URL, files=payload('audio.mp3')
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_ogg() -> None:
    response: requests.Response = requests.post(
        URL, files=payload('audio.ogg')
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_opus() -> None:
    response: requests.Response = requests.post(
        URL, files=payload('audio.opus')
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_wav() -> None:
    response: requests.Response = requests.post(
        URL, files=payload('audio.wav')
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_400_no_file_was_submitted() -> None:
    response: requests.Response = requests.post(URL, files=WRONG_PAYLOAD)
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'file': ['No file was submitted.']}


def test_post_400_not_an_audio_file() -> None:
    file: pathlib.Path = pathlib.Path(
        'tests', 'data', 'base64', 'base64_wav.txt'
    )

    payload_: dict = {'file': open(file, 'rb')}
    response: requests.Response = requests.post(URL, files=payload_)
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'file': ['Not an audio file.']}


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
