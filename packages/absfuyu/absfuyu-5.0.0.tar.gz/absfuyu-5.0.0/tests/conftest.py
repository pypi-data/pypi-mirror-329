"""
Global fixture

Version: 1.0.0
Date updated: 22/03/2024 (dd/mm/yyyy)
"""

import pytest


@pytest.fixture(scope="session")
def test_fixture_session():
    """This cache the fixture for current test session"""
    return None
