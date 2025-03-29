import requests
import os

base_url = "https://www.scrapethissite.com/pages/forms/?page_num="
output_dir = "pages"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for page_num in range(1, 25):
    url = f"{base_url}{page_num}"
    response = requests.get(url)
    file_path = os.path.join(output_dir, f"page_{page_num}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Збережено {file_path}")

print("Усі сторінки завантажено!")