from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import csv
import time

#1. csv file open
csv_name = "main_today.csv"
csv_open = open(csv_name, "w+", encoding="utf-8")
csv_writer = csv.writer(csv_open)
csv_writer.writerow(("profile_image", "name", "display_date", "image", "like_count", "title", "sub_copy"))


#2. Driver & BeautifulSoup
driver = webdriver.Chrome(ChromeDriverManager().install())

crawling_url = "https://store.kakaofriends.com/kr/index?tab=today"
driver.get(crawling_url)


#3. Parsing html code
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')
time.sleep(2)


#4. Get element selector (1)
articles = soup.select('#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article') 

#5. Get element selector (2)
for i in range(1, len(articles)+1):
    profile_image   = driver.find_element_by_css_selector(f'#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article:nth-child({i}) > section.header__Wrap-sc-1uyrtg9-0.hXrGqX > div.header__ImageWrap-sc-1uyrtg9-1.kmIBex > img')
    name            = driver.find_element_by_css_selector(f'#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article:nth-child({i}) > section.header__Wrap-sc-1uyrtg9-0.hXrGqX > div:nth-child(2) > p')
    display_date    = driver.find_element_by_css_selector(f'#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article:nth-child({i}) > section.header__Wrap-sc-1uyrtg9-0.hXrGqX > div:nth-child(2) > div > span.header__DisplayDate-sc-1uyrtg9-7.bbyqry')
    like_count      = driver.find_element_by_css_selector(f'#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article:nth-child({i}) > section:nth-child(2) > div.contents__LikeCountWrap-sc-1b0iw5u-2.fDHkJk > span > span > span')
    title           = driver.find_element_by_css_selector(f'#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article:nth-child({i}) > section:nth-child(2) > p')
    sub_copy        = driver.find_element_by_css_selector(f'#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article:nth-child({i}) > section:nth-child(2) > div.contents__SubCopy-sc-1b0iw5u-6.dLrCHR')

    images = soup.select(f'#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article:nth-child({i}) > section:nth-child(2) > div.media-slider__Wrap-bw8abp-0.ksgZQS > div > div > div')
    
    #6. Get image url
    for j in range(1, len(images)+1):
        image = driver.find_element_by_css_selector(f'#mArticle > main > div.today__Wrap-sc-1gh0i9h-0.fCbncI > article:nth-child({i}) > section:nth-child(2) > div.media-slider__Wrap-bw8abp-0.ksgZQS > div > div > div:nth-child({j}) > div > div > img')

        img_url = image.get_attribute('src')

        #7. Create csv file    
        if i == 0:
                csv_writer.writerow((profile_image.get_attribute('src'), name.text, display_date.text, img_url, like_count.text, title.text, sub_copy.text))
        else:
            csv_writer.writerow((profile_image.get_attribute('src'), name.text, display_date.text, img_url, like_count.text, title.text, sub_copy.text))


    
    

