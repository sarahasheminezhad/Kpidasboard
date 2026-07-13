from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

URL = "https://tipaxco.com/branches/standardpoint"

driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 20)

driver.get(URL)

data = []

# صبر برای بارگذاری اولیه
wait.until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, "nameAgency")
    )
)

# تعداد استان‌ها
state_count = len(
    driver.find_elements(
        By.CSS_SELECTOR,
        "span.nameAgency"
    )
)

print(f"States found: {state_count}")

for state_idx in range(state_count):

    try:

        # دوباره گرفتن استان‌ها
        states = driver.find_elements(
            By.CSS_SELECTOR,
            "span.nameAgency"
        )

        state_name = states[state_idx].text.strip()

        print(f"\n===== {state_name} =====")

        # کلیک روی استان
        driver.execute_script(
            "arguments[0].closest('a').click();",
            states[state_idx]
        )

        time.sleep(2)

        # گرفتن شهرها
        cities = driver.find_elements(
            By.CSS_SELECTOR,
            "input[name*='_rptCity'][type='button']"
        )

        city_count = len(cities)

        print(f"Cities: {city_count}")

        for city_idx in range(city_count):

            try:

                cities = driver.find_elements(
                    By.CSS_SELECTOR,
                    "input[name*='_rptCity'][type='button']"
                )

                city_name = cities[city_idx].get_attribute("value")

                print(f"   City: {city_name}")

                driver.execute_script(
                    "arguments[0].click();",
                    cities[city_idx]
                )

                time.sleep(2)

                agencies = driver.find_elements(
                    By.CSS_SELECTOR,
                    "input[name*='_reptAgency'][type='button']"
                )

                agency_count = len(agencies)

                print(f"      Agencies: {agency_count}")

                for agency_idx in range(agency_count):

                    try:

                        agencies = driver.find_elements(
                            By.CSS_SELECTOR,
                            "input[name*='_reptAgency'][type='button']"
                        )

                        agency_name = agencies[agency_idx].get_attribute(
                            "value"
                        )

                        print(
                            f"         Agency: {agency_name}"
                        )

                        driver.execute_script(
                            "arguments[0].click();",
                            agencies[agency_idx]
                        )

                        # منتظر ظاهر شدن اطلاعات
                        wait.until(
                            EC.presence_of_element_located(
                                (By.ID, "_dvAgencyDetail")
                            )
                        )

                        time.sleep(1)

                        # نام کامل
                        try:
                            branch_name = driver.find_element(
                                By.XPATH,
                                "//*[contains(@id,'lblAgencyName')]"
                            ).text.strip()
                        except:
                            branch_name = ""

                        # کد نمایندگی
                        try:
                            branch_code = driver.find_element(
                                By.CLASS_NAME,
                                "BranchCodeAgency"
                            ).text.strip()
                        except:
                            branch_code = ""

                        # مدیر
                        try:
                            manager_name = driver.find_element(
                                By.CLASS_NAME,
                                "ManagerNameAgency"
                            ).text.strip()
                        except:
                            manager_name = ""

                        # نوع
                        try:
                            branch_type = driver.find_element(
                                By.CLASS_NAME,
                                "BranchTypeAgency"
                            ).text.strip()
                        except:
                            branch_type = ""

                        # کد پستی
                        try:
                            postal_code = driver.find_element(
                                By.CLASS_NAME,
                                "PostalCodeAgency"
                            ).text.strip()
                        except:
                            postal_code = ""

                        # آدرس
                        try:
                            address = driver.find_element(
                                By.XPATH,
                                "//*[contains(@id,'lblAdress')]"
                            ).text.strip()
                        except:
                            address = ""

                        # تلفن‌ها
                        try:
                            phones = driver.find_elements(
                                By.CLASS_NAME,
                                "phoneAgency"
                            )

                            phones_text = " | ".join(
                                [
                                    p.text.strip()
                                    for p in phones
                                    if p.text.strip()
                                ]
                            )
                        except:
                            phones_text = ""

                        # لینک
                        try:
                            detail_link = driver.find_element(
                                By.XPATH,
                                "//*[contains(@id,'hlAgencyDetail')]"
                            ).get_attribute("href")
                        except:
                            detail_link = ""

                        data.append({
                            "استان": state_name,
                            "شهر": city_name,
                            "نمایندگی": agency_name,
                            "نام کامل": branch_name,
                            "کد نمایندگی": branch_code,
                            "مدیر": manager_name,
                            "نوع": branch_type,
                            "کد پستی": postal_code,
                            "تلفن": phones_text,
                            "آدرس": address,
                            "لینک": detail_link
                        })

                    except Exception as e:
                        print(
                            f"Agency Error ({agency_name}): {e}"
                        )

            except Exception as e:
                print(
                    f"City Error ({city_name}): {e}"
                )

    except Exception as e:
        print(
            f"State Error ({state_idx}): {e}"
        )

# ذخیره خروجی
df = pd.DataFrame(data)

df.to_excel(
    "tipax_agencies.xlsx",
    index=False
)

print(
    f"\nFinished. {len(df)} rows saved."
)

driver.quit()