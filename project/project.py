import urllib.request
import re
import html
from collections import Counter
import os
import csv

def get_html(link):
    req=urllib.request.Request(link)
    with urllib.request.urlopen(req) as response:
        page_html = response.read().decode('utf-8')
    return page_html

def get_author(page_html):
    regPostAuthor=re.compile('Автор:&nbsp;<span>.*?</span>', flags=re.DOTALL)
    regGarbage=re.compile('Автор:&nbsp;<span>', flags=re.DOTALL)
    regGarbage2=re.compile('</span>', flags=re.DOTALL)
    author=regPostAuthor.findall(page_html)
    new_author=[]
    for a in author:
        clean_a = regGarbage.sub("",a)
        clean_a = regGarbage2.sub("", clean_a)
        new_author.append(clean_a)
    if not new_author:
        return ('None')
    else:
        return(html.unescape(new_author[0]))

def get_page_title(page_html):
    regPostTitle=re.compile('<meta name="title" content=".*?"/>', flags=re.DOTALL)
    regGarbage=re.compile('<meta name="title" content="', flags=re.DOTALL)
    regGarbage2=re.compile('"/>', flags=re.DOTALL)
    title=regPostTitle.findall(page_html)
    new_title=[]
    for t in title:
        clean_t = regGarbage.sub("",t)
        clean_t = regGarbage2.sub("", clean_t)
        new_title.append(clean_t)
        
    return(html.unescape(new_title[0]))

def get_date(page_html):
    regPostDate=re.compile('<div class="uil-mo-popup-card__header__created__body">.*?</div>', flags=re.DOTALL)
    regGarbage=re.compile('<div class="uil-mo-popup-card__header__created__body">', flags=re.DOTALL)
    regGarbage2=re.compile('</div>', flags=re.DOTALL)
    date=regPostDate.findall(page_html)
    new_date=[]
    for d in date:
        clean_d = regGarbage.sub("",d)
        clean_d = regGarbage2.sub("", clean_d)
        clean_d = clean_d[:10]
        new_date.append(clean_d)
    return(new_date[0])

#в газете есть категории и теги, и того, и другого может бтыь больше одного
#категории шире, беру их, через запятую с пробелом
def get_topic(page_html):
    regPostTopic=re.compile('categories__list__item">.*?</a>', flags=re.DOTALL)
    regGarbage=re.compile('categories__list__item">', flags=re.DOTALL)
    regGarbage2=re.compile('</a>', flags=re.DOTALL)
    regTag = re.compile('<.*?>', re.DOTALL)
    topic=regPostTopic.findall(page_html)
    new_topic=[]
    for t in topic:
        clean_t = regGarbage.sub("",t)
        clean_t = regGarbage2.sub("", clean_t)
        clean_t = regTag.sub("", clean_t)
        new_topic.append(clean_t)
    joined_topic=', '.join(new_topic) 
    return(joined_topic)

