from dotenv import load_dotenv
load_dotenv()  
from langchain_openai import ChatOpenAI
from langchain.messages import (
    SystemMessage,  # システムメッセージ
    HumanMessage,  # 人間の質問
    AIMessage  # ChatGPTの返答
)

llm = ChatOpenAI()  # ChatGPT APIを呼んでくれる機能
message = "簡単に作れる魚料理を教えてください"  # あなたの質問をここに書く

messages = [
    SystemMessage(content="絶対に関西弁で回答してください"),
    HumanMessage(content=message)
]
response = llm.invoke(messages)
print(response)

# content='Hello! How can I assist you today?' additional_kwargs={} example=False