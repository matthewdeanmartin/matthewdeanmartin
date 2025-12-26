All libraries will be installed. DO NOT ADD if-blocks around imports to provide fallbacks if a library fails to import.

Activating venv - either the usual way, with ./.venv or prefix commands with `uv run`

Always type annotate your python code.

Prefer pathlib over non-pathlib solution, i.e. avoid using str Paths.

## Code under test

src folder, do not attempt to unit test anything outside of src

## Unit testing

Use pytest. Prefer to not put tests into classes, but as stand alone functions.

Prefer integration testing over mocking everything.

Do not do tests that asserts on "raises". These tests are often contrived, low value.

Use tmp_path fixture instead of mocking the file system.

If you set os.environ you have to undo what you did to it at end of test