import cv2
import websockets
import asyncio
import base64
import numpy as np


async def send_frames(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            ret, frame = camera.read()
            _, encoded_frame = cv2.imencode('.jpg', frame)
            base64_encoded_frame = base64.b64encode(encoded_frame.tobytes()).decode('utf-8')

            # Send the base64-encoded frame to the server
            await websocket.send(base64_encoded_frame)

            # Receive the processed frame from the server
            processed_frame = await websocket.recv()
            decoded_processed_frame = base64.b64decode(processed_frame)
            processed_frame_data = np.frombuffer(decoded_processed_frame, dtype=np.uint8)

            # Do something with the processed frame data (e.g., display it)
            processed_frame = cv2.imdecode(processed_frame_data, 1)
            cv2.imshow("Processed Frame", processed_frame)
            cv2.waitKey(1)

if __name__ == "__main__":
    url = "ws://localhost:8000/detect-age/ws"
    camera = cv2.VideoCapture(0)

    asyncio.run(send_frames(url))
