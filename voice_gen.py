# pip install pyttsx3
import torch
from omegaconf import OmegaConf
import sounddevice as sd

language = 'ru'
model_id = 'ru_v3'
device = torch.device('cpu')

model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
models = OmegaConf.load('latest_silero_models.yml')
sample_rate = 48000
speaker = 'random'
put_accent = True
put_yo = True
model.to(device)
while True:
    audio = model.apply_tts(text=example_text,
                        speaker=speaker,
                        sample_rate=sample_rate,
                        put_accent=put_accent,
                        put_yo=put_yo)
    print('ready')
    def speak(text):
        sd.play(audio)
    speak(example_text)
    if voice_path := input():
        model.save_random_voice(voice_path + '.pt')