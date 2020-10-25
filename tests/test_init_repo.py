# 3rd party
import pytest
import requests.exceptions
from apeye.requests_url import RequestsURL
from domdf_python_tools.paths import PathPlus
from pytest_git import GitRepo  # type: ignore

# this package
from repo_helper.cli.commands.init import init_repo
from tests.common import check_file_output

has_internet = True
try:
	RequestsURL("https://raw.githubusercontent.com").head(timeout=10)
except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
	has_internet = False


@pytest.mark.skipif(condition=not has_internet, reason="Requires internet connection.")
def test_init_repo(git_repo: GitRepo, demo_environment, file_regression, data_regression):
	demo_environment.globals["copyright_years"] = "2020-2021"
	demo_environment.globals["author"] = "Joe Bloggs"
	demo_environment.globals["email"] = "j.bloggs@example.com"
	demo_environment.globals["license"] = "MIT License"
	demo_environment.globals["version"] = "1.2.3"
	demo_environment.globals["enable_docs"] = True
	demo_environment.globals["travis_site"] = "com"
	demo_environment.globals["docker_shields"] = False
	demo_environment.globals["docker_name"] = ''
	demo_environment.globals["enable_pre_commit"] = True

	repo_path = PathPlus(git_repo.workspace)
	managed_files = init_repo(repo_path, demo_environment)

	for file in managed_files:
		assert (repo_path / file).exists(), file

	listing = []
	for path in repo_path.rglob("*.*"):
		path = path.relative_to(repo_path)
		if not path.parts[0] == ".git":
			listing.append(path.as_posix())

	listing.sort()

	data_regression.check(listing)
	# assert set(listing) == set(managed_files)

	assert (repo_path / "requirements.txt").read_text() == ''
	check_file_output(repo_path / "README.rst", file_regression, extension=".README.rst")
	check_file_output(repo_path / "LICENSE", file_regression, extension=".LICENSE.txt")

	assert (repo_path / "hello_world").is_dir()
	check_file_output(repo_path / "hello_world" / "__init__.py", file_regression, extension=".init._py_")

	assert (repo_path / "tests").is_dir()
	assert (repo_path / "tests/requirements.txt").read_text() == ''
	assert (repo_path / "tests" / "__init__.py").read_text() == ''

	assert (repo_path / "doc-source").is_dir()
	check_file_output(
			repo_path / "doc-source/index.rst",
			file_regression,
			extension=".docs_index.rst",
			)
	assert (repo_path / "doc-source" / "api").is_dir()
	check_file_output(
			repo_path / "doc-source/api/hello-world.rst",
			file_regression, extension=".docs_hello-world.rst"
			)
