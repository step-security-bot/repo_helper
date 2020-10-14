#!/usr/bin/env python
#
#  pypi_secure.py
"""
Add the encrypted PyPI password for Travis.
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
from typing import Optional

# 3rd party
import click

# this package
from repo_helper.cli import cli_command

__all__ = ["pypi_secure"]


@click.argument(
		"password",
		type=str,
		default='',
		)
@cli_command()
def pypi_secure(password: Optional[str] = None) -> int:
	"""
	Add the encrypted PyPI password for Travis to 'repo_helper.yml'.
	"""

	# stdlib
	import getpass
	from subprocess import PIPE, Popen

	process = Popen(["travis", "encrypt", password or getpass.getpass(), "--pro"], stdout=PIPE)
	(output, err) = process.communicate()
	exit_code = process.wait()

	with open("repo_helper.yml", encoding="UTF-8", mode="a") as fp:
		fp.write("\n")
		fp.write(f"travis_pypi_secure: {output.decode('UTF-8')}")

	return exit_code