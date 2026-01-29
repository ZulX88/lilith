import time

class Uptime:
    start = time.time()
    @classmethod
    def seconds(cls):
        return time.time() - cls.start
    @classmethod
    def human(cls):
        s = int(cls.seconds())
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"