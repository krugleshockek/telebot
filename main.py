import telebot
import requests
import translators
from telebot import types


url = "https://burgers1.p.rapidapi.com/burgers"


headers = {
	"X-RapidAPI-Host": "burgers1.p.rapidapi.com",
	"X-RapidAPI-Key": "035726d206mshb212179a4a73aedp1ad7ccjsn4dcd433d6767"
}

response = requests.request("GET", url, headers=headers)
ass_message = []
upshot = []

n = 0

for _ in response.json():
    if n <= 9:
        n += 1
        upshot.append(str(n) + ') ' + _['name'])
    else:
        break


list_of_burger = '\n' + '\n'.join(upshot)
list_of_burger += '\n'

token = '5225461298:AAEC_VwxJRSuxvD-OSQFjLYLhbZIbP1dihk'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет!! Я бот. Это бургеры, о которых я знаю ВСЁ: {list_of_burger} Натыкай "/button"')


@bot.message_handler(commands=['button'])
def button_message(message):
    klava = types.ReplyKeyboardMarkup(resize_keyboard=True)
    choose_boorger_1 = types.KeyboardButton('1')
    choose_boorger_2 = types.KeyboardButton('2') 
    choose_boorger_3 = types.KeyboardButton('3') 
    choose_boorger_4 = types.KeyboardButton('4') 
    choose_boorger_5 = types.KeyboardButton('5') 
    choose_boorger_6 = types.KeyboardButton('6')
    choose_boorger_7 = types.KeyboardButton('7')
    choose_boorger_8 = types.KeyboardButton('8')
    choose_boorger_9 = types.KeyboardButton('9')
    choose_boorger_10 = types.KeyboardButton('10')
    klava.add(choose_boorger_1, choose_boorger_2, choose_boorger_3, choose_boorger_4, choose_boorger_5, choose_boorger_6, choose_boorger_7,
                 choose_boorger_8, choose_boorger_9, choose_boorger_10)
        
    bot.send_message(message.chat.id, "Тыкни на кнопку", reply_markup=klava)
        

@bot.message_handler(content_types='text')
def message_reply(message):
    if int(message.text) + 1 in range(1, 10):
        url = "https://burgers1.p.rapidapi.com/burgers"

        headers = {
	    "X-RapidAPI-Host": "burgers1.p.rapidapi.com",
	    "X-RapidAPI-Key": "035726d206mshb212179a4a73aedp1ad7ccjsn4dcd433d6767"
        }

        line = {'name': str(upshot[int(message.text) - 1]).split(') ')[1]}
        response = requests.request("GET", url, headers=headers, params=line)
        sostav = str()
        for _ in response.json():
	        for i in _['ingredients']:
	            sostav += translators.google(i, from_language='en', to_language='ru') + ', '

        ass_message.append(response.json()[0]['name'])
        ass_message.append(response.json()[0]['addresses'][0]['country'])
        ass_message.append(translators.google(response.json()[0]['description'], from_language='en', to_language='ru'))

        bot.send_message(message.chat.id, f'Страна приготовления - {ass_message[1]}. Кратко о бургере - {ass_message[2]}.')
        bot.send_message(message.chat.id, f'Состав - {sostav[0:len(sostav) - 2]}.')


bot.infinity_polling()
