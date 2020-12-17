import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#1. csv file open
csv_name = "character_type.csv"
csv_open = open(csv_name, "w+", encoding='utf-8')
csv_writer = csv.writer(csv_open)
csv_writer.writerow(('categorySeq','name')) 

#2. Driver & BeautifulSoup 
driver = webdriver.Chrome(ChromeDriverManager().install())

org_crawling_url = "https://store.kakaofriends.com/kr/index?tab=today"
driver.get(org_crawling_url)

#3. Parsing html code
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')

time.sleep(3)

#4. Get element selector (1)
hamburger_button    = driver.find_element_by_xpath('//*[@id="innerHead"]/div/button[2]').click()
time.sleep(2)
char_button         = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul/li[3]/button').click()
time.sleep(2)
#char                = soup.selector(f'body > div:nth-child(7) > div > div > div > ul > li:nth-child(3) > ul > li > a')
char         = driver.find_elements_by_xpath('/html/body/div[6]/div/div/div/ul/li[3]/ul/li/a')

for i in char:
    character = i.get_attribute('href').split("categorySeq=",1)[1]
    name = i.text
    
    csv_writer.writerow((character, name))

driver.quit()