# CLAUDE.md - Beem Development Guide

## Project Overview

Beem is an unofficial Python library for HIVE, STEEM, and BLURT blockchains. It's a complete reimplementation based on python-bitshares and python-graphenelib (by Fabian Schuh). The library provides:

- High unit test coverage
- WebSocket node support with native Appbase calls
- Node error handling with automatic failover
- CLI tool (`beempy`) built with Click
- Blockchain object caching
- Transaction broadcasting support

**Current Version:** 0.26.1
**License:** MIT
**Supported Python:** 3.6, 3.7, 3.8, 3.9 (3.12 in progress)

## Tech Stack

**Core Dependencies:**
- `ecdsa` - Elliptic curve digital signatures
- `requests` - HTTP library
- `websocket-client` - WebSocket connections
- `pycryptodomex` - Cryptography
- `scrypt` - Key derivation
- `Click` / `click_shell` - CLI framework
- `ruamel.yaml` - YAML parsing

**Development Tools:**
- pytest, pytest-mock, pytest-cov (testing)
- tox (multi-version testing)
- flake8, pylint (linting)
- bandit (security scanning)
- sphinx (documentation)

## Directory Structure

```
beem/                    # Main package (40+ modules)
├── account.py          # Account operations
├── blockchain.py       # Blockchain interface
├── cli.py              # beempy CLI (217KB, 100+ commands)
├── hive.py/steem.py/blurt.py  # Chain-specific implementations
├── wallet.py           # Wallet management
├── comment.py          # Comment/post operations
├── transactionbuilder.py  # Transaction construction
└── exceptions.py       # Custom exceptions

beemapi/                # API layer
├── graphenerpc.py      # Graphene RPC client
└── noderpc.py          # Node RPC wrapper

beembase/               # Base operations
├── operations.py       # All blockchain operations
├── operationids.py     # Operation ID mapping
└── memo.py             # Memo encryption/decryption

beemstorage/            # Storage backends
├── sqlite.py           # SQLite storage
├── ram.py              # In-memory storage
└── masterpassword.py   # Encrypted storage

tests/beem/             # Test suite (43 test files)
examples/               # 30+ example scripts
docs/                   # Sphinx documentation
```

## Development Commands

**Testing:**
```bash
make test               # Run pytest
pytest                  # Direct pytest
tox                     # Multi-version testing
tox -e py38             # Specific Python version
tox -e short            # Quick tests
```

**Linting:**
```bash
make lint               # flake8 on main packages
tox -e flake8           # Full flake8 check
tox -e pylint           # pylint check
tox -e bandit           # Security scan
```

**Building:**
```bash
make build              # python3 setup.py build
make install            # System-wide install
make install-user       # User install
```

**Documentation:**
```bash
make docs               # Build Sphinx docs
```

## Key Files

| File | Purpose |
|------|---------|
| `setup.py` | Package definition, dependencies |
| `tox.ini` | Test environments, linting configs |
| `.flake8` | Linting rules (max-line=80, complexity=50) |
| `pytest.ini` | Test configuration |
| `.coveragerc` | Coverage settings |
| `Makefile` | Build automation |

**Entry Points:**
- CLI: `beempy` command (defined in setup.py as `beem.cli:cli`)
- Primary import: `from beem import Hive, Steem, Blurt`

## Coding Conventions

**Style:**
- UTF-8 encoding declaration on all files
- Max line length: 80 characters
- Flake8 ignored: E111, E114, E129, E501, F401, E722, E122

**Patterns:**
- Base class: `BlockchainObject` (dict-like with methods)
- Lazy loading for blockchain data
- Singleton: `shared_blockchain_instance()` pattern
- Cache support with `clear_cache()` methods
- Docstrings with `.. code-block:: python` examples

**Error Handling:**
- Custom exceptions in `beem/exceptions.py`
- Key exceptions: `AccountDoesNotExistsException`, `InvalidWifError`, `BlockDoesNotExistsException`

## CI/CD Notes

**CircleCI** (primary):
- Python 3.6, 3.7, 3.8, 3.9 matrix
- Uses Code Climate test reporter
- Config: `.circleci/config.yml`

**Travis CI:**
- Python 3.7, 3.8
- SonarCloud integration
- Config: `.travis.yml`

**AppVeyor:**
- Windows CI
- Config: `appveyor.yml`

## Quick Start

```python
from beem import Hive

# Connect to Hive blockchain
hive = Hive()

# Get account
from beem.account import Account
account = Account("username", blockchain_instance=hive)

# Get recent posts
from beem.comment import Comment
comment = Comment("@author/permlink", blockchain_instance=hive)
```

CLI usage:
```bash
beempy --help           # Show all commands
beempy info             # Node info
beempy account <name>   # Account details
```
