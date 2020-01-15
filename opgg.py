import requests
from bs4 import BeautifulSoup
import sys
import mysql.connector
mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="",
        database="opgg"
    )
mycursor = mydb.cursor()




def champions(insertornot,date):
    tablename = date + "_champions"
    res = requests.get("http://tw.op.gg/champion/")
    soup = BeautifulSoup(res.text, features="html.parser")
    # for champoin in soup.select(".champion-index__champion-item__name"):
    #    champoins.append(champoin.text)
    # 取得所有英雄名字

    # print(champoins) #印出所有英雄名字
    # result =soup
    # TOPname= soup.select("tbody.tabItem.champion-trend-tier-TOP .champion-index-table__name")
    # TOPwinrate = soup.select("tbody.tabItem.champion-trend-tier-TOP .champion-index-table__cell champion-index-table__cell--value")
    # for item in TOPwinrate:
    #    print(item.text)

    # print(TOP.select("champion-index-table__cell champion-index-table__cell--rank")[0].text)

    # for chapname in soup.select(".tabItem champion-trend-tier-TOP"):
    #    print(chapname.select(".champion-index-table__name selectorgadget_selecteds").text)

    soup = BeautifulSoup(res.text, features="html.parser")
    test = soup.findAll('tbody')

    # w =test[0].select('.champion-index-table__name')
    # print(test[1].text)
    # print(test[0].find_all("td", class_="champion-index-table__cell champion-index-table__cell--value")[0].text)
    # test1 = test[0].find_all("td", class_="champion-index-table__cell champion-index-table__cell--value")[0].text
    # test1 = test1.replace('%','')
    # test2 = float(test1)
    # print(test2)
    # for item in test[0].find_all("td", class_="champion-index-table__cell champion-index-table__cell--value")[1].text:
    #    print(item.text)

    def insertchampions(rank, name, win, pick, position):
        sql = "INSERT INTO " + tablename + " (rank , name, winrate ,pickrate ,position) VALUES (%s, %s ,%s ,%s,%s)"
        val = (rank, name, win, pick, position)
        mycursor.execute(sql, val)
        mydb.commit()

    position = ['Top', 'Jungle', 'Middle', 'Bottom', 'Support']

    for x in range(0, 5):
        print(position[x])
        n = 0
        rk = 0
        for item in test[x].select('.champion-index-table__name'):
            name = item.text
            rank = test[x].find_all("td", class_="champion-index-table__cell champion-index-table__cell--rank")[rk].text
            rk += 1
            win = test[x].find_all("td", class_="champion-index-table__cell champion-index-table__cell--value")[n].text
            win = win.replace('%', '')
            win = float(win)
            n += 1
            pick = test[x].find_all("td", class_="champion-index-table__cell champion-index-table__cell--value")[n].text
            n += 2
            pick = pick.replace('%', '')
            pick = float(pick)
            if insertornot == 'y':
                insertchampions(rank, name, win, pick, position[x])
                url="http://www.op.gg/champion/"+name+"/statistics/"+position[x]+"/matchup?"
                counter(name,url ,insertornot,position[x],date)
            else:
                pass
            #print(item + win + pick)
            print("名字:{name} 排名:{rank} 勝率:{win} 選用率:{pick}".format(name=name, rank=rank, win=win, pick=pick))
            # print('{name} is {age} years old!'.format(name = 'Justin', age = 35))
            

def counter(champoin,url,insertornot,position,date):
    tablename = date + "_counters"

    def insertcounter(name, cname, cwin, crate,times, position):
        sql = "INSERT INTO " + tablename + " (name , cname, cwin ,crate,times ,position) VALUES (%s, %s ,%s, %s ,%s,%s)"
        # (name VARCHAR(25) ,cname VARCHAR(25) , winrate FLOAT(20) ,cwin FLOAT(20),crate FLOAT(20),position VARCHAR(10),date INT(10) NOT NULL DEFAULT
        val = (champoin, cname, cwin, crate,times, position)
        mycursor.execute(sql, val)
        mydb.commit()
    cookies = dict(customLocale='en_US')
    res = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(res.text, features="html.parser")
    times = soup.select('.champion-matchup-champion-list small')  # 對線次數
    nwr = soup.select('.champion-matchup-champion-list span')  # 名字勝率機率

    # print(test)
    t = 0  # t是次數
    n = 0  # n是名字、勝率、機率
    # print(nwr[3].text)
    for item in times:

        counter = times[t].text
        counter = counter.replace(',', '')
        counter = int(counter)
        t += 1

        cname = nwr[n].text
        n += 1

        cwin = nwr[n].text
        cwin = str(cwin).strip()
        cwin = cwin.replace('%', '')
        cwin = float(cwin)
        n += 1

        crate = nwr[n].text
        crate = str(crate)
        crate = crate.replace('%', '')
        crate = float(crate)

        n += 1
        #print("名字:{cname} 勝率:{cwin} 次數:{counter} 機率:{crate}".format(cname=cname, cwin=cwin, counter=counter, crate=crate))
        if insertornot =='y':
            insertcounter(champoin, cname, cwin, crate,counter, position);


def main():

    insertornot = input('是否存入資料庫(y/whatever):')
    date = input('輸入今天日期(Ex:20181225)：')
    if insertornot == 'y':

        tablename = date+"_champions"
        creat="CREATE TABLE "+ tablename + " (rank INT(10), name VARCHAR(25) , winrate FLOAT(20) ,pickrate FLOAT(20),position VARCHAR(10),date INT(10) NOT NULL DEFAULT " + date +")"
        mycursor.execute(creat)
        tablename = date+"_counters"
        creat="CREATE TABLE "+ tablename + " (name VARCHAR(25) ,cname VARCHAR(25)  ,cwin FLOAT(20),crate FLOAT(20),times INT(10),position VARCHAR(10),date INT(10) NOT NULL DEFAULT " + date +")"
        mycursor.execute(creat)

    champions(insertornot,date)
    
main()


    






