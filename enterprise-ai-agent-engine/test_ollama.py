from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

response = llm.invoke(
    "How can AI help a company reduce costs?"
)

print(response.content)