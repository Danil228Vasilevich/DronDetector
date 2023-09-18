import numpy as np

from DataClasses.PowerBuffer import PowerBuffer

class QueuePowerBuffer:
    def __init__(self) -> None:
        self._queue: list = []
    
    def __len__(self) -> int:
        return len(self._queue)

    def add_element(self, element:PowerBuffer) -> None:
        self._queue.append(element)

    def get_element(self) -> PowerBuffer:
        answer = self._queue[0]
        del self._queue[0]
        return answer