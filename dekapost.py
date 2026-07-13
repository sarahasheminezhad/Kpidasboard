from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

URL = "https://dekapost.com/fa-IR/dekapost/4920/page/%D9%86%D9%85%D8%A7%DB%8C%D9%86%D8%AF%DA%AF%DB%8C-%D9%87%D8%A7"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get(URL)

time.sleep(5)

results = []

# پیدا کردن تمام مارکرها
markers = driver.find_elements(
    By.CSS_SELECTOR,
    ".leaflet-marker-icon"
)

print(f"Found {len(markers)} markers")

for i in range(len(markers)):

    try:

        # دوباره گرفتن مارکرها (برای جلوگیری از stale element)
        markers = driver.find_elements(
            By.CSS_SELECTOR,
            ".leaflet-marker-icon"
        )

        driver.execute_script(
            "arguments[0].click();",
            markers[i]
        )

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".leaflet-popup")
            )
        )

        popup = driver.find_element(
            By.CSS_SELECTOR,
            ".leaflet-popup"
        )

        def get_text(selector):
            try:
                return popup.find_element(
                    By.CSS_SELECTOR,
                    selector
                ).text.strip()
            except:
                return ""

        name = get_text(".nameVal")
        agency_type = get_text(".typeVal")

        # چون دو تا typeVal وجود دارد
        type_vals = popup.find_elements(
            By.CSS_SELECTOR,
            ".typeVal"
        )

        postal_code = ""
        if len(type_vals) >= 2:
            postal_code = type_vals[1].text.strip()

        state = get_text(".stateVal")
        city = get_text(".cityVal")
        phone = get_text(".telephoneVal")
        address = get_text(".addressVal")

        results.append({
            "نام نمایندگی": name,
            "نوع": agency_type,
            "کد پستی": postal_code,
            "استان": state,
            "شهر": city,
            "تلفن": phone,
            "آدرس": address
        })

        print(name)

        # بستن popup
        try:
            popup.find_element(
                By.CSS_SELECTOR,
                ".leaflet-popup-close-button"
            ).click()
        except:
            pass

        time.sleep(1)

    except Exception as e:
        print(f"Error marker {i}: {e}")

df = pd.DataFrame(results)

df.to_excel(
    "dekapost_agencies.xlsx",
    index=False
)

driver.quit()

print(f"Saved {len(df)} records")