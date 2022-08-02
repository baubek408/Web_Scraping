import requests
import img2pdf

# Create a function to request
def get_data():
    headers = {

        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"

    }

    img_list = []

    # Gather img urls
    for i in range(1,49,):
        url = f"https://www.recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg"
        req = requests.get(url=url, headers=headers)
        response = req.content

        # Saving them in a media folder
        with open(f"media/{i}.jpg", "wb") as file:
            file.write(response)
            img_list.append(f"media/{i}.jpg")  # Appending each img name in img_list
            print(f"Donwloaded {i} of 48")


    print("#"*20)
    print(img_list)

    #Creat PDF file

    with open("result.pdf", "wb") as f:
        f.write(img2pdf.convert(img_list))
    print("PDF file created successfully!")


def main():
    get_data()

if __name__ == "__main__":
    main()