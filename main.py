import openai.types.responses.response
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    response = llm.invoke("Hello, how are you?")
    print(response.content)


if __name__ == "__main__":
    main()
