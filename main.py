import pandas as pd
from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
import os


product_details = []
urls = []

for i in range(1, 14):
    urls.append(f'https://www.amazon.com/s?k=mini+pc&i=computers&rh=n%3A565098%2Cp_n_feature_twenty-eight_browse-bin%3A23724149011&dc&page={i}&qid=1661168056&rnid=23724143011&sprefix=mini+%2Caps%2C174&ref=sr_pg_{i}')

### GET WEB PAGE HTML BY PLAYRIGHT
def get_page_htmls():
    index = 0
    for url in urls:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto(url)
            page.is_visible('div.id-search')
            html = page.inner_html('#a-page')
        index += 1

### SAVE FILES IN "HTML" FORMAT FOR SAVE ACCESS
        if not os.path.exists("data"):
            os.mkdir("data")
        with open(f'data/amazon_web_page_{index}.html', 'w') as file:
            file.write(html)

### SAVE EACH CARDS URL
def get_cards_url():
    container_links = []
    for i in range(1, 14):

        with open(f'data/amazon_web_page_{i}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        cards = soup.find_all(class_='s-card-container')


    for card in cards:
        container_links.append('https://www.amazon.com' + card.find('a', href=True)['href'])
    return container_links

### SAVE EACH CARDS HTML PAGES
def get_items(links):
    index = 0
    for link in links:
        index += 1
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()
            page.goto(link)
            page.is_visible('div.id-dp')
            # page.click('#poToggleButton')
            html = page.inner_html('#ppd')


            if not os.path.exists("data/cards"):
                os.mkdir("data/cards")
            with open(f'data/cards/card_{index}.html', 'w') as file:
                file.write(html)
            page.close()
        print(f"Saved {index} card")
    return print("All cards html pages successfully saved!")

### GRABE ALL ITEMS DETAIL
def get_card_data():
    for i in range(1, 328):
        with open(f'data/cards/card_{i}.html') as file:
            card_link = file.read()
        soup = BeautifulSoup(card_link, 'lxml')
        try:
            info = soup.find("table", class_="a-normal a-spacing-micro")
            title = info.find(text=re.compile("Brand")).findNext().text.strip()
        except:
            title = soup.find('h1').find(id='productTitle').text.strip()

        try:
            price = soup.find(id="tp_price_block_total_price_ww").find(class_="a-offscreen").text
        except:
            price = 0

        try:
            operating_system = info.find(text=re.compile("Operating System")).findNext().text.strip()
        except:
            operating_system = None

        try:
            ram_memory = info.find(text=re.compile("Ram Memory Installed Size")).findNext().text.strip()
        except:
            ram_memory = None

        try:
            cpu_model = info.find(text=re.compile("CPU Model")).findNext().text.strip()
        except:
            cpu_model = None

        try:
            cpu_speed = info.find(text=re.compile("CPU Speed")).findNext().text.strip()
        except:
            cpu_model = None



        items = {
                    "title": title,
                    "operating_system": operating_system,
                    "ram_memory": ram_memory,
                    "cpu_model": cpu_model,
                    "cpu_speed": cpu_speed,
                    "price": price
                }
        product_details.append(items)
    return product_details

### SAVE IN DATAFRAME AND CSV FILE
def save_df(item_list):
    df = pd.DataFrame(item_list)
    df.to_csv('mini_pc.csv', index=False)
    return print('Complete.')

def main():
    get_page_htmls()
    get_items(get_cards_url())
    save_df(get_card_data())

if __name__ == "__main__":
    main()
