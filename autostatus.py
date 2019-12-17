#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request
import requests
import datetime
import urllib
import json
import time

from env import token

#token = env(token) #Сюда вводим свой токен.
timeKD = 600 #Сюда вводим время обновления статуса.(Время в секундах)

def startStatus():
    getCountry = requests.get(f"https://api.vk.com/method/account.getProfileInfo?v=5.95&access_token={token}").json()
    try:
        city = getCountry["response"]["city"]["title"]
    except KeyError:
        print("У профиля не указан город, по умолчанию была выбрана Москва.")
        city = "Москва"
    try:
        data = requests.get("http://api.openweathermap.org/data/2.5/weather",
        params = {"q": city,
            "appid": "778d98cf94b6609bec655b872f24b907",
            "units": "metric",
            "lang": "eng"}).json()
    except:
            pass

    try:
        print(data)
    except:
        print("no weather data")

#    try:
#        getLikes = requests.get(f"https://api.vk.com/method/photos.get?album_id=profile&rev=1&extended=1&count=1&v=5.95&access_token={token}").json()
#        getLikes = getLikes["response"]["items"][0]["likes"]["count"]
#    except IndexError:
#        print("У профиля отсутсвует аватар или лайки.")
#        getLikes = 0

    getValuts = requests.get("https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=6780a6de85b0690a6e0f02e6fc5bfd4f").json().get("data")
    Dollar = getValuts.get("USDRUB")
    Euro = getValuts.get("EURRUB")
    Dollar = Dollar[:Dollar.find('.')]
    Euro = Euro[:Euro.find('.')]

    today = datetime.datetime.today()
    nowTime = today.strftime("%H")
    nowTime = int(nowTime)
    nowTime = nowTime+4
    nowDate = today.strftime("%d.%m.%Y")
    
    if nowTime >= 6 and nowTime < 12:
        greeting = "Доброе утро,"
    elif nowTime >= 12 and nowTime < 17:
        greeting = "Добрый день,"
    elif nowTime >= 17 and nowTime < 23:
        greeting = "Добрый вечер,"
    elif nowTime >= 23 and nowTime < 6:
        greeting = "Доброй ночи,"
    else:
        greeting = "Доброго времени суток"
    
    weather = ("Сейчас {0}℃, облачность {1}%, ветер {2} на {3} градусов, давление {4} гектопаскалей, влажность {5}%".format(
        str(data["main"]["temp"]), str(data["clouds"]["all"]), str(data["wind"]["speed"]), str(data["wind"]["deg"]), str(data["main"]["pressure"]),
        str(data["main"]["humidity"])))
    
    statusSave = ("{0} {1}! {2}".format(greeting, city, weather))
    statusOut = requests.get(f"https://api.vk.com/method/status.set?text={statusSave}&v=5.95&access_token={token}").json()
#    if statusOut.get("error", None):
#        print(f"Не удалось обновить статус сервер вернул неверный код ответа: {statusOut}")
#    else:
#        print(f"Статус был обновлен")

while True:
    startStatus()
    time.sleep(timeKD)
