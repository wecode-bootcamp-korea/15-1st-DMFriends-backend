import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

csv_name = "starbucks.csv"
csv_open = open(csv_name, "w+", encoding='utf-8')
csv_writer = csv.writer(csv_open)
csv_writer.writerow(('category','title','image_url')) 
 
driver = webdriver.Chrome(ChromeDriverManager().install())

org_crawling_url = "https://www.starbucks.co.kr/menu/drink_list.do"
driver.get(org_crawling_url)
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')

time.sleep(3)

drink_list =soup.select('li.menuDataSet')

prod_list = []
for i in drink_list:
    drink = i.select_one('a')
    product_num = drink['prod']
    prod_list.append(product_num)

prod_list.remove('9200000002081')
prod_list.remove('9200000000038')
prod_list.remove('9200000003230')
prod_list.remove('128401')
prod_list.remove('128198')
prod_list.remove('9200000003218')
prod_list.remove('9200000003221')
prod_list.remove('9200000002406')
prod_list.remove('9200000003200')
prod_list.remove('9200000003209')
prod_list.remove('168016')
prod_list.remove('9200000001321')
prod_list.remove('9200000000187')
prod_list.remove('94')
prod_list.remove('9200000000190')
prod_list.remove('9200000002496')
prod_list.remove('9200000003203')
prod_list.remove('9200000003206')
prod_list.remove('128192')
prod_list.remove('110601')
prod_list.remove('110572')
prod_list.remove('9200000003215')
prod_list.remove('110563')
prod_list.remove('9200000003212')


for i, product_num in enumerate(prod_list):
    url1 = "https://www.starbucks.co.kr/menu/drink_view.do?product_cd="+ product_num
    driver.get(url1)
    full_html = driver.page_source
    soup = BeautifulSoup(full_html, 'html.parser')
    categories = driver.find_element_by_xpath('//*[@id="container"]/div[1]/div/h2/img')
    title = driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div[2]/div[1]/h4')
    image = driver.find_element_by_xpath('//*[@id="product_thum_wrap"]/ul/li/a/img')     
   
    print(categories.get_attribute('alt'))
    print(title.text)
    print(image.get_attribute('src'))
    
    csv_writer.writerow((categories.get_attribute('alt'), title.text, image.get_attribute('src')))

driver.quit()