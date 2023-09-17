import numpy as np
import threading as Tread
import subprocess
import struct
import sys

from DataClasses.PowerBufer import PowerBufer

class SweepPower:
    def __init__(
        self,
        call_back_func,
        len_bufer: int,
        start_freq: float = 2401,
        stop_freq: float = 2483,
        bin_size: float = 1,
        gain: float = 40
    ) -> None:
        # settings hack_rf
        self._freq = (start_freq, stop_freq)
        self._call_back_func = call_back_func
        self._len_bufer = len_bufer
        self._bin_size = bin_size
        if gain < 0:
            gain = 0
        if gain > 102:
            gain = 102
        self._lna_gain = 8 * (gain // 18)
        self._vga_gain = 2 * ((gain - self._lna_gain) // 2)
        self._list_freq = np.arange(
            self._freq[0] ,
            self._freq[1] ,
            self._bin_size,
        )

        #--------------------------tread----------------------------------
        self._is_alive = False
        self._event_read_tread: Tread.Event
        self._read_tread: Tread.Thread
        
        self._bufer: PowerBufer
    
    def get_alive(self):
        return self._is_alive

    def new_freq(self, min_freq: float, max_freq: float):
        is_alive = self._is_alive

        self.stop()
        self._freq = (min_freq, max_freq)

        if is_alive: self.start()

    def start(self) -> None:
        self._event_read_tread = Tread.Event()
        self._read_tread = Tread.Thread(target=self._read_data, args=(self._event_read_tread,))
        self._list_freq = np.arange(
            self._freq[0] ,
            self._freq[1] ,
            self._bin_size,
        )
        self._bufer = PowerBufer(self._list_freq)
        cmdline = [
                        "hackrf_sweep",
                        "-f", "{}:{}".format(int(self._freq[0]),
                                int(self._freq[1])),
                        "-B",
                        "-w", "{}".format(int(self._bin_size*1e6)),
                        "-l", "{}".format(int(self._lna_gain)),
                        "-g", "{}".format(int(self._vga_gain))
            ]
        self._process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                            universal_newlines=False)
        self._is_alive = True
        self._read_tread.start()

    def stop(self) -> None:
        self._event_read_tread.set()

        if self._process:
            self._process.terminate()

    def _return_data(self) -> None:
        self._call_back_func(self._bufer)
        if isinstance(self._bufer, PowerBufer): self._bufer.zeroing_data()
        else: print("error bufer not PowerBufer")
        

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

    def _bufering(self, data) -> None:
        
        self._bufer.append(data)

        # 5 -> standart_bin_size в hackrf_sweep
        if len(self._bufer) * int(5/self._bin_size) >= self._len_bufer*len(self._list_freq): self._return_data()

            

    def _read_data(self, event) -> None:
        while self._is_alive:
            
            if event.is_set():break
            
            if self._process.stdout is None:
                print(file=sys.stderr)
                continue

            buf = self._process.stdout.read(4)
            
            if buf:
                (record_length,) = struct.unpack('I', buf)
                try:
                    buf = self._process.stdout.read(record_length)
                except AttributeError as e:
                    print(e, file=sys.stderr)
                    continue
                if buf:
                    
                    self._bufering(buf)
                else:
                    break
            else:
                break
            pass





def test(data:PowerBufer):
    print(123)
    print(len(data.get_data()))
    print(len(data.get_freq()))

if __name__ == "__main__":
    test = SweepPower(test, 100) # type: ignore
    test.start()