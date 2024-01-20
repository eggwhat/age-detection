import os
import sys
train_module_path = os.path.abspath(os.path.join('..'))
if train_module_path not in sys.path:
    sys.path.append(train_module_path)

from data.consts import DATA_DIR

import numpy as np
from scipy.io import loadmat
import pandas as pd
import datetime as date
from dateutil.relativedelta import relativedelta

cols = ['age', 'gender', 'path', 'face_score1', 'face_score2']

IMDB = 'imdb'
WIKI = 'wiki'
datasets = [IMDB, WIKI]

def extract_birthdate(images_path, dataset):
    dob = []
    if dataset == IMDB:
        for file in images_path:
            temp = file.split('_')[3]
            temp = temp.split('-')
            if len(temp[1]) == 1:
                temp[1] = '0' + temp[1]
            if len(temp[2]) == 1:
                temp[2] = '0' + temp[2]

            if temp[1] == '00':
                temp[1] = '01'
            if temp[2] == '00':
                temp[2] = '01'        
            dob.append('-'.join(temp))
    elif dataset == WIKI:
        for file in images_path:
            dob.append(file.split('_')[2])
    return dob

def extract_images_path(crop_path, full_paths):
    images_path = []
    for path in full_paths:
        images_path.append(crop_path + '/' + path[0])
    return images_path

def extract_genders(gender):
    genders = []
    for n in range(len(gender)):
        if gender[n] == 1:
            genders.append('male')
        else:
            genders.append('female')
    return genders

def extract_ages(dob, photo_taken):
    age = []
    for i in range(len(dob)):
        try:
            d1 = date.datetime.strptime(dob[i][0:10], '%Y-%m-%d')
            d2 = date.datetime.strptime(str(photo_taken[i]), '%Y')
            rdelta = relativedelta(d2, d1)
            diff = rdelta.years
        except Exception as ex:
            diff = -1
        age.append(diff)
    return age

def prepare_dataframe(dataset):
    crop_path = DATA_DIR + '/' + dataset + '_crop'
    dataset_mat = crop_path + '/' + dataset + '.mat'
    dataset_data = loadmat(dataset_mat)

    photo_taken = dataset_data[dataset][0][0][1][0]
    full_paths = dataset_data[dataset][0][0][2][0]
    gender = dataset_data[dataset][0][0][3][0]
    face_score1 = dataset_data[dataset][0][0][6][0]
    face_score2 = dataset_data[dataset][0][0][7][0]

    images_path = extract_images_path(crop_path, full_paths)
    genders = extract_genders(gender)
    dob = extract_birthdate(images_path, dataset)
    age = extract_ages(dob, photo_taken)

    final = np.vstack((age, genders, images_path, face_score1, face_score2)).T
    final_df = pd.DataFrame(final)
    final_df.columns = cols
    return final_df

if __name__ == "__main__":
  meta = pd.concat((prepare_dataframe(IMDB), prepare_dataframe(WIKI)))

  # Clean up corrupted pictures
  meta = meta[meta['face_score1'] != '-inf']
  meta = meta[meta['face_score2'] == 'nan']

  meta = meta.drop(['face_score2'], axis=1)

  meta.to_csv(DATA_DIR + '/metadata.csv', index=False)

  # Data clean up based on EDA
  meta['age'] = pd.to_numeric(meta['age'])
  meta = meta[meta['age'] > -1]
  meta = meta[meta['age'] < 123]
  meta.to_csv(DATA_DIR + '/metadata-clean.csv', index=False)


  print('Amount of crop faces: ', len(meta))
  print('File is saved to ', DATA_DIR + '/metadata-clean.csv')