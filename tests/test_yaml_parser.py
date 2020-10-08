import pytest
from pytest_regressions.data_regression import DataRegressionFixture

from repo_helper.yaml_parser import (
	get_gh_actions_python_versions, get_tox_python_versions,
	get_tox_travis_python_versions,
	)


@pytest.mark.parametrize("python_versions", [
		["3.6"],
		["3.6", "3.7"],
		["3.6", "3.7", "3.8"],
		["3.6", "3.7", "3.8", "3.9-dev"],
		["3.7", "3.8", "3.9-dev"],
		["3.7", "3.8"],
		["3.8"],
		])
def test_get_tox_python_versions(data_regression: DataRegressionFixture, python_versions):
	data_regression.check(get_tox_python_versions(python_versions))


@pytest.mark.parametrize("python_versions", [
		["3.6"],
		["3.6", "3.7"],
		["3.6", "3.7", "3.8"],
		["3.6", "3.7", "3.8", "3.9-dev"],
		["3.7", "3.8", "3.9-dev"],
		["3.7", "3.8"],
		["3.8"],
		])
def test_get_tox_travis_python_versions(data_regression: DataRegressionFixture, python_versions):
	data_regression.check(get_tox_travis_python_versions(python_versions, get_tox_python_versions(python_versions)))


@pytest.mark.parametrize("python_versions", [
		["3.6"],
		["3.6", "3.7"],
		["3.6", "3.7", "3.8"],
		["3.6", "3.7", "3.8", "3.9-dev"],
		["3.7", "3.8", "3.9-dev"],
		["3.7", "3.8"],
		["3.8"],
		])
def test_get_gh_actions_python_versions(data_regression: DataRegressionFixture, python_versions):
	data_regression.check(get_gh_actions_python_versions(python_versions, get_tox_python_versions(python_versions)))
