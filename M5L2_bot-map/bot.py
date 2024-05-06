import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:  ...")
    # Допиши команды бота


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    command_args = message.text.split()
    city_name = command_args[1]
    marker_color = 'blue'  # По умолчанию цвет маркера будет синим
    if len(command_args) > 2:
        marker_color = command_args[2]  # Если указан цвет, используй его
    manager.create_grapf('map.png', cities=[city_name], marker_color=marker_color)
    with open('map.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    user_id = message.chat.id
    cities = manager.select_cities(user_id)
    if not cities:
        bot.send_message(message.chat.id, 'Вы еще не добавили ни одного города.')
        return
    for city in cities:
        marker_color = 'blue'  # По умолчанию цвет маркера будет синим
        manager.create_grapf(f'{city}.png', [city], marker_color)
        with open(f'{city}.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
