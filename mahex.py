from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

URL = "https://mahex.com/%D8%B4%D8%B9%D8%A8-%D9%88-%D9%86%D9%85%D8%A7%DB%8C%D9%86%D8%AF%DA%AF%DB%8C%D9%87%D8%A7%DB%8C-%D9%85%D8%A7%D9%87%DA%A9%D8%B3"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get(URL)

time.sleep(5)

records = []

cards = driver.find_elements(
    By.XPATH,
    "//a[contains(@href,'/agents/')]/ancestor::div[contains(@class,'flex')]"
)

print(f"Found {len(cards)} records")

for card in cards:

    try:

        # نام شعبه
        try:
            name = card.find_element(
                By.XPATH,
                ".//div[contains(@class,'font-medium')]"
            ).text.strip()
        except:
            name = ""

        # تلفن
        try:
            phone = card.find_element(
                By.XPATH,
                ".//a[contains(@href,'tel:')]"
            ).text.strip()
        except:
            phone = ""

        # آدرس
        try:
            address = card.find_element(
                By.XPATH,
                ".//div[contains(@class,'text-t3-on-surface-variant')]"
            ).text.strip()
        except:
            address = ""

        # لینک جزئیات
        try:
            detail_link = card.find_element(
                By.XPATH,
                ".//a[contains(@href,'/agents/')]"
            ).get_attribute("href")
        except:
            detail_link = ""

        records.append({
            "نام نمایندگی": name,
            "تلفن": phone,
            "آدرس": address,
            "لینک جزئیات": detail_link
        })

        print(name)

    except Exception as e:
        print(e)

driver.quit()

df = pd.DataFrame(records)

df.to_excel(
    "mahex_agents.xlsx",
    index=False
)

print(f"Saved {len(df)} rows")