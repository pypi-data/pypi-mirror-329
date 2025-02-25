from _typeshed import Incomplete
from firebase_admin import App as App
from google.cloud import firestore

existing: Incomplete

def client(app: App | None = None, database_id: str | None = None) -> firestore.Client: ...

class _FirestoreService:
    def __init__(self, app: App) -> None: ...
    def get_client(self, database_id: str | None) -> firestore.Client: ...
