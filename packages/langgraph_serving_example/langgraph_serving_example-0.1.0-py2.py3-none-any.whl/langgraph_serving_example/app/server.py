#!/usr/bin/env python

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from flows.graph import llm_client, graph
from flows.nodes import MessageState
from app.type import ReqGraphExecution, ResGraphExecution

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="PlatForm Agent App Example",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

joke_prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

joke_chain = joke_prompt | llm_client

add_routes(
    app,
    joke_chain,
    path="/joke",
)


def create_state(input_data: dict) -> MessageState:
    return MessageState(
        messages=[HumanMessage(content=input_data.get("query"))],
        prev_node="user",
    )


def parse_result(state: dict) -> ResGraphExecution:
    if state.get("messages") is None:
        # for streaming
        try:
            final_answer = list(state.values())[0]["messages"][-1].content
        except Exception as e:
            print(f"Error parsing result: {e}")
            final_answer = "Error occurred while processing the request."
        message_history = []

    else:
        # for invoke, batch
        final_answer = state.get("messages")[-1].content
        message_history = state["messages"]
    return ResGraphExecution(
        content=final_answer,
        message_history=message_history,
    )


graph_execution_chain = create_state | graph | parse_result


add_routes(
    app,
    graph_execution_chain,
    path="/graph",
    input_type=ReqGraphExecution,
    output_type=ResGraphExecution,
)
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
