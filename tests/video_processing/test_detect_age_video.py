import requests
import pytest
import os

API_URL = "http://localhost:8000/detect-age/video"
VALID_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'test_videos/valid_videos/valid_video.mp4')
INVALID_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'test_videos/invalid_videos/invalid_video.txt')


def test_valid_video():
    with open(VALID_VIDEO_PATH, 'rb') as video_file:
        files = {'file': ('test_video.mp4', video_file, 'video/mp4')}
        response = requests.post(API_URL, files=files)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'video/mp4'
    assert len(response.content) > 0


def test_invalid_file_format():
    with open(INVALID_VIDEO_PATH, 'rb') as video_file:
        files = {'file': ('test_video.txt', video_file, 'text/plain')}
        response = requests.post(API_URL, files=files)

    assert response.status_code == 400
    assert "Invalid file format" in response.text


if __name__ == "__main__":
    pytest.main()
