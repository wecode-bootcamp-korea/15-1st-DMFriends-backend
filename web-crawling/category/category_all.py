import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#1. csv file open
csv_name = "category_all.csv"
csv_open = open(csv_name, "w+", encoding='utf-8')
csv_writer = csv.writer(csv_open)
csv_writer.writerow(('product_id','sub_category','content_name','price')) 

#2. Driver & BeautifulSoup 
driver = webdriver.Chrome(ChromeDriverManager().install())

org_crawling_url = "https://store.kakaofriends.com/kr/index?tab=today"
driver.get(org_crawling_url)

#3. Parsing html code
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')
time.sleep(3)

#4. Get element selector
#4-1. Get category list
hamburger_button    = driver.find_element_by_xpath('//*[@id="innerHead"]/div/button[2]').click()
time.sleep(3)
category_button     = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/ul/li[4]/button').click()
time.sleep(3)
category            = driver.find_elements_by_xpath('/html/body/div[6]/div/div/div/ul/li[4]/ul/li/a')

del category[0]

category_list = []
for i in category:
    categorySeq = i.get_attribute('href').split("categorySeq=",1)[1]
    category_list.append(categorySeq)

#4-2. Get Product_num from main view
url1 = "https://store.kakaofriends.com/kr/products/category/subject?sort=createDatetime,desc"
driver.get(url1)
full_html   = driver.page_source
soup        = BeautifulSoup(full_html, 'html.parser')
time.sleep(3)

products = driver.find_elements_by_xpath('//*[@id="mArticle"]/div[3]/ul/li/a')

product_num = []      
for i in products:
    p_code = i.get_attribute('href').split("products/")[1]
    product_num.append(p_code)

#4-3. Get Product_detail from detail view
for i in product_num:
    url2        = "https://store.kakaofriends.com/kr/products/"+i
    driver.get(url2)
    full_html   = driver.page_source
    soup        = BeautifulSoup(full_html, 'html.parser')
    time.sleep(3) 
    
    script_text = driver.find_element_by_xpath("/html/body/script[2]").get_attribute('innerHTML')
    
    print(script_text[script_text.find('{')-1 : script_text.find('}')+1])

#print(script_text)

#csv_writer.writerow(('product_id','sub_category','content_name','price'))
#driver.quit()