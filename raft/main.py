import heapq

from typing import NamedTuple, List


class SchedulerEntry(NamedTuple):
    time: int
    entry: any

    def __lt__(self, other):
        return self.time < other.time


class Scheduler:
    def __init__(self):
        self.pq: List[SchedulerEntry] = []

    def schedule(self, time: int, entry: any):
        heapq.heappush(self.pq, SchedulerEntry(time, entry))

    def get(self):
        return heapq.heappop(self.pq)

if __name__ == '__main__':
    pass