def get_page_text(page_html):
    regPostText=re.compile('<div class="uil-block-text__text">.*?</div>', flags=re.DOTALL)
    text=regPostText.findall(page_html)
    regGarbage=re.compile('<div class="uil-block-text__text">', re.DOTALL)
    regGarbage2=re.compile('</div>', re.DOTALL)
    regTag = re.compile('<.*?>', re.DOTALL)  # это рег. выражение находит все тэги
    regScript = re.compile('<script>.*?</script>', re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', re.DOTALL)  # все комментарии
    new_text=[]
    for t in text:
        clean_t = regGarbage.sub("",t)
        clean_t = regGarbage2.sub("", clean_t)
        clean_t = regScript.sub("", clean_t)
        clean_t = regComment.sub("", clean_t)
        clean_t = regTag.sub("", clean_t)
        new_text.append(clean_t)
    plain_text=html.unescape(new_text[0])
    return plain_text

def get_links_from_page(page):
    page_link='http://gazeta-bam.ru/inova_block_mediaset/7191/card/?page='+str(page)
    page_html=get_html(page_link)
    regPostLink=re.compile('data-prefetch><a href=".*?"', flags=re.DOTALL)
    links=regPostLink.findall(page_html)
    regGarbage=re.compile('data-prefetch><a href="',re.DOTALL)
    regGarbage2=re.compile('"', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    new_links=[]
    for l in links:
        clean_l = regGarbage.sub("",l)
        clean_l=regSpace.sub("",clean_l)
        clean_l = regGarbage2.sub("", clean_l)
        clean_l='http://gazeta-bam.ru'+clean_l
        new_links.append(clean_l)
    return(new_links)

def download_news():
    page=1
    flag = True
    links=[]
    words=0
    article_count=1
    metadata_header=['path','author','header','created','sphere','topic','style']
    metadata_header=metadata_header+['audience_age','audience_level']
    metadata_header=metadata_header+['audience_size','source','publication','publ_year','medium','country','region','language']
    metadata_list=[metadata_header]
    while flag:
        links_from_page=get_links_from_page(page)
        for l in links_from_page:
            l_html=get_html(l)
            l_title=get_page_title(l_html)
            l_text=get_page_text(l_html)
            l_words=l_text.split()
            l_author=get_author(l_html)
            l_title=get_page_title(l_html)
            l_date=get_date(l_html)
            l_year=l_date[6:]
            l_month=l_date[3:5]
            print(l_date,l_month,l_year)
            l_topic=get_topic(l_html)
            words+=len(l_words)
            print(l_title)
            print(words)
            file_name='/газета/plain/'+str(l_year)+'/'+str(l_month)+'/'+'article'+str(article_count)+'.txt'
            directory=os.path.dirname(file_name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            print(directory)
            article_count+=1
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write('@au '+l_author+'\n')
                file.write('@ti '+l_title+'\n')
                file.write('@da '+l_date+'\n')
                file.write('@topic '+l_topic+'\n')
                file.write('@url '+l+'\n')
                file.write(l_text)
            metadata_const1=['нейтральный','н-возраст','н-уровень','районная']
            metadata=[file_name,l_author,l_title,l_date,'публицистика',l_topic]
            metadata=metadata+metadata_const1+[l,'БАМ',l_year]
            metadata2=['газета','Россия','Амурская область','ru']
            metadata=metadata+metadata2
            metadata_list.append(metadata)
            print(metadata)
                      
        links.append(links_from_page)
        page+=1
        if words >=100000:
            flag = False
    
    with open('/BAM/metadata.csv','w',newline='', encoding='utf-8') as csvfile:
        datawriter=csv.writer(csvfile, delimiter='\t')
        datawriter.writerows(metadata_list)
    print(links)
    print(page)

def make_text_plain_again(): #забыла сделать копию для майстема без метаданных, а скачивать повторно очень не хочется
    inp=r'\BAM\plain\2018\10' #надо бы по-человечески по папкам гулять, а то в ноябре всё сломается
    lst=os.listdir(inp)
    for fl in lst:
        f=inp+os.sep+fl
        if not os.path.exists(r'\BAM\plainer'):
            os.makedirs(r'\BAM\plainer')
        with open(f, 'r', encoding='utf-8') as file:
            lines=file.read().splitlines()
            lines=lines[5:]
            new_f=r'C:\BAM\plainer'+os.sep+fl
            with open(new_f, 'w', encoding='utf-8') as file2:
                for l in lines:
                    file2.write(l)
                
            

def run_mystem():
    inp=r'\BAM\plainer'
    lst=os.listdir(inp)
    if not os.path.exists(r'\BAM\mystem-xml\2018\10'):
        os.makedirs(r'\BAM\mystem-xml\2018\10')
    if not os.path.exists(r'\BAM\mystem-plain\2018\10'):
        os.makedirs(r'\BAM\mystem-plain\2018\10')
    for fl in lst:
        print(fl)
        os.system(r"\BAM\mystem.exe " + '--format xml -c -l -i -d --eng-gr ' + inp + os.sep + fl + r" \BAM\mystem-xml\2018\10" + os.sep + fl)
        os.system(r"\BAM\mystem.exe " + '-c -l -i -d --eng-gr ' + inp + os.sep + fl + r" \BAM\mystem-plain\2018\10" + os.sep + fl)

download_news()
make_text_plain_again()
run_mystem()
