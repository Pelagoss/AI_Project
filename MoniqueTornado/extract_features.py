import os

import librosa
import soundfile as sf
import numpy as np
import glob
import pandas as pd

def get_features(file_name):

    if file_name: 
        X, sample_rate = sf.read(file_name, dtype='float32')

    # mfcc (mel-frequency cepstrum)
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
    mfccs_scaled = np.mean(mfccs.T,axis=0)
    return mfccs_scaled

def create_label_txt():
    f = None
    path_to_filename = "model/labels.txt"
    f = open(path_to_filename, "w")
    f.write("")
    f.close()

def add_labels(label):
    path_to_filename = "model/labels.txt"
    f = open(path_to_filename, "a")

    f.write("{}\n".format(label))
    f.close()

def extract_features():
    create_label_txt()
    # path to dataset containing 10 subdirectories of .ogg files
    #sub_dirs = os.listdir('dataset')
    sub_dirs = os.listdir('audio')
    sub_dirs.sort()
    features_list = []
    for label, sub_dir in enumerate(sub_dirs):
        add_labels(sub_dir)
        #for file_name in glob.glob(os.path.join('dataset',sub_dir,"*.ogg")):
        for file_name in glob.glob(os.path.join('audio',sub_dir,"*.wav")) + glob.glob(os.path.join('audio',sub_dir,"*.ogg")):
            print("Extracting file ", file_name)
            try:
                mfccs = get_features(file_name)
            except Exception as e:
                print("Extraction error")
                continue
            features_list.append([mfccs,label])

    features_df = pd.DataFrame(features_list,columns = ['feature','class_label'])
    print(features_df.head())    
    return features_df
