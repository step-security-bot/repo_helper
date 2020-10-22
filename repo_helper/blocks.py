#!/usr/bin/env python
#
#  blocks.py
"""
Reusable blocks of reStructuredText.
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
import re
from typing import Iterable, Optional, Sequence, Union

# 3rd party
from jinja2 import BaseLoader, Environment, StrictUndefined, Template
from typing_extensions import Literal

# this package
from repo_helper._docs_shields import *
from repo_helper.shields import *

__all__ = [
		"installation_regex",
		"shields_regex",
		"short_desc_regex",
		"links_regex",
		"shields_block_template",
		"create_shields_block",
		"readme_installation_block_template",
		"create_readme_install_block",
		"create_short_desc_block",
		"docs_installation_block_template",
		"create_docs_install_block",
		"docs_links_block_template",
		"create_docs_links_block",
		]

#: Regular expression to match the installation block placeholder.
installation_regex = re.compile(r"(?s)(\.\. start installation)(.*?)(\.\. end installation)")

#: Regular expression to match the shields block placeholder.
shields_regex = re.compile(r"(?s)(\.\. start shields)(.*?)(\.\. end shields)")

#: Regular expression to match the short description block placeholder.
short_desc_regex = re.compile(r"(?s)(\.\. start short_desc)(.*?)(\.\. end short_desc)")

#: Regular expression to match the links block placeholder.
links_regex = re.compile(r"(?s)(\.\. start links)(.*?)(\.\. end links)")


shields_block_template: Template = Environment(
		loader=BaseLoader(),
		undefined=StrictUndefined,
		).from_string(
				"""\
.. start shields{% if unique_name %} {{ unique_name.lstrip("_") }}{% endif %}

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	{% if docs %}* - Docs
	  - |docs{{ unique_name }}| |docs_check{{ unique_name }}|
	{% endif %}* - Tests
	  - |travis{{ unique_name }}| \
{% if "Windows" in platforms %}|actions_windows{{ unique_name }}| {% endif %}\
{% if "macOS" in platforms %}|actions_macos{{ unique_name }}| {% endif %}\
{% if tests %}|coveralls{{ unique_name }}| {% endif %}\
|codefactor{{ unique_name }}|
	{% if on_pypi %}* - PyPI
	  - |pypi-version{{ unique_name }}| |supported-versions{{ unique_name }}| |supported-implementations{{ unique_name }}| |wheel{{ unique_name }}|{% endif %}
	{% if conda %}* - Anaconda
	  - |conda-version{{ unique_name }}| |conda-platform{{ unique_name }}|
	{% endif %}* - Activity
	  - |commits-latest{{ unique_name }}| |commits-since{{ unique_name }}| |maintained{{ unique_name }}|
	{% if docker_shields %}* - Docker
	  - |docker_build{{ unique_name }}| |docker_automated{{ unique_name }}| |docker_size{{ unique_name }}|
	{% endif %}* - Other
	  - |license{{ unique_name }}| |language{{ unique_name }}| |requires{{ unique_name }}|\
{% if pre_commit %} |pre_commit{{ unique_name }}|{% endif %}

{% if docs %}.. |docs{{ unique_name }}| {{ make_rtfd_shield(repo_name)[3:] }}

.. |docs_check{{ unique_name }}| {{ make_docs_check_shield(repo_name, username)[3:] }}{% endif %}

.. |travis{{ unique_name }}| {{ make_travis_shield(repo_name, username, travis_site)[3:] }}
{% if "Windows" in platforms %}
.. |actions_windows{{ unique_name }}| {{ make_actions_windows_shield(repo_name, username)[3:] }}
{% endif %}{% if "macOS" in platforms %}
.. |actions_macos{{ unique_name }}| {{ make_actions_macos_shield(repo_name, username)[3:] }}
{% endif %}
.. |requires{{ unique_name }}| {{ make_requires_shield(repo_name, username)[3:] }}
{% if tests %}
.. |coveralls{{ unique_name }}| {{ make_coveralls_shield(repo_name, username)[3:] }}
{% endif %}
.. |codefactor{{ unique_name }}| {{ make_codefactor_shield(repo_name, username)[3:] }}

