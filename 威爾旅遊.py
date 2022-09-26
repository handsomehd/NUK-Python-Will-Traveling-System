import requests
from bs4 import BeautifulSoup
from tkinter import *
from ttkthemes import *
from tkinter.ttk import *
#------------------------------------------------------------------------------------------------------------------------
#輸入與選擇地區
taiwandes = ['北部地區','中部地區','南部地區','東部地區','離島地區'] #建立一個區域的list作為整個程式爬蟲的基礎
print('歡迎來到，威爾公司台灣旅遊資訊系統!')
print()
print("【請選擇一個想要去的台灣地區】")
print("－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－")
count = 0
for every in taiwandes:
    if(count == 0):
        print(every, end = '')
        count = count+1
    else:
        print('、'+every, end = '')
print("")
print("－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－")
#利用迴圈來強迫使用者遵照格式輸入
#此處利用check來計算，順便能當作taiwandes這個list的計次
count = 0
times = len(taiwandes)
while True:
    check = 0
    print()
    usertype = input('⋯✈ 請輸入想去的台灣區域(中文表示):')
    for everycity in taiwandes:
        if(usertype != everycity):
            check = check+1
        else:
            break
    if(check >= 0 and check <= 4):
        break
    else:
        print('輸入錯誤，請再試一次!')
        print()
#------------------------------------------------------------------------------------------------------------------------
#根據地區，將縣市資料印出
#利用list存放爬蟲出來的縣市名稱，並印出來
listdes = []
print()
taiwanweb = 'https://www.taiwan.net.tw/m1.aspx?sNo=000050'+str(check+1)
rescity = requests.get(taiwanweb) 
soupcity = BeautifulSoup(rescity.text,'html.parser')
city = soupcity.findAll("span", class_="circularbtn-title")
print("【請選擇一個想要去的台灣縣市】")
print("－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－")
for des in city:
        des = des.string
        listdes.append(des)
count = 0
for listcity in listdes:
    if(count == 0):
        print(listcity, end = '')
        count = count+1
    else:
        print('、'+listcity, end = '')
print("")
print("－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－")

#------------------------------------------------------------------------------------------------------------------------
#輸入縣市
#先記入該地區有幾個縣市，便於讓使用者輸入跟計入縣市的list做匹配
count = len(listdes)
while True:
    check = 0
    print()
    usertype = input('⋯✈ 請輸入想去的縣市(中文表示):')
    for city in listdes:
        if(usertype != city):
            check = check+1
        else:
            break
    if(check >= 0 and check <= count-1):
        break
    else:
        print('輸入錯誤，請再試一次!')
        print()
#------------------------------------------------------------------------------------------------------------------------
#對應氣象網站，將使用者輸入的縣市，與氣象網站的網頁做匹配
resweather = requests.get('https://www.cwb.gov.tw/V8/C/S/eservice/rss.html') 
soupweather = BeautifulSoup(resweather.text,'html.parser')
if(usertype == "連江縣(馬祖)"):
    usertype = "連江縣"
cityname = "顯示"+usertype+"RSS的xml檔,另開新視窗" #網頁名稱
weather = soupweather.find("a",title=cityname)
weather_choose = "https://www.cwb.gov.tw"+weather.get("href")
weather_forecast = requests.get(weather_choose)
weather_forecast.encoding = 'UTF-8'
soup = BeautifulSoup(weather_forecast.text, "html.parser")

#------------------------------------------------------------------------------------------------------------------------
#資料變形並去除不必要項目
type(soup)
for 預報 in soup.findAll('item'):
    未來氣象 = [預報.description]
氣象分類 = str(未來氣象[0])
氣象分類 = 氣象分類.strip('<description><![CDATA[')
氣象分類 = 氣象分類.replace(']]> </','')
氣象分類 = 氣象分類.replace('\n\t','')
print()
#------------------------------------------------------------------------------------------------------------------------
#將氣象資料存入list並印出
print('')
print("◯◍●———————————"+usertype+"未來一周氣象資料———————————●◍◯")
print('')
weather_part = []
part = ''
for word in 氣象分類:
    if(word == '<' or word == 'B' or word == 'R' or word == '>'):
        if(word == '>'):
            weather_part.append(part)
            part = ''
            continue
        else:
            continue
    else:
        part = part+word
for weather_forecast in weather_part:
    print(weather_forecast)
print("◯◍●————————————————————————————————●◍◯")
#------------------------------------------------------------------------------------------------------------------------
#將縣市對應到旅遊網站
if(usertype == "連江縣"):
    usertype = "連江縣(馬祖)"
print()
listcity = []
rescity = requests.get(taiwanweb) 
soupcity = BeautifulSoup(rescity.text,'html.parser')
city = soupcity.findAll("a", class_="circularbtn")
for des in city:
        des = des.get("href")
        listcity.append(des)
#------------------------------------------------------------------------------------------------------------------------
#將該縣市的景點印出
siteweb = 'https://www.taiwan.net.tw/'+listcity[check]
res2 = requests.get(siteweb) 
soup2 = BeautifulSoup(res2.text,'html.parser')
titles2 = soup2.findAll("a", class_="card-link")
print("【請選擇一個想要去的觀光景點】")
print("－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－")
count = 0
for begin in titles2:
    if(count == 0):
        print(begin.get("title"),end = '')
        count = count+1
    elif(count == 4):
        count = 0
        print()
    else:
        print('、'+begin.get("title"), end='')
        count = count+1
print('')
print("－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－")

#------------------------------------------------------------------------------------------------------------------------
#景點輸入，並做名稱匹配
count = 0
while True:
    location = input("⋯✈ 請輸入景點：")
    for title2 in titles2:
        if(location == title2.get("title")):
            count = count+1
    if(count != 0):
        break
    else:
        print('輸入錯誤，請再試一次!')
        print()

print('')
print("◯◍●———————————以下是"+location+"的觀光資訊———————————●◍◯")
print('')
#將匹配到的名稱對應到該網站，再印出景點介紹網站的資訊
for title2 in titles2:
    if(location == title2.get("title")):
        loca3="https://www.taiwan.net.tw/"+title2.get("href")
        res3 = requests.get(loca3)
        soup3 = BeautifulSoup(res3.text,'html.parser')
        detail = soup3.find_all('p')
        for p in detail:
            p=p.text
            if (p == '建議瀏覽器：Chrome，Firefox，IE10.0以上版本 (螢幕最佳顯示效果為1920 * 1280)'):
                break
            else:
                print(p)
                print()
print("◯◍●———————————————————————————————————————●◍◯")










