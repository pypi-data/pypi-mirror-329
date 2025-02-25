import datetime
import os
import pathlib
import shlex
import shutil
import subprocess
import typing
from contextlib import contextmanager


@contextmanager
def inside_dir(dirpath: pathlib.Path):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        shutil.rmtree(str(result.project_path))


def run_inside_dir(command: str, dirpath: pathlib.Path):
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def test_bake_with_defaults(cookies):
    """
    Test that the project is baked successfully and contains certain files.
    """
    with bake_in_temp_dir(cookies) as result:
        # 确认 bake 成功
        assert result.exit_code == 0
        assert result.exception is None

        # 确认生成的项目目录存在
        assert result.project_path.is_dir()

        # 检查特定文件是否存在
        assert (result.project_path / "README.rst").is_file()

        # 确认生成的文件或目录存在
        toplevel_files = set([f.name for f in result.project_path.iterdir()])
        assert set(
            [
                "docs",
                "src",
                "tests",
                ".editorconfig",
                ".gitignore",
                ".pre-commit-config.yaml",
                "LICENSE",
                "Makefile",
                "pyproject.toml",
                "README.rst",
                "tox.ini",
            ]
        ).issubset(toplevel_files)


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project_path / "LICENSE"
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read_text()


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        assert run_inside_dir("make test", str(result.project_path)) == 0
        print("test_bake_and_run_tests path", str(result.project_path))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break project"""
    with bake_in_temp_dir(cookies, extra_context={"full_name": "name 'quote' name"}) as result:
        assert result.project_path.is_dir()
        assert run_inside_dir("make test", str(result.project_path)) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break project"""

    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project_path.is_dir()
        assert run_inside_dir("make test", str(result.project_path)) == 0


def test_bake_without_author_file(cookies):
    with bake_in_temp_dir(cookies, extra_context={"create_author_file": "n"}) as result:
        toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert "AUTHORS.rst" not in toplevel_files
        doc_files = [f.name for f in (result.project_path / "docs").iterdir()]
        assert "authors.rst" not in doc_files

        # Assert there are no spaces in the toc tree
        docs_index_path = result.project_path / "docs" / "index.rst"
        assert "contributing\n   history" in docs_index_path.read_text()

        # Check that
        manifest_path = result.project_path / "MANIFEST.in"
        assert "AUTHORS.rst" not in manifest_path.read_text()


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_make_help(cookies):
    with bake_in_temp_dir(cookies) as result:
        output = check_output_inside_dir("make help", str(result.project_path))
        assert b"check code coverage quickly with the default Python" in output


def test_bake_selecting_license(cookies):
    license_strings = {
        "MIT license": "MIT ",
        "BSD license": "Redistributions of source code must retain the " + "above copyright notice, this",
        "ISC license": "ISC License",
        "Apache Software License 2.0": "Licensed under the Apache License, Version 2.0",
        "GNU General Public License v3": "GNU GENERAL PUBLIC LICENSE",
    }
    for license, target_string in license_strings.items():
        with bake_in_temp_dir(cookies, extra_context={"open_source_license": license}) as result:
            assert target_string in (result.project_path / "LICENSE").read_text()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(cookies, extra_context={"open_source_license": "Not open source"}) as result:
        toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert "LICENSE" not in toplevel_files
        assert "License" not in (result.project_path / "README.rst").read_text()


def test_using_pytest(cookies):
    with bake_in_temp_dir(cookies, extra_context={"use_pytest": "y"}) as result:
        assert result.project_path.is_dir()
        test_file_path = result.project_path / "tests" / "test_python_boilerplate.py"
        assert "import pytest" in test_file_path.read_text()
        assert run_inside_dir("make test", str(result.project_path)) == 0


def test_not_using_pytest(cookies):
    with bake_in_temp_dir(cookies, extra_context={"use_pytest": "n"}) as result:
        assert result.project_path.is_dir()
        test_file_path = result.project_path / "tests" / "test_python_boilerplate.py"
        texts = test_file_path.read_text()
        assert "import unittest" in texts
        assert "import pytest" not in texts


def project_info(result) -> typing.Tuple[pathlib.Path, str]:
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    assert result.exception is None
    assert result.project_path.is_dir()

    project_path = result.project_path
    project_slug = project_path.name
    return project_path, project_slug


def test_bake_with_no_console_script(cookies):
    context = {"command_line_interface": "No command-line interface"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug = project_info(result)
    project_files = [f.name for f in project_path.rglob("*")]
    assert "cli.py" not in project_files

    project_config_path = project_path / "pyproject.toml"
    project_config = project_config_path.read_text(encoding="utf8")
    assert "[project.scripts]" not in project_config
    assert f"{project_slug}.cli:app" not in project_config


def test_bake_with_console_script_files(cookies):
    context = {"command_line_interface": "Typer"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug = project_info(result)
    project_files = [f.name for f in project_path.rglob("*")]
    assert "cli.py" in project_files

    project_config_path = project_path / "pyproject.toml"
    project_config = project_config_path.read_text(encoding="utf8")
    assert "[project.scripts]" in project_config
    assert f"{project_slug}.cli:app" in project_config
