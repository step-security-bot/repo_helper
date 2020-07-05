#!/bin/bash

# fix these
declare errors="{% for e in lint_fix_list %}{{ e }},{% endfor %}"

# Be belligerent for these
declare belligerent="{% for e in lint_belligerent_list %}{{ e }},{% endfor %}"

# Only warn for these
declare warnings="{% for w in lint_warn_list %}{{ w }},{% endfor %}"


if [ -z "$(git status --porcelain --untracked-files=no)" ] || [ "$1" == "-f" ]; then
  # Working directory clean

  echo "Running autopep8"
{% if py_modules %}{% for file in py_modules %}
  autopep8 --in-place --select "$errors" -a {{ source_dir }}{{ file }}.py
  autopep8 --in-place --select "$belligerent" -a -a -a {{ source_dir }}{{ file }}.py
{% endfor %}{% else %}
  autopep8 --in-place --select "$errors" -a --recursive {{ source_dir }}{{ import_name }}/
  autopep8 --in-place --select "$belligerent" -a -a -a -a -a --recursive {{ source_dir }}{{ import_name }}/
{% endif %}{% if enable_tests %}
  autopep8 --in-place --select "$errors" -a --recursive {{ tests_dir }}/
  autopep8 --in-place --select "$belligerent" -a -a -a -a -a --recursive {{ tests_dir }}/{% endif %}

  echo "Running flake8"
{% if py_modules %}{% for file in py_modules %}
    >&2 flake8 {{ source_dir }}{{ file }}.py
{% endfor %}{% else %}
    >&2 flake8 {{ source_dir }}{{ import_name }}/
{% endif %}
    >&2 flake8 {{ tests_dir }}/

  exit 0

else
  # Uncommitted changes
  >&2 echo "git working directory is not clean"
  exit 1

fi


