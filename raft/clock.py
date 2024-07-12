class Clock:
    def __init__(self):
        self.time = 0

    def get_time(self):
        return self.time

    def set_time(self,time: int):
        self.time = time