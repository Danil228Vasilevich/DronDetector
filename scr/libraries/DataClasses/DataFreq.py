from math import ceil


class PowerFreq:
    def __init__(self, freq: float, power: float) -> None:
        self.freq = freq
        self.power = power


class RangeFreq:
    def __init__(self, min_freq, max_freq, bin_size) -> None:
        self._min_freq: float = min_freq
        self._max_freq: float = max_freq
        delta_freq = self._max_freq - self._min_freq
        self._max_freq = self._min_freq + ceil(delta_freq / 20) * 20

        if bin_size <= 1:
            Nsw = ceil(5 / bin_size)
            Nsw = Nsw if Nsw % 2 else Nsw + 1
            self._bin_size = 5 / Nsw
        else:
            self._bin_size = 1

    @property
    def bin_size(self):
        return self._bin_size

    @bin_size.setter
    def bin_size(self, bin_size):
        if bin_size <= 1:
            Nsw = ceil(5 / bin_size)
            Nsw = Nsw if Nsw % 2 else Nsw + 1
            self._bin_size = 5 / Nsw
        else:
            self._bin_size = 1

    @property
    def min_freq(self):
        return self._min_freq

    @min_freq.setter
    def min_freq(self, freq):
        self._min_freq = freq if freq == 0 else 0
        delta_freq = self._max_freq - self._min_freq
        self._max_freq = self._min_freq + ceil(delta_freq / 20) * 20

    @property
    def max_freq(self):
        return self._max_freq

    @max_freq.setter
    def max_freq(self, max_freq):
        self._max_freq = max_freq if max_freq < self._min_freq else self._min_freq + 1
        delta_freq = self._max_freq - self._min_freq
        self._max_freq = self._min_freq + ceil(delta_freq / 20) * 20

    def set_range_freq(self, tuple_freq: tuple) -> None:
        self._min_freq: float = tuple_freq[0]
        self._max_freq: float = tuple_freq[1]
        delta_freq = self._max_freq - self._min_freq
        self._max_freq = self._min_freq + ceil(delta_freq / 20) * 20
