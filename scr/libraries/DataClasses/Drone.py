from .Packet import Packet


class Drone:
    def __init__(self, packet: Packet) -> None:
        self._packages: list[Packet]
        self._center_freq: float
        self._channel_width: float
        self._power_signal: float

        self._packages.append(packet)

    # -----------------------------------getters--------------------------------------
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

    # ---------------------------------------------------------------------------------
    def is_your_packet(self, packet: Packet) -> bool:
        return False

    def packet_append(self, packet: Packet) -> bool:
        is_your = self.is_your_packet(packet)
        return is_your
