import numpy as np
from abc import ABC, abstractmethod


from .PowerBuffer import PowerBuffer
from .Task import PowerTask


class Stack(ABC):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def append(self, value) -> None:
        pass

    @abstractmethod
    def get(self):
        pass


class CircularStack(Stack):
    def __init__(self, starting_buffer: list[PowerTask] = []) -> None:
        self._queue: list = starting_buffer
        self._element_number = 0

    def __len__(self) -> int:
        return len(self._queue)

    def append(self, value: PowerTask) -> None:
        self._queue.append(value)

    def get(self) -> PowerTask:
        answer_element = self._queue[self._element_number]
        self._element_number += 1
        self._element_number = (
            self._element_number if self._element_number < len(self._queue) else 0
        )
        return answer_element

    def del_element(self, element: PowerTask) -> None:
        del self._queue[self._queue.index(element)]


class QueuePowerBuffer(Stack):
    def __init__(self) -> None:
        self._queue: list = []

    def __len__(self) -> int:
        return len(self._queue)

    def append(self, value: PowerBuffer) -> None:
        self._queue.append(value)

    def get(self) -> PowerBuffer:
        answer = self._queue[0]
        del self._queue[0]
        return answer
