import undetected_chromedriver as uc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import warnings
warnings.filterwarnings('ignore')
import time
import getpass
import pandas as pd
import csv
from itertools import zip_longest


if __name__=='__main__':

    browser=uc.Chrome()


    browser.maximize_window()
    browser.get("https://www.instagram.com/") 
    time.sleep(3)### waiting for three seconds 
    username = browser.find_element(By.XPATH,('//input[@name="username"]'))
    password = browser.find_element(By.XPATH,('//input[@name="password"]'))
    username.send_keys("username")
    password.send_keys("pwd")
    submit = browser.find_element(By.XPATH,('//button[@type="submit"]'))
    submit.click()
    time.sleep(3)
    try:
        browser.find_element(By.XPATH,('//button[@class="_acan _acap _acas _aj1-"]')).click()
    except:
        pass
    time.sleep(2)
    try:
        browser.find_element(By.XPATH,('//button[@class="_a9-- _a9_0"]')).click()
    except:
        pass
    time.sleep(2)
    
    # notnow = browser.find_element(By.XPATH,("//button[contains(text(), 'Plus tard')]")).click()
    # #turn on notif
    # time.sleep(10)
    # notnow2 = browser.find_element(By.XPATH,("//button[contains(text(), 'Plus tard')]")).click()
    url ="https://www.instagram.com/explore/tags/workoutmotivation/"
    browser.get(url)

    time.sleep(10)

    items_link=[]


    last_height=browser.execute_script("return document.body.scrollHeight")

    itemTargetCount =200
    authors=[]
    followers=[]
    comments=[]
    main_comments=[]
    main_authors=[]

    while itemTargetCount > len(items_link):
        try:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

            time.sleep(1)

            new_height = browser.execute_script("return document.body.scrollHeight")

            if new_height==last_height:
                break

            links=[lien.get_attribute('href') for lien in browser.find_elements(By.XPATH,('//div[@class="_aabd _aa8k  _al3l"]/a'))]
            
            for link in links:
                items_link.append(link)
            
            print(len(items_link))
            
            
        except:
            pass
 

    # links_comments=[link.get_attribute("href") for link in browser.find_elements(By.XPATH,('//div[@class="_aabd _aa8k _aanf"]//a'))]
    # links_images=[link.get_attribute("src") for link in browser.find_elements(By.XPATH,('//div[@class="_aabd _aa8k _aanf"]//img'))]


    # authors=[]
    # followers=[]
    # comments=[]
    # main_comments=[]
    # main_authors=[]
    j=0
    for link in items_link:
        try:
        
            print(link)
            browser.get(link)
            time.sleep(1)
            # wait = WebDriverWait(browser, 10)
            comment_main = browser.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "_a9zn", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "_aade", " " ))]')
            poster = browser.find_element(By.XPATH, '//h2[@class="_a9zc"]')
            # poster=browser.find_element(By.XPATH,('//h2[@class="_a9zc"]'))
            followers_=[follower.text for follower in browser.find_elements(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "xt0psk2", " " )) and contains(concat( " ", @class, " " ), concat( " ", "x568u83", " " ))]')]
            comments_=[comment.text for comment in browser.find_elements(By.XPATH,'//div[@class="_a9zs"]')]
            print(comment_main)
            print(followers_)
            for comm in comments_:
                comments.append(comm.strip())
            for follo in followers_:
                followers.append(follo.strip())
            # followers.extend(followers_)
            # comments.extend(comments_)
            for i in range(len(followers_)):
                main_comments.append(comment_main.text.strip())
                main_authors.append(poster.text.strip())

                
            print(comments)    
            print(main_comments)    
            print(main_authors)    
                
            info= [main_authors, main_comments, followers, comments]
            B_data = zip_longest(*info)
            with open('fitness_advice.csv', 'a',encoding="utf-8") as myFile:
                wr = csv.writer(myFile)
                if j==0:
                    wr.writerow(["main_authors", "main_comments","followers","comments"])
                    
                wr.writerows(B_data)  
                j=j+1     
       
        except:
            pass


    print(items_link)  
    print(followers)      
    print(comments)      






