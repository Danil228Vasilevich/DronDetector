import numpy as np
import threading as Thread
from scipy import signal
import pickle

import matplotlib.pyplot as plt

from PowerReader import PowerReader, SweepPower

from abc import ABC, abstractmethod

from DataClasses import RangeFreq
from DataClasses import PowerBuffer
from DataClasses import QueuePowerBuffer, CircularStack
from DataClasses import PowerTask
from DataClasses import Packet


class Detector(ABC):
    def __init__(self) -> None:
        pass


class DroneDetecter(Detector):
    def __init__(self, circular_task: CircularStack, power_source_constructor) -> None:
        self._circular_task: CircularStack = circular_task
        self._is_alive = False
        self._queue: QueuePowerBuffer = QueuePowerBuffer()
        self._power_source: PowerReader = power_source_constructor(self._data_call_back)

        self._event_detecting_thread: Thread.Event
        self._detecting_thread: Thread.Thread
        self._power_sweep: SweepPower

    def _data_call_back(self, data: PowerBuffer) -> None:
        self._queue.append(data)

    def start(self) -> None:
        start_task = self._circular_task.get()

        self._event_detecting_thread = Thread.Event()
        self._detecting_thread = Thread.Thread(
            target=self._detecting, args=(self._event_detecting_thread,)
        )
        self._is_alive = True
        self._power_source.start(start_task)
        self._detecting_thread.start()

    def stop(self) -> None:
        self._event_detecting_thread.set()
        self._power_sweep.stop()
        self._is_alive = False

    def _detecting(self, event) -> None:
        while self._is_alive:
            if event.is_set():
                break
            if len(self._queue) == 0:
                continue
            power_buffer = self._queue.get()

            freq_list = power_buffer.get_freq()
            power_data = power_buffer.get_data()
            power_data = np.rot90(power_data)

            # Тут есть алгоритм


class PacketDetector:
    def __init__(self) -> None:
        pass


class PowerRecorder(DroneDetecter):
    def __init__(
        self, circular_task: CircularStack, power_source_constructor, path: str
    ) -> None:
        super().__init__(circular_task, power_source_constructor)
        self._path = path
        self._count = 0

    def _detecting(self, event) -> None:
        while self._is_alive:
            if event.is_set():
                break
            if len(self._queue) == 0:
                continue

            power_buffer = self._queue.get()
            name_file = f"{self._path}Sample{self._count}.data"
            with open(name_file, "w+b") as f:
                print("save_data")
                pickle.dump(power_buffer, f)
                self._count += 1


if __name__ == "__main__":
    freq = RangeFreq(2401, 2484, 0.5)
    task = PowerTask(freq, 100)
    stack = CircularStack([task])
    power_source = SweepPower
    detect = DroneDetecter(stack, power_source)
    detect.start()
