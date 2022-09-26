import tkinter
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import requests
from bs4 import BeautifulSoup
from tkinter import *
from ttkthemes import *
from tkinter.ttk import *

usertype = input('請輸入縣市全名:')

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
#print()

#------------------------------------------------------------------------------------------------------------------------
#tkinter介面

#主頁外觀
root = Tk()
root.title("威爾旅遊網站")
root.geometry("800x600")
bg = PhotoImage(file="logo2.png")
my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)
open = Label(root, text="歡迎來到，威爾公司台灣旅遊資訊系統!",font=("微軟正黑體", 16))
open.pack(anchor=CENTER)
open = Label(root, text="◯◍●———————————"+usertype+"未來一周氣象資料———————————●◍◯",font=("Arial", 16))
open.pack(anchor=CENTER)

#------------------------------------------------------------------------------------------------------------------------
#資料分析
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

#------------------------------------------------------------------------------------------------------------------------
#印出資料在視窗

for weather_forecast in weather_part:
    open = Label(root, text=weather_forecast,font=("Arial", 16))
    open.pack(anchor=CENTER)
open = Label(root, text="◯◍●————————————————————————————————●◍◯",font=("Arial", 16))
open.pack(anchor=CENTER)
root.mainloop()