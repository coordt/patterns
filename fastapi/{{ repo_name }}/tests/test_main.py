"""Tests for the main entrypoint."""


def test_main_module_imports():
    """The app successfully imports and configures itself."""
    from {{ package_name }} import main

    assert main.app
