# HW could be to for loop through stocks and return amount of positive/negative rather than words(gives experience with prompt engineering)
import bs4
import requests
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY"))

def request_API(prompt, tokens: bool = True):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=prompt
)

  if tokens:  # Attempt to make a seperate box for token printing
    print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')

  return response.choices[0].message.content.strip()

url='https://finance.yahoo.com/quote/'

output = ''
positives = 0
negatives = 0
stocks = []
headlineLinks = []
allHeadlineLinks = []
allHeadlines = []
headlines = []
articleData = []
allArticleData = []

stock = input("What stock do you want to webscrape?(type end to quit) ")
stocks.append(stock.upper())

while stocks[-1].lower() != 'end':
    stock = input("What stocks do you want to webscrape?(type end to quit) ")
    stocks.append(stock.upper())

for i in range(len(stocks) - 1):
    print('*********************************************************\n\n' + stocks[i], '\n\n*********************************************************')
    soup = bs4.BeautifulSoup(requests.get(url + stocks[i] + '/').text, 'html.parser')
    
    # print(soup)
    
    anchor = soup.find_all('a', attrs={'class':'subtle-link fin-size-small thumb yf-1e4diqp'})
    
    for atrb in anchor:
        headlines.append(atrb['title'])
        headlineLinks.append(atrb['href'])

    # Creating nested list for each stock
    allHeadlineLinks.append(headlineLinks)
    allHeadlines.append(headlines)

# print(headlineLinks)
for stockHeadlines in allHeadlineLinks:
    for link in stockHeadlines:
        output = ''
        article = requests.get(link)
        articleSoup = bs4.BeautifulSoup(article.content, 'html.parser')

        paragraphInfo = articleSoup.select('p', attrs={'class' : 'yf-1pe5jgt'})
        
        for info in paragraphInfo:
            if 'We are experiencing some temporary issues.' in info.getText() or 'Thank you for your patience' in info.getText() or 'Our engineers are' in info.getText():
                continue
            output += info.getText() + ' '

        # shortening output so we don't lose more money
        output = output[0:len(output)//3]
        if len(output) > 555:
            output = output[0:554]
            articleData.append(output)
        if len(output) == 0:
            continue

    allArticleData.append(articleData)

# minus 1 from the len of stocks because of the last element being end
for i in range(len(stocks) - 1):
    for data in allArticleData[i]:
        # print(data)
        sentiment = request_API([{"role": "system", "content": f"You are a stock sentiment analysis bot, return 1 if the following news about {stocks[i]} stock is positive, and 0 if it is negative. ONLY RETURN 0 or 1: {data}."}], False)
        try:
            sentiment = int(sentiment)
        except:
            print("Invalid AI Response, Got a String Instead of Number")

        if sentiment == 1:
            positives += 1
        elif sentiment == 0:
            negatives += 1
        else:
            print("Invalid AI Response, Got a Number Other Than 0 or 1")

    print(f"{stocks[i]} had {positives} positive articles, and {negatives} negative articles.")
    positives = 0
    negatives = 0
