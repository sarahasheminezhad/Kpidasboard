import requests
from openpyxl import Workbook

BASE_API = "https://pl.snapp.ir/api/v1/products"
CATEGORY = "TOOLS"

page = 1
all_names = []

while True:
    params = {
        "category": CATEGORY,
        "page": page
    }

    response = requests.get(BASE_API, params=params)
    if response.status_code != 200:
        print("خطا در دریافت داده")
        break

    data = response.json()

    products = data.get("data", [])
    if not products:
        break

    for product in products:
        name = product.get("title")
        if name:
            all_names.append(name)

    print(f"صفحه {page} خوانده شد")
    page += 1

print("تعداد کل محصولات:", len(all_names))

# ذخیره در اکسل
wb = Workbook()
ws = wb.active
ws.title = "Products"
ws.append(["Name"])

for name in all_names:
    ws.append([name])

wb.save("snapp_tools.xlsx")

print("فایل ساخته شد: snapp_tools.xlsx")
