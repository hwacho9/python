import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"
get_url = requests.get(url)

soup = BeautifulSoup(get_url.text, "html.parser")

raw_data = soup.find_all("td")

result = []
for val in raw_data:
    result.append(val.string)
print(result)