.. |pypi-version{{ unique_name }}| {{ make_pypi_version_shield(pypi_name)[3:] }}

.. |supported-versions{{ unique_name }}| {{ make_python_versions_shield(pypi_name)[3:] }}

.. |supported-implementations{{ unique_name }}| {{ make_python_implementations_shield(pypi_name)[3:] }}

.. |wheel{{ unique_name }}| {{ make_wheel_shield(pypi_name)[3:] }}
{% if conda %}
.. |conda-version{{ unique_name }}| {{ make_conda_version_shield(pypi_name, username)[3:] }}

.. |conda-platform{{ unique_name }}| {{ make_conda_platform_shield(pypi_name, username)[3:] }}
{% endif %}
.. |license{{ unique_name }}| {{ make_license_shield(repo_name, username)[3:] }}

.. |language{{ unique_name }}| {{ make_language_shield(repo_name, username)[3:] }}

.. |commits-since{{ unique_name }}| {{ make_activity_shield(repo_name, username, version)[3:] }}

.. |commits-latest{{ unique_name }}| {{ make_last_commit_shield(repo_name, username)[3:] }}

.. |maintained{{ unique_name }}| {{ make_maintained_shield()[3:] }}
{% if docker_shields %}
.. |docker_build{{ unique_name }}| {{ make_docker_build_status_shield(docker_name, username)[3:] }}

.. |docker_automated{{ unique_name }}| {{ make_docker_automated_build_shield(docker_name, username)[3:] }}

.. |docker_size{{ unique_name }}| {{ make_docker_size_shield(docker_name, username)[3:] }}
{% endif %}{% if pre_commit %}
.. |pre_commit{{ unique_name }}| {{ make_pre_commit_shield()[3:] }}
{% endif %}
.. end shields
""",
				globals={
						"make_maintained_shield": make_maintained_shield,
						"make_rtfd_shield": make_rtfd_shield,
						"make_docs_check_shield": make_docs_check_shield,
						"make_travis_shield": make_travis_shield,
						"make_actions_windows_shield": make_actions_windows_shield,
						"make_actions_macos_shield": make_actions_macos_shield,
						"make_requires_shield": make_requires_shield,
						"make_coveralls_shield": make_coveralls_shield,
						"make_codefactor_shield": make_codefactor_shield,
						"make_pypi_version_shield": make_pypi_version_shield,
						"make_python_versions_shield": make_python_versions_shield,
						"make_python_implementations_shield": make_python_implementations_shield,
						"make_wheel_shield": make_wheel_shield,
						"make_conda_version_shield": make_conda_version_shield,
						"make_conda_platform_shield": make_conda_platform_shield,
						"make_license_shield": make_license_shield,
						"make_language_shield": make_language_shield,
						"make_activity_shield": make_activity_shield,
						"make_last_commit_shield": make_last_commit_shield,
						"make_docker_build_status_shield": make_docker_build_status_shield,
						"make_docker_automated_build_shield": make_docker_automated_build_shield,
						"make_docker_size_shield": make_docker_size_shield,
						"make_pre_commit_shield": make_pre_commit_shield,
						}
				)

docs_shields_block_template: Template = Environment(
		loader=BaseLoader(),
		undefined=StrictUndefined,
		).from_string(
				"""\
