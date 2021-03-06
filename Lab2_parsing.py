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
    output = template('select_all', result=result)
    #result.replace(' ','\n')
    print(result)
    return output

@route('/insert', method='POST')
def insert():
    if request.POST.save:
        ID = request.POST.ID.strip()#1
        Name_Offer = request.POST.Name_Offer.strip()#2
        Count_room = request.POST.Count_room.strip()#3
        Adress = request.POST.Adress.strip()#4
        Area = request.POST.Area.strip()#5
        Price = request.POST.Price.strip()#6
        Price_currency = request.POST.Price_currency.strip()#7
        Phone_Number = request.POST.Phone_Number.strip()#8
        Link = request.POST.Link.strip()#9
        try:
            cur.execute("INSERT INTO links VALUES(?,?,?,?,?,?,?,?,?)", (ID, Name_Offer, Count_room, Adress, Area, Price, Price_currency, Phone_Number, Link))
            con.commit()
            return '<p>>The new Ad was inserted into the database, the ID is %s</p>' % ID
        except:
            print('Data already exists')
            logging.error('This is an error insert', exc_info=True)
            logging.info('This is an error insert', exc_info=True)
            return '<p>>The new Ad already exists into the database, the ID is %s</p>' % ID

    else:
        return template('insert_db.tpl')


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
    Area=[i.text.replace('\xa0????','').replace(',','.').replace(' ','') for i in bs_pars.find_all(class_="a10a3f92e9--info-value--bm3DC")]
    Price=[i.text.replace('\xa0', ' ').replace('???','').replace(' ','') for i in bs_pars.find_all(itemprop='price')] # pulling out the price
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
            print('?????????????? ???? ????????????????: '+str(page)+' ???? 54; ?????????????? ???? ???????????????????? ????????????: '+str(room)+' ???? 6; ??????????????: '+str(len(page_link(temporary_link))))
            del(temporary_var)

        print('?????????? ?????????? ??????????????',len(temporary_massive))
        temporary_massive=list(set(temporary_massive))
        print('?????????? ???????????????????? ??????????????', len(temporary_massive))
        Counter=0

        for link in temporary_massive:
            Counter+=1
            print('????????????', Counter, '????', len(temporary_massive))
            try:
                insert_table(connect_db,parsing_page(link),room)
            except:
                logging.error('This is an error insert', exc_info=True)
                logging.info('This is an error insert', exc_info=True)
                continue

            con.commit()
            

    print('?????????? ?????????? ??????????????',len(var))
    var=list(set(var))
    print('?????????? ???????????????????? ??????????????',len(var))






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
        a=int(input("???????????????? ??????????????:\n1.?????????????? ?????????????? ???????????????? - 1;\n2.?????????????? ?????????????? ?? ???????????????????? ??????????????(???????????? ?????????? ???????????????? ?????? ???????????????????????? ??????????????) - 2;\n3.?????????? - 3\n",))
    except:
        logging.error("Error input a",exc_info=True)
    
    if a==1:    
        create_table(cur)
        print('\n?????????????? ??????????????\n')
    elif a==2:
        parsing_offer(cur,Apart_link)
        print('\n?????????????? ??????????????????\n')
    elif a==3:
        flag=0'''
        

con.close()
