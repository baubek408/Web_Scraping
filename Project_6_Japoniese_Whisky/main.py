import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.thewhiskyexchange.com/c/35/japanese-whisky"
baseurl = "https://www.thewhiskyexchange.com"
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15"
}

whisky_links = []
def get_data():
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    items = soup.find("div", class_="product-grid").find_all(class_="product-grid__item")

    whisky_links = [baseurl + item.find("a").get("href") for item in items]
    return whisky_links


whisky_list = []

def main():
    for link in get_data():
        r = requests.get(url=link, headers=headers).content
        soup = BeautifulSoup(r, "lxml")

        name = soup.find("h1", class_="product-main__name").text.strip()
        price = soup.find("p", class_="product-action__price").text.strip()
        try:
            rating = " ".join(soup.find("div", class_="review-overview").text.split())
        except:
            rating = 'No rating'

        whisky = {
            "name": name,
            "rating": rating,
            "price": price
        }

        whisky_list.append(whisky)

    df = pd.DataFrame(whisky_list)
    print(df.head())

if __name__ == '__main__':
    main()

