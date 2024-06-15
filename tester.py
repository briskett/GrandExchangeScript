import requests

url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=8&alpha=e&page=1"
response = requests.get(url)

print("Response status code:", response.status_code)
print("Response headers:", response.headers)
print("Response content:", response.text)
