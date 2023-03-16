import json
import queue
import random as rd
import sounddevice as sd
import vosk
from sklearn.feature_extraction.text import CountVectorizer  # pip install scikit-learn
from sklearn.linear_model import LogisticRegression

from skills import *

q = queue.Queue()
vosk_model = vosk.Model('model_small')
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
show = False


def recognize(data, vectorizer, clf):
    if data:
        print(data)
        trg = words.TRIGGERS.intersection(data.split())
        forbidden = words.forbidden.intersection(data.split())
        if not trg:
            return
        elif forbidden:
            pass
        else:
            data.replace(list(trg)[0], '')
            text_vector = vectorizer.transform([data]).toarray()[0]
            answer = clf.predict([text_vector])[0]
            voice.speak(eval(answer))


def main():
    vectorizer = CountVectorizer()
    show_vect = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    clf_show = LogisticRegression()
    clf_show.fit(show_vect.fit_transform(list(words.show_data.keys())), list(words.show_data.values()))

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=lambda indata, x, y, z: q.put(bytes(indata))):
        rec = vosk.KaldiRecognizer(vosk_model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                # if 'шоу' in data or show:
                #     recognize(data, show_vect, clf_show)
                # else:
                recognize(data, vectorizer, clf)


print('LOG main.py has been initialized')

if __name__ == '__main__':
    main()
