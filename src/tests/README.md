# Tests

## Test Directory Convention

The `src/tests` directory's structure mirrors the layout of the Django application modules it tests.
This convention ensures a straightforward path mapping from application code to corresponding tests, though it's selectively applied to modules we choose to test.

Convention:
If a module in the application, such as `src/main/views.py` or `src/nurse/models.py`, has associated tests, those tests reside in a similarly structured path within `src/tests`.
Test modules are prefixed with `test_`, reflecting the module name they test.

Examples:

- Tests for `src/main/views.py` are found in `src/tests/main/test_views.py`
- Tests for `src/nurse/models.p` are located in `src/tests/nurse/test_models.py`
