# firebase-admin-stubs

Type stubs for the `firebase-admin` Python package.

## Installation

```bash
pip install firebase-admin-stubs
```

## Usage

These stubs provide type information for the `firebase-admin` package. They will be automatically used by type checkers like mypy when you import `firebase-admin`.

```python
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate('path/to/serviceAccount.json')
app = initialize_app(cred)
```

## Development

This package contains type stubs for the `firebase-admin` package. The stubs are manually curated to provide accurate type information for the Firebase Admin SDK.

## License

MIT
