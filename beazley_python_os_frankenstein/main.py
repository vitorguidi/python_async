class Task:
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)

class SystemCall:
    def handle(self):
        pass

class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)

# Create a new task
class NewTask(SystemCall):
    def __init__(self,target):
        self.target = target
    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
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
        return newTask.tid

    def schedule(self, task):
        self.ready.append(task)

    def exit(self, task):
        del self.taskmap[task.tid]

    def mainloop(self):
        while self.taskmap:
            task = self.ready.pop(0)
            try:
                result = task.run()
                print(result)
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
                self.schedule(task)
            except StopIteration:
                print(f'exiting task {task.tid}')
                self.exit(task)

def foo():
    my_tid = yield GetTid()
    for i in range(5):
        yield f'Foo just ran with tid = {my_tid}'

def create_child():
    child = yield NewTask(foo())
    yield f'created child task {child}'


sched = Scheduler()

sched.new(create_child())

sched.mainloop()
