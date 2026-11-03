"""
tasks/exceptions.py
Business and Domain Exceptions for Life Recovery Assistant (LRA).
"""

class LRAException(Exception):
    """Base exception for all domain and business errors in LRA."""
    def __init__(self, message: str = "A domain error occurred.", code: str = "domain_error"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class CapacityExceededError(LRAException):
    """Raised when daily planned duration exceeds allowed capacity threshold."""
    def __init__(self, message: str = "Total task duration exceeds daily allowed capacity."):
        super().__init__(message=message, code="capacity_exceeded")


class EmptyPlanCandidateError(LRAException):
    """Raised when no actionable or eligible tasks are available to form a plan."""
    def __init__(self, message: str = "No eligible pending tasks found for the requested date."):
        super().__init__(message=message, code="no_candidate_tasks")


class InvalidRecoveryStateError(LRAException):
    """Raised when attempting recovery session operations on an invalid task state."""
    def __init__(self, message: str = "Recovery action cannot be performed in the current state."):
        super().__init__(message=message, code="invalid_recovery_state")
