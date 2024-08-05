"""
- Импортируйте необходимые библиотеки: `selenium`, `webdriver`, `By`, `WebDriverWait`, `expected_conditions`, `time` и `json`.
- Определите **User Agent**
- Запустите **веб-драйвер Chrome.**
- Перейдите на страницу канала **YouTube**.
- Дождитесь загрузки страницы.
- Установите время паузы прокрутки и получите текущую высоту страницы.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # класс для указания типа селектора
from selenium.webdriver.common.by import By  # класс для ожидания наступления события
from selenium.webdriver.support.ui import WebDriverWait  # включает проверки, такие как видимоть элемента на странице, доступность элемента для клика и так далее
from selenium.webdriver.support import expected_conditions as EC  # ошибки в Selenium (сервер не отвечает, страницы не существует и т.д.)
from selenium.webdriver.chrome.options import Options
import time
# import json


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agent}")
# chrome_options.add_argument('--ignore-certificate-errors-spki-list')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.youtube.com/@progliveru/videos")

WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
)

scroll_pause = 2
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(scroll_pause)
    page_height = driver.execute_script("return document.documentElement.scrollHeight")

    if last_height == page_height:
        break

    last_height = page_height
    print(f"Высота last_height: {last_height}")

print(f"Высота: {page_height}")

driver.quit()
