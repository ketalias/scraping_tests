from bs4 import BeautifulSoup
import time
import json
import os

pages_dir = "pages"
times = []

for page_num in range(1, 25):
    file_path = os.path.join(pages_dir, f"page_{page_num}.html")
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    start_time = time.perf_counter()
    rows = soup.find("table").find_all("tr")[1:]
    data = [(row.find_all("td")[0].text.strip(),
             row.find_all("td")[1].text.strip(),
             row.find_all("td")[2].text.strip(),
             row.find_all("td")[3].text.strip()) for row in rows]
    end_time = time.perf_counter()
    times.append(end_time - start_time)

with open("data/bs_results.json", "w", encoding="utf-8") as f:
    json.dump({"beautifulsoup": times}, f, indent=4)

avg_time = sum(times) / len(times)
total_time = sum(times)
print(f"BeautifulSoup: середній час на сторінку {avg_time:.6f} секунд, загальний час {total_time:.6f} секунд, {len(data) * 24} рядків")