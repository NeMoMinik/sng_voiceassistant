from omegaconf import OmegaConf
from time import sleep
import torch
import sounddevice as sd
import os
import pickle
language = 'ru'
model_id = 'ru_v3'
device = torch.device('cpu')
def_path = 'C:/Users/User/Desktop/sng_voiceassistant/voices/'
model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)

models = OmegaConf.load('latest_silero_models.yml')
sample_rate = 48000
speaker = 'aidar'
put_accent = True
put_yo = True
model.to(device)
with open('cache.pl', 'rb') as f:
    cache = pickle.load(f)


def speak(text, save=True):
    text = "<speak><prosody rate='fast'>" + text + "</prosody></speak>"
    if text in cache.keys():
        audio = cache[text]
        sd.play(audio)
    else:
        audio = model.apply_tts(ssml_text=text,
                                # voice_path='C:/Users/User/Desktop/sng_voiceassistant/voices/funny.pt',
                                speaker=speaker,
                                sample_rate=sample_rate,
                                put_accent=put_accent,
                                put_yo=put_yo)
        cache.update({text: audio})
        if save:
            sd.play(audio)
            with open('cache.pl', 'wb') as f:
                pickle.dump(cache, f)
        else:
            sd.play(audio)
    sleep(len(audio) / 36000)


print('LOG voice.py has been initialized')