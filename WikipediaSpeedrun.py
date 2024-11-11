import bs4
import requests
from openai import OpenAI
import os

def scrapeWikipedia(url: str):
    soup = bs4.BeautifulSoup(requests.get(url).content, 'html.parser')
    # print(soup)

    output = {}

    # Delete all hidden categories(used find because there's only one instance of this class on each webpage)
    hidden_elements = soup.find('div', class_='mw-hidden-catlinks mw-hidden-cats-hidden')
    hidden_elements.decompose()

    # Delete all text hidden behind a button(counts as a click in speedruns so we don't want it)
    hidden_elements = soup.select('tr', style='display: none;')

    for element in hidden_elements:
        element.decompose()

    page_info = soup.select('a')
    # print(page_info)

    # Loop through all of the page's anchor tags
    for info in page_info:
        # Ignores the text that doesn't have a title
        try:
            # Adds the title & link after splitting irrelevant stuff and stripping whitespaces
            output[info['title'].split(':')[1].strip()] = info['href']
        except:
            continue
    return output
# print(scrapeWikipedia("https://en.wikipedia.org/wiki/Minecraft"))


def includedIn(item: str, dictionary: dict):

    BASE_URL = 'https://en.wikipedia.org'

    for value in dictionary:
        if item == BASE_URL + dictionary[value]:
            return True
# print(includedIn("https://en.wikipedia.org/wiki/Category:Nintendo_Network_games", scrapeWikipedia("https://en.wikipedia.org/wiki/Minecraft")))

path = {}
currentBest = ''
win = False

client = OpenAI(api_key=os.getenv("API_KEY"))

currentUrl = input("Enter starting link")
end = input("Enter ending link")

currentInfo = scrapeWikipedia(currentUrl)

# Check if the end link is on the current page
while not includedIn(end, currentInfo):
    for value in currentInfo:
        if not currentBest:
            currentBest = value
        else:
            

print(win)
        
        

# Feed to ai

# Follow links

# Feed to ai, repeat

# Test Speedrun Links
# https://en.wikipedia.org/wiki/Minecraft
# https://en.wikipedia.org/wiki/Skibidi_Toilet