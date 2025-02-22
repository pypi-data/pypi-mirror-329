from abc import ABC, abstractmethod
from typing import Awaitable

from pydantic import BaseModel, PrivateAttr

from emp_agents.models import Message


class AbstractConversationProvider(BaseModel, ABC):
    @abstractmethod
    def set_history(self, messages: list[Message]) -> None:
        pass

    @abstractmethod
    def add_message(self, message: Message) -> None:
        pass

    @abstractmethod
    def add_messages(self, messages: list[Message]) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def get_history(self) -> list[Message] | Awaitable[list[Message]]:
        pass


class ConversationProvider(AbstractConversationProvider):
    _history: list[Message] = PrivateAttr(default_factory=list)

    def set_history(self, messages: list[Message]) -> None:
        self.reset()
        self.add_messages(messages)

    def add_message(self, message: Message) -> None:
        self._history.append(message)

    def add_messages(self, messages: list[Message]) -> None:
        self._history.extend(messages)

    def reset(self) -> None:
        self._history.clear()

    def get_history(self) -> list[Message] | Awaitable[list[Message]]:
        return self._history.copy()
