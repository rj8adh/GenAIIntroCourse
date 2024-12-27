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

print(request_API([{"role": "system", "content": f"Can the following question be answered with a boolean response: \"how many letters does the work have\". If the question CAN'T be answered with a boolean, return 0. If the question CAN be answered with a boolean, return 1. ONLY RETURN 1 or 0, NO LETTERS"}], False))

