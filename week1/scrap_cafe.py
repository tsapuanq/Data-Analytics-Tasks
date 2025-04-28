from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Можно включить, чтобы скрыть окно
driver = webdriver.Chrome(options=options)
driver.get("https://2gis.kz/kokshetau")

# 1) Вводим "кафе" в поиск
search_input = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class*="_cu5ae4"]'))
)
search_input.send_keys("кафе")
search_input.submit()

time.sleep(5)  # Ждем, пока подгрузятся результаты

# 2) Делаем "бесконечный скролл" (здесь 10 раз)
for _ in range(10):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(1)

# 3) Находим все карточки
cards = driver.find_elements(By.CSS_SELECTOR, 'div[class*="_1kf6gff"]')
print(f"Найдено карточек: {len(cards)}")

data = []

# 4) Для каждой карточки достаем нужные поля
for card in cards:
    try:
        name = card.find_element(By.CSS_SELECTOR, 'span[class*="_lvwrwt"]').text
    except:
        name = ''

    try:
        link = card.find_element(By.CSS_SELECTOR, 'a[href*="/firm/"]').get_attribute('href')
    except:
        link = ''

    try:
        rating = card.find_element(By.CSS_SELECTOR, 'div[class*="y10azs"]').text
    except:
        rating = ''

    try:
        votes = card.find_element(By.CSS_SELECTOR, 'div[class*="jspdzm"]').text
    except:
        votes = ''

    try:
        address = card.find_element(By.CSS_SELECTOR, 'span[class*="1w0zi9t"]').text
    except:
        address = ''

    # Пример сбора описания (если есть):
    try:
        desc_blocks = card.find_elements(By.CSS_SELECTOR, 'div[class*="4cxmt7"]')
        description = ' '.join(block.text for block in desc_blocks).strip()
    except:
        description = ''

    # Промо, тип — аналогично
    # ...
    
    data.append({
        "name": name,
        "link": link,
        "rating": rating,
        "votes": votes,
        "address": address,
        "description": description
    })

# 5) Сохраняем в CSV
df = pd.DataFrame(data)
df.to_csv("cafes_kokshetau.csv", index=False, encoding='utf-8')
driver.quit()
print(f"✅ Собрано {len(df)} заведений.")
