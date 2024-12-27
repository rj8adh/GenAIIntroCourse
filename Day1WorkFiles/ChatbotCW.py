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

print("Hey there, welcome to the chatgpt chatbot")

history = []

while True:
    chat = input()
    AI_answer = request_API([{"role": "system", "content": f"You are an AI chatbot required to help the user. Use this history to generate your response: {history}), the user has asked {chat}"}], False)
    
    # Keeping track of chat history
    print(AI_answer)
    history.append({"role": "user", "content": chat})
    history.append({"role": "system", "content": AI_answer})
   
