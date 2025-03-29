import json
import matplotlib.pyplot as plt
import numpy as np
import os

# Завантажуємо результати
with open("data/css_results.json", "r", encoding="utf-8") as f:
    css_data = json.load(f)
with open("data/xpath_results.json", "r", encoding="utf-8") as f:
    xpath_data = json.load(f)
with open("data/bs_results.json", "r", encoding="utf-8") as f:
    bs_data = json.load(f)

# Витягуємо списки часу
css_times = css_data["css_selectors"]
xpath_times = xpath_data["xpath"]
bs_times = bs_data["beautifulsoup"]

# Обчислюємо середні та загальні значення
avg_css = sum(css_times) / len(css_times)
total_css = sum(css_times)
avg_xpath = sum(xpath_times) / len(xpath_times)
total_xpath = sum(xpath_times)
avg_bs = sum(bs_times) / len(bs_times)
total_bs = sum(bs_times)

print(f"CSS-селектори: середній час на сторінку {avg_css:.6f} с, загальний час {total_css:.6f} с")
print(f"XPath: середній час на сторінку {avg_xpath:.6f} с, загальний час {total_xpath:.6f} с")
print(f"BeautifulSoup: середній час на сторінку {avg_bs:.6f} с, загальний час {total_bs:.6f} с")

output_dir = "graphs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

plt.style.use("ggplot")

plt.figure(figsize=(10, 6))
plt.boxplot([css_times, xpath_times, bs_times], 
            tick_labels=["CSS-селектори", "XPath", "BeautifulSoup"],
            patch_artist=True, 
            boxprops=dict(facecolor="lightblue", color="blue"),
            whiskerprops=dict(color="blue"),
            capprops=dict(color="blue"),
            medianprops=dict(color="red"))
plt.title("Час парсингу на сторінку (Boxplot)", fontsize=14, fontweight="bold")
plt.ylabel("Час на сторінку (секунди)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.savefig(os.path.join(output_dir, "boxplot_comparison.png"), dpi=300)
plt.close()

plt.figure(figsize=(10, 6))
plt.hist(css_times, bins=20, alpha=0.7, label="CSS-селектори", color="blue")
plt.hist(xpath_times, bins=20, alpha=0.7, label="XPath", color="green")
plt.hist(bs_times, bins=20, alpha=0.7, label="BeautifulSoup", color="orange")
plt.title("Розподіл часу парсингу на сторінку (Histogram)", fontsize=14, fontweight="bold")
plt.xlabel("Час на сторінку (секунди)", fontsize=12)
plt.ylabel("Частота", fontsize=12)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.savefig(os.path.join(output_dir, "histogram_comparison.png"), dpi=300)
plt.close()

plt.figure(figsize=(10, 6))
for i, times in enumerate([css_times, xpath_times, bs_times]):
    plt.scatter(range(len(times)), times, label=["CSS-селектори", "XPath", "BeautifulSoup"][i], 
                color=["blue", "green", "orange"][i], alpha=0.6)
plt.title("Час парсингу для кожної сторінки (Scatter)", fontsize=14, fontweight="bold")
plt.xlabel("Номер сторінки", fontsize=12)
plt.ylabel("Час на сторінку (секунди)", fontsize=12)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.savefig(os.path.join(output_dir, "scatter_comparison.png"), dpi=300)
plt.close()

plt.figure(figsize=(10, 6))
methods = ["CSS-селектори", "XPath", "BeautifulSoup"]
averages = [avg_css, avg_xpath, avg_bs]
plt.bar(methods, averages, color=["blue", "green", "orange"], edgecolor="black")
plt.title("Середній час парсингу на сторінку (Bar)", fontsize=14, fontweight="bold")
plt.ylabel("Час на сторінку (секунди)", fontsize=12)
for i, v in enumerate(averages):
    plt.text(i, v + 0.0001, f"{v:.6f}", ha="center", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.7, axis="y")
plt.savefig(os.path.join(output_dir, "bar_avg_comparison.png"), dpi=300)
plt.close()

plt.figure(figsize=(10, 6))
methods = ["CSS-селектори", "XPath", "BeautifulSoup"]
totals = [total_css, total_xpath, total_bs]
plt.bar(methods, totals, color=["blue", "green", "orange"], edgecolor="black")
plt.title("Загальний час парсингу 24 сторінок (Bar)", fontsize=14, fontweight="bold")
plt.ylabel("Загальний час (секунди)", fontsize=12)
for i, v in enumerate(totals):
    plt.text(i, v + 0.01, f"{v:.2f}", ha="center", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.7, axis="y")
plt.savefig(os.path.join(output_dir, "bar_total_comparison.png"), dpi=300)
plt.close()

print("Графіки збережено в папці 'graphs':")
print(" - boxplot_comparison.png")
print(" - histogram_comparison.png")
print(" - scatter_comparison.png")
print(" - bar_avg_comparison.png")
print(" - bar_total_comparison.png")