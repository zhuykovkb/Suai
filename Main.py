import random
import telebot
import urllib.request as urllib2

import Constaints
import RaspParse

types = telebot.types
bot = telebot.TeleBot(Constaints.token)
print(bot.get_me())


def log(message, answer):
    print("\n ::::::::::")
    from datetime import datetime
    print((datetime.now()))
    print("Сообщение от {0} {1}. (id = {2})\nТекст - {3}".format(message.from_user.first_name,
                                                                 message.from_user.last_name,
                                                                 str(message.from_user.id),
                                                                 message.text))
    print(answer)


@bot.message_handler(commands=[Constaints.Week[0]])
def handleText(message):
    group = message.text.split(Constaints.Week[1])[1][1:]
    answer = RaspParse.GetWeekRasp(group)
    log(message, answer)

    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=[Constaints.Today[0]])
def handleText(message):
    group = message.text.split(Constaints.Today[1])[1][1:]
    answer = RaspParse.GetTodayRasp(group)
    log(message, answer)

    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=[Constaints.Tomorrow[0]])
def handleText(message):
    group = message.text.split(Constaints.Tomorrow[1])[1][1:]
    answer = RaspParse.GetTomorrowRasp(group)
    log(message, answer)

    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=[Constaints.Parity])
def handleText(message):
    answer = RaspParse.GetParity()
    log(message, answer)

    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=[Constaints.Teacher[0]])
def handleText(message):
    tch = message.text.split(Constaints.Teacher[1])[1][1:]
    answer = RaspParse.GetTeacherID(tch)
    log(message, answer)

    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['start'])
def handle_start(message):
    answer = Constaints.StartAnswer
    log(message, answer)

    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['help'])
def handleText(message):
    answer = Constaints.HelpAnswer
    log(message, answer)

    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, answer)


@bot.message_handler(content_types=['text'])
def handleText(message):
    url = 'https://pp.vk.me/c631925/v631925802/2492/l7IqI7KdW6g.jpg'
    urllib2.urlretrieve(url, 'sorryCat.jpg')
    img = open('sorryCat.jpg', 'rb')

    random.seed()
    rndFact = Constaints.Facts[random.randint(0, len(Constaints.Facts) - 1)]

    bot.send_chat_action(message.from_user.id, 'upload_photo')
    bot.send_photo(message.from_user.id, img, rndFact)
    img.close()

    log(message, rndFact)


bot.polling(none_stop=True, interval=0)
