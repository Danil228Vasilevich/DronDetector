import numpy as np
import threading as Tread
import subprocess
import struct
import sys
import copy
from math import ceil


from DataClasses.PowerBuffer import PowerBuffer
from DataClasses.DataFreq import RangeFreq


class SweepPower:
    def __init__(
        self,
        call_back_func,
        len_buffer: int,
        freq: RangeFreq,
        bin_size: float = 1,
        gain: float = 40,
    ) -> None:
        # settings hack_rf
        self._freq = (freq.min_freq, freq.max_freq)
        self._call_back_func = call_back_func
        self._len_buffer = len_buffer

        if bin_size <= 1:
            Nsw = ceil(5/bin_size)
            Nsw = Nsw if Nsw%2  else Nsw + 1
            self._bin_size = 5/Nsw
        else: self._bin_size = 1

        if gain < 0:
            gain = 0
        if gain > 102:
            gain = 102
        self._lna_gain = 8 * (gain // 18)
        self._vga_gain = 2 * ((gain - self._lna_gain) // 2)
        self._list_freq = np.arange(
            self._freq[0],
            self._freq[1],
            self._bin_size,
        )

        # --------------------------tread----------------------------------
        self._is_alive = False
        self._event_read_tread: Tread.Event
        self._read_tread: Tread.Thread
        self._buffer: PowerBuffer

        self._limit_len_buffer: int

    def get_alive(self):
        return self._is_alive

    def new_freq(self, min_freq: float, max_freq: float):
        is_alive = self._is_alive

        self.stop()
        self._freq = (min_freq, max_freq)

        if is_alive:
            self.start()

    def start(self) -> None:
        self._event_read_tread = Tread.Event()
        self._read_tread = Tread.Thread(
            target=self._read_data, args=(self._event_read_tread,)
        )
        self._list_freq = np.arange(
            self._freq[0],
            self._freq[1],
            self._bin_size,
        )


        #тут блять не всегда 5 сука надо думать как
        amount_freq = ceil(ceil(20/self._bin_size)/4)
        amount_freq = amount_freq if amount_freq % 2 else amount_freq + 1
        print(amount_freq)

        self._limit_len_buffer = ceil(self._len_buffer * ((self._freq[1] - self._freq[0]) / self._bin_size) / amount_freq)
        print(self._limit_len_buffer)
        
        self._buffer = PowerBuffer(self._list_freq)
        cmdline = [
            "hackrf_sweep",
            "-f",
            "{}:{}".format(int(self._freq[0]), int(self._freq[1])),
            "-B",
            "-w",
            "{}".format(int(self._bin_size * 1e6)),
            "-l",
            "{}".format(int(self._lna_gain)),
            "-g",
            "{}".format(int(self._vga_gain)),
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

    # def singl_shot(self):
    #     self.stop()
    #     self._is_alive = True
    #     cmdline = [
    #         "hackrf_sweep",
    #         "-f",
    #         "{}:{}".format(int(self._freq[0]), int(self._freq[1])),
    #         "-1",
    #         "-w",
    #         "{}".format(int(self._bin_size * 1e6)),
    #         "-l",
    #         "{}".format(int(self._lna_gain)),
    #         "-g",
    #         "{}".format(int(self._vga_gain)),
    #     ]
    #     data = subprocess.check_output(
    #         cmdline, universal_newlines=False, stderr=subprocess.DEVNULL
    #     )
    #     self._alive = False
    #     return self._list_freq, data

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
    range_freq = RangeFreq(2401, 2483)
    
    test = SweepPower(test, 100, range_freq, 0.5)  # type: ignore
    test.start()
