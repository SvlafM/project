import sqlite3

# Создание таблицы web_link, если она не существует
def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS web_link (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    link TEXT,
                    title TEXT,
                    authors TEXT,
                    publication_date TEXT,
                    citations INTEGER,
                    language TEXT
                )''')

    conn.commit()
    conn.close()

# Добавление записи в таблицу web_link
def add_link(link, title, authors, publication_date, citations, language):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO web_link (link, title, authors, publication_date, citations, language) VALUES (?, ?, ?, ?, ?, ?)",
                (link, title, authors, publication_date, citations, language))

    conn.commit()
    conn.close()

# Получение списка записей из таблицы web_link с применением фильтров
def get_links(filters):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    query = "SELECT link, title FROM web_link WHERE 1=1"
    params = []

    if 'title' in filters:
        query += " AND title LIKE ?"
        params.append('%' + filters['title'] + '%')

    if 'authors' in filters:
        query += " AND authors LIKE ?"
        params.append('%' + filters['authors'] + '%')

    if 'publication_date' in filters:
        query += " AND publication_date = ?"
        params.append(filters['publication_date'])

    if 'citations' in filters:
        query += " AND citations >= ?"
        params.append(filters['citations'])

    c.execute(query, params)
    results = c.fetchall()

    conn.close()
    return results

# Пример использования

# Создание таблицы, если она не существует
create_table()

# Добавление записей в таблицу
add_link("http://example.com/article1", "Article 1", "John Doe", "2022-01-01", 10, "English")
add_link("http://example.com/article2", "Article 2", "Jane Smith", "2022-02-01", 5, "English")
add_link("http://example.com/article3", "Article 3", "John Doe", "2022-03-01", 20, "Spanish")

# Получение списка записей с применением фильтров
filters = {
    'title': 'Article',
    'authors': 'John',
    'citations': 15
}

results = get_links(filters)
for result in results:
    print(result[0], result[1])