import requests
import time
import psutil
from parsel import Selector
from lxml import html
from bs4 import BeautifulSoup
import json

url = "https://www.cia.gov/the-world-factbook/countries/ukraine/"

response = requests.get(url)
html_content = response.text

def scrape_with_css(html_content):
    selector = Selector(text=html_content)
    sections = selector.css("h2.section-h2::text").getall()
    contents = selector.css("div.wfb-text-box > p::text").getall()
    return list(zip(sections, contents[:len(sections)]))  # Обмежуємо вміст кількістю секцій

def scrape_with_xpath(html_content):
    tree = html.fromstring(html_content)
    sections = tree.xpath("//h2[contains(@class, 'section-h2')]/text()")
    contents = tree.xpath("//div[contains(@class, 'wfb-text-box')]/p/text()")
    return list(zip(sections, contents[:len(sections)]))  # Обмежуємо вміст кількістю секцій

def scrape_with_bs4(html_content):
    soup = BeautifulSoup(html_content, "lxml")  # Використовуємо lxml для швидкості
    sections = soup.find_all("h2", class_="section-h2")
    contents = soup.find_all("div", class_="wfb-text-box")
    results = []
    for section, content in zip(sections, contents):
        section_title = section.text.strip()
        content_text = content.find("p").text.strip() if content.find("p") else ""
        results.append((section_title, content_text))
    return results

def measure_performance(scrape_func, html_content):
    cpu_before = psutil.cpu_percent(interval=None)
    mem_before = psutil.Process().memory_info().rss / (1024 * 1024)  # у МБ

    start_time = time.time()
    scrape_func(html_content)
    end_time = time.time()

    cpu_after = psutil.cpu_percent(interval=None)
    mem_after = psutil.Process().memory_info().rss / (1024 * 1024)  # у МБ

    execution_time = end_time - start_time
    cpu_usage = (cpu_before + cpu_after) / 2
    mem_usage = mem_after - mem_before

    return execution_time, cpu_usage, mem_usage

methods = {
    "CSS-селектори (Parsel)": scrape_with_css,  # Додаємо "(Parsel)" для чіткості
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

# Виведення середніх значень
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
with open('scraper_performance_nested.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("\nРезультати збережено у файл 'scraper_performance.json'")