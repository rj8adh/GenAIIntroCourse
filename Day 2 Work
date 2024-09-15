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


message_history = []
user_word = input("Enter word for AI to try and guess: ")

for i in range(1, 21):

  if i < 20:
    AI_answer = request_API([{"role": "system", "content": f"(You are playing 20 questions.) You are trying to guess a word that a user has inputted. Ask a simple question which has a definite YES or NO answer to try and guess the word. (Also, here's the message history up to this point {message_history})"}], False)
    message_history.append({"role": "system", "content": AI_answer})
    print(AI_answer)
  elif i == 20:
    AI_answer = request_API([{"role": "system", "content": f"(You are playing 20 questions.) You are now on your last guess, so try and make it a guess of the actual thing. (Also, here's the message history up to this point {message_history})"}], False)
    message_history.append({"role": "system", "content": AI_answer})
    print(AI_answer)


  user_response = input("\nYes or No: ")
  message_history.append({"role": "user", "content": user_response})

  if user_response.upper() == "QUIT":
    break

  if user_response.upper() in ['YOU GOT IT', 'CORRECT']:
    break
