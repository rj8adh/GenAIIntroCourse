from openai import OpenAI
import os
# Any commented-out code is for the challenge homework of adding emojis

client = OpenAI(api_key=os.getenv("API_KEY"))


def request_API(prompt, tokens: bool = True):
  response = client.chat.completions.create(model="gpt-3.5-turbo",
                                            messages=prompt)

  if tokens:  # Attempt to make a seperate box for token printing
    print(
        f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n'
    )

  return response.choices[0].message.content.strip()


# Main game
# items_crafted = ["Water 💧", "Fire 🔥", "Earth 🌍", "Paneer Tika Masala 🍛"]
items_crafted = ["Water", "Fire", "Earth", "Paneer Tikka Masala"]
print("Not So Finite Craft")
print("-" * 20)

while True:
  # bool1 = False
  # bool2 = False

  print(f"{items_crafted}\n")

  first_item = input("Enter first item: ")
  second_item = input("Enter second item: ")

  if first_item == "Quit" or second_item == "Quit":
    print("Game exited")
    break

  # for item in items_crafted:
  #   if item[:-2] == first_item:
  #     bool1 = True
  #   elif item[:-2] == second_item:
  #     bool2 = True

  # if not(bool1 and bool2):
  #   print("\nInvalid items\n")
  #   continue

  if first_item not in items_crafted or second_item not in items_crafted:
    print("\nInvalid Item(s)\n")
    continue

  # new_item = request_API([{"role": "user", "content": f"Return an item and ONLY ONE ITEM that combines the two given items(one or two words, don't combine words): {first_item} and {second_item} (also, make sure the words make some sense at least). Also add ONE, AND ONLY ONE Emoji at the end of the item WITH A SPACE name that represents the item"}], False)
  new_item = request_API([{
      "role":
      "user",
      "content":
      f"Return an item and ONLY ONE ITEM that combines the two given items(one or two words, don't combine words): {first_item} and {second_item}"
  }], False)

  print(f"\n{new_item}\n")

  # if new_item[:-2] not in items_crafted:
  #   items_crafted.append(new_item)

  if new_item not in items_crafted:
    items_crafted.append(new_item)
