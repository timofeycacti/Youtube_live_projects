import telebot
import random
import time
import threading

TOKEN = '7732213939:AAHenmeUBxyOwWVHmWD-H1HVH07gld74DR4'
file = open('./botusers.txt', 'r+')
file.write("")
cards = open('./cards.txt', 'r+')
cards.write("")

bot = telebot.TeleBot(TOKEN)
# texts = [["first", 1000, 0]]
texts=[]
users = {}
cooldown = 1800

@bot.message_handler(func=lambda message: "/versus" in message.text.lower())
def versus(message):
    global users
    userid = str(message.from_user.id)
    if userid not in users:
        users[userid] = [0, [], 0]
    userstats = users[userid]
    if userstats[2] <= 0:
        reward = random.choice(texts)
        if reward[2] not in userstats[1]:
            userstats[1].append(reward[2])
        userstats[0] += reward[1]
        userstats[2] = cooldown
        bot.send_photo(message.chat.id, open(f"./pictures/{reward[2]}","rb"), f"Вы нашли карточку! \n{reward[0]}\nи получили {reward[1]} очков!")
    else:
        bot.reply_to(message, f"А вот и нет, вонючий спамер! Жди еще {userstats[2]} секунд!")

@bot.message_handler(func=lambda message: "/profile" in message.text.lower())
def sigmabosinnchik(message):
    userid = str(message.from_user.id)
    name = message.from_user.first_name
    try:
        userstats = users[userid]
        bot.reply_to(message, f"Вы пользователь {name}\n у вас {len(userstats[1])}/{len(texts)} карточек!\n {userstats[0]} очков!")
    except:
        bot.reply_to(message, "похоже вас нет в базе :(")

@bot.message_handler(func=lambda message: "/reload" in message.text.lower())
def reload(message):
    global users
    cards = open('./cards.txt', 'w+')
    file = open('./botusers.txt', 'r')
    cusers = file.read().splitlines()
    file.close()

    for i in cusers:
        cuser = i.split(" ")
        if len(cuser) >= 2 and cuser[0] not in users:
            users[cuser[0]] = [int(cuser[1]), cuser[2].split(","), 0]

    file = open('./botusers.txt', 'w')
    for i in users:
        card_list = [str(card) for card in users[i][1]]
        file.write(f'{i} {users[i][0]} {",".join(card_list)}\n')

    cardsgot = cards.read().splitlines()
    for i in cardsgot:
        a = i.split(" ")
        if not i in texts:
            texts.append([a[0], a[1], len(texts)])

    curstring = ""
    for i in texts:
        curstring += f"{i[0]} {i[1]} {i[2]}\n"

    cards.write(curstring)
    cards.close()
    file.close()
    if hasattr(message,"id"):
        bot.reply_to(message, "Я обновил базу данных!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if "/++" in message.caption:
        if message.from_user.username in ["Dan_molnia", "cvetocheckcactus"]:
            try:
                cphoto=bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)
                with open(f"./pictures/{len(texts)}","wb") as new_file:
                    new_file.write(cphoto)
                text = message.caption.split(" ")
                texts.append([" ".join(text[1:-1]), int(text[-1]), len(texts)]) #тут может быть ошибка
                bot.reply_to(message, f"успешно добавлено! айди: {len(texts)}")

            except:
                bot.reply_to(message, "неправильный формат")
        else:
            print(message.from_user.username)
            bot.reply_to(message, "Добавление только через @dan_molnia или @cvetocheсkcactus !")


def loop():
    global users
    reload("ddd")
    while True:
        for i in list(users.keys()):
            if users[i][2] > 0:
                users[i][2] -= 1
        time.sleep(1)

infinite_loop_thread = threading.Thread(target=loop)
infinite_loop_thread.daemon = True
infinite_loop_thread.start()

print("bot запущен")
bot.polling()
