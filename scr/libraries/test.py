import subprocess
import time


def test():
    cmdline = ["hackrf_sweep", "-f", "{}:{}".format(2401, 2408)]
    _process = subprocess.Popen(
        cmdline,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        # universal_newlines=False,
    )
    while True:
        print(_process.stdout.readline())

        time.sleep(0.5)
        print("timer")
        count = 0
        for i in _process.stdout:
            print(count)
            print(i)
            count += 1
        
        time.sleep(5)

        _process = subprocess.check_output(
        cmdline,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        # universal_newlines=False,
        )
        
        
        # print(_process.stdout.readlines())
        # try:
        #     buf = _process.stdout.read(4)
        # except AttributeError as e:
        #     print(e, file=sys.stderr)
        #     continue

        # if buf:
        #     print()
        #     (record_length,) = struct.unpack('I', buf)
        #     try:
        #         buf = _process.stdout.read(record_length)
        #     except AttributeError as e:
        #         print(e, file=sys.stderr)
        #         continue
        #     if buf:
        #         _bufering(buf)
        #     else:
        #         break
        # else:
        #     break


test()
