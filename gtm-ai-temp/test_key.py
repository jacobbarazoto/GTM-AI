from openai import OpenAI
import os

# Make sure your .env has OPENAI_API_KEY set, or set it directly here:
# os.environ["OPENAI_API_KEY"] = "sk-..."

# my key
os.environ["OPENAI_API_KEY"] = "_key_"
# ld key
# os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hi, which model is this?"}]
)

print(resp.choices[0].message.content)
