#TODO Fix prompt engineering to make sure output doesn't work with invalid questions
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

user_topic = input("Enter a topic for the AI\'s word: ")
ai_word = AI_answer = request_API([{"role": "system", "content": f"You are playing the game 20 Questions. The user has given the following topic: {user_topic}. Generate ONE WORD that falls under this topic."}], False)
print(f"The word\'s {ai_word} you sneaky cheater")
for i in range(1, 21): # Decided to do 1 to 21 to make it convenient for debugging and printing guesses

  if i < 20:
    question = input("Enter a YES or NO question for the AI to answer, or enter GUESS if you're trying to guess the word ")
  elif i == 20:
    question = input("This is your last guess, so you should try and guess the actual word")

  if (question.lower() == "guess"):
      question = input("What word are you guessing? ")
      if question.lower() == ai_word.lower():
        break
      print("Incorrect")
      continue
  
  AI_answer = request_API([{"role": "system", "content": f"(You are playing 20 questions and you have the word: {ai_word}). Consider the following question: {question}. If this question has no definitive yes or no answer, return 2. If this question is true, return 1. If this question is false return 0. ONLY RETURN A ONE DIGIT NUMBER"}], False)
  try:
    AI_answer = int(AI_answer)
  except:
    print("INVALID AI RESPONSE, try adjusting the prompt")

  print(AI_answer)
  if (AI_answer == 1):
    print("Yes")
  elif (AI_answer == 0):
    print("No")
  else:
    print("INVALID QUESTION: " + str(AI_answer))
    i-=1

if (i == 20):
  print(f"You lost =(")
else:
  print(f"YOU WON IN {i} GUESSES!!!")