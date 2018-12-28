from flask import Flask, render_template, request
import os
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
def result():
    search = request.args.get('search', '').strip()
    page = request.args.get('page', '').strip()
    with open('tempfile.txt', 'w', encoding='utf-8') as f:
        f.write(search)
    lemmed = os.system('C:\mystem.exe -w -l -d tempfile.txt tempresult.txt')
    with open('tempresult.txt', encoding='utf-8') as f:
        text = f.read().replace('{', '').replace('}', ' ').strip()
    conn = sqlite3.connect('BAMdb.db')
    c = conn.cursor()
    c.execute("SELECT COUNT (lemmed) FROM texts WHERE lemmed  LIKE ?", ('%' + text + '%',))
    q = c.fetchone()[0]
    print(q)
    if page == '':
        p = 0
    else:
        p = int(page)
    c.execute("SELECT title, url, plain, lemmed FROM texts WHERE lemmed  LIKE ? LIMIT 10 OFFSET ?",
              ('%' + text + '%', p * 10))
    res = c.fetchall()
    previews = []
    search1 = search.replace(' ', '+')
    i = 0
    l = len(res)
    for r in res:
        pos = r[3].find(text)
        n = r[3][:pos].count(' ')
        t = r[2].split()
        t1 = text.split()
        start = n - 20
        middle = 20
        if start < 0:
            start = 0
            middle = n
        finish = n + 20
        if finish > len(t):
            finish = len(t)
        t = t[start:finish]
        newtext = [' '.join(t[:middle]), ' '.join(t[middle:middle + len(t1)]), ' '.join(t[middle + len(t1):])]
        previews.append(newtext)
    return render_template('results.html', search=search1, res=res, previews=previews, i=i, l=l, p=p, q=q)


if __name__ == '__main__':
    app.run()