.. start shields{% if unique_name %} {{ unique_name.lstrip("_") }}{% endif %}

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	{% if docs %}* - Docs
	  - |docs{{ unique_name }}| |docs_check{{ unique_name }}|
	{% endif %}* - Tests
	  - |travis{{ unique_name }}| \
{% if "Windows" in platforms %}|actions_windows{{ unique_name }}| {% endif %}\
{% if "macOS" in platforms %}|actions_macos{{ unique_name }}| {% endif %}\
{% if tests %}|coveralls{{ unique_name }}| {% endif %}\
|codefactor{{ unique_name }}|
	{% if on_pypi %}* - PyPI
	  - |pypi-version{{ unique_name }}| |supported-versions{{ unique_name }}| |supported-implementations{{ unique_name }}| |wheel{{ unique_name }}|{% endif %}
	{% if conda %}* - Anaconda
	  - |conda-version{{ unique_name }}| |conda-platform{{ unique_name }}|
	{% endif %}* - Activity
	  - |commits-latest{{ unique_name }}| |commits-since{{ unique_name }}| |maintained{{ unique_name }}|
	{% if docker_shields %}* - Docker
	  - |docker_build{{ unique_name }}| |docker_automated{{ unique_name }}| |docker_size{{ unique_name }}|
	{% endif %}* - Other
	  - |license{{ unique_name }}| |language{{ unique_name }}| |requires{{ unique_name }}|\
{% if pre_commit %} |pre_commit{{ unique_name }}|{% endif %}

{% if docs %}.. |docs{{ unique_name }}| {{ make_rtfd_shield(repo_name)[3:] }}

.. |docs_check{{ unique_name }}| {{ make_docs_check_shield(repo_name, username)[3:] }}{% endif %}

.. |travis{{ unique_name }}| {{ make_travis_shield(repo_name, username, travis_site)[3:] }}
{% if "Windows" in platforms %}
.. |actions_windows{{ unique_name }}| {{ make_actions_windows_shield(repo_name, username)[3:] }}
{% endif %}{% if "macOS" in platforms %}
.. |actions_macos{{ unique_name }}| {{ make_actions_macos_shield(repo_name, username)[3:] }}
{% endif %}
.. |requires{{ unique_name }}| {{ make_requires_shield(repo_name, username)[3:] }}
{% if tests %}
.. |coveralls{{ unique_name }}| {{ make_coveralls_shield(repo_name, username)[3:] }}
{% endif %}
.. |codefactor{{ unique_name }}| {{ make_codefactor_shield(repo_name, username)[3:] }}

.. |pypi-version{{ unique_name }}| {{ make_pypi_version_shield(pypi_name)[3:] }}

.. |supported-versions{{ unique_name }}| {{ make_python_versions_shield(pypi_name)[3:] }}

.. |supported-implementations{{ unique_name }}| {{ make_python_implementations_shield(pypi_name)[3:] }}

.. |wheel{{ unique_name }}| {{ make_wheel_shield(pypi_name)[3:] }}
{% if conda %}
.. |conda-version{{ unique_name }}| {{ make_conda_version_shield(pypi_name, username)[3:] }}

.. |conda-platform{{ unique_name }}| {{ make_conda_platform_shield(pypi_name, username)[3:] }}
{% endif %}
.. |license{{ unique_name }}| {{ make_license_shield(repo_name, username)[3:] }}

.. |language{{ unique_name }}| {{ make_language_shield(repo_name, username)[3:] }}

.. |commits-since{{ unique_name }}| {{ make_activity_shield(repo_name, username, version)[3:] }}

.. |commits-latest{{ unique_name }}| {{ make_last_commit_shield(repo_name, username)[3:] }}

.. |maintained{{ unique_name }}| {{ make_maintained_shield()[3:] }}
{% if docker_shields %}
.. |docker_build{{ unique_name }}| {{ make_docker_build_status_shield(docker_name, username)[3:] }}

.. |docker_automated{{ unique_name }}| {{ make_docker_automated_build_shield(docker_name, username)[3:] }}

