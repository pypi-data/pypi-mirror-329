from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnableSerializable,
    RunnableConfig,
)
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    AIMessage,
    SystemMessage,
)
from typing import Any
from flows.base import BaseNode, BaseState
from typing import Annotated
from collections.abc import Callable


class MessageState(BaseState):
    """State는 예시. messages에 기록하는 방식
    messages: list[AnyMessage] - 메시지 리스트
    additional_kwargs: dict[str, Any] - 추가적인 정보. 메세지로 담기에는 마이너한 정보이거나, 다음 노드에서 바로쓰는것이 아니지만 누군가는 사용할 정보 등을 저장.
    prev_node: str - 이전 노드 이름.
    next_node: str - 다음 노드 이름. Conditional Edge인 경우에만 사용. 그 외의 경우 None이어도 됨.
    """

    messages: Annotated[list[AnyMessage], add_messages] = []
    additional_kwargs: dict[str, Any] = {}
    prev_node: str = "user"
    next_node: str | None = None

    @property
    def agent_scratchpad(self):
        """messages를 string으로 변환한 값"""
        agent_scratchpad_list = []
        for message in self.messages:
            content = f"""
            "node_name": {message.name}
            "role": {message.type}
            "content": {message.content}
            """
            agent_scratchpad_list.append(content)
        return "\n====================\n".join(agent_scratchpad_list)

    @property
    def prev_answer(self):
        """이전 노드의 결과이자, 현 노드의 input이 될 내용"""
        return self.messages[-1].content

    @property
    def user_question(self):
        """사용자 질문"""
        return self.messages[0].content

    def update_message(
        self, content: str, message_type: str, node_name: str | None = None
    ) -> None:
        if node_name is None:
            node_name = self.prev_node
        if message_type == "tool":
            self.messages.append(ToolMessage(content=content, name=node_name))
        elif message_type == "human":
            self.messages.append(HumanMessage(content=content, name=node_name))
        elif message_type == "system":
            self.messages.append(SystemMessage(content=content, name=node_name))
        elif message_type == "ai":
            self.messages.append(AIMessage(content=content, name=node_name))
        else:
            self.messages.append(AIMessage(content=content, name=node_name))


# BaseNode를 상속받아서 새로운 Node를 정의
class MessageNode(BaseNode):
    """단일 함수 또는 Runnable을 받는 노드.
    target_function: Callable | Runnable - 실행할 로직. 함수(Callable) 또는 Runnable을 받음.
    name : str - 노드 이름. 로깅용.
    self.runnable: target_function을 Runnable으로 변환. 최종 로직을 self.runnable에 담음.
    """

    def __init__(self, target_function: Callable | Runnable, name: str = ""):
        self.target_function = target_function
        self.name = name
        self.runnable: RunnableSerializable = self.build()

    def build(self) -> RunnableSerializable:
        """init에서 받은 args로 Runnable을 생성"""
        if isinstance(self.target_function, Runnable):
            return self.target_function
        elif isinstance(self.target_function, Callable):
            return RunnableLambda(self.target_function)
        else:
            raise ValueError("Invalid target function")

    def __call__(self, state: BaseState, config: RunnableConfig = {}) -> dict:
        """runnable 실행, 결과 State에 반영"""
        # callbacks = config.get("callbacks", [])
        new_state = self.runnable.invoke(input=state, config=config)
        new_state.prev_node = self.name
        return new_state
