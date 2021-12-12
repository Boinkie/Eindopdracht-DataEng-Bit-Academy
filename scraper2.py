import time
import csv

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
url = 'https://www.brickwatch.net/nl-NL/'
driver.get(url)
driver.maximize_window()

# variabelen aanmaken voor zoekopdracht
query_zoon = '75954'

time.sleep(tijd)

# accept cookies
accept_cookies = driver.find_element(By.CSS_SELECTOR, '#cookie-banner > div > div').click()

# zoekbox selecteren en zoekopdracht activeren
search_box = driver.find_element(By.XPATH, '//*[@id="navsearch"]/div[2]/input').send_keys(query_zoon)
push_search = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navsearch"]/div[2]/button/i'))
        )
push_search.click()
search_expand = driver.find_element(By.XPATH, '//*[@id="row-all"]/td/button').click()

# tijd om pagina in te laden
time.sleep(tijd)

# lijst aanmaken om de zoekgegevens in op te slaan
data = []

# page source grijpen en inlezen met BS
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
result = soup.prettify()

# soup output printen naar textfile om na te kijken
with open('result.txt', 'w', encoding="utf-16") as file:
    file.write(result)
    
# zoek alle elementen van tabel met sellers en prijzen
search_object = soup.findAll('tr', class_='row-collapse collapse in')
for item in search_object:
    #prijzen scrapen
    row = []
    sub_item = item.findAll('td')
    for x in sub_item:
        tekst = x.text
        row.append(tekst)
    
    # verkoper scrapen
    img = item.find('img')
    try:
        seller = img.get('title')
    except:
        seller = item.find('td').text
    data.append([seller, row[3]])
driver.quit()

# data wegschrijven in csv bestand
header = ['seller', 'price']
with open('brick.csv', 'w', encoding='UTF8') as f:   
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
print("De resultaten zijn gescraped en weggeschreven in brick.csv.")
