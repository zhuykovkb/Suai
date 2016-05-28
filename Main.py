import telebot
import Constaints
import RaspParse

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


@bot.message_handler(commands=['wk'])
def handleText(message):
    group = message.text.split('/wk')[1][1:]
    answer = RaspParse.GetWeekRasp(group)
    log(message, answer)

    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['td'])
def handleText(message):
    group = message.text.split('/td')[1][1:]
    answer = RaspParse.GetTodayRasp(group)
    log(message, answer)

    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['tm'])
def handleText(message):
    group = message.text.split('/tm')[1][1:]
    answer = RaspParse.GetTomorrowRasp(group)
    log(message, answer)

    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['parity'])
def handleText(message):
    answer = RaspParse.GetPairty()
    log(message, answer)

    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['tch'])
def handleText(message):
    tch = message.text.split('/tch')[1][1:]
    answer = RaspParse.GetTeacherID(tch)
    log(message, answer)

    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['start'])
def handleText(message):
    answer = "Комманд здесь по сути нет, достаточно ввести номер своей группы. Если есть буквы, просто пишем слитно. На регистр похуй"
    log(message, answer)

    bot.send_message(message.from_user.id, answer)


@bot.message_handler(commands=['help'])
def handleText(message):
    answer = "Помощи хочешь? - Нахуй иди!"
    log(message, answer)

    bot.send_message(message.from_user.id, answer)


@bot.message_handler(content_types=["commands"])
def handleCommand(message):
    print("Пришла комманда")


@bot.message_handler(content_types=["text"])
def handleText(message):
    answer = 'no'
    bot.send_message(message.from_user.id, answer)
    log(message, answer)


@bot.message_handler(content_types=["document"])
def handleDoc(message):
    print("Пришел документ")


@bot.message_handler(content_types=["audio"])
def handleAudio(message):
    print("Пришло аудио")


@bot.message_handler(content_types=["photo"])
def handlePhoto(message):
    print("Пришло фото")


@bot.message_handler(content_types=["sticker"])
def handleSticker(message):
    print("Пришел стикер")


bot.polling(none_stop=True, interval=0)
