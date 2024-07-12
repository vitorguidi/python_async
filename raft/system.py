from raft.clock import Clock
from raft.raft_node import RaftNode
from raft.scheduler import Scheduler
class System:
    def __init__(self, replicas: int):
        self.clock = Clock()
        self.sched = Scheduler(self.clock)
        self.nodes = [RaftNode(i, clock) for i in range(replicas)]
        for node in self.nodes:
            node.set_peers(self.nodes)

    def loop(self):
        pass