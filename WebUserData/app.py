from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

# Функция для получения данных из таблицы user_data
def get_user_data():
    conn = psycopg2.connect(database="runners_db", user="rabadan", password="1",
                            host=os.environ.get("DATABASE_HOST"), port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_data")
    rows = list(cur.fetchall())
    cur.close()
    conn.close()
    return rows

# Отображение данных на главной веб-странице
@app.route('/')
def index():
    rows = get_user_data()
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)

