
import os
import openai

openai.organization = "org-FJdvXADZhfDn09iHQlkuHXgP"
openai.api_key = "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"


completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Hey can you tell me what is trading exactly in 20 words?"}
  ]
)

print(completion.choices[0])