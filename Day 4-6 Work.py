# -*- coding: utf-8 -*-
"""OpenAI_Project.ipynb

Original file is located at
    https://colab.research.google.com/drive/1Z-dK2cvQnqtUdrpY2ild6lzNdLjgwTJY

Step by Step lesson plan:
Day 1: Base game with no items, health, enemies, etc.
Day 2: Adding Entity Class and work on enemy--HW will be to finish implementing enemies, but we will give them answer sheet if they get stuck
Day 2 BONUS: Add counterattack messages using AI to write an attack that the enemy with given name would do
Day 3: Adding Items -- HW will be to add health regen stuff, again, answer sheet will be provided if they get stuck
"""

from openai import OpenAI
import random
import time
import os

# For fancy printing:
import time
import sys


# Day 1
def request_API(prompt, tokens: bool=True):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )

    if tokens:
        print(f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n')

    return response.choices[0].message.content.strip()

# Day 1
def decide_next(context, gen_enemy):
    # returns what to print based on whether or not you're spawning an enemy
    if gen_enemy:
        next_move = request_API([{"role": "system", "content": f"You are generating the next steps of a RPG game, using this message history context {context}, generate the next step."}, {"role": "user", "content": "Generate the next step in the story (only one step), but this time, make an enemy"}], False)
    else:
        next_move = request_API([{"role": "system", "content": f"You are generating the next steps of a RPG game, using this message history context {context}, generate the next step following what the user asks for as closely as possible."}, {"role": "user", "content": "Generate the next step in the story (only one step), without an enemy"}], False)

    return next_move

# Day 2
class Entity:

    def __init__(self, health: int, name, inventory: dict):
        self.name = name
        self.health = health
        self.inventory = inventory

    def attack(self, target, damage_multiplier=1): # ADD WEAPON
        if self.health >= 0:
            target.health -= 2 * damage_multiplier # weapon.damage
            print(f"{self.name} attacks {target.name} for {str(2 * damage_multiplier)} damage!") # Future: attempt to add AI generated hurt messages
        if target.health <= 0:
            print(f"{target.name} has been defeated!")

    def add_item(self, item):
        self.inventory.add(item)
        print(f"{self.name} has added {item} to their inventory!")

    def heal(self, percentage):
        heal_amount = int(round((100 - self.health)  * percentage))
        self.health += heal_amount
        print(f"{self.name} has healed for {round(heal_amount)} health!")

# Day 2 HW
class Enemy(Entity):
    def __init__(self, bg_info, power: int): # Removed health because we decide that based on power level
        self.name = request_API([{"role": "system", "content": "You are a simple game designer, and your friend asked you about how you make such good game characters. He then gives you a prompt about what type of enemy he wants, and you simply return the name."}, {"role": "user", "content": f"Make an enemy that would be found based on this background information {bg_info}"}], False)
        self.power = power

        # Changing the health and drops based on power level
        match power:
            case 1:
                self.health = 10
                self.drops = ['Stone Sword', 'Stone Sword', 'Stone Sword', 'Healing Potion']
            case 2:
                self.health = 20
                self.drops = ['Iron Sword', 'Iron Sword', 'Iron Sword','Healing Potion' ]
            case 3:
                self.health = 30
                self.drops = ['Blood Sword', 'Blood Sword', 'Blood Sword', "Mini's"]
            case 4:
                self.health = 40
                self.drops = ['Decapitator', 'Decapitator', 'Decapitator', 'Big Pot']
            case 5:
                self.health = 50
                self.drops = ['Decapitator', 'Fanum Tax', 'Fanum Tax', 'Chug Jug']

# Day 3
class Weapon:
    def __init__ (self, name, damage):
        self.name = name
        self.damage = damage

        if self.name in ['Stone Sword', 'Iron Sword', 'Blood Sword', 'Decapitator', 'Fanum Tax']:
            match self.name:
                case 'Stone Sword':
                    self.damage *= 2
                case 'Iron Sword':
                    self.damage *= 3
                case 'Blood Sword':
                    self.damage *= 4
                case 'Decapitator':
                    self.damage *= 5
                case 'Fanum Tax':
                    self.damage *= 6
        else:
            self.damage *= 1


# Day 2 BONUS
def counter_attack(enemy):
    print(request_API([{"role": "user", "content": f"(15 words max )Make an attack that an enemy named {enemy} would use"}]))

# Just fancy stuff for slow printing -- NOT NEEDED
def print_slow(text, sleep_time=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(sleep_time)

# MAIN GAME: (ORIGINAL)


# REMINDER TO REMOVE API KEY WHEN UPLOADING TO INTERNET -- may teach about .env or just use replit secret
client = OpenAI(api_key=os.getenv("API_KEY"))


exit = False
message_history = []
next_move = ""
is_enemy = False
enemies_encountered = 0
player_weapon_determination = [] # This is just a variable made to make sure that the weapon that's being actively equipped isn't a lower power level then that of any other weapon in the player's arsenal

weapon_def = {
    'Stone Sword': 1.5,
    'Iron Sword': 1.8,
    'Blood Sword': 2.2,
    'Decapitator': 2.6,
    'Fanum Tax': 3.5,
}

player = Entity(name="Player", health=100, inventory=[])
player_weapon = Weapon("Fist", 1)

# Day 1 -- Start of game

print_slow("Welcome to the AI generated RPG!\n", 0.01)
beginning_context = input("Where do you want your adventure to start? ")
print()
next_move = decide_next(beginning_context, False)
message_history.append({"role": "system", "content": next_move})
print()
print_slow(f"> {next_move}", 0.01)

if __name__ == "__main__": # MAIN GAME LOOP -- Mix of ALL days
    while True:
        print(f"\nPlayer health = {int(player.health)}")
        print(f"Player inventory = {player.inventory}")
        prompt = input("User: ") # Continues the game after the first input
        print()

        if prompt.lower() in ['exit', 'break', 'quit', 'bye']:
            exit = True
            break
        if exit:
            break

        message_history.append({"role": "user", "content": prompt}) # Format and append to history the user's input in a way the AI can understand it
        # message_history.append({"role": "user", "content": f"The players inventory: {player.inventory}"})


        # Day 3 HW -- Healing mechanism
        if "heal" in prompt.lower():
            if "Healing Potion" in player.inventory:
                player.heal(0.60)
                player.inventory.remove("Healing Potion")
            elif "Mini's" in player.inventory:
                  player.heal(0.70)
                  player.inventory.remove("Mini's")
            elif "Big Pot" in player.inventory:
                  player.heal(0.80)
                  player.inventory.remove("Big Pot")
            elif "Chug Jug" in player.inventory:
                  player.heal(1)
                  player.inventory.remove("Chug Jug")
            else:
                print_slow("Nice Try u Bummmmmm")


        # Day 2 HW -- Enemy Fighting
        for element in prompt.split():
            if is_enemy and element.lower() in ["attack", "fight", "punch", "kick", "eat", "kill"]:
                player.attack(enemy, player_weapon.damage)

                if random.randint(1, 2) == 1: # Player getting attacked is a 50% chance
                    counter_attack(enemy.name)
                    enemy.attack(player, damage_multiplier=enemy.power)

                if enemy.health <= 0:
                    is_enemy = False
                    enemies_encountered += 1
                    print_slow("\nEnemy Defeated!\n")

                    # Drops item randomly based on the amount of enemies there have been, can change it to drop every time for simplicity
                    if enemies_encountered % random.randint(2, 3) == 0:
                        dropped_item = random.choice(enemy.drops)
                        print_slow(f"You got a {dropped_item}!\n")


                        # Setting up the weapon logic
                        if dropped_item in player.inventory:
                            pass
                        else:
                            player.inventory.append(dropped_item)
                            # Here, you need to scan the list, checking for the weapon(s) that are there, then use a predetermined dictionary to see if the weapon value is greater than the incoming weapon value, and change the player's power/weapon damage accordingly
                            for item in player.inventory:
                                if item in weapon_def.keys():
                                    player_weapon_determination.append(weapon_def[item])

                                    highest_valued_weapon = max(player_weapon_determination)

                                    for key, value in weapon_def.items():
                                        if value == highest_valued_weapon:
                                            player_weapon = Weapon(item, weapon_def[item])

                    message_history.append({"role": "user", "content": f"the enemy (with the name of {enemy.name})is now defeated."})
                    break
                else:
                    print_slow(f"\nEnemy has {enemy.health} hp left", 0.05)


        # Day 2 -- Enemy spawning logic
        if random.randint(1, 4) == 1 and is_enemy == False: # 1/4 chance for an enemy to spawn
            AI_response = decide_next(message_history, True)
            message_history.append({"role": "assistant", "content": AI_response})

            if random.randint(1, 50) == 1:
                if random.randint(1, 100) == 1:
                    enemy = Enemy(next_move, power=5)
                    print_slow(f"You encountered a mega boss! {enemy.name} has {enemy.health} health!")
                else:
                    enemy = Enemy(next_move, power=4)
                    print_slow(f"You encountered a boss! {enemy.name} has {enemy.health} health!")
            else:
                enemy = Enemy(next_move, power=int(random.randint(1, 3))) # Only used 1-3 here because any health above that should be a boss fight
                print_slow(f"An enemy has appeared!\n{enemy.name} has {enemy.health} health!")


            is_enemy = True
        else:
            if is_enemy == False:
                AI_response = decide_next(message_history, False)
                message_history.append({"role": "assistant", "content": AI_response})

                print_slow(f"> {AI_response}")


        # Lose statement
        if player.health <= 0: #or len(message_history) >= 100:
            print("GAME OVER!")
            break