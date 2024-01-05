import os
import cv2
import numpy as np
from datetime import datetime
from keras.preprocessing.image import ImageDataGenerator


class ImageAugmentor:
    def __init__(self, source_directory, target_directory):
        self.source_directory = source_directory
        self.target_directory = target_directory

    def calculate_age(self, dob, photo_year):
        return photo_year - dob.year

    def augment_image(self, img):
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=0.25,
            brightness_range=[0.4, 1.5],
            horizontal_flip=True,
            channel_shift_range=40,
            fill_mode='nearest')

        generator = datagen.flow(np.array([img]), batch_size=1)
        augmented_image = generator.next()[0]
        return augmented_image

    def detect_faces(self, img):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # pretrained model
        )
        faces = face_classifier.detectMultiScale(
            gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )
        face_images = []  # To store the extracted face images
        for (x, y, w, h) in faces:
            face_img = img[y:y + h, x:x + w]
            face_images.append(face_img)
        return {
            'result': cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
            'face_images': face_images
        }

    def process_images(self):
        for dirname in os.listdir(self.source_directory):
            current_dir = os.path.join(self.source_directory, dirname)
            for filename in os.listdir(current_dir):
                fname = filename.rstrip('.jpg')
                parts = fname.split('_')
                if len(parts) >= 3:
                    try:
                        dob = datetime.strptime(parts[1], '%Y-%m-%d')
                    except:
                        continue
                    photo_year = int(parts[2])

                    age = self.calculate_age(dob, photo_year)
                    if age < 10 or age > 50:
                        img_path = os.path.join(current_dir, filename)
                        image = cv2.imread(img_path)

                        if self.detect_faces(image):
                            save_path = os.path.join(self.target_directory, f'augmented_{filename}')
                            if os.path.exists(save_path):
                                continue
                            augmented_image = self.augment_image(image)
                            cv2.imwrite(save_path, cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))


source_dir = 'wiki_crop_big'
target_dir = './data_augmented'
augmentor = ImageAugmentor(source_dir, target_dir)
augmentor.process_images()
