from _typeshed import Incomplete

INVALID_ARGUMENT: str
FAILED_PRECONDITION: str
OUT_OF_RANGE: str
UNAUTHENTICATED: str
PERMISSION_DENIED: str
NOT_FOUND: str
CONFLICT: str
ABORTED: str
ALREADY_EXISTS: str
RESOURCE_EXHAUSTED: str
CANCELLED: str
DATA_LOSS: str
UNKNOWN: str
INTERNAL: str
UNAVAILABLE: str
DEADLINE_EXCEEDED: str

class FirebaseError(Exception):
    def __init__(self, code, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...
    @property
    def code(self): ...
    @property
    def cause(self): ...
    @property
    def http_response(self): ...

class InvalidArgumentError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class FailedPreconditionError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class OutOfRangeError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class UnauthenticatedError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class PermissionDeniedError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class NotFoundError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class ConflictError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class AbortedError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class AlreadyExistsError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class ResourceExhaustedError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class CancelledError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class DataLossError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class UnknownError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class InternalError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class UnavailableError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class DeadlineExceededError(FirebaseError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...
