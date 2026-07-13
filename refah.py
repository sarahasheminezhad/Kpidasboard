from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

URL = "https://cardinfo.ir/بانک/جستجو"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

results = []

# -----------------------------
# گرفتن لیست شهرها فقط یک بار
# -----------------------------
driver.get(URL)

# باز کردن لیست شهر
wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#town_name + .ss-main")
    )
).click()

wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".ss-list .ss-option")
    )
)

city_elements = driver.find_elements(
    By.CSS_SELECTOR,
    ".ss-list .ss-option"
)

cities = []

for c in city_elements:
    txt = c.text.strip()
    if txt != "":
        cities.append(txt)

print("تعداد شهرها:", len(cities))

# -----------------------------
# پیمایش شهرها
# -----------------------------
for city in cities:

    try:

        print("=" * 40)
        print(city)

        # هر بار صفحه را از نو باز کن
        driver.get(URL)

        # -----------------
        # انتخاب بانک
        # -----------------
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#bank_name + .ss-main")
            )
        ).click()

        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".ss-list .ss-option")
            )
        )

        banks = driver.find_elements(
            By.CSS_SELECTOR,
            ".ss-list .ss-option"
        )

        for b in banks:
            if b.text.strip() == "بانک رفاه کارگران":
                b.click()
                break

        time.sleep(1)

        # -----------------
        # انتخاب شهر
        # -----------------
        driver.find_element(
            By.CSS_SELECTOR,
            "#town_name + .ss-main"
        ).click()

        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".ss-list .ss-option")
            )
        )

        options = driver.find_elements(
            By.CSS_SELECTOR,
            ".ss-list .ss-option"
        )

        found = False

        for op in options:
            if op.text.strip() == city:
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    op
                )
                time.sleep(0.3)
                op.click()
                found = True
                break

        if not found:
            print("شهر پیدا نشد")
            continue

        time.sleep(1)

        # -----------------
        # جستجو
        # -----------------
        driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        ).click()

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table tbody")
            )
        )

        rows = driver.find_elements(
            By.CSS_SELECTOR,
            "table tbody tr"
        )

        i = 0

        while i < len(rows):

            rows = driver.find_elements(
                By.CSS_SELECTOR,
                "table tbody tr"
            )

            if i >= len(rows):
                break

            cols = rows[i].find_elements(By.TAG_NAME, "td")

            if len(cols) >= 3:

                branch = cols[0].text.strip()
                code = cols[1].text.strip()
                phone = cols[2].text.strip()

                address = ""

                if i + 1 < len(rows):

                    addr_cols = rows[i + 1].find_elements(
                        By.TAG_NAME,
                        "td"
                    )

                    if len(addr_cols) == 1:
                        address = addr_cols[0].text.strip()

                results.append({
                    "شهر": city,
                    "نام شعبه": branch,
                    "کد": code,
                    "تلفن": phone,
                    "آدرس": address
                })

            i += 2

        print("ثبت شد")

    except Exception as e:
        print("خطا:", e)

# -----------------------------
# ذخیره
# -----------------------------
df = pd.DataFrame(results)

df.to_excel(
    "BankRefahBranches.xlsx",
    index=False
)

driver.quit()

print("=" * 40)
print("پایان عملیات")
print("تعداد رکوردها:", len(df))
print("فایل ذخیره شد: BankRefahBranches.xlsx")