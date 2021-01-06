from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from json import dumps,loads
class InstaBot:
    def __init__(self):
        pass

    def login(self,username,password):
        self.browser=webdriver.Chrome()
        self.username=username
        self.password=password
        self.browser.get("https://www.instagram.com")
        time.sleep(4)
        self.browser.find_element_by_name("username").send_keys(self.username)
        self.browser.find_element_by_name("password").send_keys(self.password)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click() 
        time.sleep(3)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]/div').click()
        time.sleep(3)

    def getData(self,n):
        self.browser.find_elements_by_css_selector(".Y8-fY")[n].click()
        time.sleep(5)
        jscommand = """
        followers = document.querySelector(".isgrP");
        followers.scrollTo(0, followers.scrollHeight);
        var lenOfPage=followers.scrollHeight;
        return lenOfPage;
        """
        lenOfPage = self.browser.execute_script(jscommand)
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(1)
            lenOfPage = self.browser.execute_script(jscommand)
            if lastCount == lenOfPage:
             match=True
        time.sleep(5)
        followersList = []
        followers = self.browser.find_elements_by_css_selector(".FPmhX.notranslate._0imsa ")
        for follower in followers:
            followersList.append(follower.text)
        self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
        return followersList

    def getFollowers(self):
        return self.getData(1)

    def getFollows(self):
        return self.getData(2)

    def unFollow(self,list_):
        self.browser.find_elements_by_css_selector(".Y8-fY")[2].click()
        time.sleep(5)
        jscommand = """
        followers = document.querySelector(".isgrP");
        followers.scrollTo(0, followers.scrollHeight);
        var lenOfPage=followers.scrollHeight;
        return lenOfPage;
        """
        lenOfPage = self.browser.execute_script(jscommand)
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(1)
            lenOfPage = self.browser.execute_script(jscommand)
            if lastCount == lenOfPage:
             match=True
        time.sleep(5)
        follows = self.browser.find_elements_by_css_selector(".FPmhX.notranslate._0imsa ")
        unfollow_buttons = self.browser.find_elements_by_css_selector(".sqdOP.L3NKy._8A5w5    ")
        for follow in range(len(follows)) :
            for user in list_:
                if follows[follow].text==user:
                    time.sleep(2)
                    unfollow_buttons[follow+1].click()
                    time.sleep(2)
                    self.browser.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]").click()
                    print(f"[+] {user} takipten çıkıldı.")
        self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
  
    def removeUnFollowers(self):
        self.save(self.update())
        data=self.read()
        data=data[len(data)-1]
        self.unFollow(data["geri takip etmeyenler"])

    def followAllFollowers(self):
        self.browser.find_elements_by_css_selector(".Y8-fY")[1].click()
        time.sleep(5)
        jscommand = """
        followers = document.querySelector(".isgrP");
        followers.scrollTo(0, followers.scrollHeight);
        var lenOfPage=followers.scrollHeight;
        return lenOfPage;
        """
        lenOfPage = self.browser.execute_script(jscommand)
        match=False
        while(match==False):
            lastCount = lenOfPage
            time.sleep(1)
            lenOfPage = self.browser.execute_script(jscommand)
            if lastCount == lenOfPage:
             match=True
        time.sleep(5)
        follow_buttons = self.browser.find_elements_by_css_selector(".sqdOP.L3NKy.y3zKF     ")
        time.sleep(2)
        print(follow_buttons)
        for i in range(len(follow_buttons)): 
             follow_buttons[i].click()
             time.sleep(2)
             #self.browser.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]").click()
        self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
        
    def update(self):
        f=self.getFollowers()
        u=self.getFollows()
        data={
        "tarih":datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "takipçilerin":f,
        "takip ettiklerin":u,
        "geri takip etmediklerin":list(set(f)-set(u)),
        "geri takip etmeyenler":list(set(u)-set(f))
        }
        return data

    def save(self,data):
        with open("data.log","a+") as log:
            log.write(f"{data}\n")
    def read(self):
        with open("data.log","r") as f:
            data=[]
            lines=f.read().replace("'",'"').split("\n")
            for line in lines:
                try:
                  data.append(loads(line))
                except:
                    pass
        return data
    def stop(self):
        self.browser.close()

