import requests
import pathlib


POST_URL: str = 'http://localhost:8000/api/v1/file/'
URL_LIST: str = 'http://localhost:8000/api/v1/text/'
URL_DETAIL = (
    URL_LIST +
    '337096cb374d208ebf4deae2eb365956c090ccfb1c9b7a35bda7874a803eb648/'
)
WRONG_URL_DETAIL = (
    URL_LIST +
    '1/'
)
TEXT: str = 'hano world'
OPTIONS: dict = {
    "name": "Text Instance",
    "description": "",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ]
}


def test_403() -> None:
    response: requests.Response = requests.get(WRONG_URL_DETAIL)
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
    file: pathlib.Path = pathlib.Path('tests', 'data', 'audio', name)
    payload: dict = {'file': open(file, 'rb')}

    return payload


def test_get_list_404() -> None:
    response: requests.Response = requests.get(URL_LIST, headers=HEADERS)

    assert response.status_code == 404


def test_get_detail_200() -> None:
    requests.post(POST_URL, files=payload('audio.aac'), headers=HEADERS)
    response: requests.Response = requests.get(URL_DETAIL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 200
    assert 'ready' in data.keys()
    assert 'text' in data.keys()


def test_get_detail_404() -> None:
    response: requests.Response = requests.get(
        WRONG_URL_DETAIL, headers=HEADERS
    )
    assert response.status_code == 404


def test_head_detail_200() -> None:
    response: requests.Response = requests.head(URL_DETAIL, headers=HEADERS)

    assert response.status_code == 200


def test_post_405() -> None:
    response: requests.Response = requests.post(
        URL_DETAIL, headers=HEADERS
    )
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "POST" not allowed.'


def test_put_405() -> None:
    response: requests.Response = requests.put(URL_DETAIL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "PUT" not allowed.'


def test_patch_405() -> None:
    response: requests.Response = requests.patch(URL_DETAIL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "PATCH" not allowed.'


def test_delete_405() -> None:
    response: requests.Response = requests.delete(URL_DETAIL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "DELETE" not allowed.'


def test_options_200() -> None:
    response: requests.Response = requests.options(URL_DETAIL, headers=HEADERS)
    data: dict = response.json()

    assert response.status_code == 200
    assert data == OPTIONS
