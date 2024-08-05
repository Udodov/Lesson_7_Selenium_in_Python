from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pymongo import MongoClient
import time

# Настройка MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['labirint_db']
collection = db['books']

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=chrome_options)

try:
    browser.get("https://www.labirint.ru/genres/2308/")
    WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    
    last_height = browser.execute_script("return document.documentElement.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        WebDriverWait(browser, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        new_height = browser.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    title_xpath = "//a[@class='product-title-link']"
    author_xpath = "//div[@class='product-author']/a"
    price_xpath = "//span[@class='price-val']"
    discount_xpath = "//span[@class='price-old']"

    title_elements = WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.XPATH, title_xpath)))
    author_elements = WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.XPATH, author_xpath)))
    price_elements = WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.XPATH, price_xpath)))
    discount_elements = browser.find_elements(By.XPATH, discount_xpath)

    for i in range(min(len(title_elements), len(author_elements), len(price_elements))):
        try:
            title = title_elements[i].text.strip()
            author = author_elements[i].text.strip()
            discounted_price = price_elements[i].text.strip().replace(' ', '').replace('₽', '')
            
            # Проверяем, есть ли скидка
            original_price = discounted_price
            if i < len(discount_elements):
                original_price = discount_elements[i].text.strip().replace(' ', '').replace('₽', '')
            
            book_data = {
                'title': title,
                'author': author,
                'original_price': float(original_price),
                'discounted_price': float(discounted_price)
            }
            
            collection.insert_one(book_data)
            
        except Exception as e:
            print(f"Ошибка при обработке книги: {e}")

except Exception as E:
    print(f'Произошла ошибка {E}')
finally:
    browser.quit()
    client.close()

print("Данные успешно сохранены в MongoDB.")
