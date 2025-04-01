import requests
import time
import psutil
from parsel import Selector
from lxml import html
from bs4 import BeautifulSoup
import json

url = "https://news.ycombinator.com"

response = requests.get(url)
html_content = response.text

def scrape_with_css(html_content):
    selector = Selector(text=html_content)
    titles = selector.css('.athing .storylink::text').getall()
    links = selector.css('.athing .storylink::attr(href)').getall()
    return list(zip(titles, links))

def scrape_with_xpath(html_content):
    tree = html.fromstring(html_content)
    titles = tree.xpath("//tr[@class='athing']//a[@class='storylink']/text()")
    links = tree.xpath("//tr[@class='athing']//a[@class='storylink']/@href")
    return list(zip(titles, links))

def scrape_with_bs4(html_content):
    soup = BeautifulSoup(html_content, 'lxml')  # Залишаємо lxml як парсер для швидкості
    stories = soup.find_all('tr', class_='athing')
    results = []
    for story in stories:
        link_element = story.find('a', class_='storylink')
        if link_element:
            title = link_element.get_text()
            link = link_element['href']
            results.append((title, link))
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
    "XPath": scrape_with_xpath,
    "CSS-селектори (Parsel)": scrape_with_css,
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
with open('scraper_performance_simple.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("\nРезультати збережено у файл 'scraper_performance.json'")