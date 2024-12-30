# Looks to be working consistently, need further testing before implementing in wikipedia speedrun script

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY"))

def request_API(prompt, tokens: bool = True):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=.5
)

    if tokens:  # Attempt to make a seperate box for token printing
        print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')

    return response.choices[0].message.content.strip()

print(request_API([{"role": "system", "content": f"In one word(only letters), is the question: \"how many letters is the word\" a binary question? It MUST have a DEFINITIVE yes or no reply to be a binary question."}], False))

