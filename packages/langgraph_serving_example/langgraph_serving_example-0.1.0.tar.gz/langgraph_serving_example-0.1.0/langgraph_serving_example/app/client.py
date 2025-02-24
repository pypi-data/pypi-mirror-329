import os
from langserve import RemoteRunnable
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
import ssl
import httpx

load_dotenv(".env")

client = None
request_with_sk_ssl = os.environ.get("REQUEST_WITH_SK_SSL", False)
if request_with_sk_ssl:
    cert_file = os.environ.get("SSL_CERT_FILE", "./ssl_cacert.pem")
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(cafile=cert_file)
    client = httpx.Client(verify=ssl_context)


llm_client = ChatOpenAI(
    api_key=os.environ.get("GATEWAY_API_KEY"),
    base_url=os.environ.get("GATEWAY_ENDPOINT"),
    model=os.environ.get("GATEWAY_MODEL"),
)


if __name__ == "__main__":
    ####### 단순 실행 ######
    connection_test = llm_client.invoke("hello")

    joke_chain = RemoteRunnable("http://localhost:18080/joke/")

    parrots_joke = joke_chain.invoke({"topic": "parrots"})
    print(">>> Parrots Joke")
    print(parrots_joke)
    print("---")

    agent = RemoteRunnable("http://localhost:18080/graph/")

    result = agent.invoke({"query": "What is the capital of France?"})
    print(">>> Capital of France")
    print(result)
    print("---")
    ####### Chaining 해서 실행  ######
    prompt_template = """
    Create a quiz show question. With 4 multiple choices.
    Format must be like this:
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "answer": "..."

    Let's start! Question is {content}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = agent | prompt | llm_client

    final_result = chain.invoke({"query": "What is the capital of France?"})
    print(">>> Capital of Korea")
    print(final_result)
    print("---")
