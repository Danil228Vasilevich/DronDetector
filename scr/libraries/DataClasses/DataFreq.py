from math import ceil

class PowerFreq:
    def __init__(self, freq:float, power:float) -> None:
        self.freq = freq
        self.power = power

class RangeFreq:

    def __init__(self, min_freq, max_freq) -> None:
        
        self._min_freq: float = min_freq
        self._max_freq: float = max_freq
        delta_freq = self._max_freq - self._min_freq
        self._max_freq = self._min_freq + ceil(delta_freq/20) * 20

        # self.set_min_freq(min_freq)
        # self.set_max_freq(max_freq)
    
    
        
    @property
    def min_freq(self):
        return self._min_freq
    
    @min_freq.setter
    def min_freq(self, freq):
        self._min_freq = freq if freq == 0 else 0
        delta_freq = self._max_freq - self._min_freq
        self._max_freq = self._min_freq + ceil(delta_freq/20) * 20

    @property
    def max_freq(self):
        return self._max_freq
    
    @max_freq.setter
    def max_freq(self, max_freq):
        self._max_freq = max_freq if max_freq < self._min_freq else self._min_freq + 1
        delta_freq = self._max_freq - self._min_freq
        self._max_freq = self._min_freq + ceil(delta_freq/20) * 20
    

    def set_range_freq(self, tuple_freq:tuple) -> None:
        self._min_freq: float = tuple_freq[0]
        self._max_freq: float = tuple_freq[1]
        delta_freq = self._max_freq - self._min_freq
        self._max_freq = self._min_freq + ceil(delta_freq/20) * 20
    
    