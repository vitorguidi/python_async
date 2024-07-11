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

class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid
    def handle(self):
        target_task = self.sched.taskmap.get(self.tid, None)
        if target_task:
            target_task.target.close()
            target_task.sendval = True
        else:
            target_task.sendval = False
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
    while True:
        yield f'Foo just ran with tid = {my_tid}'

def create_and_kill_child():
    my_tid = yield GetTid()
    yield f'create_and_kill_child just ran with tid={my_tid}'
    child = yield NewTask(foo())
    yield f'created child task {child}'
    yield KillTask(child)



sched = Scheduler()

sched.new(create_and_kill_child())

sched.mainloop()
