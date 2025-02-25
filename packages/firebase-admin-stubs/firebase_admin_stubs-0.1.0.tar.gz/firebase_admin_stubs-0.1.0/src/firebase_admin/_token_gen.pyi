import google.auth
from _typeshed import Incomplete
from firebase_admin import _auth_utils, exceptions as exceptions
from google.auth import transport

ID_TOKEN_ISSUER_PREFIX: str
ID_TOKEN_CERT_URI: str
COOKIE_ISSUER_PREFIX: str
COOKIE_CERT_URI: str
MIN_SESSION_COOKIE_DURATION_SECONDS: Incomplete
MAX_SESSION_COOKIE_DURATION_SECONDS: Incomplete
MAX_TOKEN_LIFETIME_SECONDS: Incomplete
FIREBASE_AUDIENCE: str
RESERVED_CLAIMS: Incomplete
METADATA_SERVICE_URL: str
ALGORITHM_RS256: str
ALGORITHM_NONE: str
AUTH_EMULATOR_EMAIL: str

class _EmulatedSigner(google.auth.crypt.Signer):
    key_id: Incomplete
    def __init__(self) -> None: ...
    def sign(self, message): ...

class _SigningProvider:
    def __init__(self, signer, signer_email, alg=...) -> None: ...
    @property
    def signer(self): ...
    @property
    def signer_email(self): ...
    @property
    def alg(self): ...
    @classmethod
    def from_credential(cls, google_cred): ...
    @classmethod
    def from_iam(cls, request, google_cred, service_account): ...
    @classmethod
    def for_emulator(cls): ...

class TokenGenerator:
    ID_TOOLKIT_URL: str
    app: Incomplete
    http_client: Incomplete
    request: Incomplete
    base_url: Incomplete
    def __init__(self, app, http_client, url_override: Incomplete | None = None) -> None: ...
    @property
    def signing_provider(self): ...
    def create_custom_token(self, uid, developer_claims: Incomplete | None = None, tenant_id: Incomplete | None = None): ...
    def create_session_cookie(self, id_token, expires_in): ...

class CertificateFetchRequest(transport.Request):
    def __init__(self, timeout_seconds: Incomplete | None = None) -> None: ...
    @property
    def session(self): ...
    @property
    def timeout_seconds(self): ...
    def __call__(self, url, method: str = 'GET', body: Incomplete | None = None, headers: Incomplete | None = None, timeout: Incomplete | None = None, **kwargs): ...

class TokenVerifier:
    request: Incomplete
    id_token_verifier: Incomplete
    cookie_verifier: Incomplete
    def __init__(self, app) -> None: ...
    def verify_id_token(self, id_token, clock_skew_seconds: int = 0): ...
    def verify_session_cookie(self, cookie, clock_skew_seconds: int = 0): ...

class _JWTVerifier:
    project_id: Incomplete
    short_name: Incomplete
    operation: Incomplete
    url: Incomplete
    cert_url: Incomplete
    issuer: Incomplete
    articled_short_name: Incomplete
    def __init__(self, **kwargs) -> None: ...
    def verify(self, token, request, clock_skew_seconds: int = 0): ...

class TokenSignError(exceptions.UnknownError):
    def __init__(self, message, cause) -> None: ...

class CertificateFetchError(exceptions.UnknownError):
    def __init__(self, message, cause) -> None: ...

class ExpiredIdTokenError(_auth_utils.InvalidIdTokenError):
    def __init__(self, message, cause) -> None: ...

class RevokedIdTokenError(_auth_utils.InvalidIdTokenError):
    def __init__(self, message) -> None: ...

class InvalidSessionCookieError(exceptions.InvalidArgumentError):
    def __init__(self, message, cause: Incomplete | None = None) -> None: ...

class ExpiredSessionCookieError(InvalidSessionCookieError):
    def __init__(self, message, cause) -> None: ...

class RevokedSessionCookieError(InvalidSessionCookieError):
    def __init__(self, message) -> None: ...
