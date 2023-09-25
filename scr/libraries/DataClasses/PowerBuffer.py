from numpy import ndarray
import struct
import numpy as np
from DataClasses.Task import PowerTask


class PowerBuffer:
    def __init__(self, task: PowerTask) -> None:
        self._buffer = []
        self._task: PowerTask = task
        self._list_freq = np.arange(
            self._task.range_freq.min_freq,
            self._task.range_freq.max_freq,
            self._task.range_freq.bin_size,
        )

    def __len__(self):
        return len(self._buffer)

    @property
    def task(self):
        return self._task

    def get_freq(self) -> ndarray:
        return self._list_freq

    def append(self, data: bytes) -> None:
        self.buffering(data)

    def buffering(self, data: bytes) -> None:
        self._buffer.append(data)

    def get_data(self) -> ndarray:
        data = self._unpack_data()
        return data

    def zeroing_data(self) -> None:
        self._buffer = []

    def _unpack_data(self) -> ndarray:
        data = np.frombuffer(self._buffer[0][16:], dtype="<f4")
        quantity_freq = len(data)

        size_y = int((len(self._buffer) * quantity_freq) / len(self._list_freq))
        size_x = len(self._list_freq)
        size_buf = (size_x, size_y)

        unpack_data = np.full(size_buf, None, dtype="float32")
        for buf in self._buffer:
            freq = struct.unpack("QQ", buf[:16])

            point_data = int(
                (int(freq[0] * 10e-7) - self._list_freq[0])
                // self._task.range_freq.bin_size
            )

            data = np.frombuffer(buf[16:], dtype="<f4")

            for i in range(len(data)):
                if (point_data + i) >= len(self._list_freq):
                    continue

                line = unpack_data[point_data + i]
                unpack_data[point_data + i] = np.hstack((data[i], line[:-1]))

        return unpack_data
