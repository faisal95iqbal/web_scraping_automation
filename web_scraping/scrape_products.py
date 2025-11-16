import requests
from bs4 import BeautifulSoup
import csv
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://scrapeme.live/shop/"

def scrape_products():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()  # stop if the site is unreachable

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("li.product")

    data = []

    for item in products:
        title = item.select_one("h2").get_text(strip=True)
        price = item.select_one("span.price").get_text(strip=True)

        data.append({"title": title, "price": price})
        print(f"{title} → {price}")

    # Save to CSV
    with open("products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price"])
        writer.writeheader()
        writer.writerows(data)

    print("\nSaved products.csv successfully!")

scrape_products()
