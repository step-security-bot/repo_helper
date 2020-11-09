#!/usr/bin/env python
#
#  pre_commit.py
"""
Configuration for `pre-commit <https://pre-commit.com>`_.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import functools
import pathlib
import posixpath
import re
from io import StringIO
from textwrap import indent
from typing import Iterable, List, MutableMapping, Union

# 3rd party
import attr
import jinja2
from apeye.url import URL
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from ruamel import yaml
from typing_extensions import Literal, TypedDict

# this package
from repo_helper.files import management

__all__ = ["GITHUB_COM", "make_github_url", "Hook", "Repo", "make_pre_commit"]

#: Instance of :class:`apeye.url.URL` that points to the GitHub website.
GITHUB_COM: URL = URL("https://github.com")


@functools.lru_cache()
def make_github_url(username: str, repository: str) -> URL:
	"""
	Construct a URL to a GitHub repository from a username and repository name.

	:param username: The username of the GitHub account that owns the repository.
	:param repository: The name of the repository.
	"""

	return GITHUB_COM / username / repository


class _BaseHook(TypedDict):
	#: Which hook from the repository to use.
	id: str  # noqa: A003


class Hook(_BaseHook, total=False):
	"""
	Represents a pre-commit hook.
	"""

	#: Allows the hook to be referenced using an additional id when using pre-commit run <hookid>.
	alias: str

	#: Override the name of the hook - shown during hook execution.
	name: str

	#: Override the language version for the hook. See https://pre-commit.com/#overriding-language-version
	language_version: str

	#: Override the default pattern for files to run on.
	files: str

	#: File exclude pattern.
	exclude: str

	#: Override the default file types to run on. See https://pre-commit.com/#filtering-files-with-types.
	types: List[str]

	#: File types to exclude.
	exclude_types: List[str]

	#: List of additional parameters to pass to the hook.
	args: List[str]

	stages: List[Literal["commit", "merge-commit", "push", "prepare-commit-msg", "commit-msg", "manual"]]
	"""
	Confines the hook to the commit, merge-commit, push, prepare-commit-msg, commit-msg,
	post-checkout, or manual stage.
	See https://pre-commit.com/#confining-hooks-to-run-at-certain-stages.
	"""

	additional_dependencies: List[str]
	"""
	A list of dependencies that will be installed in the environment where this hook gets run.
	One useful application is to install plugins for hooks such as eslint."""

	#: If :py:obj:`True`, this hook will run even if there are no matching files.
	always_run: bool

	#: If :py:obj:`True`, forces the output of the hook to be printed even when the hook passes.
	verbose: bool

	#: If present, the hook output will additionally be written to a file.
	log_file: str


def _hook_converter(hooks: Iterable[Union[str, Hook]]) -> List[Hook]:
	return [hook if isinstance(hook, dict) else {"id": hook} for hook in hooks]


@attr.s
class Repo:
	"""
	Represents a repository providing a pre-commit hooks.
	"""

	#: The repository url to git clone from.
	repo: URL = attr.ib(converter=URL)

	#: The revision or tag to clone at.
	rev: str = attr.ib(converter=str)

	hooks: List[Hook] = attr.ib(converter=_hook_converter)

	def to_dict(self) -> MutableMapping[str, Union[str, List[Hook]]]:
		return {
				"repo": str(self.repo),
				"rev": self.rev,
				"hooks": self.hooks,
				}


pre_commit_hooks = Repo(
		repo=make_github_url("pre-commit", "pre-commit-hooks"),
		rev="v3.3.0",
		hooks=[
				"check-added-large-files",
				"check-ast",
				"check-byte-order-marker",
				"check-case-conflict",
				"check-executables-have-shebangs",
				"check-json",
				"check-toml",
				"check-yaml",
				"check-merge-conflict",
				"check-symlinks",
				"check-vcs-permalinks",
				"detect-private-key",
				"end-of-file-fixer",
				"trailing-whitespace",
				"mixed-line-ending",
				]
		)

pygrep_hooks = Repo(
		repo=make_github_url("pre-commit", "pygrep-hooks"),
		rev="v1.5.1",
		hooks=["python-no-eval"],
		)

pyupgrade = Repo(
		repo=make_github_url("asottile", "pyupgrade"),
		rev="v2.7.3",
		hooks=[{"id": "pyupgrade", "args": ["--py36-plus"]}]
		)

lucas_c_hooks = Repo(
		repo=make_github_url("Lucas-C", "pre-commit-hooks"),
		rev="v1.1.9",
		hooks=["remove-crlf", "forbid-crlf"],
		)

# shellcheck = Repo(
# 		repo=make_github_url("shellcheck-py", "shellcheck-py"),
# 		rev="v0.7.1.1",
# 		hooks=["shellcheck"]
# 		)
#
# yamllint = Repo(
# 		repo=make_github_url("adrienverge", "yamllint"),
# 		rev="v1.23.0",
# 		hooks=["yamllint"]
# 		)


@management.register("pre-commit", ["enable_pre_commit"])
def make_pre_commit(repo_path: pathlib.Path, templates: jinja2.Environment) -> List[str]:
	"""
	Add configuration for ``pre-commit``.

	https://github.com/pre-commit/pre-commit

	# See https://pre-commit.com for more information
	# See https://pre-commit.com/hooks.html for more hooks

	:param repo_path: Path to the repository root.
	:param templates:
	"""

	docs_dir = templates.globals["docs_dir"]
	import_name = templates.globals["import_name"]
	stubs_package = templates.globals["stubs_package"]

	non_source_files = [
			posixpath.join(docs_dir, "conf"),
			"__pkginfo__",
			"make_conda_recipe",
			"setup",
			]

	domdfcoding_hooks = Repo(
			repo=make_github_url("domdfcoding", "pre-commit-hooks"),
			rev="v0.1.1",
			hooks=[
					{"id": "requirements-txt-sorter", "args": ["--allow-git"]},
					{
							"id": "check-docstring-first",
							"exclude": fr"^({'|'.join(non_source_files)}|{templates.globals['tests_dir']}/.*)\.py$"
							},
					"bind-requirements",
					]
			)

	flake8_dunder_all = Repo(
			repo=make_github_url("domdfcoding", "flake8-dunder-all"),
			rev="v0.1.0",
			hooks=[{
					"id": "ensure-dunder-all",
					"files": fr"^{import_name}{'-stubs' if stubs_package else ''}/.*\.py$"
					}]
			)

	yapf_isort = Repo(
			repo=make_github_url("domdfcoding", "yapf-isort"),
			rev="v0.4.4",
			hooks=[{"id": "yapf-isort", "exclude": fr"^({'|'.join(non_source_files)})\.py$"}]
			)

	pre_commit_file = PathPlus(repo_path / ".pre-commit-config.yaml")

	dumper = yaml.YAML()
	dumper.indent(mapping=2, sequence=3, offset=1)

	output = StringList([
			f"# {templates.globals['managed_message']}",
			"---",
			'',
			f"exclude: {templates.globals['pre_commit_exclude']}",
			'',
			"repos:",
			])

	indent_re = re.compile("^ {3}")

	for hook in [
			pre_commit_hooks,
			domdfcoding_hooks,
			flake8_dunder_all,
			pygrep_hooks,
			pyupgrade,
			lucas_c_hooks,
			yapf_isort,
			]:
		buf = StringIO()
		dumper.dump(hook.to_dict(), buf)
		output.append(indent_re.sub(" - ", indent(buf.getvalue(), "   ")))
		output.blankline(ensure_single=True)

	pre_commit_file.write_lines(output)

	return [pre_commit_file.name]
