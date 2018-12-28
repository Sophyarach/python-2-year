import re
import os
import sqlite3


def clear_mystem(file):
    with open(file, encoding='utf-8') as f:
        print(f)
        text = f.read()
        print(text)
        text = re.sub(r'{([а-яА-ЯёЁ\-]*)[?=].*?}', r'\1', text)
    return text


def clear_everything():
    inp = r'\BAM\mystem-plain\2018\10'
    lst = os.listdir(inp)
    for fl in lst:
        f = inp + os.sep + fl
        print(f)
        text = clear_mystem(f)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(text)


conn = sqlite3.connect('BAMdb.db')


def add_to_db():
    inp1 = r'\BAM\plain\2018\10'
    inp2 = r'\BAM\mystem-plain\2018\10'
    inp3 = r'\BAM\plainer'
    lst = os.listdir(inp1)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS texts(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title TEXT,
        url TEXT,
        plain TEXT,
        lemmed TEXT)''')

    for fl in lst:
        f1 = inp1 + os.sep + fl
        with open(f1, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            ti = lines[1]
            ti = ti[4:]
            url = lines[4]
            url = url[5:]
        f2 = inp2 + os.sep + fl
        with open(f2, 'r', encoding='utf-8') as file:
            lemmed = file.read()
        f3 = inp3 + os.sep + fl
        with open(f3, 'r', encoding='utf-8') as file:
            text = file.read()
        c.execute('INSERT INTO texts (title, url, plain, lemmed) VALUES (?,?,?,?)', (ti, url, text, lemmed))

    conn.commit()


# clear_everything()
add_to_db()