.. |docker_size{{ unique_name }}| {{ make_docker_size_shield(docker_name, username)[3:] }}
{% endif %}{% if pre_commit %}
.. |pre_commit{{ unique_name }}| {{ make_pre_commit_shield()[3:] }}
{% endif %}
.. end shields
""",
				globals={
						"make_maintained_shield": make_docs_maintained_shield,
						"make_rtfd_shield": make_docs_rtfd_shield,
						"make_docs_check_shield": make_docs_docs_check_shield,
						"make_travis_shield": make_docs_travis_shield,
						"make_actions_windows_shield": make_docs_actions_windows_shield,
						"make_actions_macos_shield": make_docs_actions_macos_shield,
						"make_requires_shield": make_docs_requires_shield,
						"make_coveralls_shield": make_docs_coveralls_shield,
						"make_codefactor_shield": make_docs_codefactor_shield,
						"make_pypi_version_shield": make_docs_pypi_version_shield,
						"make_python_versions_shield": make_docs_python_versions_shield,
						"make_python_implementations_shield": make_docs_python_implementations_shield,
						"make_wheel_shield": make_docs_wheel_shield,
						"make_conda_version_shield": make_docs_conda_version_shield,
						"make_conda_platform_shield": make_docs_conda_platform_shield,
						"make_license_shield": make_docs_license_shield,
						"make_language_shield": make_docs_language_shield,
						"make_activity_shield": make_docs_activity_shield,
						"make_last_commit_shield": make_docs_last_commit_shield,
						"make_docker_build_status_shield": make_docs_docker_build_status_shield,
						"make_docker_automated_build_shield": make_docs_docker_automated_build_shield,
						"make_docker_size_shield": make_docs_docker_size_shield,
						"make_pre_commit_shield": make_docs_pre_commit_shield,
						}
				)


def create_shields_block(
		username: str,
		repo_name: str,
		version: Union[str, int],
		*,
		conda: bool = True,
		tests: bool = True,
		docs: bool = True,
		travis_site: Literal["com", "org"] = "com",
		pypi_name: Optional[str] = None,
		unique_name: str = '',
		docker_shields: bool = False,
		docker_name: str = '',
		platforms: Optional[Iterable[str]] = None,
		pre_commit: bool = False,
		on_pypi: bool = True,
		template=shields_block_template,
		) -> str:
	"""
	Create the shields block for insertion into the README, documentation etc.

	:param username: The username of the GitHub account that owns the repository.
	:param repo_name: The name of the repository.
	:param version:
	:param conda:
	:param tests:
	:param docs:
	:param travis_site:
	:param pypi_name: The name of the project on PyPI. Defaults to the value of ``repo_name`` if unset.
	:param unique_name: An optional unique name for the reST substitutions.
	:param docker_shields: Whether to show shields for Docker. Default :py:obj:`False`.
	:param docker_name: The name of the Docker image on DockerHub.
	:param platforms: List of supported platforms.
	:param pre_commit: Whether to show a shield for pre-commit
	:param on_pypi:
	:param shields_block_template:

	:return: The shields block created from the above settings.
	"""

	if unique_name and not unique_name.startswith("_"):
		unique_name = f"_{unique_name}"

	if not pypi_name:
		pypi_name = repo_name

	if platforms:
		platforms = set(platforms)

	return template.render(
			username=username,
			repo_name=repo_name,
			tests=tests,
			conda=conda,
			docs=docs,
			travis_site=travis_site,
			pypi_name=pypi_name,
			version=version,
			unique_name=unique_name,
			docker_name=docker_name,
			docker_shields=docker_shields,
			platforms=platforms,
			pre_commit=pre_commit,
			on_pypi=on_pypi,
			)


readme_installation_block_template = Environment(loader=BaseLoader, undefined=StrictUndefined).from_string(  # type: ignore
		"""\
.. start installation

