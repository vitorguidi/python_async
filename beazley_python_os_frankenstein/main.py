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

class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid
    def handle(self):
        result = self.sched.waitforexit(self.task, self.tid)
        self.task.sendval = result
        if not result:
            self.sched.schedule(self.task)

class Scheduler:
    def __init__(self):
        self.ready = []
        self.taskmap = {}
        self.exit_waiting = {}
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
        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)

    def waitforexit(self, task, waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid, []).append(task)
            return True
        else:
            return False

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

def foo(n):
    my_tid = yield GetTid()
    while n > 0:
        n = n-1
        yield f'Foo just ran with tid = {my_tid}'

def create_and_kill_child():
    my_tid = yield GetTid()
    yield f'create_and_kill_child just ran with tid={my_tid}'
    child = yield NewTask(foo(10))
    yield f'created child task {child}'
    yield WaitTask(child)
    yield f'child {child} finished, exiting now'



sched = Scheduler()

sched.new(create_and_kill_child())

sched.mainloop()
