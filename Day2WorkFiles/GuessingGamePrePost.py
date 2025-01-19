"""
Precondition: Required Libraries are imported, variables are instantiated, and request_API is defined

Postcondition: Create a guessing game where the AI attempts to guess a word that the user has given.
NOTE: I'd recommend asking the user if the AI guessed the answer correct, rather than check if the AI reponse is an exact match

Algorithm: 
          Write a loop that iterates 20 times
          Provide the message history so far and ask the AI to give a yes or no question to ask the user
          On the last guess, ask the AI to make a final guess based on the message history
          Print how many guesses it took the AI(print win message if the AI failed)
"""


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

history = []
user_word = input("Enter word for AI to try and guess: ")