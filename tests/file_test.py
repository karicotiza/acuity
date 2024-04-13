import requests
import pathlib


def test_file_recognition() -> None:
    url: str = 'http://localhost:8000/api/v1/file/'
    file: pathlib.Path = pathlib.Path('tests', 'audio.wav')
    files: dict = {'file': open(file, 'rb')}

    response: requests.Response = requests.post(url=url, files=files)
    data: dict = response.json()

    assert response.status_code == 201
    assert data.get('status') == 'hano world'
