from requests_html import HTMLSession
import chompjs
import itertools
import pandas as pd


def fetch(x):
    baseurl = "https://www.rei.com"
    r = s.get(f"https://www.rei.com/c/hiking-backpacks?page={x}")
    results = [baseurl + link.attrs['href'] for link in r.html.find("#search-results > ul > li > a ")]
    return list(dict.fromkeys(results))

def parse_product(url):
    r = s.get(url)
    details = r.html.find('script[type="application/ld+json"]', first=True)
    data = chompjs.parse_js_object(details.text)
    return data

def main():
    urls = [fetch(x) for x in range(1, 3)]  # Fetching only 2 first pages
    products = list(itertools.chain.from_iterable(urls))  # Getting products info from each links
    return [parse_product(url) for url in products]  # Calling method parse_product

if __name__ == '__main__':
    s = HTMLSession()
    df = pd.json_normalize(main())
    df.to_csv('rei_bacpacks.csv', index=False)
    print("Finished.")

