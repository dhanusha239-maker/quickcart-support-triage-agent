from src.llm_client import chat

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Say hello in one sentence."}
]

print(chat(messages))