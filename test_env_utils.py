"""
tests/test_env_utils.py
=======================
Basic tests for get_env_var and list_env_connections.
Run with: pytest
"""

import os
import pytest
from pyenvdemo import get_env_var, list_env_connections


def test_get_env_var_returns_value(monkeypatch):
    monkeypatch.setenv("DB_SERVER", "test-server.database.windows.net")
    assert get_env_var("DB_SERVER") == "test-server.database.windows.net"


def test_get_env_var_returns_default_when_missing():
    result = get_env_var("NONEXISTENT_VAR", default="fallback")
    assert result == "fallback"


def test_get_env_var_warns_when_missing_no_default():
    with pytest.warns(UserWarning, match="NONEXISTENT_VAR"):
        result = get_env_var("NONEXISTENT_VAR")
    assert result is None


def test_list_env_connections_returns_list(monkeypatch):
    monkeypatch.setenv("DB_SERVER", "test-server")
    results = list_env_connections()
    assert isinstance(results, list)
    assert all("platform" in r and "variable" in r and "is_set" in r for r in results)


def test_list_env_connections_detects_set_var(monkeypatch):
    monkeypatch.setenv("SNOWFLAKE_ACCOUNT", "xy12345.us-east-1")
    results = list_env_connections()
    snowflake_account = next(r for r in results if r["variable"] == "SNOWFLAKE_ACCOUNT")
    assert snowflake_account["is_set"] is True
    assert snowflake_account["platform"] == "Snowflake"
