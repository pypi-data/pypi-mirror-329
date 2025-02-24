from pydantic import BaseModel
from langgraph.graph.message import AnyMessage, add_messages  # noqa: F401


class ReqGraphExecution(BaseModel):
    """Graph 실행 요청"""

    query: str


class ResGraphExecution(BaseModel):
    """Graph 실행 결과"""

    content: str
    messages: list[AnyMessage] = []
