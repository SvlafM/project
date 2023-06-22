from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from googletrans import Translator
import sqlite3

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

MAX_LOAD = 0.8  # Пороговое значение нагрузки на сервер
CAPTCHA_ATTEMPTS = 3  # Количество попыток ввода капчи
BAN_TIME = 3600  # Время блокировки IP (в секундах)

# Подключение к базе данных SQLite
conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS web_link (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT, title TEXT, authors TEXT, publication_date TEXT, citations INTEGER)')
conn.close()

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10/minute")  # Ограничение числа запросов до 10 в минуту
def search():
    if request.method == 'POST':
        query = request.form['query']  # Получаем данные из формы поиска

        # Проверка нагрузки на сервер
        load = calculate_server_load()  # Функция для расчета нагрузки
        if load > MAX_LOAD:
            # Нагрузка выше порогового значения - проверяем капчу
            if not verify_captcha():
                return render_template('captcha.html')  # Отображаем страницу с капчей

        results = []

        # Проверяем, нужно ли выполнять перевод запроса
        translate_query = request.form.get('translate_query')
        if translate_query:
            translator = Translator()
            translated_query = translator.translate(query).text
        else:
            translated_query = query

        # Фильтры по различным критериям
        filters = {
            'title': request.form.get('title_filter'),
            'authors': request.form.get('authors_filter'),
            'date': request.form.get('date_filter'),
            'citations': request.form.get('citations_filter')
        }

        # Формируем SQL-запрос с учетом переведенного запроса и фильтров
        sql_query = f"SELECT link, title FROM web_link WHERE title LIKE '%{translated_query}%'"

        for field, value in filters.items():
            if value:
                sql_query += f" AND {field} LIKE '%{value}%'"

        # Выполняем SQL-запрос
        conn = sqlite3.connect('database.db')
        results = conn.execute(sql_query).fetchall()
        conn.close()

        return render_template('results.html', query=query, results=results, query_params=request.form)

    return render_template('search.html')

@app.route('/captcha', methods=['POST'])
def captcha():
    # Проверяем правильность ответа на капчу
    answer = request.form['answer']
    if answer == str(6):
        return render_template('search.html')
    else:
        return render_template('captcha.html', message='Неверный ответ')

def calculate_server_load():
    # Функция для расчета нагрузки на сервер
    # Реализуйте ваш алгоритм расчета нагрузки
    return 0.5

def verify_captcha():
    # Функция для проверки правильности капчи
    # Реализуйте ваш алгоритм проверки капчи
    return True

if __name__ == '__main__':
    app.run()
