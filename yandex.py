from time import sleep
from bs4 import BeautifulSoup
from telegram import send_telegram
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main():
    ser = Service('/Users/mac/Desktop/chromedriver')
    op = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=ser, options=op)
    browser.implicitly_wait(5)
    url_rest = 'https://yandex.ru/maps/org/salone_pasta_bar/205155748378/reviews/?ll=30.343560%2C59.938707&z=30'
    browser.get(url_rest)
    browser.maximize_window()
    browser.find_element(By.CLASS_NAME, "rating-ranking-view").click()
    browser.find_elements(By.CLASS_NAME, "rating-ranking-view__popup-line")[1].click()
    sleep(5)
    source_data = browser.page_source
    soup = BeautifulSoup(source_data, features="html.parser")
    reviews = soup.find_all('div', {'class': 'business-reviews-card-view__review'})
    for item in reviews:
        parse_review(item) 
    browser.close()
        
def parse_review(review):
    date_time = ''
    id_review = ''
    author_name = ''
    author_url = ''
    rating = 0
    text = ''
    
    date_tr = review.find('span', {'class': 'business-review-view__date'})
    date = str(date_tr.find('meta')).split()[1].split('=')[1].split('T')[0].replace('"','')
    time = str(date_tr.find('meta')).split()[1].split('=')[1].split('T')[1][0:5]
    date_time = date + ' ' + time
    
    rating_tr = review.find('div', {'class': 'business-rating-badge-view__stars'})
    rating_tt = rating_tr.find_all('span', {'class': 'inline-image _loaded business-rating-badge-view__star _size_m'})
    for i in rating_tt:
        rating +=1
    
    author_url_tr = review.find('a', {'class': 'business-review-view__user-icon'})
    author_url = str(author_url_tr).split()[2].split('"')[1]
    
    author_name = str(review.find('span', {'itemprop': 'name'})).split('>')[1].split('<')[0]
    
    text = str(review.find('span', {'class': 'business-review-view__body-text'})).split('>')[1].split('<')[0]
    
    id_review = author_url.split('/')[-1]
    
    result = {'site': 'Yandex', 'date_time': date_time, 'review_id': id_review, 
              'author_name': author_name, 'author_url': author_url, 'rating': rating, 'text': text }
    search_id(result)
    
def search_id(review_info):
    with open('rev_id.txt', 'r') as file:
        count = 0
        unic_id = review_info['review_id']
        for item in file.readlines():
            line = item.strip()
            if line == unic_id:
                count += 1
        if count == 0:   
            get_message(review_info)
            with open('rev_id.txt', 'a') as file:
                file.write(f'\n{unic_id}')
        else:
            count = 0

def get_message(review_info):
    review_site = review_info['site']
    review_date = review_info['date_time']
    review_author_name = review_info['author_name']
    review_author_url = review_info['author_url']
    review_author = f'<a href="{review_author_url}">{review_author_name}</a>'
    rating = {1: '★✩✩✩✩',
              2: '★★✩✩✩',
              3: '★★★✩✩',
              4: '★★★★✩',
              5: '★★★★★'}
    review_rating = rating[review_info['rating']]
    review_text = review_info['text']
    
    message = f'''
    {review_rating}
    {review_site}, {review_date}
    автор: {review_author}
    
    {review_text}'''
    send_telegram(message)

if __name__ == '__main__':
    while True:
        sleep(60)
        main()