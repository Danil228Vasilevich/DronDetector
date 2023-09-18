import subprocess
import time


def test():
    cmdline = ["hackrf_sweep", "-f", "2401:2483"]
    _process = subprocess.Popen(
        cmdline,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        # universal_newlines=False,
    )
    ex = 2
    old_time = time.time()
    datas = []
    while True:
        new_time = time.time()
        if new_time - old_time > 2:
            print(len(datas))
            old_time = time.time()
            datas = []
        
        if _process is not None: data = _process.stdout.readline()

        datas.append(data)

        # time.sleep(1)
        # print("timer")
        # count = 0
        # _process.terminate()
        # data = _process.stdout.readlines()
        # print(data, len(data))
        #print(len(_process.stdout.readlines()))
        
        #time.sleep(5)
        
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
