#!/usr/bin/python
# Creator Kingtebe
# Date 05-01-2022, 18:27 WIB
# Support https://t.me/Captain_bulls
# Follow my github https://github.com/Musk-ID
import os,re,sys,time,datetime
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    exit("# Module requests and bs4 not installed ")

class mainbot:
    def __init__(self):
        self.ses = requests.Session()
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        self.col = lambda code: "\x1b[1;"+str(code)+"m"
        self.base = "https://cryptowin.io"

    def get_user(self):
        url = self.base + "/account"
        req = self.ses.get(url).text
        par = BeautifulSoup(req,"html.parser")
        try:
            username = re.search("</span>\s([^>]+)\</",req).group(1)
            balance = re.search('"true">\</i>\s([^>]+)\</h2',req).group(1)
            referal = par.find("input",{"type":"text","id":"refLink","class":"form-control"}).get("value")
            address = par.find("input",{"type":"text","id":"btcaddress","class":"form-control","name":"address","aria-describedby":"helpBlock"}).get("value")
            return username,balance,referal,address
        except AttributeError:
            os.remove(".cookie")
            exit(self.col(97)+" ["+self.col(92)+"!"+self.col(97)+"]  There is an error !\n")

    def countdown(self,second):
        while second:
            mins,secs = divmod(second,60)
            timer = self.col(97)+" ["+self.col(92)+"•"+self.col(97)+"] Waiting ⟨{:02d}:{:02d}⟩ ".format(mins,secs)
            print(timer,end="\r")
            time.sleep(1)
            second -= 1

    def get_claim(self):
        if not os.path.exists(".cookie"):
           print(self.col(97)+"\n ["+self.col(92)+"•"+self.col(97)+"] Please take cookies from the web cryptowin.io")
           open(".cookie","w").write(input(self.col(97)+" ["+self.col(92)+"•"+self.col(97)+"] Input cookie : "))
        self.ses.headers.update({"Host":"cryptowin.io","cache-control":"max-age=0","upgrade-insecure-requests":"1","user-agent":"Mozilla/5.0 (Linux; Android 8.1.0; CPH1853) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36","cookie":open(".cookie").read()})
        account = self.get_user()
        print("")
        print(self.col(97)+" ["+self.col(92)+"+"+self.col(97)+"] Getting Account Info...");time.sleep(2.4);print(self.col(97)+" ["+self.col(92)+"+"+self.col(97)+"] creator  : kingtebe\n"+self.col(97)+" ["+self.col(92)+"+"+self.col(97)+"] support  : https://t.me/Captain_bulls\n"+self.col(97)+" ["+self.col(92)+"+"+self.col(97)+"] username :",str(account[0])+"\n"+self.col(97)+" ["+self.col(92)+"+"+self.col(97)+"] balance  :",str(account[1]),"BTC\n"+self.col(97)+" ["+self.col(92)+"+"+self.col(97)+"] referral :",str(account[2])+"\n"+self.col(97)+" ["+self.col(92)+"+"+self.col(97)+"] address  :",str(account[3])+"\n"+self.col(97)+" ["+self.col(92)+"+"+self.col(97)+"] Bot Starting...\n");time.sleep(1.5)
        while True:
            try:
                 url = self.base + "/faucet"
                 req = BeautifulSoup(self.ses.get(url).text,"html.parser")
                 csrf = req.find("input",{"type":"hidden","name":"csrfToken"})
                 Idcaptcha = req.findAll("img")[2].get("src")
                 captcha = self.ses.get(self.base + Idcaptcha)
                 with open("img.png",mode="wb") as save:
                      save.write(captcha.content)
                 os.system("termux-open img.png")
                 total = input(self.col(97)+" ["+self.col(92)+"•"+self.col(97)+"] Input captcha : ")
                 data = {
                     "csrfToken":csrf.get("value"),
                     "captcha":total,
                     "claim":""
                 }
                 url = self.base + "/faucet"
                 post = self.ses.post(url,data=data)
                 page = self.ses.get(self.base + "/faucet").text
                 repr = self.get_user()
                 try:
                     earn = re.search("('([^>]+)',\s'([^>]+).*?')",page)
                     print(self.col(97)+" ["+self.col(92)+self.time+self.col(97)+"]"+earn.group(1).replace("<b>","").replace("</b>","").removeprefix("'success',").replace("'","").replace("You have successfully claimed","successfully claimed").replace("!","")+self.col(90)+" - "+self.col(97)+repr[1])
                     self.countdown(int(60*15))
                 except AttributeError:
                     print(self.col(97)+" ["+self.col(92)+"!"+self.col(97)+"] Captcha invalid ",flush=True,end="\r")
                     continue
            except requests.exceptions.ReadTimeout:continue
            except requests.exceptions.ConnectionError:continue


if __name__=='__main__':
    try:
        App = mainbot()
        App.get_claim()
    except KeyboardInterrupt:
         exit()
