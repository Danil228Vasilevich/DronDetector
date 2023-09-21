import numpy as np
import threading as Thread
from scipy import signal

import matplotlib.pyplot as plt

from PowerReader import PowerReader, SweepPower


from DataClasses.DataFreq import RangeFreq
from DataClasses.PowerBuffer import PowerBuffer
from DataClasses.Queue import QueuePowerBuffer, CircularStack
from DataClasses.Task import PowerTask


class Detecter:
    def __init__(self, circular_task: CircularStack, power_source_constructor) -> None:
        self._circular_task: CircularStack = circular_task
        self._is_alive = False
        self._queue: QueuePowerBuffer = QueuePowerBuffer()
        self._power_source: PowerReader = power_source(self._data_call_back)

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

            # тут есть алгоритм
            fig, axs = plt.subplots(nrows=3, ncols=1)

            # plt.plot(power_data[2])
            new_power_data = signal.medfilt2d(power_data, kernel_size=3)

            # exp_data = np.exp(
            #     np.subtract(
            #         new_power_data[2],
            #         np.mean(power_data[2]),
            #     )
            # )
            exp_data = np.exp(power_data[2])

            list_freq = power_buffer.get_freq()

            axs[0].plot(new_power_data[2])
            axs[0].plot(power_data[2])
            axs[0].plot(
                np.ones(len(new_power_data[2]))
                * np.mean(power_data[2][power_data[2] < np.mean(power_data[2])])
            )

            axs[1].plot(list_freq, exp_data)
            axs[2].plot(list_freq, np.sqrt(exp_data))

            plt.show()


if __name__ == "__main__":
    freq = RangeFreq(2401, 2484, 0.5)
    task = PowerTask(freq, 100)
    stack = CircularStack([task])
    power_source = SweepPower
    detect = Detecter(stack, power_source)
    detect.start()
