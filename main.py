import json
import queue
import random as rd
import sounddevice as sd
import vosk
import nltk
from fuzzywuzzy import fuzz
import time

import words

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from skills import *
import voice

stop_words = stopwords.words("russian")
q = queue.Queue()
vosk_model = vosk.Model('model_small')
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
show = False


def recognize(data):
    if data:
        trg = words.TRIGGERS.intersection(data.split())
        forbidden = words.forbidden.intersection(data.split())
        dat_stop = map(lambda x: morph.parse(x)[0].normal_form, data.split())
        data = filter(lambda x: x not in stop_words and x not in trg, data.split())
        data = ' '.join(map(lambda x: morph.parse(x)[0].normal_form, data))
        if not trg:
            return
        elif forbidden:
            pass
        else:
            print(data)
            print(' '.join(dat_stop))
            answer = '"Извините, я вас не понял"'
            k_max = 0
            for i in words.data_set.keys():
                k = fuzz.token_sort_ratio(i, data)
                print(k, i)
                if k > 85 and k > k_max:
                    k_max = k
                    answer = words.data_set[i]
            voice.speak(eval(answer))


def main():
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=lambda indata, x, y, z: q.put(bytes(indata))):
        rec = vosk.KaldiRecognizer(vosk_model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data)
            else:
                time.sleep(0.1)


print('LOG main.py has been initialized')

if __name__ == '__main__':
    main()
