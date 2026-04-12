"""Unit tests for the batten CLI core functions.

These test the CLI's internal functions without requiring copier or
external tools -- they exercise the Python logic directly.
"""
import os
import sys
import textwrap
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_cli():
    """Import CLI functions by exec'ing the batten script."""
    cli_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "batten")
    ns = {"__file__": cli_path, "__name__": "__batten_test__"}
    with open(cli_path) as f:
        src = f.read()
    code = src.split('if __name__ == "__main__":')[0]
    exec(compile(code, cli_path, "exec"), ns)
    return ns


CLI = _load_cli()


class TestStripComment:
    def test_simple_comment(self):
        assert CLI["_strip_comment"]("key: value # comment") == "key: value"

    def test_no_comment(self):
        assert CLI["_strip_comment"]("key: value") == "key: value"

    def test_hash_in_double_quotes(self):
        assert CLI["_strip_comment"]('color: "#FF0000"') == 'color: "#FF0000"'

    def test_hash_in_single_quotes(self):
        assert CLI["_strip_comment"]("color: '#FF0000'") == "color: '#FF0000'"

    def test_comment_after_quoted(self):
        assert CLI["_strip_comment"]('color: "#FF0000" # red') == 'color: "#FF0000"'

    def test_full_line_comment(self):
        assert CLI["_strip_comment"]("# full comment") == ""

    def test_empty_line(self):
        assert CLI["_strip_comment"]("") == ""


class TestParseYamlBasic:
    def test_simple_dict(self):
        text = "key: value\nnum: 42\nbool: true"
        result = CLI["_parse_yaml_basic"](text)
        assert result == {"key": "value", "num": 42, "bool": True}

    def test_nested_dict(self):
        text = "parent:\n  child: value"
        result = CLI["_parse_yaml_basic"](text)
        assert result == {"parent": {"child": "value"}}

    def test_inline_list(self):
        text = "items: [a, b, c]"
        result = CLI["_parse_yaml_basic"](text)
        assert result == {"items": ["a", "b", "c"]}

    def test_empty_list(self):
        text = "items: []"
        result = CLI["_parse_yaml_basic"](text)
        assert result == {"items": []}

    def test_boolean_values(self):
        text = "yes: true\nno: false"
        result = CLI["_parse_yaml_basic"](text)
        assert result == {"yes": True, "no": False}

    def test_comments_stripped(self):
        text = "key: value # comment\n# full comment\nother: data"
        result = CLI["_parse_yaml_basic"](text)
        assert result == {"key": "value", "other": "data"}

    def test_quoted_hash(self):
        text = 'color: "#FF0000"'
        result = CLI["_parse_yaml_basic"](text)
        assert result == {"color": "#FF0000"}


class TestGet:
    def test_simple(self):
        assert CLI["_get"]({"a": 1}, "a") == 1

    def test_nested(self):
        assert CLI["_get"]({"a": {"b": {"c": 3}}}, "a.b.c") == 3

    def test_missing(self):
        assert CLI["_get"]({"a": 1}, "b") is None

    def test_missing_with_default(self):
        assert CLI["_get"]({"a": 1}, "b", "default") == "default"

    def test_missing_nested(self):
        assert CLI["_get"]({"a": 1}, "a.b.c") is None


class TestProjectSlug:
    def test_simple(self):
        assert CLI["_project_slug"]({"project": {"name": "My Project"}}) == "my-project"

    def test_special_chars(self):
        assert CLI["_project_slug"]({"project": {"name": "My (Special) Project!"}}) == "my--special--project"

    def test_already_slug(self):
        assert CLI["_project_slug"]({"project": {"name": "my-project"}}) == "my-project"

    def test_default(self):
        assert CLI["_project_slug"]({}) == "project"


class TestBuildCopierFlags:
    def test_basic(self):
        data = {"project": {"name": "Test"}, "version": 1}
        flags = CLI["build_copier_flags"](data)
        assert "-d" in flags
        assert "project_name=Test" in flags

    def test_boolean_lowercased(self):
        data = {"languages": {"python": {"enabled": True}}}
        flags = CLI["build_copier_flags"](data)
        assert "lang_python=true" in flags

    def test_transform(self):
        data = {"methodology": {"type": "custom"}}
        flags = CLI["build_copier_flags"](data)
        assert "custom_methodology=true" in flags

    def test_batten_methodology(self):
        data = {"methodology": {"type": "batten"}}
        flags = CLI["build_copier_flags"](data)
        assert "custom_methodology=false" in flags


class TestBuildFindNameExpr:
    def test_python(self):
        result = CLI["_build_find_name_expr"](["python"])
        assert "*.py" in result

    def test_multi(self):
        result = CLI["_build_find_name_expr"](["python", "typescript"])
        assert "*.py" in result
        assert "*.ts" in result
        assert "-o" in result

    def test_empty_defaults_to_python(self):
        result = CLI["_build_find_name_expr"]([])
        assert "*.py" in result

    def test_java(self):
        result = CLI["_build_find_name_expr"](["java"])
        assert "*.java" in result
        assert "*.kt" in result


class TestEnabledLangs:
    def test_python_only(self):
        data = {"languages": {"python": {"enabled": True}, "go": {"enabled": False}}}
        assert CLI["_enabled_langs"](data) == ["python"]

    def test_multiple(self):
        data = {"languages": {"python": {"enabled": True}, "go": {"enabled": True}}}
        result = CLI["_enabled_langs"](data)
        assert "python" in result
        assert "go" in result

    def test_none(self):
        data = {"languages": {}}
        assert CLI["_enabled_langs"](data) == []
