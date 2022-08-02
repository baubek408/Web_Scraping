import time

from bs4 import BeautifulSoup
import os
import requests
import lxml
url = "https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/"
def get_all_pages():

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"

    }
    # r = requests.get(url=url, headers=headers)
    # if not os.path.exists("data"):
    #     os.mkdir("data")
    #
    # with open("data/page_1.html", "w") as f:
    #     f.write(r.text)
    #
    with open(f"data/page_1.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    pages_count = int(soup.find("div", class_="bx-pagination-container").find_all("a")[-2].text)
    print(pages_count)

    for i in range(1, pages_count + 1):
        url = f"https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}"
        r = requests.get(url=url, headers=headers)

        with open(f"data/page_{i}.html", "w") as file:
            file.write(r.text)

        time.sleep(2)
    return pages_count + 1

def collect_data(pages_count):

    for page in range(1, pages_count):
        with open(f"data/page_{page}.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        



def main():
    pages_count = get_all_pages()

if __name__ == '__main__':
    main()