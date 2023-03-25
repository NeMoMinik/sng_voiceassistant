import time
import words
from num2words import num2words
import requests as rq
import pymorphy2 as pm2

morph = pm2.MorphAnalyzer()


class Schedule:
    sched_time = [range(480, 521), range(521, 531), range(531, 571), range(571, 586), range(586, 626), range(626, 641), range(641, 681), range(681, 696), range(696, 736)]
    sched_items = [...]

    @classmethod
    def get_lesson_num(cls):
        for i, j in zip(cls.sched_time, range(len(cls.sched_items))):
            if get_time() in i:
                return j
        else:
            return -1

    @classmethod
    def get_time(cls):
        current_time = time.localtime()
        current_time = current_time.tm_min + current_time.tm_hour * 60
        return current_time


def get_time():
    current_time = time.localtime()
    mins_val = current_time.tm_min
    hour_val = current_time.tm_hour

    mins = morph.parse('минута')[0].make_agree_with_number(mins_val).word
    hours = morph.parse('час')[0].make_agree_with_number(hour_val).word

    hour_val = num2words(hour_val, lang='ru')
    mins_val = num2words(mins_val, lang='ru')

    if mins_val.split()[-1] == 'один':
        mins_val = mins_val.replace('один', 'одна')
    elif mins_val.split()[-1] == 'два':
        mins_val = mins_val.replace('два', 'две')
    return f'Сейчас {hour_val} {hours} {mins_val} {mins}'


def weather():
    try:
        response = rq.get('https://api.weather.yandex.ru/v2/informers/?lat=54.988717&lon=82.8514709', headers={'X-Yandex-API-Key': 'e936d04b-df94-43f0-9501-cca9a4e15e5b'})
        if response.status_code == 200:
            r = response.json()['fact']
            temp = r['temp']
            f_temp = r['feels_like']
            t_text = morph.parse('градус')[1].make_agree_with_number(temp).word
            condition = r['condition']
            speed = r['wind_speed']
            meter = morph.parse('метр')[0].make_agree_with_number(int(str(speed)[-1])).word
            text = f'Сейчас {words.weather_conditions[condition]}, {num2words(temp, lang="ru")} {t_text} цельсия, ощущается как {num2words(f_temp, lang="ru")}. Скорость в+етра {num2words(speed, lang="ru")} {meter} в секунду.'.replace('запятая ', '')
            return text
        else:
            return 'Извините, не удалось получить доступ к данным о погоде.'
    except rq.exceptions.ConnectionError:
        return 'Извините, не удалось получить доступ к данным о погоде.'


def week_day():
    current_time = time.localtime()
    return f'сегодня {words.week[current_time.tm_wday]}'


def day():
    current_time = time.localtime().tm_mday
    current_month = time.localtime().tm_mon
    word = num2words(current_time, lang='ru', to='ordinal').split()
    day_word = morph.parse(word[-1])[0].inflect({'accs', 'neut'})[0]
    if len(word) > 1:
        word = word[0] + ' ' + day_word
    else:
        word = day_word
    return f'Сегодня {word} {words.months[current_month - 1]}.'


def lesson(data):
    return 'Пока что это функция недоступна'


def when_lesson():
    t = Schedule.get_time()
    for j, i in enumerate(Schedule.sched_time):
        if t in i:
            x = i[-1] - t
            if x == 1:
                x = 60 - time.localtime().tm_sec
                sec = morph.parse('секунда')[0].make_agree_with_number(x).word
                return f'До начала урока {x} {sec}. Поторопись!'
            else:
                minutes = morph.parse('минута')[0].make_agree_with_number(x).word
                return f'До конца перемены {x} {minutes}'
    else:
        return 'Кажется, уроки уже закончились'


def hi():
    t = time.localtime().tm_hour
    if t < 13:
        return "Доброе утро", True
    elif t < 17:
        return "Добрый день", True
    else:
        return "Добрый вечер", True


print('LOG skills.py has been initialized')