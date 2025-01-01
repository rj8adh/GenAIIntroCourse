from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY"))


def request_API(prompt, tokens: bool = True):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=prompt
)

  if tokens:  # Display amount of tokens used
    print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')

  return response.choices[0].message.content.strip()


items_crafted = ["Water", "Fire", "Earth", "Paneer Tikka Masala"]
print("Not So Finite Craft")
print("-" * 20)

while True:
  print(f"{items_crafted}\n")

  first_item = input("Enter first item: ")
  second_item = input("Enter second item: ")

  if first_item == "Quit" or second_item == "Quit": # Checks if user quit game
    print("Game exited")
    break

  if first_item not in items_crafted or second_item not in items_crafted: # Checks to make sure you have the items you are crafting with
    print("\nInvalid Item(s)\n")
    continue

  # Same request_API call, but formatted differently to show other ways to format the same call
  new_item = request_API([{
      "role": "user",
      "content":
      f"Return an item and ONLY ONE ITEM that combines the two given items(one or two words, don't combine words): {first_item} and {second_item}"
  }], False)

  print(f"\n{new_item}\n")

  if new_item not in items_crafted: # Makes sure no duplicates are in list
    items_crafted.append(new_item)
