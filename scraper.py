import time
import datetime as dt
from decimal import Decimal

# importeer selenium modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# importeer webdriver en Beautiful Soup
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# sql connector voor database communicatie
import mysql.connector

# tijd om te wachten; pas deze aan als de scraper niet goed werkt
tijd = 2

# driver opzetten 
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
url = 'https://www.google.nl'
driver.get(url)
driver.maximize_window()

# variabelen aanmaken voor zoekopdracht
query_zoon = 'lego potter 75968'
query_dochter = 'playmobil kasteel 70447'


# Zoekopdracht voor zoon opstarten

# accept cookies
accept_cookies = driver.find_element(By.CSS_SELECTOR, '#L2AGLb').click()

# zoekbox selecteren en zoekopdracht activeren
time.sleep(tijd)
search_box = driver.find_element(By.NAME, 'q').send_keys(query_zoon)
time.sleep(tijd)
push_search = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type = "submit"]'))
        )
push_search.click()

push_shopping = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#hdtb-msb > div:nth-child(1) > div > div:nth-child(2) > a'))
        )
push_shopping.click()

# accept cookies van shopping
accept_cookies = driver.find_element(By.CSS_SELECTOR, '#yDmH0d > div.T1diZc.KWE8qe > c-wiz > div:nth-child(3) > div > div:nth-child(2) > div').click()
accept_cookies = driver.find_element(By.CSS_SELECTOR, '#islmp > div > div > div.tmS4cc.jpaVhe.AfKuZd > div > div > div > div > div > div:nth-child(2) > div').click()

# tijd om pagina in te laden
time.sleep(tijd)

# lijst aanmaken om de zoekgegevens in op te slaan
data = []
current_time = dt.date.today()

# page source grijpen en inlezen met BS
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
result = soup.prettify()

# soup output printen naar textfile om na te kijken
with open('result.txt', 'w', encoding="utf-16") as file:
    file.write(result)
    
# zoek alle elementen van google ads
search_object = soup.findAll('div', {'class', 'n9INWd'})
for item in search_object:
    try:
        title = item.find('div', class_='iKMEte hLMyCc uDz8te').text
    except:
        title = 'empty'
    try:
        seller = item.find('div', class_='kaNpvd nLaBQd hLMyCc').text
    except:
        seller = 'empty'
    try:
        link = item.find('a')['href']
    except:
        link = 'empty'
    try:
        price = item.find('div', class_='t3Ss7 hLMyCc').text
        #price = (price.strip('€ '))
    except:
        price = 'empty'
    try:
        new_var = item.find('img')
        image= new_var.get('src')
        if len(image) > 1000:
            image = 'empty'
    except: 
        image = 'empty'
    
    data.append([title, seller, link, price, image, current_time])

# Verbinding met de SQL Server
conn = mysql.connector.connect(
    host = "localhost",
    user = "bit_academy",
    password = "bit_academy")

# maak cursor aan zodat SQL query kan worden uitgevoerd na het schrijven ervan
cursor = conn.cursor()

# Maak de database
cursor.execute("CREATE DATABASE IF NOT EXISTS Scraping;")
cursor.execute("USE Scraping;")
# Maak de tabel en de kolommen
cursor.execute("DROP TABLE IF EXISTS Lego;")
cursor.execute("""CREATE TABLE IF NOT EXISTS Lego(
    id              INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(255),
    seller          VARCHAR(255),
    link            VARCHAR(600),
    price           VARCHAR(255),
    image           VARCHAR(600),
    searchDate      VARCHAR(255)
);""")

query = ("INSERT INTO Scraping.Lego(title, seller, link, price, image, searchDate) VALUES (%s,%s,%s,%s,%s,%s)")
cursor.executemany(query, data)
conn.commit()
conn.close()

# printen dat de opdracht klaar is
driver.quit() 
print(f"Alle zoekresultaten van {query_zoon} zijn in de database opgeslagen. Succes ermee!")

# Zoekopdracht voor dochter opstarten
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
url = 'https://www.google.nl'
driver.get(url)
driver.maximize_window()

# accept cookies
accept_cookies = driver.find_element(By.CSS_SELECTOR, '#L2AGLb').click()

# zoekbox selecteren en zoekopdracht activeren
time.sleep(tijd)
search_box = driver.find_element(By.NAME, 'q').send_keys(query_dochter)
time.sleep(tijd)
push_search = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type = "submit"]'))
        )
push_search.click()


# push shopping
push_shopping = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#hdtb-msb > div:nth-child(1) > div > div:nth-child(4) > a'))
        )
push_shopping.click()

# tijd om pagina in te laden
time.sleep(tijd)

# lijst aanmaken om de zoekgegevens in op te slaan
data = []
current_time = dt.date.today()

# page source grijpen en inlezen met BS
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
result = soup.prettify()

# soup output printen naar textfile om na te kijken
with open('result.txt', 'w', encoding="utf-16") as file:
    file.write(result)
    
# zoek alle elementen van google ads
search_object = soup.findAll('div', {'class', 'KZmu8e'})
for item in search_object:
    try:
        title = item.find('div', class_='sh-np__product-title translate-content').text
    except:
        title = 'empty'
    try:
        seller = item.find('div', class_='sh-np__seller-container').text
    except:
        seller = 'empty'
    try:
        link = item.find('a')['href']
    except:
        link = 'empty'
    try:
        price = item.find('b', class_='translate-content').text
    except:
        price = 'empty'
    try:
        new_var = item.find('img', src=True)
        image= new_var.get('src')
        if len(image) > 1000:
            image = 'empty'
    except: 
        image = 'empty'
    
    data.append([title, seller, link, price, image, current_time])

# Verbinding met de SQL Server
conn = mysql.connector.connect(
    host = "localhost",
    user = "bit_academy",
    password = "bit_academy")

# maak cursor aan zodat SQL query kan worden uitgevoerd na het schrijven ervan
cursor = conn.cursor()

# Maak de database
cursor.execute("CREATE DATABASE IF NOT EXISTS Scraping;")
cursor.execute("USE Scraping;")
# Maak de tabel en de kolommen
cursor.execute("""CREATE TABLE IF NOT EXISTS Playmobil(
    id              INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(255),
    seller          VARCHAR(255),
    link            VARCHAR(600),
    price           VARCHAR(255),
    image           VARCHAR(600),
    searchDate      VARCHAR(255)
);""")

query = ("INSERT INTO Scraping.Playmobil(title, seller, link, price, image, searchDate) VALUES (%s,%s,%s,%s,%s,%s)")
cursor.executemany(query, data)
conn.commit()
conn.close()

# opdracht klaar; de driver afsluiten en printen dat de opdracht klaar is    
driver.quit()
print(f"Alle zoekresultaten van {query_dochter} zijn in de database opgeslagen. Succes ermee!")
