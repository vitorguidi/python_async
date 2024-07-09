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
            print(f'popped task {task.tid} at time {task_time}')
            try:
                result = task.run()
                print(result)
                self.schedule(task)
            except StopIteration:
                self.exit(task)


def looper(x, identifier):
    for i in range(x):
        yield i, identifier


sched = Scheduler()

sched.new(looper(20, 'bob'))
sched.new(looper(35, 'sandra'))

sched.mainloop()
