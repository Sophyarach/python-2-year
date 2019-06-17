#Программа генерирует марковские цепочки, в качестве материала беря попарно книги c названиями типа "The art of ..."
#Внимание, книги были переведены из пдф в тхт первым попавшимся сайтом в гугле и не чистились.
#На красоту времени не хватило
#Сайт туточки: http://sophyarach.pythonanywhere.com/?
#Я у мамы теоретик, а не кампутирщик, не бейте

import markovify
import requests
import random
from flask import Flask
from flask import render_template, request, redirect
arts=('advertising','bonsai','dance','dentistry','digital_photography',
      'firework','fugue','genes','happiness','helicopter','illumination','lego',
      'longsword_combat','loving','programming','psychotherapy','public_speaking','war','web_design','wordly_wisdom')
arts_str=''
for a in arts:
    arts_str+='Art of '+a.capitalize()+', '
arts_str=arts_str[:-2]

def get_wisdom():
    two_arts=random.sample(arts,2)
    response1=requests.get('https://raw.githubusercontent.com/Sophyarach/python-2-year/master/final_project/texts/%s.txt' % two_arts[0])
    response2=requests.get('https://raw.githubusercontent.com/Sophyarach/python-2-year/master/final_project/texts/%s.txt' % two_arts[1])
    arts_text=response1.text+response2.text
    m=markovify.Text(arts_text)

    wisdom=''
    for i in range(5):
      wisdom+=m.make_sentence()+' '
    return(two_arts, wisdom)

app = Flask(__name__)

@app.route('/')
def index():
    two_arts,wisdom=get_wisdom()
    return '''
<html>
    <head>
        <title>Art of Everything</title>
    </head>
    <body>
        <h1>Art of everything</h1>
        За кучу лет человечество понаписало кучу книг с названиями типа "Art of ...", начиная с "Искусства войны", заканчивая "Искусством программирования"
        Всех этих книг и не перечитаешь... Поэтому это сделала моя программа за вас. А теперь пересказывает сразу две книги подряд.
        Список возможных "искусств":
        <br>'''+arts_str+'''<br>
        <form method="GET">
            <p align="center">Сгенерировать мудрость?
            <input type="submit" value="Да"></p>
            <br>
        Сгенерирована мудрость на тему <b>Art of '''+two_arts[0].capitalize()+'''</b> и <b>Art of '''+two_arts[1].capitalize()+'''</b>
        <br>
        <br>
        '''+wisdom+'''
        <br>
</form>


    </body>
</html>'''

