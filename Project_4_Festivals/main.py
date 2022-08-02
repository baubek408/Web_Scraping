from bs4 import BeautifulSoup
import requests
import lxml
import json

headers = {
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
}

domen = "https://www.skiddle.com"


#Collect all Fests URLs

fests_url_list = []


for i in range(0, 120, 24):

    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=18%20May%202022&to_date=&genre%5B%5D=house&genre%5B%5D=trance&genre%5B%5D=hard%20dance&genre%5B%5D=electronic&genre%5B%5D=edm&maxprice=500&o={i}&bannertitle=June"
    r = requests.get(url, headers=headers)
    json_data = json.loads(r.text)
    html_response = json_data["html"]

    with open(f"index_{i}.html", "w") as file:
        file.write(html_response)

    with open(f"index_{i}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all("a", class_="card-details-link")

    for item in cards:
        fest_url = domen + item.get("href")
        fests_url_list.append(fest_url)

#Collect fest info
fest_list_result=[]
count = 0

for url in fests_url_list:

    count +=1
    print(count)
    print(url)
    r = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(r.text, "lxml")
        fest_info_block = soup.find("div", class_="top-info-cont")

        fest_title = fest_info_block.find("h1").text.strip()
        fest_date = fest_info_block.find("h3").text.strip()
        fest_location_url = domen + fest_info_block.find("a", class_="tc-white").get("href")

        # Get contact details and info
        r = requests.get(url=fest_location_url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        contact_details = soup.find("h2", string="Venue contact details and info").find_next()
        items = [item.text for item in contact_details.find_all("p")]

        contact_details_dict = {}
        for contact_detail in items:
            contact_detail_list = contact_detail.split(":")

            if len(contact_detail) == 3:
                contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip() + ":"\
                                                                       + contact_detail_list[2].strip()
            else:
                contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip()

            fest_list_result.append(
                {
                    "Fest name" : fest_title,
                    "Fest date" : fest_date,
                    "Contacts data" : contact_detail_list
                }
            )

    except Exception as ex:
        print(ex)
        print("Damn... There was some error....")

with open("fest_list_result.json", "a", encoding="utf-8") as file:
    json.dump(fest_list_result, file, indent=4,  ensure_ascii=False)

