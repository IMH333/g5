#Main Code Here

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("Go fix this")

client = OpenAI(api_key=api_key)

prompt = ("Hows your day?")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt,
)

print(response)
