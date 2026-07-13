from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import os
import time
import random

# ---------- تنظیمات ----------
BASE_URL = "https://www.digikala.com/main/vehicles-spare-parts/"
OUTPUT_CSV = "all_vendors_digikala_vehicles.csv"
MAX_THREADS = 3
# ------------------------------

def create_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


# -------------------------------
# مرحله 1: استخراج دسته‌بندی‌ها
# -------------------------------
driver = create_driver()
wait = WebDriverWait(driver, 20)
driver.get(BASE_URL)
time.sleep(random.uniform(2, 4))

category_links = set()

try:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    links = driver.find_elements(By.TAG_NAME, "a")

    for l in links:
        href = l.get_attribute("href")
        if href and "/search/category-" in href:
            category_links.add(href)

except:
    print("دسته‌بندی پیدا نشد")
    driver.quit()
    exit()

print("تعداد دسته‌بندی:", len(category_links))


# -------------------------------
# مرحله 2: استخراج محصولات
# -------------------------------
all_product_links = set()

for cat in category_links:
    print("ورود به دسته:", cat)
    driver.get(cat)
    time.sleep(random.uniform(2, 4))

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    except:
        continue

    # اسکرول برای lazy load
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 2))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    products = driver.find_elements(By.TAG_NAME, "a")
    for p in products:
        href = p.get_attribute("href")
        if href and "/product/dkp-" in href:
            all_product_links.add(href)

print("تعداد کل محصولات:", len(all_product_links))
driver.quit()


# -------------------------------
# مرحله 3: استخراج لینک فروشنده‌ها
# -------------------------------
driver = create_driver()
wait = WebDriverWait(driver, 15)

all_sellers = set()

for idx, product in enumerate(all_product_links):
    print(f"{idx+1}/{len(all_product_links)} محصول")
    driver.get(product)
    time.sleep(random.uniform(2, 3))

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    except:
        continue

    sellers = driver.find_elements(By.TAG_NAME, "a")
    for s in sellers:
        link = s.get_attribute("href")
        if link and "/seller/" in link:
            all_sellers.add(link)

driver.quit()
print("تعداد فروشنده یکتا:", len(all_sellers))


# -------------------------------
# مرحله 4: استخراج اطلاعات فروشنده
# -------------------------------
def fetch_seller_info(seller_link):
    driver_local = create_driver()
    wait_local = WebDriverWait(driver_local, 15)

    try:
        driver_local.get(seller_link)
        time.sleep(random.uniform(2, 4))

        wait_local.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        shop_title = driver_local.find_element(By.TAG_NAME, "h1").text.strip()

    except:
        shop_title = "یافت نشد"

    driver_local.quit()
    return (shop_title, seller_link)


final_data = []

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(fetch_seller_info, link) for link in all_sellers]

    for future in as_completed(futures):
        result = future.result()
        print("پردازش شد:", result[0])
        final_data.append(result)
        time.sleep(random.uniform(0.5, 1.5))


# -------------------------------
# ذخیره CSV
# -------------------------------
if os.path.exists(OUTPUT_CSV):
    os.remove(OUTPUT_CSV)

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["عنوان فروشگاه", "لینک فروشگاه"])
    writer.writerows(final_data)

print("فایل ساخته شد:", OUTPUT_CSV)
