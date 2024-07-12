import enum
from typing import List, Self

from raft.clock import Clock
from raft.rpc import AppendEntriesRequest, AppendEntriesResponse, RequestVoteRequest, RequestVoteResponse


class RaftState(enum.Enum):
    follower = 0
    candidate = 1
    leader = 2


class RaftNode:
    def __init__(self, node_id: int, clock: Clock):
        self.inbox = []
        self.clock = clock
        self.state = RaftState.follower
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
        self.nextIndex = [0 for i in range(self.peers)]
        self.matchIndex = [0 for i in range(self.peers)]

    def handle_append_entries(self, req: AppendEntriesRequest):
        resp = AppendEntriesResponse(self.id, req.sender, req.term, False)
        yield resp

    def handle_request_vote(self, req: RequestVoteRequest):
        resp = RequestVoteResponse(self.id, req.sender, req.term, False)
        yield resp

    def tick_for_election(self):
        pass
        # this will be tricky, it runs concurrently with answering rpcs
        # how can I avoid this from running concurrently with rpcs?
