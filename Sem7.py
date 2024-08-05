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
    browser.get("https://www.youtube.com/@progliveru/videos")
    WebDriverWait(browser, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    page_height = browser.execute_script("return document.documentElement.scrollHeight")
    print(f"Текущая высота : {page_height}")

    # - В цикле прокрутите страницу вниз, чтобы загрузить динамически загружаемые видео.
    # - Подождите, пока страница загрузит новые добавленные видео.
    # - Рассчитайте новую высоту страницы.
    # - Проверьте, совпадает ли новая высота с предыдущей. Если да, значит, все видео загружены, и вы можете выйти из цикла.

    # Подсказки:

    # - Используйте метод execute_script() для прокрутки страницы вниз.
    # - Используйте метод time.sleep(), чтобы приостановить выполнение на указанное время.

    pause_time = 3
    time.sleep(pause_time)

    last_height = page_height
    while True:
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(pause_time)
        new_page_height = page_height = browser.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_height:
            break
        last_height = new_page_height
    print(last_height)

    # Задание 3
    # - Найдите все названия видео на странице с помощью XPath.

    # - Найдите все элементы метаданных на странице с помощью XPath.

    # - Извлеките текст из заголовков видео и метаданных.

    # - Создайте словарь для хранения данных.

    video_titles_xpath = "//*[@id='video-title-link']"
    metadata_xpath = "//div[@id='metadata-line']/span[1]"
    published_xpath = "//div[@id='metadata-line']/span[2]"

    video_titles = browser.find_elements(By.XPATH, video_titles_xpath)
    metadata_elements = browser.find_elements(By.XPATH, metadata_xpath)
    published_elements = browser.find_elements(By.XPATH, published_xpath)

    video_data = {}

    for i in range(min(len(video_titles), len(metadata_elements))):
        title = video_titles[i].text

        views = metadata_elements[i].text
        ago = published_elements[i].text
        video_data[title] = {'views': views.strip(), 'published': ago.strip()}

    with open('GB_youtube.json', 'w', encoding='utf-8') as json_file:
        json.dump(video_data, json_file, ensure_ascii=False, indent=4)
        
except Exception as E:
    print(f'Произошла ошибка {E}')
finally:
    browser.quit()