# plyvel-stubs

Type stubs for [plyvel](https://github.com/wbolster/plyvel), a Python interface
to LevelDB.

## Installation

```bash
pip install plyvel-stubs
```

## Usage

These stubs provide type information for the plyvel package. Once installed,
your type checker (like mypy, pyright, or Pylance) will automatically use these
stubs when checking code that uses plyvel.

## Supported Types

The package provides type information for:

- `DB` class for LevelDB database operations
- `WriteBatch` class for batch operations
- `PrefixedDB` class for prefix-based database operations

## Example

```python
from plyvel import DB

db = DB("/path/to/db", create_if_missing=True)
db.put(b"key", b"value")
value = db.get(b"key")  # Type: Optional[bytes]

# Using with context manager
with db.write_batch() as batch:
    batch.put(b"key1", b"value1")
    batch.put(b"key2", b"value2")

# Using prefix database
prefixed_db = db.prefixed_db(b"prefix-")
prefixed_db.put(b"key", b"value")  # Will store as "prefix-key"
```

## Development

This package contains only type stubs (.pyi files) for the plyvel package. It
does not contain any runtime code.

## License

MIT License - see LICENSE file for details.
