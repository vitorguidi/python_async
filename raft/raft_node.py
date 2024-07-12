import enum
from typing import List, Self

class RaftState(enum.Enum):
    follower = 0
    candidate = 1
    leader = 2

class RaftNode():
    def __init__(self, node_id: int):
        self.id = node_id
        self.peers = []
        # volatile state
        self.commitIndex = None
        self.lastApplied = None
        # volatile leader state
        self.nextIndex = []
        self.matchIndex = []
        # persistent state
        self.current_term = 0
        self.voted_for = None
        self.log = []

    def set_peers(self, nodes: List[Self]):
        self.peers = filter(lambda x: self.id != x.id, nodes)


