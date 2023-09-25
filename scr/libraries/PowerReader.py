import numpy as np
import threading as Tread
import subprocess
import struct
import sys
import copy
from math import ceil

from abc import ABC, abstractmethod

from DataClasses.PowerBuffer import PowerBuffer
from DataClasses.DataFreq import RangeFreq
from DataClasses.Task import PowerTask


class PowerReader(ABC):
    def __init__(self, call_back_func) -> None:
        self._call_back_func = call_back_func
        self._is_alive = False

    @property
    def alive(self):
        return self._is_alive

    @abstractmethod
    def start(self, task: PowerTask):
        pass

    @abstractmethod
    def stop(self):
        pass


class SweepPower(PowerReader):
    def __init__(self, call_back_func) -> None:
        super().__init__(call_back_func)

        # --------------------------tread----------------------------------
        self._event_read_tread: Tread.Event
        self._read_tread: Tread.Thread
        self._buffer: PowerBuffer

        self._limit_len_buffer: int

    def start(self, task: PowerTask) -> None:
        self._event_read_tread = Tread.Event()
        self._read_tread = Tread.Thread(
            target=self._read_data, args=(self._event_read_tread,)
        )
        self._list_freq = np.arange(
            task.range_freq.min_freq,
            task.range_freq.max_freq,
            task.range_freq.bin_size,
        )

        amount_freq = ceil(ceil(20 / task.range_freq.bin_size) / 4)

        amount_freq = amount_freq if amount_freq % 2 else amount_freq + 1

        self._limit_len_buffer = ceil(
            task.sample_length
            * (
                (task.range_freq.max_freq - task.range_freq.min_freq)
                / task.range_freq.bin_size
            )
            / amount_freq
        )

        self._buffer = PowerBuffer(task)
        cmdline = [
            "hackrf_sweep",
            "-f",
            "{}:{}".format(
                int(task.range_freq.min_freq), int(task.range_freq.max_freq)
            ),
            "-B",
            "-w",
            "{}".format(int(task.range_freq.bin_size * 1e6)),
            "-l",
            "{}".format(int(task.lna_gain)),
            "-g",
            "{}".format(int(task.vga_gain)),
        ]
        self._process = subprocess.Popen(
            cmdline,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=False,
        )
        self._is_alive = True
        self._read_tread.start()

    def stop(self) -> None:
        self._event_read_tread.set()

        if self._process:
            self._process.terminate()

    def _return_data(self) -> None:
        self._call_back_func(copy.copy(self._buffer))
        if isinstance(self._buffer, PowerBuffer):
            self._buffer.zeroing_data()
        else:
            print("error buffer not PowerBuffer")

    def _buffering(self, data) -> None:
        self._buffer.append(data)

        if len(self._buffer) >= self._limit_len_buffer:
            self._return_data()

    def _read_data(self, event) -> None:
        while self._is_alive:
            if event.is_set():
                break

            if self._process.stdout is None:
                print(file=sys.stderr)
                continue

            buf = self._process.stdout.read(4)

            if buf:
                (record_length,) = struct.unpack("I", buf)
                try:
                    buf = self._process.stdout.read(record_length)
                except AttributeError as e:
                    print(e, file=sys.stderr)
                    continue
                if buf:
                    self._buffering(buf)
                else:
                    break
            else:
                break
            pass


def test(data: PowerBuffer):
    print(data.get_data()[0])


if __name__ == "__main__":
    range_freq = RangeFreq(2401, 2483, 0.5)

    test = SweepPower(test, 100, range_freq)  # type: ignore
    test.start()
