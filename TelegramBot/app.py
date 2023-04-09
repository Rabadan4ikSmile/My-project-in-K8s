import requests
import psycopg2
import os
API_link = "https://api.telegram.org/bot6182814059:AAHVgGdddOEWjkrXkuTxZ1I0qqjVC-TZa8I"


# Функция для отправки сообщений пользователю
def send_message(chat_id, text):
    url = API_link + "/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)


# Функция для добавления записи в таблицу user_data
def add_user_data(name, age, gender, chat_id):
    conn = psycopg2.connect(database="runners_db", user="rabadan", password="1",
                            host=os.environ.get("DATABASE_HOST"), port="5432")
    cur = conn.cursor()
    # Создаем новую запись в таблице user_data
    cur.execute("INSERT INTO user_data (name, age, gender, chat_id) VALUES (%s, %s, %s, %s)",
                (name, age, gender, chat_id))
    conn.commit()
    cur.close()
    conn.close()


# Функция для обработки команды /start
def start_command(update):
    chat_id = update["message"]["chat"]["id"]
    send_message(chat_id, "Введите ФИО:")
    # Сохраняем chat_id в переменную global_chat_id для дальнейшего использования в функции add_user_data
    global global_chat_id
    global_chat_id = chat_id
    # Обнуляем значения переменных для нового пользователя
    global global_name
    global_name = ""
    global global_age
    global_age = None
    global global_gender
    global_gender = ""


# Функция для обработки сообщения от пользователя
def handle_message(update):
    chat_id = update["message"]["chat"]["id"]
    text = update["message"]["text"]
    try:
        if global_chat_id == chat_id:
            global global_name
            global global_age
            global global_gender
            if not global_name:
                global_name = text
                send_message(chat_id, "Введите возраст:")
            elif not global_age:
                try:
                    global_age = int(text)
                    send_message(chat_id, "Введите пол (муж/жен):")
                except ValueError:
                    send_message(chat_id, "Некорректный ввод. Введите возраст:")
            elif not global_gender:
                if text.lower() in ("муж", "жен"):
                    global_gender = text.lower()
                # Добавляем пользователя в базу данных
                    add_user_data(global_name, global_age, global_gender, global_chat_id)
                    send_message(global_chat_id, "Данные сохранены")
                else:
                    send_message(chat_id, "Некорректный ввод. Введите пол (муж/жен):")
    except NameError:
        if text == "/start":
            start_command(update)

# ID последнего обработанного обновления
last_update_id = None

while True:
    # Получаем обновления
    response = requests.get(API_link + "/getUpdates", params={"offset": last_update_id})
    updates = response.json()["result"]

    # Обрабатываем каждое обновление
    for update in updates:

        # Обновляем ID последнего обработанного обновления
        last_update_id = update["update_id"] + 1

        # Если в обновлении есть сообщение от пользователя
        if "message" in update and "text" in update["message"]:
            text = update["message"]["text"]

            # Обработка команды /start
            if text == "/start":
                start_command(update)
            # Обработка сообщения от пользователя
            else:
                handle_message(update)
