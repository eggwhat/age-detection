from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from PIL import Image
from classes import CLASSES, class_labels_reassign

import sys
sys.path.append('../../../../backend')
from core.models.resnet18_7c import Resnet18_7C

def read_data(n = 100):
  path_to_metadatacsv = os.path.realpath('D:\WUT\IML\data/win-metadata-clean-aug.csv')
  df = pd.read_csv(path_to_metadatacsv)
  df['target'] = df['age'].map(class_labels_reassign)
  print(f"0: {len(df[df['target'] == 0])}")
  print(f"1: {len(df[df['target'] == 1])}")
  print(f"2: {len(df[df['target'] == 2])}")
  print(f"3: {len(df[df['target'] == 3])}")
  print(f"4: {len(df[df['target'] == 4])}")
  print(f"5: {len(df[df['target'] == 5])}")
  print(f"6: {len(df[df['target'] == 6])}")
  df0 = df[df['target'] == 0].head(n)
  df1 = df[df['target'] == 1].head(n)
  df2 = df[df['target'] == 2].head(n)
  df3 = df[df['target'] == 3].head(n)
  df4 = df[df['target'] == 4].head(n)
  df5 = df[df['target'] == 5].head(n)
  df6 = df[df['target'] == 6].head(n)
  return pd.concat([df0, df1, df2, df3, df4, df5, df6])
  

if __name__ == "__main__":
  Resnet18_7CModel = Resnet18_7C(model_path='../scripts/output-aug-lr01-25e-step5/model.pt')  # init trained model
  df = read_data(n = 100)
  print(len(df))
  y_true = df['target']
  y_pred = []
  for index, row in df.iterrows():
    img = Image.open(row.path).convert('RGB')
    y_pred.append(Resnet18_7CModel.predict_class(img))

  print("Prediction completed.")
  print(f"y_true: {len(y_true)}. y_pred: {len(y_pred)}")
  cm = confusion_matrix(y_true, y_pred)
  accuracy = accuracy_score(y_true, y_pred)
  print(f'Accuracy: {accuracy * 100:.2f}%')

  output_dir = os.path.join('', 'output')
  isExist = os.path.exists(output_dir)
  if not isExist:
      os.makedirs(output_dir)
      print("Output dir is created!")

  plt.figure(figsize=(8, 6))
  sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=range(0, 7), yticklabels=range(0, 7))
  plt.xlabel('Predicted')
  plt.ylabel('True')
  plt.title(f'Confusion Matrix. Accuracy: {accuracy * 100:.2f}%')
  plt.savefig('./output/confusion_matrix.png')

