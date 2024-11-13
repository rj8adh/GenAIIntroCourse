# TODO Fix prompt engineering to make results more relevant

import bs4
import requests
from openai import OpenAI
import os

BASE_URL = 'https://en.wikipedia.org'
alphabet = ""

# Not needed in actual assignment, just so I can see how much money im wasting
def updateTokens(numTokens: int):
    
    try:
        with open('promptTokens.txt', 'r') as file:
            content = file.read()
            totalTokens = int(content) if content else 0  # Handle empty file
    except (FileNotFoundError, ValueError):
        totalTokens = 0  # Initialize if the file doesn't exist or contains invalid content

    totalTokens += numTokens

    # Write the updated total back to the file
    with open('promptTokens.txt', 'w') as file:
        file.write(str(totalTokens))

    return totalTokens

def request_API(prompt, tokens: bool = True):
    client = OpenAI(api_key=os.getenv("API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt
)

    if tokens:  # Attempt to make a seperate box for token printing
        print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')
        updateTokens(response.usage.total_tokens)

    return response.choices[0].message.content.strip()

def scrapeWikipedia(url: str):
    print("LINK YOU\'re SCRAPING: " + url)
    soup = bs4.BeautifulSoup(requests.get(url).content, 'html.parser')
    # print(soup)

    output = {}
    textList = []
    try:
        # Delete all hidden categories(used find because there's only one instance of this class on each webpage)
        hidden_elements = soup.find('div', class_='mw-hidden-catlinks mw-hidden-cats-hidden')
        hidden_elements.decompose()
    except:
        pass
    
    try:
        # Delete all junk
        hidden_elements = soup.select('tr', style='display: none;')
        hidden_elements += soup.select('li', class_='interlanguage-link interwiki-nl mw-list-item')
        hidden_elements += soup.select('sup', class_='noprint Inline-Template noprint noexcerpt Template-Fact')

        for element in hidden_elements:
            element.decompose()

    except:
        pass

    page_info = soup.select('a')
    # print(page_info)

    # Loop through all of the page's anchor tags
    for info in page_info:
        # Placeholder so we don't lose a ton of money testing
        if len(output) <= 25:
            # Ignores the text that doesn't have a title
            try:
                # Adds the title & link after splitting irrelevant stuff and stripping whitespaces
                if not 'https://wikimediafoundation.org' in info['href'].split('&')[0]:
                    output[info['title'].split(':')[1].strip()] = info['href'].split('&')[0]
                    textList.append(info['title'].split(':')[1].strip())
            except:
                continue
        else:
            break
    return output, textList
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

currentUrl = BASE_URL + "/wiki/" + input("Enter starting page ")
endName = input("Enter ending page ")
endLink = BASE_URL + "/wiki/" + endName

currentInfo, linkTextList = scrapeWikipedia(currentUrl)
print(currentInfo)
# Check if the end link is on the current page
while (not includedIn(endLink, currentInfo)) and attempts < 11:
    try:
        index = int(request_API([{"role": "system", "content": f"You are a bot trying to end up on the {endName} topic. Choose the most related item to the topic from the following list: {linkTextList}. ONLY RETURN THE INDEX, NO WORDS"}]))
        print("INDEX IS", index)
    except:
        print("Something wrong with chatgpt response, try editing prompt")
        break

    print(currentInfo)
    currentLink = currentInfo[linkTextList[index]]
    print(f"Current Best: {linkTextList[index]}, Link: {BASE_URL + currentLink}")

    if ("https://" in currentLink):
        currentInfo, linkTextList = scrapeWikipedia(currentLink)
    else:
        currentInfo, linkTextList = scrapeWikipedia(BASE_URL + currentLink)


    attempts += 1

        

# Feed to ai

# Follow links

# Feed to ai, repeat

# Test Speedrun Links
# https://en.wikipedia.org/wiki/Minecraft
# https://en.wikipedia.org/wiki/Skibidi_Toilet