from enum import IntEnum

class JobTypes(IntEnum):
    INACTIVE = 0
    FINISHED = 1
    QUEUED = 2
    CANCELLED = 3
    FAILED = 4
    EXECUTING = 5