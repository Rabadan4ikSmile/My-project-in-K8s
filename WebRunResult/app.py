from flask import Flask, render_template
import psycopg2
import os
app = Flask(__name__)

# Функция для получения данных из таблицы run_result
def get_run_result():
    conn = psycopg2.connect(database="runners_db", user="rabadan", password="1",
                             host=os.environ.get("DATABASE_HOST"), port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM run_result")
    rows = list(cur.fetchall())
    cur.close()
    conn.close()
    return rows

# Отображение данных на веб-странице /run_result
@app.route('/run_result')
def run_result():
    rows = get_run_result()
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)

