import logging
#from os import 
from bottle import route, run, request, template
from typing import Counter
import requests
from bs4 import BeautifulSoup
import sqlite3

logging.basicConfig(filename='log',filemode='w', format='%(asctime)s - %(message)s')

con=sqlite3.connect(r'Cian/Cian_inform.db')
cur = con.cursor()

@route('/Cian')
def select():
    cur.execute("SELECT * FROM Flat")
    result = cur.fetchall()
    result.replace(' ','\n')
    print(result)
    return template('<b>{{name}}</b>!', name=result)

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/insert', method='GET')
def insert():
    if request.GET.save:
        id = str(cursor.lastrowid+1)
        href = request.GET.href.strip()
        title = request.GET.title.strip()
        cursor.execute("INSERT INTO links VALUES(?,?,?)", (id, href, title))
        new_id = cursor.lastrowid

        conn.commit()

    else:
        return template('new_task.tpl')


site='https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=1&room2=1'

def page_link(url):
    start_url='https://www.cian.ru'
    r = requests.get(url)
    bs_pars = BeautifulSoup(r.content, 'html.parser')
    #print(bs_pars.find_all(class_="a10a3f92e9--img-link-wrapper--wi8vG"))
    href_url=list(set([i['href'] for i in bs_pars.find_all(href=True) if 'https://www.cian.ru/sale/flat/' in i['href']]))
    return href_url

#print(page_link(site))
#print('Amount =',len(page_link(site)))

def parsing_page(url):
    
    Information=[] # storage massive

    r = requests.get(url, stream=True) # input get
    bs_pars = BeautifulSoup(r.content, 'html.parser') # processing get

    ID=url.replace('https://www.cian.ru/sale/flat/','').replace('/','')
    Name=[i.text for i in bs_pars.find_all(class_="a10a3f92e9--title--UEAG3")]
    Area=[i.text.replace('\xa0м²','').replace(',','.').replace(' ','') for i in bs_pars.find_all(class_="a10a3f92e9--info-value--bm3DC")]
    Price=[i.text.replace('\xa0', ' ').replace('₽','').replace(' ','') for i in bs_pars.find_all(itemprop='price')] # pulling out the price
    Price_currency=[i['content'] for i in bs_pars.find_all(itemprop='priceCurrency')] # pulling currency
    Phone_Number=[i.text for i in bs_pars.find_all(class_="a10a3f92e9--phone--_OimW")]
    address=[i for i in bs_pars.find_all(itemprop='name')]
    #Descriptor=[i.text.replace('\n',' ') for i in bs_pars.find_all(itemprop="description")]
   
    Information=[ID,Name[0],address[-1]['content'],float(Area[0]),Price[0],Price_currency[0],Phone_Number[0],url]
    
    return Information




def parsing_offer(connect_db,var):
    for room in Rooms:
        temporary_massive=[]
        for page in range(1,55):
            temporary_link='https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p='+str(page)+'&region=1&room'+str(room)+'=1'
            temporary_var=[temporary_massive.append(i) for i in page_link(temporary_link)]
            print('Процесс по странице: '+str(page)+' из 54; Процесс по количеству комнат: '+str(room)+' из 6; Найдено: '+str(len(page_link(temporary_link))))
            del(temporary_var)

        print('Общее число записей',len(temporary_massive))
        temporary_massive=list(set(temporary_massive))
        print('Число уникальных записей', len(temporary_massive))
        Counter=0

        for link in temporary_massive:
            Counter+=1
            print('Запись', Counter, 'из', len(temporary_massive))
            try:
                insert_table(connect_db,parsing_page(link),room)
            except:
                logging.error('This is an error insert', exc_info=True)
                logging.info('This is an error insert', exc_info=True)
                continue

            con.commit()
            

    print('Общее число записей',len(var))
    var=list(set(var))
    print('Число уникальных записей',len(var))






def create_table(connect_db):
    connect_db.execute('''CREATE TABLE Flat ( 
                       ID INTEGER primary key not null unique,
                       Name_Offer TEXT,
                       Count_room INTEGER,
                       Adress TEXT,
                       Area REAL,
                       Price INTEGER,
                       Price_Currency TEXT,
                       Phone_Number TEXT,
                       Link TEXT not null unique);''')
                       

def insert_table(connect_db,massiv,count_room):
    string_massiv=str(massiv[0])+", '"+str(massiv[1])+"', "+str(count_room)+",'"+str(massiv[2])+"', "+str(massiv[3])+", "+str(massiv[4])+", '"+str(massiv[5])+"', '"+str(massiv[6])+"', '"+str(massiv[7])+"'"
    print(string_massiv)
    connect_db.execute("INSERT INTO Flat VALUES ("+str(string_massiv)+")")


run(host='localhost', port=8080)




'''flag=1
while flag==True:
    try:
        a=int(input("Выберите вариант:\n1.Создать таблицу напишите - 1;\n2.Парсинг страниц и заполнение таблицы(только после создания или пересоздания таблицы) - 2;\n3.Выход - 3\n",))
    except:
        logging.error("Error input a",exc_info=True)
    
    if a==1:    
        create_table(cur)
        print('\nТаблица создана\n')
    elif a==2:
        parsing_offer(cur,Apart_link)
        print('\nТаблица заполнина\n')
    elif a==3:
        flag=0'''
        

con.close()
