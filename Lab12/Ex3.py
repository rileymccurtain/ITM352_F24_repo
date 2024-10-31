# Parse a website to extract specific contents using BeautifulSoup
from bs4 import BeautifulSoup
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://shidler.hawaii.edu/itm/people"

print(f"Opening {url}...")
itm_html = urllib.request.urlopen(url)
html_to_parse = BeautifulSoup(itm_html, "html.parser")
pretty_html = html_to_parse.prettify()

lines = pretty_html.splitlines()
lines_to_print = 10

#Print the first few lines
for line in lines[:lines_to_print]:
    print(line)

# Find just the people in the ITM page
list_of_people = html_to_parse.find_all('h2', class_="title")

# Create a list of the people found
itm_people = []
for element in list_of_people:
    itm_people.append(element.text)
    print(element.text)

print("Number of ITM faculty: ", len(itm_people))