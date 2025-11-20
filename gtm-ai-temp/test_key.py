from openai import OpenAI
import os

# Make sure your .env has OPENAI_API_KEY set, or set it directly here:
# os.environ["OPENAI_API_KEY"] = "sk-..."

# my key
os.environ["OPENAI_API_KEY"] = "_key_"
# ld key
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hi, which model is this?"}]
)

print(resp.choices[0].message.content)
