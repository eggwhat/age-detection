import pandas as pd
import os
import cv2 

def detect_faces(path_to_image, minNeighbors = 5):
    img = cv2.imread(path_to_image)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml" # pretrained model
    )
    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=minNeighbors, minSize=(40, 40)
    )
    crops = []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        crops.append(img[y:y+h, x:x+w])
    return {
        'result': cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
        'faces': faces,
        'crops': crops
    }

def evaluate(input_dir, df, minNeighbors = 5):
    toReview = []
    falsePositives = 0
    notDetected = 0
    notDetectedRows = []
    for index, row in df.iterrows():
        path_to_image = input_dir + '/images/' + row.image_name
        detected = detect_faces(path_to_image, minNeighbors)
        if len(detected['faces']) != row.faces_n:
            toReview.append({ 'row': row, 'output': detected})
        if len(detected['faces']) > row.faces_n:
            falsePositives = falsePositives + (len(detected['faces']) - row.faces_n)
        if len(detected['faces']) < row.faces_n:
            notDetected = notDetected + (row.faces_n - len(detected['faces']))
            notDetectedRows.append({'row': row, 'output': detected})
        
    return {
        'good': len(df) - len(toReview),
        'toReview': toReview,
        'falsePositives': falsePositives,
        'notDetected': notDetected,
        'notDetectedRows': notDetectedRows
    }

    

if __name__ == "__main__":
    input_dir = os.path.join('', 'data')
    m_path = input_dir + '/faces.csv'  # change this to your metadata file
    df_faces = pd.read_csv(m_path)
    df_faces = df_faces.groupby('image_name').size().reset_index(name='faces_n')
    print(f"Amount of images: {len(df_faces)}")
    # evaluate(input_dir, df_faces)