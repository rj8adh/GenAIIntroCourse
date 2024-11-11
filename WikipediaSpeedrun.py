# TODO Fix bug where script randomly redirects to arabic wikipedia

import bs4
import requests
from openai import OpenAI
import os

BASE_URL = 'https://en.wikipedia.org/wiki'

def request_API(prompt, tokens: bool = True):

    client = OpenAI(api_key=os.getenv("API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt
)

    if tokens:  # Attempt to make a seperate box for token printing
        print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')

    return response.choices[0].message.content.strip()

def scrapeWikipedia(url: str):
    print(url)
    soup = bs4.BeautifulSoup(requests.get(url).content, 'html.parser')
    # print(soup)

    output = {}
    try:
        # Delete all hidden categories(used find because there's only one instance of this class on each webpage)
        hidden_elements = soup.find('div', class_='mw-hidden-catlinks mw-hidden-cats-hidden')
        hidden_elements.decompose()
    except:
        pass
    
    try:
        # Delete all text hidden behind a button(counts as a click in speedruns so we don't want it)
        hidden_elements = soup.select('tr', style='display: none;')

        for element in hidden_elements:
            element.decompose()
    except:
        pass

    page_info = soup.select('a')
    # print(page_info)

    # Loop through all of the page's anchor tags
    for info in page_info:
        # Placeholder so we don't lose a ton of money testing
        if len(output) <= 10:
            # Ignores the text that doesn't have a title
            try:
                # Adds the title & link after splitting irrelevant stuff and stripping whitespaces
                output[info['title'].split(':')[1].strip()] = info['href']
            except:
                continue
        else:
            break
    return output
# print(scrapeWikipedia("https://en.wikipedia.org/wiki/Minecraft"))


def includedIn(item: str, dictionary: dict):

    for value in dictionary:
        if item == dictionary[value]:
            return True
    return False
# print(includedIn("https://en.wikipedia.org/wiki/Category:Nintendo_Network_games", scrapeWikipedia("https://en.wikipedia.org/wiki/Minecraft")))


path = {}
currentBest = ''
win = False
attempts = 0

currentBest = ''
currentUrl = BASE_URL + "/" + input("Enter starting page ")
endName = input("Enter ending page ")
endLink = BASE_URL + "/" + endName

currentInfo = scrapeWikipedia(currentUrl)
print(currentInfo)
# Check if the end link is on the current page
while (not includedIn(endLink, currentInfo)) and attempts < 11:
    for value in currentInfo:
        if not currentBest:
            print("CURRENT LINK IS: " + currentInfo[value])
            currentBest = value

            if attempts != 0:
                currentUrl = "https://en.wikipedia.org" + currentInfo[value]

        else:
            if 0 == request_API([{"role": "system", "content": f"Return the number 1 if the word: \"{currentBest}\", is more related to the word(s): \"{endName}\", than the word(s) \"{value}\", and return 0 if this is false."}]):
                currentBest = value
                currentUrl = "https://en.wikipedia.org" + currentInfo[value]

    print(f"Current Best: {currentBest}, Link: {currentUrl}")
    currentInfo = scrapeWikipedia(currentUrl)
    currentBest = ''
    attempts += 1


        
        

# Feed to ai

# Follow links

# Feed to ai, repeat

# Test Speedrun Links
# https://en.wikipedia.org/wiki/Minecraft
# https://en.wikipedia.org/wiki/Skibidi_Toilet