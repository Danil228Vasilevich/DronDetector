from math import ceil

from DataClasses.DataFreq import RangeFreq


class PowerTask:
    def __init__(
        self,
        range_freq: RangeFreq,
        sample_length: int,
        gain: float = 40,
    ) -> None:
        self.range_freq: RangeFreq = range_freq
        self._sample_length = sample_length if sample_length > 0 else 1

        if gain < 0:
            gain = 0
        if gain > 102:
            gain = 102
        self._lna_gain = 8 * (gain // 18)
        self._vga_gain = 2 * ((gain - self._lna_gain) // 2)

        # print(self._bin_size)

    @property
    def sample_length(self):
        return self._sample_length

    @sample_length.setter
    def sample_length(self, sample_length):
        self._sample_length = sample_length if sample_length > 0 else 1

    @property
    def gain(self):
        return {"lna_gain": self._lna_gain, "vga_gain": self._vga_gain}

    @gain.setter
    def gain(self, gain):
        if gain < 0:
            gain = 0
        elif gain > 102:
            gain = 102
        self._lna_gain = 8 * (gain // 18)
        self._vga_gain = 2 * ((gain - self._lna_gain) // 2)

    @property
    def vga_gain(self):
        return self._vga_gain

    @property
    def lna_gain(self):
        return self._lna_gain
