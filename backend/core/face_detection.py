import cv2
from PIL import Image


def detect_faces(img, model):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # pretrained model
    )
    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        face_img = img[y:y+h, x:x+w]
        prediction = model.predict(Image.fromarray(face_img).convert('RGB'))
        cv2.putText(img, prediction, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    return {
        'faces': faces
    }


def detect_faces_video(img, model):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # pretrained model
    )
    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )

    predictions = []
    for (x, y, w, h) in faces:
        face_img = img[y:y+h, x:x+w]
        predictions.append(model.predict(Image.fromarray(face_img).convert('RGB')))
    return {
        'faces': faces,
        'predictions': predictions
    }


def apply_bounding_box(frame, detected_faces):
    for (x, y, w, h), prediction in zip(detected_faces['faces'], detected_faces['predictions']):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
        cv2.putText(frame, prediction, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame
