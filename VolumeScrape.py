import requests
from bs4 import BeautifulSoup


url = "https://runescape.wiki/w/Zarosian_insignia"
response = requests.get(url)

if response.status_code == 200:
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with attribute data-attr-param="volume"
    elements = soup.find_all(attrs={"data-attr-param": "volume"})

    # Print the text content of each found element
    for element in elements:
        print(element.text)

