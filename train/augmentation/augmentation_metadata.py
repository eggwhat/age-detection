import os
import cv2
import numpy as np
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator


class ImageAugmentor:
    def __init__(self, target_directory, metadata_path, metadata_columns):
        self.target_directory = target_directory
        self.metadata_path = metadata_path
        self.metadata_columns = metadata_columns
        self.num_images_per_age = {}
        self.datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=0.25,
            brightness_range=[0.4, 1.5],
            horizontal_flip=True,
            channel_shift_range=40,
            fill_mode='nearest')
        for age in range(0, 11):
            self.num_images_per_age[age] = 9
        for age in range(50, 121):
            if age < 57:
                self.num_images_per_age[age] = 1
            elif age < 63:
                self.num_images_per_age[age] = 2
            elif age < 73:
                self.num_images_per_age[age] = 3
            elif age < 82:
                self.num_images_per_age[age] = 5
            else:
                self.num_images_per_age[age] = 9


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
        print(f"Start augmentation. metadata: {self.metadata_path}. Target: {self.target_directory}")
        metadata = pd.read_csv(self.metadata_path)
        augmented_metadata = {col: [] for col in self.metadata_columns}
        for index, row in metadata.iterrows():
            img_path = row['path']
            age = row['age']
            _, filename = os.path.split(img_path)
            name, _ = os.path.splitext(filename)
            if age < 10 or age > 50:
                print(f"Image to be augmented. Age: {age}")
                image = cv2.imread(img_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                if self.detect_faces(image):
                    print(f"Faces detected.")
                    generator = self.datagen.flow(np.array([image]), batch_size=8)
                    for i in range(self.num_images_per_age[age]):
                        output_path = os.path.abspath(os.path.join(self.target_directory, f'aug_{i}_{name}.jpg'))
                        if os.path.exists(output_path):
                            print(f"WARN: image with such path already exists: {output_path}")
                            continue
                        print(f"Saving image to {output_path}")
                        augmented_image = generator.next()[0].astype('uint8')
                        cv2.imwrite(output_path, cv2.cvtColor(augmented_image, cv2.COLOR_BGR2RGB))
                        print(f"SAVED. {output_path}")
                        augmented_metadata['age'].append(row['age'])
                        augmented_metadata['gender'].append(row['gender'])
                        augmented_metadata['path'].append(output_path)
                        augmented_metadata['face_score1'].append(1)

        augmented_metadata_df = pd.DataFrame(augmented_metadata)
        updated_metadata = pd.concat([metadata, augmented_metadata_df], ignore_index=True)
        print(f"Saving augmented metadata. Number of rows: {len(updated_metadata)}")
        updated_metadata.to_csv(self.metadata_path, index=False)


if __name__ == "__main__":
    target_dir = os.path.join('', 'data', 'augmented')  # change this to your output directory
    isExist = os.path.exists(target_dir)
    if not isExist:
        os.makedirs(target_dir)
        print("Augmented dir is created!")
    metadata_dir = os.path.join('..', 'data')  # change this to your metadata directory
    m_path = metadata_dir + '/metadata-clean.csv'  # change this to your metadata file
    m_columns = ['age', 'gender', 'path', 'face_score1']
    augmentor = ImageAugmentor(target_dir, m_path, m_columns)
    augmentor.process_images()
