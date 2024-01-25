import os
import requests
import pytest

API_URL = "http://localhost:8000/detect-age/multiple"
TEST_IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'test_images')


def test_valid_images():
    files = {('files', ('valid_image_1.jpg', open(os.path.join(TEST_IMAGES_PATH,
                                                               'valid_images/valid_image_1.jpg'), 'rb'), 'image/jpeg')),
             ('files', ('valid_image_2.png', open(os.path.join(TEST_IMAGES_PATH,
                                                               'valid_images/valid_image_2.png'), 'rb'), 'image/png'))}

    response = requests.post(API_URL, files=files)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/x-zip-compressed'
    assert len(response.content) > 0


def test_invalid_file_format():
    files = [('files', ('invalid_image_1.txt', open(os.path.join(TEST_IMAGES_PATH,
                                            'invalid_images/invalid_image_1.txt'), 'rb'), 'text/plain')),
             ('files', ('invalid_image_2.yml', open(os.path.join(TEST_IMAGES_PATH,
                                            'invalid_images/invalid_image_2.yml'), 'rb'), 'text/yaml'))]

    response = requests.post(API_URL, files=files)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['detail'] == 'Invalid file format. Please upload an image.'


if __name__ == "__main__":
    pytest.main()
