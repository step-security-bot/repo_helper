#  !/usr/bin/env python
#
#  linting.py
"""
Configuration for various linting tools, such as
`Flake8 <https://flake8.pycqa.org/en/latest/>`_,
`Pylint <https://www.pylint.org/>`_, and
`autopep8 <https://github.com/hhatto/autopep8/>`_,
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import pathlib
import shutil
from typing import List

# 3rd party
import jinja2
from domdf_python_tools.paths import clean_writer, make_executable

# this package
from .templates import template_dir

__all__ = [
		"lint_fix_list",
		"lint_belligerent_list",
		"lint_warn_list",
		"make_pylintrc",
		"make_lint_roller",
		"code_only_warning",
		]

lint_fix_list = [
		"E301",
		"E303",
		"E304",
		"E305",
		"E306",
		"E502",
		"W291",
		"W293",
		"W391",
		"E226",
		"E225",
		"E241",
		"E231",
		]

lint_belligerent_list = ["W292", 'E265']

lint_warn_list = [
		"E101",
		"E111",
		"E112",
		"E113",
		"E121",
		"E122",  # "E124",
		"E125",
		"E127",
		"E128",
		"E129",
		"E131",
		"E133",
		"E201",
		"E202",
		"E203",
		"E211",
		"E222",
		"E223",
		"E224",
		"E225",
		"E227",
		"E228",
		"E242",
		"E251",
		"E261",
		"E262",
		"E271",
		"E272",
		"E402",
		"E703",
		"E711",
		"E712",
		"E713",
		"E714",
		"E721",
		"W504",
		"E302",

  # flake8_2020
		"YTT101",  # sys.version[:3] referenced (python3.10)
		"YTT102",  # sys.version[2] referenced (python3.10)
		"YTT103",  # sys.version compared to string (python3.10)
		"YTT201",  # sys.version_info[0] == 3 referenced (python4)
		"YTT202",  # six.PY3 referenced (python4)
		"YTT203",  # sys.version_info[1] compared to integer (python4)
		"YTT204",  # sys.version_info.minor compared to integer (python4)
		"YTT301",  # sys.version[0] referenced (python10)
		"YTT302",  # sys.version compared to string (python10)
		"YTT303",  # sys.version[:1] referenced (python10)

		# flake8_strftime
		"STRFTIME001",  # Linux-specific strftime code used
		"STRFTIME002",  # Windows-specific strftime code used

		# flake8_pytest
		"PT001",  # use @pytest.fixture() over @pytest.fixture (configurable by pytest-fixture-no-parentheses)
		"PT002",  # configuration for fixture '{name}' specified via positional args, use kwargs
		"PT003",  # scope='function' is implied in @pytest.fixture()
		"PT004",  # fixture '{name}' does not return anything, add leading underscore
		"PT005",  # fixture '{name}' returns a value, remove leading underscore
		"PT006",  # wrong name(s) type in @pytest.mark.parametrize, expected {expected_type} (configurable by pytest-parametrize-names-type)
		"PT007",  # wrong values type in @pytest.mark.parametrize, expected {expected_type} (configurable by pytest-parametrize-values-type and pytest-parametrize-values-row-type)
		"PT008",  # use return_value= instead of patching with lambda
		"PT009",  # use a regular assert instead of unittest-style '{assertion}'
		"PT010",  # set the expected exception in pytest.raises()
		"PT011",  # set the match parameter in pytest.raises({exception}) (configurable by pytest-raises-require-match-for)
		"PT012",  # pytest.raises() block should contain a single simple statement
		"PT013",  # found incorrect import of pytest, use simple 'import pytest' instead
		"PT014",  # found duplicate test cases {indexes} in @pytest.mark.parametrize
		"PT015",  # assertion always fails, replace with pytest.fail()
		"PT016",  # no message passed to pytest.fail()
		"PT017",  # found assertion on exception {name} in except block, use pytest.raises() instead
		"PT018",  # assertion should be broken down into multiple parts
		"PT019",  # fixture {name} without value is injected as parameter, use @pytest.mark.usefixtures instead
		"PT020",  # @pytest.yield_fixture is deprecated, use @pytest.fixture
		"PT021",  # use yield instead of request.addfinalizer

		# flake8_rst_docstrings
		"RST201",  # Block quote ends without a blank line; unexpected unindent.
		"RST202",  # Bullet list ends without a blank line; unexpected unindent.
		"RST203",  # Definition list ends without a blank line; unexpected unindent.
		"RST204",  # Enumerated list ends without a blank line; unexpected unindent.
		"RST205",  # Explicit markup ends without a blank line; unexpected unindent.
		"RST206",  # Field list ends without a blank line; unexpected unindent.
		"RST207",  # Literal block ends without a blank line; unexpected unindent.
		"RST208",  # Option list ends without a blank line; unexpected unindent.
		"RST210",  # Inline strong start-string without end-string.
		"RST211",  # Blank line required after table.
		"RST212",  # Title underline too short.
		"RST213",  # Inline emphasis start-string without end-string.
		"RST214",  # Inline literal start-string without end-string.
		"RST215",  # Inline interpreted text or phrase reference start-string without end-string.
		"RST216",  # Multiple roles in interpreted text (both prefix and suffix present; only one allowed).
		"RST217",  # Mismatch: both interpreted text role suffix and reference suffix.
		"RST218",  # Literal block expected; none found.
		"RST219",  # Inline substitution_reference start-string without end-string.
		"RST299",  # Previously unseen warning, not yet assigned a unique code.
		"RST301",  # Unexpected indentation.
		"RST302",  # Malformed table.
		"RST303",  # Unknown directive type “XXX”.
		"RST304",  # Unknown interpreted text role “XXX”.
		"RST305",  # Undefined substitution referenced: “XXX”.
		"RST306",  # Unknown target name: “XXX”.
		"RST399",  # Previously unseen major error, not yet assigned a unique code.
		"RST401",  # Unexpected section title.
		"RST499",  # Previously unseen severe error, not yet assigned a unique code.
		"RST900",  # Failed to load file (e.g. unicode encoding issue under Python 2)
		"RST901",  # Failed to parse file
		"RST902",  # Failed to parse __all__ entry
		"RST903",  # Failed to lint docstring (e.g. unicode encoding issue under Python 2)

		# flake8-quotes
		"Q000",  # Remove bad quotes
		"Q001",  # Remove bad quotes from multiline string
		"Q002",  # Remove bad quotes from docstring
		"Q003",  # Change outer quotes to avoid escaping inner quotes
		]

code_only_warning = [
		# pydocstyle
		"D100",  # Missing docstring in public module
		"D101",  # Missing docstring in public class
		"D102",  # Missing docstring in public method
		"D103",  # Missing docstring in public function
		"D104",  # Missing docstring in public package
		# "D105",  # Missing docstring in magic method
		"D106",  # Missing docstring in public nested class
		"D107",  # Missing docstring in __init__
		"D201",  # No blank lines allowed before function docstring
		"D204",  # 1 blank line required after class docstring
		"D207",  # Docstring is under-indented
		"D208",  # Docstring is over-indented
		"D209",  # Multi-line docstring closing quotes should be on a separate line
		"D210",  # No whitespaces allowed surrounding docstring text
		"D211",  # No blank lines allowed before class docstring
		"D212",  # Multi-line docstring summary should start at the first line
		"D213",  # Multi-line docstring summary should start at the second line
		"D214",  # Section is over-indented
		"D215",  # Section underline is over-indented
		"D300",  # Use “”“triple double quotes”“”
		"D301",  # Use r”“” if any backslashes in a docstring
		"D400",  # First line should end with a period
		# "D401",  # First line should be in imperative mood
		"D402",  # First line should not be the function’s "signature"
		"D403",  # First word of the first line should be properly capitalized
		"D404",  # First word of the docstring should not be "This"
		"D415",  # First line should end with a period, question mark, or exclamation point
		"D417",  # Missing argument descriptions in the docstring
		]

# TODO: E302 results in tabs being converted to spaces. File bug report for autopep8


def make_pylintrc(repo_path: pathlib.Path, templates: jinja2.Environment) -> List[str]:
	"""
	Copy .pylintrc into the desired repository

	:param repo_path: Path to the repository root.
	:param templates:
	:type templates: jinja2.Environment
	"""

	shutil.copy2(str(template_dir / "pylintrc"), str(repo_path / ".pylintrc"))

	return [".pylintrc"]


def make_lint_roller(repo_path: pathlib.Path, templates: jinja2.Environment) -> List[str]:
	"""
	Add the lint_roller.sh script to the desired repo

	:param repo_path: Path to the repository root.
	:param templates:
	:type templates: jinja2.Environment
	"""

	lint_roller = templates.get_template("lint_roller.sh")

	with (repo_path / "lint_roller.sh").open('w', encoding="UTF-8") as fp:
		clean_writer(lint_roller.render(), fp)

	make_executable(repo_path / "lint_roller.sh", )

	return ["lint_roller.sh"]