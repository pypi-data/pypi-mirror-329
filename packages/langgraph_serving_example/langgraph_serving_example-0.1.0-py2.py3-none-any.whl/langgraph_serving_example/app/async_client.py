import os
from langserve import RemoteRunnable
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
import ssl
import httpx
import asyncio


load_dotenv(".env")

client = None
request_with_sk_ssl = os.environ.get("REQUEST_WITH_SK_SSL", False)
if request_with_sk_ssl:
    cert_file = os.environ.get("SSL_CERT_FILE", "./ssl_cacert.pem")
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(cafile=cert_file)
    client = httpx.Client(verify=ssl_context)




async def main():
    joke_chain = RemoteRunnable("http://localhost:8080/joke/")
    async for chunk in joke_chain.astream({"topic": "bear"}):
        print(chunk)


asyncio.run(main())
