import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from scipy.io.wavfile import write

from keras.models import load_model
import extract_features
import numpy as np
import sounddevice as sd
import colorama

colorama.init()

def float2pcm(sig, dtype='int16'):
    sig = np.asarray(sig)
    dtype = np.dtype(dtype)
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)


if __name__ == "__main__":
    #labels = ["MoniqueTornado", "Noise"]
    labels = []
    with open('MoniqueTornado/model/labels.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        label = line.replace('\n', "")
        labels.append(f'{colorama.Fore.GREEN}{label}{colorama.Fore.WHITE}')

    model = load_model("MoniqueTornado/model/trained_cnn.h5")

    fs = 44100  # Sample rate
    seconds = 4  # Duration of recording
    file_name = "MoniqueTornado/output/output.wav"

    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished

        write('MoniqueTornado/output/output.wav', fs, float2pcm(myrecording))

    print("Testing "+file_name+"...")

    prediction_feature = extract_features.get_features(file_name)
    prediction_feature = np.expand_dims(np.array([prediction_feature]), axis=2)

    prediction = model.predict(prediction_feature)

    better_class = np.argmax(prediction[0])

    print("Predicted class : "+colorama.Fore.GREEN+labels[better_class]+colorama.Fore.WHITE + " at "+str(prediction[0][better_class]*100)+"%")
