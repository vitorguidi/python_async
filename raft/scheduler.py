import heapq

from typing import NamedTuple, List

from raft.clock import Clock


class SchedulerEntry(NamedTuple):
    time: int
    entry: any
    taskId: int

    def __lt__(self, other):
        return self.time < other.time or (self.time == other.time and self.taskId < other.taskId)


class Scheduler:
    taskid = 0
    def __init__(self, clock: Clock):
        self.pq: List[SchedulerEntry] = []
        self.clock = clock

    def schedule(self, time: int, entry: any):
        heapq.heappush(self.pq, SchedulerEntry(time, entry, Scheduler.taskid))
        Scheduler.taskid += 1

    def get(self):
        return heapq.heappop(self.pq)