from typing import List


class Rpc:
    def __init__(self, sender: int, receiver: int):
        self.sender = sender
        self.receiver = receiver


class RequestVoteRequest(Rpc):
    def __init__(self, sender: int, receiver: int, term: int, candidate_id: int, last_log_index: int,
                 last_log_term: int):
        super().__init__(sender, receiver)
        self.term = term
        self.candidate_id = candidate_id
        self.last_log_index = last_log_index
        self.last_log_term = last_log_term


class RequestVoteResponse(Rpc):
    def __init__(self, sender: int, receiver: int, term: int, vote_granted: bool):
        super().__init__(sender, receiver)
        self.term = term
        self.vote_granted = vote_granted


class AppendEntriesRequest(Rpc):
    def __init__(self, sender: int, receiver: int, term: int, leader_id: int, prev_log_index: int, prev_log_term: int,
                 entries: List[any], leader_commit: int):
        super().__init__(sender, receiver)
        self.term = term
        self.leader_id = leader_id
        self.prev_log_index = prev_log_index
        self.prev_log_term = prev_log_term
        self.entries = entries
        self.leader_commit = leader_commit


class AppendEntriesResponse(Rpc):
    def __init__(self, sender: int, receiver: int, term: int, success: bool):
        super().__init__(sender, receiver)
        self.term = term
        self.success = success
