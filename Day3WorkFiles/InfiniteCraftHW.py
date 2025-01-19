from openai import OpenAI
import os
# Any commented-out code is for the challenge homework of adding emojis

client = OpenAI(api_key=os.getenv("API_KEY"))


def request_API(prompt, tokens: bool = True):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=prompt
)

  if tokens:  # Display amount of tokens used
    print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')

  return response.choices[0].message.content.strip()

# Main game
items_crafted = ["Water 💧", "Fire 🔥", "Earth 🌍", "Paneer Tika Masala 🍛"]
print("Not So Finite Craft")
print("-" * 20)

while True:
  bool1 = False
  bool2 = False
  item_exists = False

  print(f"{items_crafted}\n")

  first_item = input("Enter first item: ").lower()
  second_item = input("Enter second item: ").lower()

  if first_item == "Quit" or second_item == "Quit":
    print("Game exited")
    break

  for item in items_crafted:
    # We need to loop over the list to check if the users items match any of the items in the inventory
    if item[:-2].lower() == first_item: # We have to check index [:-2] because we want to exclude the space and emoji at the end of each inventory item
      bool1 = True
    elif item[:-2].lower() == second_item:
      bool2 = True

  if not(bool1 and bool2): # Makes sure the items you're attempting to craft with are in your inventory
    print("\nInvalid items\n")
    continue

  new_item = request_API([{"role": "user", "content": f"Return an item and ONLY ONE ITEM that combines the two given items(one or two words, don't combine words): {first_item} and {second_item} (also, make sure the words make some sense at least). Also add ONE, AND ONLY ONE Emoji at the end of the item WITH A SPACE name that represents the item"}], False)

  print(f"\n{new_item}\n")

  for item in items_crafted:
    if item[:-2] == new_item[:-2]:
      item_exists = True

  if (not item_exists):
    items_crafted.append(new_item)
  else:
    print("Item already exists in inventory")
