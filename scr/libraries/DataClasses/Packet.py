class Packet:
    def __init__(
        self,
        center_freq: float,
        channel_width: float,
        channel_hight: float,
        power_signal: float,
    ) -> None:
        self._center_freq: float
        self._channel_width: float
        self._channel_hight: float
        self._power_signal: float

        # ------------------check_setter_data---------------------
        if channel_width <= 0:
            raise Exception("drone width channel <= 0")
        if channel_hight <= 0:
            raise Exception("drone hight channel <= 0")
        if center_freq - channel_width / 2 < 0:
            raise Exception("drone start freq < 0")
        if power_signal > 100:
            raise Exception("Drone power signal too big")

        # ------------------set_data-------------------------------

        self._center_freq = center_freq
        self._channel_hight = channel_hight
        self._channel_width = channel_width
        self._power_signal = power_signal

    @property
    def power_signal(self):
        return self._power_signal

    @property
    def center_freq(self):
        return self._center_freq

    @property
    def channel_width(self):
        return self._channel_width

    @property
    def start_freq(self):
        return self._center_freq - (self._channel_width / 2)

    @property
    def stop_freq(self):
        return self._center_freq + (self._center_freq / 2)
