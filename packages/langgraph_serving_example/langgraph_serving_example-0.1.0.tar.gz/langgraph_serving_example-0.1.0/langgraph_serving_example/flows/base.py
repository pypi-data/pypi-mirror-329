from abc import ABC, abstractmethod
from langchain_core.runnables import (
    RunnableConfig,
    RunnableSerializable,
)

from pydantic import BaseModel


class BaseAgent:
    """Agent의 추상클래스. AIX 플랫폼에서는 UI로 BaseAgent의 구현체를 만들어서 BaseNode의 self.runnable에  넣어줄 예정입니다."""

    def __init__(self) -> None: ...

    def build(self) -> None: ...

    def invoke(self, input_data: dict) -> dict: ...


class BaseState(BaseModel):
    """Agent끼리 주고받을 데이터 구조체."""

    ...


class BaseNode(ABC):
    @abstractmethod
    def __init__(self, name: str = ""):
        """Node의 추상클래스
        runnable: RunnableSerializable - 실행할 로직.
        name: str - 노드 이름. 로깅용.

        구현체에서 runnable을 생성하기 위한 args를 추가.
        """
        self.runnable: RunnableSerializable = self.build()
        self.name: str = name

    @abstractmethod
    def build(self) -> RunnableSerializable:
        """init으로 부터 받은 args로 최종 runnable을 생성."""
        pass

    @abstractmethod
    def __call__(self, state: BaseState, config: RunnableConfig):
        """runnable 실행, 결과 State에 반영"""
        pass
