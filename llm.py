#V2 start
from ollama import chat


MODEL = "qwen3:4b-instruct"

def ask_llm(messages, tools=None):

    response = chat(
        model=MODEL,
        messages=messages,
        tools=tools,
        think=False
    )

    return response.message
#V2 end