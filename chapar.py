from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.chaparnet.com/agencies"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

driver.get(URL)

time.sleep(3)

all_records = []

# پیدا کردن dropdown استان
province_select = wait.until(
    EC.presence_of_element_located(
        (By.TAG_NAME, "select")
    )
)

select = Select(province_select)

province_count = len(select.options)

print(f"Total Provinces: {province_count}")

for province_index in range(1, province_count):

    try:

        province_select = wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "select")
            )
        )

        select = Select(province_select)

        province_name = (
            select.options[province_index]
            .text
            .strip()
        )

        print(f"\n===== {province_name} =====")

        select.select_by_index(province_index)

        time.sleep(2)

        agencies = driver.find_elements(
            By.CSS_SELECTOR,
            ".agencyItem"
        )

        print(f"Agencies: {len(agencies)}")

        for agency_index in range(len(agencies)):

            try:

                agencies = driver.find_elements(
                    By.CSS_SELECTOR,
                    ".agencyItem"
                )

                agency = agencies[agency_index]

                header = agency.find_element(
                    By.CSS_SELECTOR,
                    ".agencyName"
                )

                driver.execute_script(
                    "arguments[0].click();",
                    header
                )

                time.sleep(0.5)

                agency_name = ""

                try:
                    agency_name = agency.find_element(
                        By.CSS_SELECTOR,
                        ".agencyName h3"
                    ).text.strip()
                except:
                    pass

                city_text = ""

                try:
                    city_text = agency.find_element(
                        By.CSS_SELECTOR,
                        ".agencyLocation"
                    ).text.strip()
                except:
                    pass

                html = agency.find_element(
                    By.CSS_SELECTOR,
                    ".agencyInfoPadd"
                ).get_attribute("innerHTML")

                soup = BeautifulSoup(
                    html,
                    "html.parser"
                )

                record = {
                    "استان انتخابی": province_name,
                    "نام نمایندگی": agency_name,
                    "موقعیت": city_text
                }

                rows = soup.find_all("div")

                for row in rows:

                    span = row.find("span")

                    if not span:
                        continue

                    key = (
                        span.get_text(" ", strip=True)
                        .replace(":", "")
                        .strip()
                    )

                    span.extract()

                    value = row.get_text(
                        " ",
                        strip=True
                    )

                    if key:
                        record[key] = value

                all_records.append(record)

                print(agency_name)

            except Exception as e:

                print(
                    f"Agency Error: {e}"
                )

    except Exception as e:

        print(
            f"Province Error: {e}"
        )

driver.quit()

df = pd.DataFrame(all_records)

df.to_excel(
    "chapar_agencies.xlsx",
    index=False
)

print(
    f"\nFinished. Saved {len(df)} records."
)