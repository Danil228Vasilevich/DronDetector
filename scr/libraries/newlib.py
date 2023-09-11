import numpy as np
import asyncio


class PokaXz:
    def __init__(
        self,
        call_back_func: function,
        exposure: float,
        start_freq: float = 2401,
        stop_freq: float = 2483,
        bin_size: float = 1,
        interval: float = 0.0,
        gain: float = 40,
        ppm: float = 0,
        crop: float = 0,
        device_rndex: int = 0,
        sample_rate: int = 20000000,
    ) -> None:
        # settings hack_rf
        self._freq = (start_freq, stop_freq)
        self._call_back_func = call_back_func
        self._bin_size = bin_size
        self._interval = interval
        self._sample_rate = sample_rate

        if gain < 0:
            gain = 0
        if gain > 102:
            gain = 102
        self._lna_gain = 8 * (gain // 18)
        self._vga_gain = 2 * ((gain - self._lna_gain) // 2)

        self._ppm = ppm
        self._crop = crop
        self._device_rndex = device_rndex

        self._list_freq = np.arange(
            self._freq[0] + self._bin_size / 2,
            self._freq[1] - self._bin_size / 2,
            self._bin_size,
        )

        self._is_alive = False

    def get_alive(self):
        return self._is_alive

    def new_freq(self, min_freq: float, max_freq: float):
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def _return_data(self):
        pass

    def singl_shot(self):
        self.Stop()
        self._is_alive = True
        cmdline = [
            "hackrf_sweep",
            "-f",
            "{}:{}".format(int(self._freq[0]), int(self._freq[1])),
            "-1",
            "-w",
            "{}".format(int(self._bin_size * 1e6)),
            "-l",
            "{}".format(int(self._lna_gain)),
            "-g",
            "{}".format(int(self._vga_gain)),
        ]
        data = subprocess.check_output(
            cmdline, universal_newlines=False, stderr=subprocess.DEVNULL
        )
        self._alive = False
        return self._list_freq, data

    async def _read_data(self):
        pass
