import json
import urllib.request
from collections import Counter

def get_data(user, token):
    page=1
    url = 'https://api.github.com/users/%s/repos?page=%d&per_page=100&access_token=%s' % (user, page, token)
    response = urllib.request.urlopen(url)  
    text = response.read().decode('utf-8')  
    page_data = json.loads(text)
    data=page_data
    while True:
        page+=1
        url = 'https://api.github.com/users/%s/repos?page=%d&per_page=100&access_token=%s' % (user, page, token)
        response = urllib.request.urlopen(url)  
        text = response.read().decode('utf-8')  
        page_data = json.loads(text)
        if len(page_data)==0:
            break
        data+=page_data
    return data

def rep_print(user, token):
    data=get_data(user,token)
    for i in data:
        print("%s: %s" %(i["name"],i["description"]))
                                                
def get_languages(user,token): #я не очень умная и не заметила, что в repos есть язык, поэтому сделала отдельный запрос и все работает медленно
    data=get_data(user, token) #зато если в репозитории больше одного языка, это учитывается
    lang_dict={} #но не всё в languages языки
    for i in data:
        repo=i["name"]
        lang_url = 'https://api.github.com/repos/%s/%s/languages?access_token=%s' % (user, repo, token)
        lang_response = urllib.request.urlopen(lang_url)
        text = lang_response.read().decode('utf-8')
        lang_data=json.loads(text)
        for lang in lang_data:
            if not (lang in lang_dict):
                lang_dict[lang] = 1
            else:
                lang_dict[lang] += 1
    return(lang_dict)

def user_rep_count(user, token):
    data = get_data(user, token)
    return(len(data))

def find_max_rep_count(user_list, token):
    user_dict={}
    for user in user_list:
        user_dict[user]=user_rep_count(user,token)
    max_user=max(user_dict, key=user_dict.get)
    print('Больше всего репозиториев у пользователя %s, у него их целых %d.' %(max_user,user_dict.get(max_user)))

def find_popular_language(user_list, token):
    lang_dict={}
    res_counter=Counter(lang_dict)
    for user in user_list:
        user_counter=Counter(get_languages(user,token))
        res_counter.update(user_counter)
    lang_dict=dict(res_counter)
    max_language=max(lang_dict, key=lang_dict.get)
    print('Самый популярный язык: %s, он используется в %d репозиториях.' %(max_language, lang_dict.get(max_language)))

def find_followers(user, token):
    url = 'https://api.github.com/users/%s?access_token=%s' % (user, token)
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    data = json.loads(text)
    return(data['followers'])

def find_max_follower_count(user_list, token):
    user_dict={}
    for user in user_list:
        user_dict[user]=find_followers(user,token)
    max_followers=max(user_dict, key=user_dict.get)
    print('Самый популярный пользователь: %s, у него %d фолловеров.' %(max_followers,user_dict.get(max_followers)))

def user_description(user, token):
    print('Вы выбрали пользователя %s' % user )
    print('Вот список его репозиториев:')
    rep_print(user,token)
    print('В этих репозиториях используются следующие языки:')
    languages=get_languages(user, token)
    for language in languages:
        print('%s используется в %d репозиториях.' %(language,languages.get(language))) 

def main(user_list, token):
    print('Список пользователей:')
    print(user_list)
    print('Введите имя одного из них')
    flag = False
    while not flag:
        user = input()
        if user in user_list:
            flag = True
        else:
            print('Такого пользователя в списке нет, попробуйте ещё')
    user_description(user,token)
    find_max_rep_count(user_list,token)
    find_popular_language(user_list,token)
    find_max_follower_count(user_list,token)
        
    
            
token = "ЗДЕСЬ ДОЛЖЕН БЫТЬ ВАШ ТОКЕН" #введите свой токен! И пользователей тоже можете других вбить заодно
user_list={'elmiram', 'maryszmary', 'lizaku', 'nevmenandr', 'ancatmara', 'roctbb', 'akutuzov', 'agricolamz', 'lehkost', 'kylepjohnson', 'mikekestemont', 'demidovakatya', 'shwars', 'JelteF', 'timgraham', 'arogozhnikov', 'jasny', 'bcongdon', 'whyisjake', 'gvanrossum'}
main(user_list, token)
