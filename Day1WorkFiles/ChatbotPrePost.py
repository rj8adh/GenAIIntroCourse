"""
Precondition: Required Libraries are imported, variables are instantiated, and request_API is defined(explained in class)

Postcondition: Create an infinite ai chatbot WITH HISTORY that stops when the user types end

Algorithm: 
          Initialize an empty list called history
          Create an infinite loop
          Create a variable that gets user input
          Create a variable that gets ChatGPT's response to the the user input. (We will explain how to do this)
          Print the AI's response
          Add the user message and ai response to history
"""


from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY"))
history = []

def request_API(prompt, tokens: bool = True):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=prompt
)

  if tokens:  # Attempt to make a seperate box for token printing
    print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')

  return response.choices[0].message.content.strip()

  print("Hey there, welcome to the chatgpt chatbot")

  #Code Here
