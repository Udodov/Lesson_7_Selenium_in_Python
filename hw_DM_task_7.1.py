from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import json

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=chrome_options)

try:
    browser.get("https://www.labirint.ru/genres/2308/")
    WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    page_height = browser.execute_script("return document.documentElement.scrollHeight")
    print(f"Текущая высота : {page_height}")

    pause_time = 3
    time.sleep(pause_time)

    last_height = page_height
    while True:
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(pause_time)
        new_page_height = browser.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_height:
            break
        last_height = new_page_height
    print(f"Финальная высота: {last_height}")

    title_xpath = "//a[@class='product-title-link']"
    author_xpath = "//div[@class='product-author']/a"
    price_xpath = "//span[@class='price-val']"

    title_elements = browser.find_elements(By.XPATH, title_xpath)
    author_elements = browser.find_elements(By.XPATH, author_xpath)
    price_elements = browser.find_elements(By.XPATH, price_xpath)

    book_data = {}

    for i in range(min(len(title_elements), len(author_elements), len(price_elements))):
        title = title_elements[i].text.strip()
        author = author_elements[i].text.strip()
        price = price_elements[i].text.strip()
        book_data[title] = {'author': author, 'price': price}

    with open('labirint_books.json', 'w', encoding='utf-8') as json_file:
        json.dump(book_data, json_file, ensure_ascii=False, indent=4)

except Exception as E:
    print(f'Произошла ошибка {E}')
finally:
    browser.quit()
