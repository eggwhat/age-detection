import websockets
import os
import pytest
import cv2
import base64

API_WS_URL = "ws://localhost:8000/detect-age/ws"
FRAME_PATH = os.path.join(os.path.dirname(__file__), 'frame.jpg')


@pytest.mark.asyncio
async def test_detect_age_single_websocket():
    async with websockets.connect(API_WS_URL) as websocket:
        frame = cv2.imread(FRAME_PATH)
        for _ in range(3):
            _, encoded_frame = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(encoded_frame.tobytes()).decode('utf-8')
            await websocket.send(frame_data)
            response = await websocket.recv()
            assert len(response) > 0


if __name__ == "__main__":
    pytest.main()
