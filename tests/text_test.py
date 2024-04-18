import requests

URL_LIST: str = 'http://localhost:8000/api/v1/text/'
URL_DETAIL = (
    URL_LIST +
    '10e0e1c3828817839a450f9895c85e975122801e27f65faee4cdb7d588b8e305/'
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


def test_get_list_404() -> None:
    response: requests.Response = requests.get(URL_LIST)

    assert response.status_code == 404


def test_get_detail_404() -> None:
    response: requests.Response = requests.get(URL_DETAIL)
    data: dict = response.json()

    assert response.status_code == 200
    assert 'ready' in data.keys()
    assert 'text' in data.keys()


def test_head_detail_200() -> None:
    response: requests.Response = requests.head(URL_DETAIL)

    assert response.status_code == 200


def test_post_405() -> None:
    response: requests.Response = requests.post(
        URL_DETAIL,
    )
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "POST" not allowed.'


def test_put_405() -> None:
    response: requests.Response = requests.put(URL_DETAIL)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "PUT" not allowed.'


def test_patch_405() -> None:
    response: requests.Response = requests.patch(URL_DETAIL)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "PATCH" not allowed.'


def test_delete_405() -> None:
    response: requests.Response = requests.delete(URL_DETAIL)
    data: dict = response.json()

    assert response.status_code == 405
    assert data.get('detail', '') == 'Method "DELETE" not allowed.'


def test_options_200() -> None:
    response: requests.Response = requests.options(URL_DETAIL)
    data: dict = response.json()

    assert response.status_code == 200
    assert data == OPTIONS
