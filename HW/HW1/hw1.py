import random

def choose_theme():
    flag=False
    while not flag:
        print('Выберите тему:\n 1.Астрономия\n 2.Лингвистика\n 3. Кулинария\n Введите число от 1 до 3')
        theme=input()
        if theme=='1':
            print('Выбрана тема "Астрономия"')
            res='Астрономия.txt'
            flag=True
        if theme=='2':
            print('Выбрана тема "Лингвистика"')
            res='Лингвистика.txt'
            flag=True
        if theme=='3':
            print('Выбрана тема "Кулинария"')
            res='Кулинария.txt'
            flag = True
        if not flag:
            print('Вы ввели что-то не то')
    return res

def choose_word(theme):
    file=open(theme,'r',encoding='utf-8')
    word=[s.strip() for s in file]
    res=random.choice(word)
    file.close()
    return res

def form(n):
    if n==1:
        return ' попытка'
    if 2<=n<=4:
        return ' попытки'
    if n>=5:
        return ' попыток'
    if n==0:
        return ' попыток'

def check_letter(s):
    if len(s)==1 and ((s>='а') and (s<='я') or (s=='ё')):
        return s
    else:
        print('Это не буква')
        return False

def game(word):
    tries=10
    solved = False
    tried_letters=set()
    question=['_']*len(word)
    print(''.join(question))
    while tries>0 and not solved:
        is_letter = False
        print('Осталось' + str(tries) + form(tries))
        while not is_letter:
            print ('Введите букву:')
            letter=check_letter(input().lower())
            if letter and (letter in tried_letters):
                print('Эту букву вы уже пробовали')
            else:
                is_letter=True
        tried_letters.add(letter)
        if letter in word:
            print ('Такая буква есть!')
            for i in range(len(word)):
                if word[i]==letter:
                    question[i]=letter
                    print(''.join(question))
            if word==''.join(question):
                solved=True
        else:
            print ('Такой буквы нет.')
            tries=tries-1
    if solved:
        print('Вы выиграли! Это слово "' + word +'"')
    if tries==0:
        print('Вы проиграли! Это было слово:'+word)

game(choose_word(choose_theme()))
        
