"""Shared fixtures. Data is loaded once per session, not once per test."""
import pandas as pd
import pytest

from capstone import paths


@pytest.fixture(scope="session")
def waiting():
    return pd.read_csv(paths.WAITING_LISTS_CSV)


@pytest.fixture(scope="session")
def staffing():
    return pd.read_csv(paths.STAFFING_CSV)


@pytest.fixture(scope="session")
def health():
    return pd.read_csv(paths.HEALTH_INFO_CSV)


@pytest.fixture(scope="session")
def diet():
    return pd.read_csv(paths.DIET_INFO_CSV)


@pytest.fixture(scope="session")
def statins():
    return pd.read_csv(paths.STATINS_ZIP, compression="zip", low_memory=False)


@pytest.fixture(scope="session")
def attendances():
    return pd.read_csv(paths.ATTENDANCES_CSV, parse_dates=["arrival_datetime"])


@pytest.fixture(scope="session")
def observations():
    return pd.read_csv(paths.OBSERVATIONS_CSV)
