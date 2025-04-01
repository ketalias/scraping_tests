import json
import matplotlib.pyplot as plt

# Назви файлів (змініть, якщо у вас інші назви)
json_files = [
    'scraper_performance_simple.json',  # Наприклад, для news.ycombinator.com
    'scraper_performance_nested.json',  # Наприклад, для nyc.gov
    'scraper_performance_nontype.json'   # Наприклад, для cia.gov
]

# Назви сайтів для легенди
site_names = [
    'Hacker News',
    'NYC Buildings',
    'CIA World Factbook'
]

# Методи, які ми порівнюємо
methods = ['XPath', 'CSS-селектори (Parsel)', 'BeautifulSoup']

# Збираємо дані з JSON-файлів
data = {'execution_time': [], 'cpu_usage': [], 'memory_change': []}
for file in json_files:
    with open(file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        exec_times = [json_data[method]['averages']['avg_execution_time'] for method in methods]
        cpu_usages = [json_data[method]['averages']['avg_cpu_usage'] for method in methods]
        mem_changes = [json_data[method]['averages']['avg_memory_change'] for method in methods]
        data['execution_time'].append(exec_times)
        data['cpu_usage'].append(cpu_usages)
        data['memory_change'].append(mem_changes)

# Налаштування графіків
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

# Функція для побудови стовпчиків
def plot_bars(ax, data, ylabel, title):
    bar_width = 0.25
    x = range(len(methods))
    for i, site_data in enumerate(data):
        ax.bar([pos + bar_width * i for pos in x], site_data, bar_width, label=site_names[i])
    ax.set_xticks([pos + bar_width for pos in x])
    ax.set_xticklabels(methods)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()

# Графік 1: Час виконання
plot_bars(ax1, data['execution_time'], 'Час (секунди)', 'Середній час виконання')

# Графік 2: Використання CPU
plot_bars(ax2, data['cpu_usage'], 'CPU (%)', 'Середнє використання CPU')

# Графік 3: Зміна пам’яті
plot_bars(ax3, data['memory_change'], 'Пам’ять (МБ)', 'Середня зміна пам’яті')

# Налаштування відображення
plt.tight_layout()
plt.show()