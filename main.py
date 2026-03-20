import telebot
import requests
from config import BOT_TOKEN, WEATHER_API
bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "В каком городе Украины хотите узнать погоду?")
@bot.message_handler(func=lambda message: True)
def weather(message):
    city = message.text.strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},UA&appid={WEATHER_API}&units=metric&lang=ru"
    response = requests.get(url).json()
    if response.get("cod") != 200:
        bot.reply_to(message, "Город не найден!")
        return
    temp = response["main"]["temp"]
    feels = response["main"]["feels_like"]
    desc = response["weather"][0]["description"].capitalize()
    wind = response["wind"]["speed"]
    reply = f"Погода в {city}:\n{desc}\n Температура: {temp}°C (ощущается как {feels}°C)\n Ветер: {wind} м/с"
    bot.reply_to(message, reply)
bot.infinity_polling()