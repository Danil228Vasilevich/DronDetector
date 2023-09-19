import numpy as np
import threading as Tread
import subprocess
import struct
import sys
import copy
from math import ceil
from numpy import ndarray


from DataClasses.PowerBuffer import PowerBuffer
from DataClasses.DataFreq import RangeFreq
from DataClasses.Task import PowerTask


class SweepPower:
    def __init__(self, call_back_func, task: PowerTask) -> None:
        # settings hack_rf
        self._call_back_func = call_back_func
        self._task = task

        # --------------------------tread----------------------------------
        self._is_alive = False
        self._event_read_tread: Tread.Event
        self._read_tread: Tread.Thread
        self._buffer: PowerBuffer

        self._limit_len_buffer: int

    def get_alive(self):
        return self._is_alive

    def start(self) -> None:
        self._event_read_tread = Tread.Event()
        self._read_tread = Tread.Thread(
            target=self._read_data, args=(self._event_read_tread,)
        )
        self._list_freq = np.arange(
            self._task.range_freq.min_freq,
            self._task.range_freq.max_freq,
            self._task.range_freq.bin_size,
        )

        # тут блять не всегда 5 сука надо думать как
        amount_freq = ceil(ceil(20 / self._task.range_freq.bin_size) / 4)
        amount_freq = amount_freq if amount_freq % 2 else amount_freq + 1
        print(amount_freq)

        self._limit_len_buffer = ceil(
            self._task.sample_length
            * (
                (self._task.range_freq.max_freq - self._task.range_freq.min_freq)
                / self._task.range_freq.bin_size
            )
            / amount_freq
        )
        print(self._limit_len_buffer)

        self._buffer = PowerBuffer(self._task)
        cmdline = [
            "hackrf_sweep",
            "-f",
            "{}:{}".format(
                int(self._task.range_freq.min_freq), int(self._task.range_freq.max_freq)
            ),
            "-B",
            "-w",
            "{}".format(int(self._task.range_freq.bin_size * 1e6)),
            "-l",
            "{}".format(int(self._task.lna_gain)),
            "-g",
            "{}".format(int(self._task.vga_gain)),
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
