import heapq
import random


class Task:
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)

    def __lt__(self, other):
        return self.taskid < other.taskid

class SystemCall:
    def handle(self):
        pass

class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)

class Scheduler:
    def __init__(self):
        self.ready = []
        self.taskmap = {}
        self.time = 0

    def new(self, target):
        newTask = Task(target)
        self.taskmap[newTask.tid] = newTask
        self.schedule(newTask)

    def schedule(self, task):
        heapq.heappush(self.ready, (self.time + random.randrange(10), task))

    def exit(self, task):
        del self.taskmap[task.tid]

    def mainloop(self):
        while self.taskmap:
            (task_time, task) = heapq.heappop(self.ready)
            if self.time < task_time:
                self.time = task_time
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                self.schedule(task)
            except StopIteration:
                self.exit(task)


def looper(x, identifier):
    for i in range(x):
        yield i, identifier

def foo():
    my_tid = yield GetTid()
    for i in range(5):
        yield f'Foo just ran with tid = {my_tid}'


sched = Scheduler()

sched.new(foo())

sched.mainloop()
