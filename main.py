import ollama

response = ollama.chat(model='wizardlm2:7b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])