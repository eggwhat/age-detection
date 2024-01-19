import cv2
import numpy as np
import os


def generate_video(frames, temp_dir, frame_rate):
    height, width, _ = np.array(frames[0]).shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = os.path.join(temp_dir, 'output.mp4')
    video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (width, height))

    for frame in frames:
        video_writer.write(frame)

    video_writer.release()

    with open(output_path, 'rb') as output_file:
        return output_file.read()


def process_video(file_path, detect_faces_video, apply_bounding_box, model):
    frames = []
    video = cv2.VideoCapture(file_path)
    frame_rate = int(video.get(cv2.CAP_PROP_FPS))

    index = 0
    res = None
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if index % 5 == 0:
            res = detect_faces_video(frame, model)
        frame = apply_bounding_box(frame, res)
        frames.append(frame)
        index += 1

    video.release()
    return frames, frame_rate
