import random as rd
from nltk.corpus import stopwords
import json
import pymorphy2 as pm2

stop_words = stopwords.words("russian")
morph = pm2.MorphAnalyzer()

TRIGGERS = {'портал', 'порталы', 'бокал', 'порт'}

with open('intents.json', 'r', encoding='utf-8') as f:
    data_set = json.load(f)
    y = list(data_set.keys())
    for i in y:
        k = map(lambda x: morph.parse(x)[0].normal_form, i.split())
        k = ' '.join(filter(lambda x: x not in stop_words, k))
        data_set[k] = data_set.pop(i)

with open('intents.json', 'w', encoding='utf-8') as f:
    json.dump(data_set, f, indent=4, ensure_ascii=False)

weather_conditions = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно',
    'drizzle': 'морось',
    'light-rain': 'небольшой дождь',
    'rain': 'дождь',
    'moderate-rain': 'умеренно сильный дождь',
    'heavy-rain': 'сильный дождь',
    'continuous-heavy-rain': 'длительный сильный дождь',
    'showers': 'ливень',
    'wet-snow': 'дождь со снегом',
    'light-snow': 'небольшой снег',
    'snow': 'снег',
    'snow-showers': 'снегопад',
    'hail': 'град',
    'thunderstorm': 'сухая гроза',
    'thunderstorm-with-rain': 'дождь с грозой',
    'thunderstorm-with-hail': 'гроза с градом',
}
week = ['понед+ельник', 'вт+орник', 'сред+а', 'четв+ерг', 'п+ятница', 'суб+ота', 'воскрес+енье']

months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

forbidden = {...}

show_data = {'начинай шоу': 'show = True',
             'заканчивай шоу': 'show = False'}


print('LOG words.py has been initialized')