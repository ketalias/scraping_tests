import requests
import time
import psutil
from parsel import Selector
from lxml import html
from bs4 import BeautifulSoup
import json

url = "https://www.nyc.gov/site/buildings/index.page"

response = requests.get(url)
html_content = response.text

def scrape_with_css(html_content):
    selector = Selector(text=html_content)
    titles = selector.css("h2::text").getall()
    contents = selector.css("div.content p::text").getall()
    # Обрізаємо contents до довжини titles, щоб уникнути невідповідності
    return list(zip(titles, contents[:len(titles)]))

def scrape_with_xpath(html_content):
    tree = html.fromstring(html_content)
    titles = tree.xpath("//h2/text()")
    contents = tree.xpath("//div[contains(@class, 'content')]//p/text()")
    # Обрізаємо contents до довжини titles
    return list(zip(titles, contents[:len(titles)]))

def scrape_with_bs4(html_content):
    soup = BeautifulSoup(html_content, "lxml")  # Використовуємо lxml для швидкості
    titles = soup.find_all("h2")
    contents = soup.find_all("div", class_="content")
    results = []
    for title, content in zip(titles, contents):
        title_text = title.text.strip()
        content_text = content.find("p").text.strip() if content.find("p") else ""
        results.append((title_text, content_text))
    return results

def measure_performance(scrape_func, html_content):
    cpu_before = psutil.cpu_percent(interval=None)
    mem_before = psutil.Process().memory_info().rss / (1024 * 1024)

    start_time = time.time()
    scrape_func(html_content)
    end_time = time.time()

    cpu_after = psutil.cpu_percent(interval=None)
    mem_after = psutil.Process().memory_info().rss / (1024 * 1024)

    execution_time = end_time - start_time
    cpu_usage = (cpu_before + cpu_after) / 2
    mem_usage = mem_after - mem_before

    return execution_time, cpu_usage, mem_usage

methods = {
    "CSS-селектори (Parsel)": scrape_with_css,
    "XPath": scrape_with_xpath,
    "BeautifulSoup": scrape_with_bs4
}

results = {method: [] for method in methods}
json_data = {}

for method_name, scrape_func in methods.items():
    print(f"\nРезультати для {method_name}:")
    for i in range(3):
        exec_time, cpu, mem = measure_performance(scrape_func, html_content)
        results[method_name].append((exec_time, cpu, mem))
        print(f"  Ітерація {i+1}:")
        print(f"    Час виконання: {exec_time:.4f} секунд")
        print(f"    Використання CPU: {cpu:.2f}%")
        print(f"    Зміна пам’яті: {mem:.2f} МБ")
    
    # Зберігаємо дані для JSON
    json_data[method_name] = {
        "iterations": [
            {
                "execution_time": round(d[0], 4),
                "cpu_usage": round(d[1], 2),
                "memory_change": round(d[2], 2)
            } for d in results[method_name]
        ]
    }

print("\nСередні значення за 3 ітерації:")
for method_name, data in results.items():
    avg_time = sum([d[0] for d in data]) / 3
    avg_cpu = sum([d[1] for d in data]) / 3
    avg_mem = sum([d[2] for d in data]) / 3
    print(f"{method_name}:")
    print(f"  Середній час виконання: {avg_time:.4f} секунд")
    print(f"  Середнє використання CPU: {avg_cpu:.2f}%")
    print(f"  Середня зміна пам’яті: {avg_mem:.2f} МБ")
    
    # Додаємо середні значення в JSON
    json_data[method_name]["averages"] = {
        "avg_execution_time": round(avg_time, 4),
        "avg_cpu_usage": round(avg_cpu, 2),
        "avg_memory_change": round(avg_mem, 2)
    }

# Записуємо результати в JSON файл
with open('scraper_performance_nontype.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("\nРезультати збережено у файл 'scraper_performance.json'")