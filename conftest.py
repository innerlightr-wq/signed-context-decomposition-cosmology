"""Make the canonical top-level ``signedctx`` module importable during tests.

The repository ships **one** implementation: ``signedctx.py`` at the repository
root.  pytest prepends the directory containing this file (the rootdir) to
``sys.path``, so ``import signedctx`` resolves to that module no matter which
working directory ``pytest`` is invoked from.

This file exists only so that the import does not depend on the current working
directory.  It deliberately does *not* manipulate ``sys.path`` itself: an earlier
layout carried a second, older copy under ``src/`` together with a
``sys.path.insert`` in ``tests/conftest.py``, which silently redirected
``import signedctx`` to the stale copy.  Both are gone.  See
``docs/CODE_ARCHITECTURE.md``.
"""
