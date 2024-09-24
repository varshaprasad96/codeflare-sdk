from enum import Enum
from dataclasses import dataclass


class AppWrapperStatus(Enum):
    """
    Defines the possible reportable phases of an AppWrapper.
    """

    SUSPENDED = "suspended"
    RESUMING = "resuming"
    RUNNING = "running"
    RESETTING = "resetting"
    SUSPENDING = "suspending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    TERMINATING = "terminating"


@dataclass
class AppWrapper:
    """
    For storing information about an AppWrapper.
    """

    name: str
    status: AppWrapperStatus
