import requests
from bs4 import BeautifulSoup

# Make a request to the website
url = "https://en.wiktionary.org/wiki/Appendix:Arabic_Frequency_List_from_Quran/Arabic_Frequency_List_from_Quran_1-1000"
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find the desired data using CSS selectors or search methods
data = soup.select('#element_id')

# Extract the information you want from the data
for item in data:
    print(item.text)
