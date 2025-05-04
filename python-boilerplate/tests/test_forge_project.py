from pathlib import Path
from typing import Optional

import pytest
from pytest import param
from project_forge.testing import Forge

PATTERN_PATH = Path(__file__).parent.parent / "python_boilerplate" / "pattern.toml"


@pytest.mark.parametrize(["initial_context"], [
    param(None, id="Defaults"),
    param({"author": 'name "quote" name'}, id="Quoted value"),
    param({"author": "O'Connor"}, id="Apostrophe in value")
])
def test_forge_and_run_tests_is_successful(forger: Forge, initial_context: Optional[dict]):

    """Forging the pattern.toml file and running tests is successful."""
    with forger.forge(PATTERN_PATH, initial_context=initial_context) as result:
        assert result.project_path.isdir()
        assert forger.run_inside_dir("uv sync --group test", result.project_path) == 0
        result = forger.run_inside_dir("pytest", result.project_path)

        if result.returncode != 0:
            print("pytest error:", result.stdout, result.stderr)

        assert result.returncode == 0
