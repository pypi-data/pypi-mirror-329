import time

class CountDown:
    def __init__(self):
        pass;

    def counting(self):
        my_time = int(input("Countdown: "))
        for x in range(my_time, 0, -1):
            seconds = x % 60
            minutes = int(x / 60) % 60
            hours = int(x / 3600)
            print(f"\r{hours:02}:{minutes:02}:{seconds:02}", end="", flush=True)
            time.sleep(1)