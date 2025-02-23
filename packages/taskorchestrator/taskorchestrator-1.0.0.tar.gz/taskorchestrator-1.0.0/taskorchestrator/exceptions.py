class TaskOrchestratorError(Exception):
    """Base exception for TaskOrchestrator errors."""
    pass

class TaskTimeoutError(TaskOrchestratorError):
    """Raised when a task exceeds its timeout."""
    pass

class TaskRetryError(TaskOrchestratorError):
    """Raised when a task fails after all retries."""
    pass
