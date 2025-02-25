import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run only integration tests (tests decorated with `pytest.mark.integration`)",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "integration: mark test as an integration test")


def pytest_collection_modifyitems(config: pytest.Config, items) -> None:
    if config.getoption("--integration"):
        skip_non_integration = pytest.mark.skip(reason="not an integration test")
        for item in items:
            if "integration" not in item.keywords:
                item.add_marker(skip_non_integration)
    else:
        skip_non_unit_test = pytest.mark.skip(reason="not a unit test")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_non_unit_test)
