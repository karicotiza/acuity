import requests
import pathlib

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


def test_403() -> None:
    response: requests.Response = requests.get(URL)
    data: dict = response.json()

    assert response.status_code == 403
    assert (
        data.get('detail', '') ==
        'Authentication credentials were not provided.'
    )


AUTH_URL: str = 'http://localhost:8000/api/token/'
USERNAME: str = 'admin'
PASSWORD: str = 'admin'


def test_authentication() -> None:
    response: requests.Response = requests.post(
        AUTH_URL, {'username': USERNAME, 'password': PASSWORD}
    )

    data: dict = response.json()

    assert response.status_code == 200
    assert data.get('access', '')
    assert data.get('refresh', '')


JWT = ''

response: requests.Response = requests.post(
        AUTH_URL, {'username': USERNAME, 'password': PASSWORD}
    )

data: dict = response.json()
JWT = data.get('access', '')
HEADERS = {'Authorization': f'Bearer {JWT}'}


def payload(name: str):
    file: pathlib.Path = pathlib.Path('tests', 'data', 'base64', name)
    payload: dict = {'base64': open(file, 'r', encoding='utf-8')}

    return payload


def wait(link: str) -> None:
    while True:
        redirect: requests.Response = requests.get(link, headers=HEADERS)
        redirect_data: dict = redirect.json()

        assert redirect.status_code == 200

        if redirect_data.get('ready'):
            assert redirect_data.get('text') == TEXT
            break

        else:
            sleep(0.2)


def test_get_405() -> None:
    response: requests.Response = requests.get(URL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "GET" not allowed.'


def test_head_405() -> None:
    response: requests.Response = requests.head(URL, headers=HEADERS)

    assert response.status_code == 405


def test_post_caching() -> None:
    sleep(5)

    response: requests.Response = requests.post(
        URL, payload('base64_wav.txt'), headers=HEADERS
    )
    data: dict = response.json()
    link: str = data.get('link', '')
    redirect: requests.Response = requests.get(link, headers=HEADERS)

    assert redirect.status_code == 200

    sleep(2)

    redirect_: requests.Response = requests.get(link, headers=HEADERS)
    redirect_data: dict = redirect_.json()

    assert redirect_.status_code == 200
    assert redirect_data.get('ready') is True
    assert redirect_data.get('text') == TEXT


def test_post_201_aac() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_aac.txt'), headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_aiff() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_aiff.txt'), headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_flac() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_flac.txt'), headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_m4a() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_m4a.txt'), headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_mp3() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_mp3.txt'), headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_ogg() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_ogg.txt'), headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_opus() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_opus.txt'), headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_201_wav() -> None:
    response: requests.Response = requests.post(
        URL, payload('base64_wav.txt'), headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 201

    link: str = data.get('link', '')

    wait(link)


def test_post_400_missing_field() -> None:
    response: requests.Response = requests.post(
        URL, files=WRONG_PAYLOAD, headers=HEADERS
    )
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

    response: requests.Response = requests.post(
        URL, payload_, headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'base64': ['Malformed base64 data.']}


def test_post_400_not_an_audio_another_file() -> None:
    file: pathlib.Path = pathlib.Path('tests', 'data', 'base64', 'image.txt')
    payload_: dict = {'base64': open(file, 'r', encoding='utf-8')}

    response: requests.Response = requests.post(
        URL, payload_, headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'base64': ['Not an audio.']}


def test_post_400_not_an_audio_random_characters() -> None:
    payload_: dict = {'base64': 'aaaa'}

    response: requests.Response = requests.post(
        URL, payload_, headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 400
    assert data == {'base64': ['Not an audio.']}


def test_put_405() -> None:
    response: requests.Response = requests.put(URL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "PUT" not allowed.'


def test_patch_405() -> None:
    response: requests.Response = requests.patch(URL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "PATCH" not allowed.'


def test_delete_405() -> None:
    response: requests.Response = requests.delete(URL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "DELETE" not allowed.'


def test_options_200() -> None:
    response: requests.Response = requests.options(URL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 200
    assert data == OPTIONS
