import lxml.html
import time
import json
import os

pages_dir = "pages"
times = []

for page_num in range(1, 25):
    file_path = os.path.join(pages_dir, f"page_{page_num}.html")
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    tree = lxml.html.fromstring(html)

    start_time = time.perf_counter()
    teams = tree.cssselect("table tr td:nth-child(1)")
    years = tree.cssselect("table tr td:nth-child(2)")
    wins = tree.cssselect("table tr td:nth-child(3)")
    losses = tree.cssselect("table tr td:nth-child(4)")
    data = [(t.text.strip(), y.text.strip(), w.text.strip(), l.text.strip()) 
            for t, y, w, l in zip(teams, years, wins, losses)]
    end_time = time.perf_counter()
    times.append(end_time - start_time)

with open("data/css_results.json", "w", encoding="utf-8") as f:
    json.dump({"css_selectors": times}, f, indent=4)

avg_time = sum(times) / len(times)
total_time = sum(times)
print(f"CSS-селектори: середній час на сторінку {avg_time:.6f} секунд, загальний час {total_time:.6f} секунд, {len(data) * 24} рядків")