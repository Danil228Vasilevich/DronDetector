import numpy as np
import threading as Thread
from scipy import signal

import matplotlib.pyplot as plt

from HackSweep import SweepPower


from DataClasses.DataFreq import RangeFreq
from DataClasses.PowerBuffer import PowerBuffer
from DataClasses.Queue import QueuePowerBuffer


class Detect:
    def __init__(self, list_listenable_freq: list[RangeFreq]) -> None:
        self._list_listenable_freq: list[RangeFreq] = list_listenable_freq

        self._is_alive = False
        self._queue: QueuePowerBuffer = QueuePowerBuffer()

        self._event_detecting_thread: Thread.Event
        self._detecting_thread: Thread.Thread
        self._power_sweep: SweepPower

    def _data_call_back(self, data: PowerBuffer) -> None:

        self._queue.add_element(data)

    def start(self) -> None:
        self._power_sweep = SweepPower(
            self._data_call_back,
            100,
            self._list_listenable_freq[0],
            bin_size=0.5
        )
        self._event_detecting_thread = Thread.Event()
        self._detecting_thread = Thread.Thread(
            target=self._detecting, args=(self._event_detecting_thread,)
        )
        self._is_alive = True
        self._power_sweep.start()
        self._detecting_thread.start()

    def stop(self) -> None:
        self._event_detecting_thread.set()
        self._power_sweep.stop()
        self._is_alive = False

    def _detecting(self, event) -> None:
        while self._is_alive:
            if event.is_set():break
            if len(self._queue) == 0:continue
            power_buffer = self._queue.get_element()
            
            freq_list = power_buffer.get_freq()
            power_data = power_buffer.get_data()
            power_data = np.rot90(power_data)
            
            # тут есть алгоритм

            plt.plot(power_data[2])
            new_power_data = signal.medfilt2d(power_data, kernel_size=3)


            
            plt.plot(new_power_data[2])
            
            
            plt.show()

if __name__ == "__main__":
    freq = RangeFreq(2401, 2550)
    detect = Detect([freq])
    detect.start()