``{{ modname }}`` can be installed from PyPI{% if conda %} or Anaconda{% endif %}.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install {{ pypi_name }}
{% if conda %}
To install with ``conda``:

	* First add the required channels

	.. code-block:: bash
{% for channel in conda_channels %}
		$ conda config --add channels http://conda.anaconda.org/{{ channel }}{% endfor %}

	* Then install

	.. code-block:: bash

		$ conda install {{ pypi_name }}
{% endif %}
.. end installation
"""
		)


def create_readme_install_block(
		modname: str,
		username: str,
		conda: bool = True,
		pypi: bool = True,
		pypi_name: Optional[str] = None,
		conda_channels: Optional[Sequence[str]] = None,
		) -> str:
	"""
	Create the installation instructions for insertion into the README.

	:param modname: The name of the program / library.
	:param username: The username of the GitHub account that owns the repository.
	:param conda: Whether to show Anaconda installation instructions.
	:param pypi: Whether to show PyPI installation instructions.
	:param pypi_name: The name of the project on PyPI. Defaults to the value of ``repo_name`` if unset.
	:param conda_channels: List of required Conda channels.

	:return: The installation block created from the above settings.
	"""

	if not conda_channels and conda:
		raise ValueError("Please supply a list of 'conda_channels' if Conda builds are supported")

	if not pypi_name:
		pypi_name = modname

	if pypi:
		return readme_installation_block_template.render(
				modname=modname,
				username=username,
				conda=conda,
				pypi_name=pypi_name,
				conda_channels=conda_channels,
				)
	else:
		return "\n.. start installation\n.. end installation\n"


def create_short_desc_block(short_desc: str) -> str:
	"""
	Creates the short description block insertion into the README, documentation etc.

	:param short_desc: A short description of the program / library.

	:return: The short description block created from the above settings.
	"""

	return f"""\
.. start short_desc

**{short_desc}**

.. end short_desc"""


docs_installation_block_template = Environment(
		loader=BaseLoader,  # type: ignore
		undefined=StrictUndefined,
		).from_string(
				"""\
.. start installation

.. installation:: {{ pypi_name }}
{% if pypi %}	:pypi:{% endif %}
	:github:
{% if conda %}	:anaconda:
	:conda-channels: {{ conda_channels }}
{% endif %}
.. end installation
"""
				)


def create_docs_install_block(
		repo_name: str,
		username: str,
		conda: bool = True,
		pypi: bool = True,
		pypi_name: Optional[str] = None,
		conda_channels: Optional[Sequence[str]] = None,
		) -> str:
	"""
	Create the installation instructions for insertion into the documentation.

	:param repo_name: The name of the GitHub repository.
	:param username: The username of the GitHub account that owns the repository.
		(Not used; ensures API compatibility with :func:`~.create_readme_install_block`)
	:param conda: Whether to show Anaconda installation instructions.
	:param pypi: Whether to show PyPI installation instructions.
	:param pypi_name: The name of the project on PyPI. Defaults to the value of ``repo_name`` if unset.
	:param conda_channels: List of required Conda channels.

	:return: The installation block created from the above settings.
	"""

	if not conda_channels and conda:
		raise ValueError("Please supply a list of 'conda_channels' if Conda builds are supported")

	if not pypi_name:
		pypi_name = repo_name

	if conda_channels is None:
		conda_channels = []

	return docs_installation_block_template.render(
			conda=conda,
			pypi=pypi,
			pypi_name=pypi_name,
			conda_channels=", ".join(conda_channels),
			)


docs_links_block_template = Environment(loader=BaseLoader, undefined=StrictUndefined).from_string(  # type: ignore
		"""\
.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/{{ username }}/{{ repo_name}}>`__

.. end links
"""
		)


def create_docs_links_block(username: str, repo_name: str) -> str:
	"""
	Create the documentation links block.

	:param username: The username of the GitHub account that owns the repository.
	:param repo_name: The name of the GitHub repository.

	:return: The documentation links block created from the above settings.
	"""

	return docs_links_block_template.render(username=username, repo_name=repo_name)
