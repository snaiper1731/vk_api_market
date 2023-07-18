import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
import random
import sqlite3
import schedule
import threading
import logging
from tokken import main_token

session = vk_api.VkApi(token=main_token)

session_api = session.get_api()
PEER_ID = 194363260
db = sqlite3.connect('action.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
   userID BIGINT,
   act TEXT,
   dis TEXT,
   battletag TEXT,
   points INT,
   questACT TEXT,
   questPop INT,
   quest50pop INT,
   vkDonut INT
   )""")
db.commit()
userAct = '0'

photo = ["BLAZAR.png", "brakhma.png", "Stormrage.png", "drakonik.png", "Emperor.png", "Flick_l.png", "Helios.png",
         "magaz.png", "SANI.png", "Storm.png", "Stormelite.png", "Suzaku.png", "TOCCATA.png", "roz.jpg"]
suck = 'C:/Users/Roman/PycharmProjects/Vk/'
upload = VkUpload(session)

quests_20 = {"vopros20": "otvet20",
}

quests_50 = {"vopros50": "otvet50",
}

quests_100 = "vopros100": "otvet100",
}

quests_500 = {"vopros500": "otvet500",
}


def send_massage(user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0,

    }
    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    session.method("messages.send", post)


def message_post(user_id):
    session_api.messages.send(user_id=user_id, attachment='wall-215328370_3%2Fall', random_id=0)


def fix_message(msg):
    msg = "'" + msg + "'"
    return msg


def random_question(point: str) -> list[str]:
    # Получаем переменные с вопросами
    if point == "20 points":
        quest_choose20 = random.choice(list(quests_20.keys()))
        true_answer_20 = quests_20[quest_choose20]
        return quest_choose20, true_answer_20

    elif point == "50 points":
        quest_choose50 = random.choice(list(quests_50.keys()))
        true_answer_50 = quests_50[quest_choose50]

        return quest_choose50, true_answer_50

    elif point == "100 points":
        quest_choose100 = random.choice(list(quests_100.keys()))
        true_answer_100 = quests_100[quest_choose100]
        return quest_choose100, true_answer_100

    elif point == "500 points":
        quest_choose500 = random.choice(list(quests_500.keys()))
        true_answer_500 = quests_500[quest_choose500]
        return quest_choose500, true_answer_500


def upload_photo(user_id, message, photo):
    image_path = f"C:/Users/Roman/PycharmProjects/Vk/{photo}"
    attachments = []
    upload_image = upload.photo_messages(photos=image_path)[0]
    attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image["id"]))
    session.method('messages.send', {'user_id': user_id,
                                     'random_id': 0,
                                     'message': message,
                                     'attachment': ','.join(attachments)
                                     })


def shed(event):
    def bd_update():
        sql.execute("UPDATE users SET questPop = '2'")
        sql.execute("UPDATE users SET quest50pop = '3'")

    schedule.every(1).hour.do(bd_update)

    while not event.isSet():
        event.wait(3600)
        d1 = datetime.datetime.now()
        Hour = d1.strftime('%H')
        Day_week = d1.strftime('%a')
        if Hour == "00" and Day_week == 'Mon':
            schedule.run_pending()
        else:
            pass


def main():
    while True:
        try:
            for event in VkLongPoll(session).listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    msg = event.text.lower()
                    user_id = event.user_id
                    keyboard = VkKeyboard()
                    sql.execute(f"SELECT userID FROM users WHERE userID = '{user_id}'")
                    if sql.fetchone() is None:
                        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                    (user_id, "noTAG", "0", "0", "0", "0", "2", "3", "0"))
                        db.commit()
                        keyboard.add_button("Rocket League", VkKeyboardColor.NEGATIVE)
                        keyboard.add_button("Hearthstone", VkKeyboardColor.POSITIVE)
                        send_massage(user_id, "Выберите вашу дисциплину", keyboard)



                    else:
                        userAct = sql.execute(F"SELECT act FROM users WHERE userID = '{user_id}'").fetchone()[0]
                        userId = sql.execute(F"SELECT userID FROM users").fetchall()
                        userDIS = sql.execute(F"SELECT dis FROM users WHERE userID = '{user_id}'").fetchone()[0]
                        userPOINTs = sql.execute(F"SELECT points FROM users WHERE userID = '{user_id}'").fetchone()[0]
                        userTAG = sql.execute(F"SELECT battletag FROM users WHERE userID = '{user_id}'").fetchone()[0]
                        questACT = sql.execute(F"SELECT questACT FROM users WHERE userID = '{user_id}'").fetchone()[0]
                        userDON = sql.execute(F"SELECT vkDonut FROM users WHERE userID = '{user_id}'").fetchone()[0]
                        questPOP = sql.execute(F"SELECT questPop FROM users WHERE userID = '{user_id}'").fetchone()[0]
                        questPOP50 = sql.execute(F"SELECT quest50pop FROM users WHERE userID = '{user_id}'").fetchone()[
                            0]

                        if questPOP != 0 and userDON == 0:
                            sql.execute(f"UPDATE users SET questPop = '1' WHERE userID = {user_id}")
                            db.commit()

                        elif questPOP != 0 and userDON != 0:
                            pass

                        if userAct == "noTAG" and msg == "rocket league":
                            sql.execute(f"UPDATE users SET dis = 'Rocket League' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id,
                                         "Пока что этот проект находится в планах, попробуйте выбрать другой!",
                                         keyboard)

                        elif userAct == "newUSER" and msg == "rocket league":
                            sql.execute(f"UPDATE users SET dis = 'Rocket League' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id,
                                         "Пока что этот проект находится в планах, попробуйте выбрать другой!",
                                         keyboard)



                        elif userDIS == "Rocket League" and msg == "назад":
                            sql.execute(f"UPDATE users SET dis = '0' WHERE userID= {user_id}")
                            db.commit()
                            keyboard.add_button("Rocket League", VkKeyboardColor.NEGATIVE)
                            keyboard.add_button("Hearthstone", VkKeyboardColor.POSITIVE)
                            send_massage(user_id, 'choose dis', keyboard)

                        elif userDIS == "Rocket League" and userAct == "newUSER" and msg == "назад":

                            keyboard.add_line()
                            keyboard.add_button("Изменить BattleTag", VkKeyboardColor.SECONDARY)

                        elif userAct == "noTAG" and msg == "hearthstone":
                            sql.execute(f"UPDATE users SET act = 'goTAG' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id, "Введите свой BattleTAG", )

                        elif userAct == "goTAG":
                            sql.execute(f"UPDATE users SET battletag = {fix_message(msg)} WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET act = 'newUSER' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Rocket League", VkKeyboardColor.NEGATIVE)
                            keyboard.add_button("Hearthstone", VkKeyboardColor.POSITIVE)
                            send_massage(user_id,
                                         "Вы в списке участников!\n Пожалуйста, снова выберете вашу дисциплину.",
                                         keyboard)




                        elif userAct == "newUSER" and msg == "hearthstone":
                            sql.execute(f"UPDATE users SET dis = 'Hearthstone' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET act = 'setCHANGE' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Магазин", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Розыгрыш", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Участвовать", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Дополнительные очки", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Количество points", VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                            keyboard.add_openlink_button("VK Donut",
                                                         "https://vk.com/@triadatournaments-podpiska-vk-donut")
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите интересующий вас раздел", keyboard)

                        elif userAct == "setCHANGE" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'newUSER' WHERE userID= {user_id}")
                            sql.execute(f"UPDATE users SET dis = '0' WHERE userID= {user_id}")
                            db.commit()
                            keyboard.add_button("Rocket League", VkKeyboardColor.NEGATIVE)
                            keyboard.add_button("Hearthstone", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Изменить BattleTag", VkKeyboardColor.SECONDARY)
                            send_massage(user_id, 'Выберете вашу дисциплину', keyboard)

                        elif userAct == "newUSER" and msg == "изменить battletag":
                            sql.execute(f"UPDATE users SET act = 'editTAG' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id, "Напишите свой BattleTag")

                        elif userAct == "editTAG":
                            sql.execute(f"UPDATE users SET battletag = {fix_message(msg)} WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET act = 'newUSER' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Rocket League", VkKeyboardColor.NEGATIVE)
                            keyboard.add_button("Hearthstone", VkKeyboardColor.POSITIVE)
                            send_massage(user_id, "Ваш BattleTag успешно изменён")




                        elif userAct == "setCHANGE" and msg == "розыгрыш":
                            upload_photo(user_id, "ИСПЫТАЙ СВОЮ УДАЧУ В МЕГА КОНКУРСЕ!\n"
                                                  "\n🎁Призы:\n"
                                                  "1 место - 1 Девайс из 'магазина лиги' на выбор.\n"
                                                  "2 место - Пропуск 'Завсегдатая'\n"
                                                  "3 место - Пропуск 'Завсегдатая'\n"
                                                  "4 место - Набор скинов для Полей Сражений"
                                                  "\n5 место - Мини-набор любого дополнения на выбор"
                                                  "\n6 место - Стартовый пакет новичка"
                                                  "\n7 место - 7 паков"
                                                  "\n8 место - Бонусы для полей сражений"
                                                  "\n9 место - Добивание для полей сражений"
                                                  "\n\n📝 Условия:"
                                                  "\n— Поставить лайк на данный пост:"
                                                  "\nvk.cc/cfNiGm"
                                                  "\nvk.cc/cfNiGm"
                                                  "\nvk.cc/cfNiGm"
                                                  "\n— Написать в комментариях под постом свой 'BattleTag'"
                                                  "\n\nК участию допускаются все игроки получившие не меньше"
                                                  "\n500 TRP"
                                                  "\nВ ТУРНИРАХ СЕРИИ🔥TRIADA X REDRAGON LEAGUE #3."
                                                  "\n\n📆Итоги подведем в прямом эфире 11.12.2022г"
                                                  "\n\nЖелаем удачи!", "roz.jpg")

                        elif userAct == "setCHANGE" and msg == "количество points":
                            send_massage(user_id, f"Ваше количество TRP={userPOINTs}")


                        elif userAct == "Read" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'setCHANGE' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Магазин", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Розыгрыш", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Учавствовать", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Количество points", VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                            keyboard.add_openlink_button("VK Donut",
                                                         "https://vk.com/@triadatournaments-podpiska-vk-donut")
                            keyboard.add_line()
                            keyboard.add_openlink_button("VK Donut",
                                                         "https://vk.com/@triadatournaments-podpiska-vk-donut")
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите интересующий вас раздел", keyboard)



                        elif userAct == "setCHANGE" and msg == "магазин":
                            sql.execute(f"UPDATE users SET act = 'BUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровые мыши", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые клавиатуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Игровые гарнитуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые ковры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Стрим-микрофоны", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Акустические системы", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Бонусы", VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Назад', VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, 'Здесь вы можете потратить ваши TRP!', keyboard)

                        elif userAct == "BUY" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'setCHANGE' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Магазин", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Розыгрыш", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Участвовать", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Дополнительные очки", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Количество points", VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                            keyboard.add_openlink_button("VK Donut",
                                                         "https://vk.com/@triadatournaments-podpiska-vk-donut")
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите интересующий вас раздел", keyboard)

                        elif userAct == "BUY" and msg == "игровые мыши":
                            sql.execute(f"UPDATE users SET act = 'Mouse' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Мышь Stormrage", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Мышь Emperor", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Мышь Storm Elite", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "Mouse" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровые мыши", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые клавиатуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Игровые гарнитуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые ковры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Стрим-микрофоны", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Акустические системы", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Бонусы", VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Назад', VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, 'Здесь вы можете потратить ваши TRP', keyboard)

                        elif userAct == "BUY" and msg == "игровые клавиатуры":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARD' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Клавиатура Draconic", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Клавиатура Sani", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Клавиатура Brahma", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выбирай", keyboard)

                        elif userAct == "KEYBOARD" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровые мыши", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые клавиатуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Игровые гарнитуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые ковры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Стрим-микрофоны", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Акустические системы", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Бонусы", VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Назад', VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, 'Здесь вы можете потратить ваши TRP', keyboard)

                        elif userAct == "BUY" and msg == "игровые гарнитуры":
                            sql.execute(f"UPDATE users SET act = 'GAR' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровая гарнитура Redragon Helios", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "GAR" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровые мыши", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые клавиатуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Игровые гарнитуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые ковры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Стрим-микрофоны", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Акустические системы", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Бонусы", VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Назад', VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, 'Здесь вы можете потратить ваши TRP', keyboard)

                        elif userAct == "BUY" and msg == "игровые ковры":
                            sql.execute(f"UPDATE users SET act = 'COVRI' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Коврик Suzaku", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Коврик Flick L", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "COVRI" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровые мыши", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые клавиатуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Игровые гарнитуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые ковры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Стрим-микрофоны", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Акустические системы", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Бонусы", VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Назад', VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, 'Здесь вы можете потратить ваши TRP', keyboard)

                        elif userAct == "Mouse" and msg == "мышь stormrage":
                            sql.execute(f"UPDATE users SET act = 'BUYMOUSESTORM' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купить/1500 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            upload_photo(user_id,
                                         "IR-лазерный сенсор, возможность настройки dpi в диапазоне от 100 до 10000, регулируемая скорость опроса и программная управляемая RGB подсветка корпуса - вот отличительные особенности модели. Большой ресурс нажатия кнопок и разумная цена - идеальный выбор для продуманного геймера.",
                                         "Stormrage.png")
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "BUYMOUSESTORM" and msg == "купить/1500 points" and userPOINTs >= 1500:
                            a = userPOINTs
                            a -= 1500
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл мышь stormrage")

                        elif userAct == "BUYMOUSESTORM" and msg == "купить/1500 points" and userPOINTs < 1500:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")










                        elif userAct == "BUYMOUSESTORM" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'Mouse' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Мышь Stormrage", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Мышь Emperor", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Мышь Storm Elite", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "Mouse" and msg == "мышь emperor":
                            sql.execute(f"UPDATE users SET act = 'BUYMOUSEMPEROR' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купить/1500 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            upload_photo(user_id,
                                         "IR-лазерный сенсор, возможность настройки dpi в диапазоне от 100 до 10000, регулируемая скорость опроса и программная управляемая RGB подсветка корпуса - вот отличительные особенности модели. Большой ресурс нажатия кнопок и разумная цена - идеальный выбор для продуманного геймера",
                                         "Emperor.png")
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "BUYMOUSEMPEROR" and msg == "купить/1500 points" and userPOINTs >= 1500:
                            a = userPOINTs
                            a -= 1500
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл мышь emperor")

                        elif userAct == "BUYMOUSEMPEROR" and msg == "купить/1500 points" and userPOINTs < 1500:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")





                        elif userAct == "BUYMOUSEMPEROR" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'Mouse' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Мышь Stormrage", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Мышь Emperor", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Мышь Storm Elite", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "Mouse" and msg == "мышь storm elite":
                            sql.execute(f"UPDATE users SET act = 'BUYMOUSESTORMELITE' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купить/1900 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            upload_photo(user_id,
                                         "Высококлассный оптический сенсор Pixart 3327, качественные переключатели Huano с ресурсом в 20 млн нажатий, невероятно гибкий и прочный кабель. Лёгкий вес, красивая подсветка и прекрасное соотношение «цена/качество» делают эту модель прекрасным выбором!",
                                         "Stormelite.png")
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "BUYMOUSESTORMELITE" and msg == "купить/1900 points" and userPOINTs >= 1900:
                            a = userPOINTs
                            a -= 1900
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл мышь storm Elite")

                        elif userAct == "BUYMOUSESTORMELITE" and msg == "купить/1900 points" and userPOINTs < 1900:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")

                        elif userAct == "KEYBOARDDRACONICBUY" and msg == "купить/1900 Points" and userPOINTs < 1900:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")

                        elif userAct == "BUYMOUSESTORMELITE" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'Mouse' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Мышь Stormrage", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Мышь Emperor", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Мышь Storm Elite", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "KEYBOARD" and msg == "клавиатура draconic":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARDDRACONIC' WHERE userID = {user_id}")
                            db.commit()
                            image = suck + photo[3]
                            image2 = suck + photo[7]
                            attachments = []
                            upload_image = upload.photo_messages(photos=image)[0]
                            upload_image2 = upload.photo_messages(photos=image2)[0]
                            attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image["id"]))
                            attachments.append('photo{}_{}'.format(upload_image2['owner_id'], upload_image2["id"]))
                            keyboard.add_button("Купить", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            session.method("messages.send", {"user_id": user_id,
                                                             "message": "Компактная игровая клавиатура с коричневыми механическими переключателями повышенной износостойкости, программируемой RGB-подсветкой и дополнительными игровыми функциями! Беспроводная конструкция и укороченный корпус для экономии места на вашем столe.",
                                                             "random_id": 0, 'attachment': ','.join(attachments)})
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)


                        elif userAct == "KEYBOARDDRACONIC" and msg == "купить":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARDDRACONICBUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Чёрная/3500 Points", VkKeyboardColor.SECONDARY)
                            keyboard.add_button("Белая/4000 Points", VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.POSITIVE)
                            send_massage(user_id, "Выберите цвет", keyboard)

                        elif userAct == "KEYBOARDDRACONICBUY" and msg == "белая/4000 points" and userPOINTs >= 4000:
                            a = userPOINTs
                            a -= 4000
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл клавиатура Draconic белая")

                        elif userAct == "KEYBOARDDRACONICBUY" and msg == "белая/4000 points" and userPOINTs < 4000:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")

                        elif userAct == "KEYBOARDDRACONICBUY" and msg == "чёрная/3500 points" and userPOINTs >= 3500:
                            a = userPOINTs
                            a -= 3500
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл клавиатура Draconic чёрная")

                        elif userAct == "KEYBOARDDRACONICBUY" and msg == "чёрная/3500 points" and userPOINTs < 3500:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")

                        elif userAct == "KEYBOARDDRACONICBUY" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARDDRACONIC' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купить", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Можете передумать или вернуться в прошлый раздел", keyboard)


                        elif userAct == "KEYBOARDDRACONIC" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARD' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Клавиатура Draconic", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Клавиатура Sani", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Клавиатура Brahma", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "KEYBOARD" and msg == "клавиатура sani":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARDsani' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купить/3000 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            upload_photo(user_id,
                                         "Лучшая клавиатура для долгих игр или работы. Прочный кабель, привлекательный дизайн, настраиваемая RGB подсветка и влагоустойчивая конструкция корпуса. Девайс распознает одновременное нажатие 104 клавиш и оснащен топовыми механическими переключателями OUTEMU Blue.",
                                         "SANI.png")
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "KEYBOARDsani" and msg == "купить/3000 points" and userPOINTs >= 3000:
                            a = userPOINTs
                            a -= 3000
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл клавиатура Sani")

                        elif userAct == "KEYBOARDsani" and msg == "купить/3000 points" and userPOINTs < 3000:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")

                        elif userAct == "KEYBOARD" and msg == "клавиатура brahma":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARDbrahma' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купить/4500 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            upload_photo(user_id,
                                         "Влагоустойчивая конструкция и повышенная износостойкость сделают эту модель вашим лучшим игровым партнером на долгие годы! Качественные переключатели, удобная подставка для рук, регулятор громкости на корпусе клавиатуры, прочный провод и великолепные возможности для геймера.",
                                         "brakhma.png")
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "KEYBOARDbrahma" and msg == "купить/4500 points" and userPOINTs >= 4500:
                            a = userPOINTs
                            a -= 4500
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл клавиатура Brahma")

                        elif userAct == "KEYBOARDbrahma" and msg == "купить/4500 points" and userPOINTs < 4500:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")

                        elif userAct == "KEYBOARDsani" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARD' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Клавиатура Draconic", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Клавиатура Sani", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Клавиатура Brahma", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "KEYBOARDbrahma" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'KEYBOARD' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Клавиатура Draconic", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Клавиатура Sani", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Клавиатура Brahma", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "COVRI" and msg == "коврик suzaku":
                            sql.execute(f"UPDATE users SET act = 'COVRIsuzaku' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("купить/900 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("назад", VkKeyboardColor.NEGATIVE)
                            upload_photo(user_id,
                                         "Большой размер ковра - 80х30 сантиметров - позволит застелить весь стол! В основании - вспененная натуральная резина высокой плотности. Гладкий и прочный шёлк покрытия легко очищается от загрязнений и не деформируется даже при попадании на него жидкости.",
                                         "Suzaku.png")
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "COVRIsuzaku" and msg == "купить/900 points" and userPOINTs >= 900:
                            a = userPOINTs
                            a -= 900
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл коврик suzaku")

                        elif userAct == "COVRIsuzaku" and msg == "купить/900 points" and userPOINTs < 900:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")

                        elif userAct == "COVRIsuzaku" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'COVRI' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Коврик Suzaku", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Коврик Flick L", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "COVRI" and msg == "коврик flick l":
                            sql.execute(f"UPDATE users SET act = 'COVRIflick' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("купить/700 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("назад", VkKeyboardColor.NEGATIVE)
                            upload_photo(user_id,
                                         "Игровой ковер среднего размера с прошитыми краями и гладким влагоотталкивающим покрытием Speed для максимальной скорости перемещения мыши. Оптимальная толщина в 4мм сглаживает все возможные неровности.",
                                         "Helios.png")
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "COVRIflick" and msg == "купить/700 points" and userPOINTs >= 700:
                            a = userPOINTs
                            a -= 700
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл коврик Flick L")

                        elif userAct == "COVRIflick" and msg == "купить/700 points" and userPOINTs < 700:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")


                        elif userAct == "COVRIflick" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'COVRI' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Коврик Suzaku", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Коврик Flick L", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "GAR" and msg == "игровая гарнитура redragon helios":
                            sql.execute(f"UPDATE users SET act = 'GARhel' WHERE userID = {user_id}")
                            db.commit()
                            upload_photo(user_id,
                                         "Профессиональная игровая гарнитура с виртуальным объемным звуком 7.1, эквалайзером, высококачественными 50-мм динамиками с неодимовыми магнитами и комфортными охватывающими амбушюрами из протеиновой пены.",
                                         "Helios.png")
                            keyboard.add_button("купить/5000 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "GARhel" and msg == "купить/5000 points" and userPOINTs >= 5000:
                            a = userPOINTs
                            a -= 5000
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл игровая гарнитура redragon helios")

                        elif userAct == "GARhel" and msg == "купить/5000 points" and userPOINTs < 5000:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")


                        elif userAct == "GARhel" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'GAR' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровая гарнитура Redragon Helios", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "BUY" and msg == "стрим-микрофоны":
                            sql.execute(f"UPDATE users SET act = 'STRIM' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Стрим микрофон Redragon Blazar", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "STRIM" and msg == "стрим микрофон redragon blazar":
                            sql.execute(f"UPDATE users SET act = 'STRIMblazar' WHERE userID = {user_id}")
                            db.commit()
                            upload_photo(user_id,
                                         "Высококачественный микрофон с подсветкой в металлическом корпусе. Оптимален для стриминга и подкастов, также подходит для онлайн игр, озвучания, записи вокала и акустической музыки.",
                                         "BLAZAR.png")
                            keyboard.add_button("купить/6500 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "STRIMblazar" and msg == "купить/6500 points" and userPOINTs >= 6500:
                            a = userPOINTs
                            a -= 6500
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл стрим микрофон redragon blazar")

                        elif userAct == "STRIMblazar" and msg == "купить/6500 points" and userPOINTs < 6500:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")


                        elif userAct == "STRIMblazar" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'STRIM' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Стрим микрофон Redragon Blazar", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "STRIM" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровые мыши", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые клавиатуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Игровые гарнитуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые ковры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Стрим-микрофоны", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Акустические системы", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Бонусы", VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Назад', VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, 'Здесь вы можете потратить ваши TRP', keyboard)

                        elif userAct == "BUY" and msg == "акустические системы":
                            sql.execute(f"UPDATE users SET act = 'ACUSTIC' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Акустическая система Redragon Toccata", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "ACUSTIC" and msg == "акустическая система redragon toccata":
                            sql.execute(f"UPDATE users SET act = 'ACUSTICtoc' WHERE userID = {user_id}")
                            db.commit()
                            upload_photo(user_id,
                                         "Мощная акустическая система со встроенными пассивными излучателями. Глубокий бас, красивая подсветка, стильный дизайн - акустика идеально вписывается в современный интерьер. Питание от USB, удобный регулятор громкости звука.",
                                         "TOCCATA.png")
                            keyboard.add_button("купить/7000 Points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id,
                                         "Более подробную информацию о девайсе смотрите на официальном сайте:"
                                         "\nvk.cc/6ylBkk"
                                         "\nvk.cc/6ylBkk", keyboard)

                        elif userAct == "ACUSTICtoc" and msg == "купить/7000 points" and userPOINTs >= 7000:
                            a = userPOINTs
                            a -= 7000
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id,
                                         "Спасибо за покупку, ваш запрос был отправлен на обработку администратору.")
                            send_massage(user_id=160788373,
                                         message=f"user_ID={user_id}\nbattletag= {userTAG}\nприборёл акустическая система redragon toccata")

                        elif userAct == "ACUSTICtoc" and msg == "купить/7000 points" and userPOINTs < 7000:
                            send_massage(user_id, "У вас недостаточно TRP что бы приобрести данный товар")

                        elif userAct == "ACUSTICtoc" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'ACUSTIC' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Акустическая система Redragon Toccata", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "ACUSTIC" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровые мыши", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые клавиатуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Игровые гарнитуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые ковры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Стрим-микрофоны", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Акустические системы", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Бонусы", VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Назад', VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, 'Здесь вы можете потратить ваши TRP', keyboard)

                        elif userAct == "BUY" and msg == "бонусы":
                            sql.execute(f"UPDATE users SET act = 'BONUS' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купоны и промокоды со скидками до 80%", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Брелки Hearthstone", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "BONUS" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BUY' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Игровые мыши", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые клавиатуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Игровые гарнитуры", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Игровые ковры", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Стрим-микрофоны", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Акустические системы", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Бонусы", VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Назад', VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, 'Здесь вы можете потратить ваши TRP', keyboard)

                        elif userAct == "BONUS" and msg == "купоны и промокоды со скидками до 80%":
                            sql.execute(f"UPDATE users SET act = 'BONUSPROM' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("купить", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id,
                                         "Купоны и промокоды со скидками до 80%. На такие крупные бренды как:"
                                         "\n1)Grow Food — уникальный сервис по доставке готового сбалансированного питания на неделю. Лидер рынка с самыми доступными ценами."
                                         "\n2)IVI — крупнейший в России онлайн-кинотеатр, работающий на рынке профессионального видеоконтента."
                                         "\n3)BESTWATCH — интернет-магазин наручных часов, доставивший свой первый заказ в 1999 году и пользуется заслуженным уважением по всей России."
                                         "\n4)Domino`s Pizza — сеть №1 по доставке пиццы во всем мире! Более 160 ресторанов в России.",
                                         keyboard)


                        elif userAct == "BONUSPROM" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BONUS' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купоны и промокоды со скидками до 80%", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Брелки Hearthstone", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "BONUS" and msg == "брелки hearthstone":
                            sql.execute(f"UPDATE users SET act = 'BONUSbrel' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("купить", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Брелки Hearthstone 4-х видов", keyboard)

                        elif userAct == "BONUSbrel" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'BONUS' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Купоны и промокоды со скидками до 80%", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Брелки Hearthstone", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите товар который вас интересует", keyboard)

                        elif userAct == "setCHANGE" and msg == "дополнительные очки":
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("20 points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("50 points", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("100 points", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("500 points", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите категорию", keyboard)

                        elif userAct == "inGAME" and msg == "20 points" and questPOP != 0:
                            dick = random_question("20 points")
                            sql.execute(f"UPDATE users SET act = 'inGAME20' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '{dick[1].lower()}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id, "пишите всё русскими буквами и цифрами")
                            send_massage(user_id, f"{dick[0]}")

                        elif userAct == "inGAME20" and questACT != 0 and msg == questACT and questPOP != 0:
                            send_massage(user_id, "молодец")
                            a = userPOINTs
                            b = questPOP
                            b -= 1
                            a += 20
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '0' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questPop = '{b}' WHERE userID = {user_id}")
                            db.commit()

                        elif userAct == "inGAME" and msg == "20 points" and questPOP == 0:

                            send_massage(user_id,
                                         "Вы уже потратили своё количество попыток на этой неделе. Попробуйте похже или оформите подписку VK Donuts")


                        elif userAct == "inGAME" and msg == "50 points" and questPOP == 0:

                            send_massage(user_id,
                                         "Вы уже потратили своё количество попыток на этой неделе. Попробуйте похже или оформите подписку VK Donuts")

                        elif userAct == "inGAME" and msg == "100 points" and questPOP == 0:

                            send_massage(user_id,
                                         "Вы уже потратили своё количество попыток на этой неделе. Попробуйте похже или оформите подписку VK Donuts")

                        elif userAct == "inGAME" and msg == "500 points" and questPOP == 0:

                            send_massage(user_id,
                                         "Вы уже потратили своё количество попыток на этой неделе. Попробуйте похже или оформите подписку VK Donuts")



                        elif userAct == "inGAME20" and questACT != 0 and msg != questACT:
                            send_massage(user_id, "ne молодец")
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '0' WHERE userID = {user_id}")
                            db.commit()


                        elif userAct == "inGAME" and msg == "50 points" and questPOP != 0 and questPOP50 != 0:
                            dick = random_question("50 points")
                            sql.execute(f"UPDATE users SET act = 'inGAME50' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '{dick[1].lower()}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id, "пишите всё русскими буквами и цифрами")
                            send_massage(user_id, f"{dick[0]}")

                        elif userAct == "inGAME50" and questACT != 0 and msg == questACT:
                            send_massage(user_id, "молодец")
                            a = userPOINTs
                            a += 50
                            b = questPOP
                            b -= 1
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '0' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questPop = '{b}' WHERE userID = {user_id}")
                            db.commit()

                        elif userAct == "inGAME50" and questACT != 0 and msg != questACT:
                            a = questPOP50
                            a -= 1
                            send_massage(user_id, "ne молодец")
                            sql.execute(f"UPDATE users SET quest50pop = '{a}' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '0' WHERE userID = {user_id}")
                            db.commit()

                        elif questPOP50 == 0 and questPOP != 0:
                            a = questPOP
                            a -= 1
                            sql.execute(f"UPDATE users SET questPop = '{a}' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET quest50pop = '3' WHERE userID = {user_id}")
                            db.commit()

                        elif userAct == "inGAME" and msg == "100 points" and questPOP != 0:
                            dick = random_question("100 points")
                            sql.execute(f"UPDATE users SET act = 'inGAME100' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '{dick[1].lower()}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id, "пишите всё русскими буквами и цифрами")
                            send_massage(user_id, f"{dick[0]}")

                        elif userAct == "inGAME100" and questACT != 0 and msg == questACT:
                            send_massage(user_id, "молодец")
                            a = userPOINTs
                            a += 100
                            b = questPOP
                            b -= 1
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '0' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questPop = '{b}' WHERE userID = {user_id}")
                            db.commit()

                        elif userAct == "inGAME100" and questACT != 0 and msg != questACT:
                            send_massage(user_id, "ne молодец")
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '0' WHERE userID = {user_id}")
                            db.commit()

                        elif userAct == "inGAME" and msg == "500 points" and questPOP != 0:
                            dick = random_question("500 points")
                            sql.execute(f"UPDATE users SET act = 'inGAME500' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '{dick[1].lower()}' WHERE userID = {user_id}")
                            db.commit()
                            send_massage(user_id, "пишите всё русскими буквами и цифрами")
                            send_massage(user_id, f"{dick[0]}")

                        elif userAct == "inGAME500" and questACT != 0 and msg == questACT:
                            send_massage(user_id, "молодец")
                            a = userPOINTs
                            a += 500
                            b = questPOP
                            b -= 1
                            sql.execute(f"UPDATE users SET points = '{a}' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '0' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questPop = '{b}' WHERE userID = {user_id}")
                            db.commit()

                        elif userAct == "inGAME500" and questACT != 0 and msg != questACT:
                            b = questPOP
                            b -= 1
                            send_massage(user_id, "ne молодец")
                            sql.execute(f"UPDATE users SET act = 'inGAME' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questACT = '0' WHERE userID = {user_id}")
                            sql.execute(f"UPDATE users SET questPop = '{b}' WHERE userID = {user_id}")
                            db.commit()

                        elif userAct == "inGAME" and msg == "назад":
                            sql.execute(f"UPDATE users SET act = 'setCHANGE' WHERE userID = {user_id}")
                            db.commit()
                            keyboard.add_button("Магазин", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Розыгрыш", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Участвовать", VkKeyboardColor.POSITIVE)
                            keyboard.add_button("Дополнительные очки", VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button("Количество points", VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                            keyboard.add_openlink_button("VK Donut",
                                                         "https://vk.com/@triadatournaments-podpiska-vk-donut")
                            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
                            send_massage(user_id, "Выберите интересующий вас раздел", keyboard)


                        elif userAct == "setCHANGE" and msg == "участвовать":
                            message_post(user_id)

        except:
            logging.basicConfig(
                level=logging.DEBUG,
                filename="Errorlog.log",
                format="%(asctime)s :: %(module)s :: %(levelname)s :: %(funcName)s: %(lineno) d :: %(message)s",
                datefmt='%H:%M:%S'
            )


if __name__ == '__main__':
    event = threading.Event()
    thr1 = threading.Thread(target=shed, args=(event,))
    thr1.start()
    main()
