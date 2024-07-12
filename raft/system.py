from raft.raft_node import RaftNode
from raft.scheduler import Scheduler
class System:
    def __init__(self, replicas: int):
        self.sched = Scheduler()
        self.nodes = [RaftNode(i) for i in range(replicas)]
        for node in self.nodes:
            node.set_peers(self.nodes)

    def loop(self):
        pass