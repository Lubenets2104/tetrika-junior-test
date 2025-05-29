import requests
from bs4 import BeautifulSoup
from collections import Counter
import csv
import time

BASE_URL = "https://ru.wikipedia.org"
START_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"

def get_animals_count_by_letter():
    current_url = START_URL
    counts = Counter()

    while current_url:
        print("Обрабатываем страницу:", current_url)
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, "html.parser")

        category_div = soup.find("div", {"id": "mw-pages"})
        if not category_div:
            break

        links = category_div.find_all("a")
        for link in links:
            title = link.text.strip()
            if title and title[0].isalpha() and title[0].isupper():
                counts[title[0]] += 1

        next_page_link = soup.find("a", text="Следующая страница")
        if next_page_link:
            current_url = BASE_URL + next_page_link["href"]
            time.sleep(0.5)  # чтобы не спамить
        else:
            current_url = None

    return counts

def save_counts_to_csv(counts, filename="beasts.csv"):
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for letter, count in sorted(counts.items()):
            writer.writerow([letter, count])

if __name__ == "__main__":
    counts = get_animals_count_by_letter()
    save_counts_to_csv(counts)
    print("Готово! Данные записаны в beasts.csv")
