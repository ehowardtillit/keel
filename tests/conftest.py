"""Shared fixtures for KEEL template tests."""

import os
import subprocess

import pytest

KEEL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COPIER_AVAILABLE = (
    subprocess.run(["which", "copier"], capture_output=True).returncode == 0
    and subprocess.run(["copier", "--version"], capture_output=True).returncode == 0
)


def _copier_copy(target_dir, **overrides):
    """Run copier copy with given overrides into target_dir."""
    defaults = {
        "project_name": "Test Project",
        "github_owner": "test-owner",
        "source_dirs": "src/",
        "license": "MIT",
        "lang_python": "false",
        "lang_typescript": "false",
        "lang_go": "false",
        "lang_rust": "false",
        "lang_php": "false",
        "lang_elixir": "false",
        "lang_java": "false",
        "python_version": "3.12",
        "java_version": "21",
        "custom_methodology": "false",
        "skip_agent_instructions": "false",
        "branching_model": "simple",
        "agent_claude_code": "true",
        "agent_cursor": "true",
        "agent_github_copilot": "true",
        "agent_codex": "false",
        "mempalace_enabled": "false",
        "gstack_enabled": "false",
        "runtime_enforcement": "none",
        "merge_gate": "none",
        "codeguard_enabled": "false",
        "dependency_updates": "dependabot",
    }
    defaults.update(overrides)
    cmd = ["copier", "copy", "--trust", "--force", KEEL_ROOT, str(target_dir)]
    for k, v in defaults.items():
        cmd += ["-d", f"{k}={v}"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, f"copier copy failed:\n{result.stderr}"


@pytest.fixture
def render(tmp_path):
    """Fixture that returns a function to render templates with given overrides."""
    def _render(**overrides):
        target = tmp_path / "output"
        target.mkdir()
        _copier_copy(target, **overrides)
        return target
    return _render
