from lxml import etree
import time
import json
import os

# Шлях до папки зі сторінками
pages_dir = "pages"
times = []

# Обробляємо всі сторінки
for page_num in range(1, 25):
    file_path = os.path.join(pages_dir, f"page_{page_num}.html")
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    tree = etree.HTML(html)

    start_time = time.perf_counter()
    rows = tree.xpath("//table/tr")[1:]
    data = [(row.xpath("./td[1]/text()")[0].strip(),
             row.xpath("./td[2]/text()")[0].strip(),
             row.xpath("./td[3]/text()")[0].strip(),
             row.xpath("./td[4]/text()")[0].strip()) for row in rows]
    end_time = time.perf_counter()
    times.append(end_time - start_time)

# Збереження результатів
with open("data/xpath_results.json", "w", encoding="utf-8") as f:
    json.dump({"xpath": times}, f, indent=4)

avg_time = sum(times) / len(times)
total_time = sum(times)
print(f"XPath: середній час на сторінку {avg_time:.6f} секунд, загальний час {total_time:.6f} секунд, {len(data) * 24} рядків")