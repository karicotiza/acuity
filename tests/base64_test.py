import requests
import pathlib


def test_base64_recognition() -> None:
    url: str = 'http://localhost:8000/api/v1/base64/'
    file: pathlib.Path = pathlib.Path('tests', 'base64.txt')
    payload: dict = {'base64': open(file, 'r', encoding='utf-8')}

    response: requests.Response = requests.post(url=url, data=payload)
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('status') == 'hano world'
