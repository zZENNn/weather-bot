from array import array
from tokenize import String

import telebot
from telebot import types
import config
import requests
import json

bot = telebot.TeleBot(config.TOKEN)

conditions_RU = {
'clear':'ясно ☀',
'partly-cloudy' : 'малооблачно 🌤',
'cloudy' : 'облачно с прояснениями.⛅',
'overcast' : 'пасмурно.☁',
'drizzle' : 'морось.🌧',
'light-rain' : 'небольшой дождь.🌧',
'rain' : 'дождь.☔',
'moderate-rain' : 'умеренно сильный дождь.☔',
'heavy-rain' : 'сильный дождь.☔',
'continuous-heavy-rain' : 'длительный сильный дождь.☔',
'showers' : 'ливень.☔',
'wet-snow' : 'дождь со снегом.🌧❄',
'light-snow' : 'небольшой снег.❄',
'snow' : 'снег.❄',
'snow-showers' : 'снегопад.❄❄❄',
'hail' : 'град.🌨',
'thunderstorm' : 'гроза.⚡',
'thunderstorm-with-rain' : 'дождь с грозой.⛈',
'thunderstorm-with-hail' : 'гроза с градом.⚡🌨',
}

city = 'Новосибирск'#город по умолчанию

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сменить город")
    btn2 = types.KeyboardButton("Погода")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f'Привет! Для взаимодействия с ботом используй кнопки.\nТекущий город:\n{city}', reply_markup=markup)
@bot.message_handler(commands=['set_city'])
@bot.message_handler(func=lambda message: message.text == "Сменить город")
def set_city(message):
    
    bot.send_message(message.chat.id,'Введите город:')
    @bot.message_handler(func=lambda message: True)
    def city_answer(message):
        global city
        city = message.text
        bot.send_message(message.chat.id,city)

@bot.message_handler(commands=['get_weather'])
@bot.message_handler(func=lambda message: message.text == "Погода")
def get_weather(message):
    geocode_req = requests.get(f'https://geocode-maps.yandex.ru/1.x?geocode={city}&apikey={config.GEO_CODE_API_TOKEN}')
    # print(geocode_req.content)
    geocode_req_json = json.loads(geocode_req.content)
    point = geocode_req_json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    arr_point = str(point).split(' ')
    long = arr_point[0]
    lat = arr_point[1]
    
    req = requests.get(f'https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={long}&[lang=ru_RU]&[limit=1]&[hours=false]&[extra=false]',headers={'X-Yandex-API-Key':config.YA_WEATHER_API_TOKEN })
    answer_json = req.json()
    temp = str(answer_json['fact']['temp']) + '°C'
    cond = answer_json['fact']['condition']
    condition = conditions_RU[cond]
    mess = f'Погода в {city} сейчас:\n{temp}\n{condition}'
    #print('condition: ' + str(answer_json['fact']['condition']))
    bot.send_message(message.chat.id,mess)


# RUN
bot.polling(none_stop=True)
