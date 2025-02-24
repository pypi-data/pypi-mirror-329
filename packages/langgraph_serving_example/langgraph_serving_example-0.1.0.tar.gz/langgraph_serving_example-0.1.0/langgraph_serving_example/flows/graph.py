import os
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)
from langchain_community.retrievers import WikipediaRetriever
from langgraph.prebuilt import create_react_agent
from langgraph.graph import END, StateGraph, START
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import (
    HumanMessage,
)
from flows.nodes import MessageNode, MessageState

from typing import Annotated
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL  # poetry group dev
import ssl
import httpx
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv


# GPT 4 이상 사용하세요

load_dotenv(".env")
client = None
request_with_sk_ssl = os.environ.get("REQUEST_WITH_SK_SSL", False)
if request_with_sk_ssl:
    cert_file = os.environ.get("SSL_CERT_FILE", "./ssl_cacert.pem")
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(cafile=cert_file)
    client = httpx.Client(verify=ssl_context)

# llm_client = AzureChatOpenAI(
#     azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
#     api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
#     api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
#     azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
#     timeout=60,
#     client=client,
# )
llm_client = ChatOpenAI(
    api_key=os.environ.get("GATEWAY_API_KEY"),
    base_url=os.environ.get("GATEWAY_ENDPOINT"),
    model=os.environ.get("GATEWAY_MODEL"),
)


######### Coder #########
@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""

    repl = PythonREPL()

    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )


code_runnable = RunnableLambda(lambda x: x.model_dump()) | create_react_agent(
    llm_client, tools=[python_repl_tool]
)
update_status_runnable = {
    "content": code_runnable,
    "state": RunnablePassthrough(),
} | RunnableLambda(
    lambda x: (setattr(x["state"], "messages", x["content"]["messages"]) or x["state"])
)

# create coder - Runnable을 넣어서 노드 생성
coder_agent = MessageNode(update_status_runnable, name="Coder")


######### Researcher #########
def researcher(state):
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    print("researcher", state)
    question = state.prev_answer
    wiki_retriever = WikipediaRetriever()
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the context provided.
        Context: {context}
        Question: {question}
        """
    )
    format_docs = lambda x: "\n\n".join(doc.page_content for doc in x)
    chain = (
        {"context": wiki_retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm_client
        | StrOutputParser()
    )
    result = chain.invoke(question)
    state.next_node = None
    state.prev_node = "Researcher"
    state.update_message(result, "ai")
    return state


# create researcher - 함수(Callable)를 넣어서 노드 생성
researcher_agent = MessageNode(researcher, name="Researcher")


######### Supervisor #########
def supervisor(state):
    from pydantic import BaseModel

    # 감독하는 멤버
    members = ["Researcher", "Coder"]
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        " following workers:  {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. "
        " IF tasks from Researcher or Coder are adequately completed,"
        " respond with FINISH."
    )

    # 팀의 supervisor는 LLM 노드 입니다.
    # 역할: 다음 프로세스를 할 agent 선정, 프로세스를  Finish할지 결정
    options = ["FINISH"] + members

    class routeResponse(BaseModel):
        next: str

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join(members))
    supervisor_chain = (
        RunnableLambda(lambda x: x.messages)
        | prompt
        | llm_client.with_structured_output(routeResponse)
    )
    result = supervisor_chain.invoke(state)
    # TODO: with_structured_output is not working. It should be fixed.
    # state.next_node = result.next
    if state.prev_node == "Researcher":
        state.next_node = "FINISH"
    else:
        state.next_node = "Researcher"
    state.prev_node = "Supervisor"
    return state


# create supervisor
supervisor_agent = MessageNode(supervisor, name="Supervisor")

######### Create Graph #########
workflow = StateGraph(MessageState)

workflow.add_node("Researcher", researcher_agent)
workflow.add_node("Coder", coder_agent)
workflow.add_node("Supervisor", supervisor_agent)

workflow.add_edge("Researcher", "Supervisor")
workflow.add_edge("Coder", "Supervisor")

conditional_map = {
    "researcher": "Researcher",
    "coder": "Coder",
    "finish": END,
}

workflow.add_conditional_edges(
    "Supervisor", lambda x: x.next_node.lower(), conditional_map
)
workflow.add_edge(START, "Supervisor")

graph = workflow.compile()

if __name__ == "__main__":
    ######### Test #########
    print(">>>> Test Invoke ")
    final_answer = graph.invoke(
        MessageState(
            messages=[HumanMessage(content="Who is NewJeans?")],
            prev_node="user",
        )
    )
    print(final_answer["messages"][-1].content)

    # print(">>>> Test Stream ")
    # test_messages = MessageState(
    #     messages=[HumanMessage(content="Who is NewJeans?")],
    #     prev_node="user",
    # )
    # test_messages = MessageState(
    #     messages=[
    #         HumanMessage(content="Code hello world and print it to the terminal")
    #     ],
    #     prev_node="user",
    # )

    # events = graph.stream(test_messages, stream_mode="values")

    # printer = EventPrinter()
    # for event in events:
    #     printer.print_event(event)
