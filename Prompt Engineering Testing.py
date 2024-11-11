# Looks to be working consistently, need further testing before implementing in wikipedia speedrun script

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

similar = "Minecraft"
word1 = "Blocks"
word2 = "Nintendo"
print(request_API([{"role": "system", "content": f"Return the number 1 if the word: \"{word1}\", is more related to the word: \"{similar}\", than the word \"{word2}\", and return 0 if this is false"}]))