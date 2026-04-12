"""Template rendering tests for KEEL.

Tests that Copier templates render correctly across key configuration
combinations, producing valid output without Jinja artifacts.
"""
import os
import re
import pytest

JINJA_ARTIFACT_RE = re.compile(r"\{\{.*?\}\}|\{%.*?%\}|\{#.*?#\}")


def _assert_no_jinja_artifacts(path):
    content = path.read_text()
    matches = JINJA_ARTIFACT_RE.findall(content)
    real_artifacts = [m for m in matches if "${{" not in m.replace(" ", "")]
    assert not real_artifacts, f"Jinja artifacts in {path}: {real_artifacts}"


def _assert_valid_yaml(path):
    import yaml
    with open(path) as f:
        yaml.safe_load(f)


# ── Language-specific tests ──────────────────────────────────────────────────

class TestPythonOnly:
    def test_ci_has_python_jobs(self, render):
        out = render(lang_python="true")
        ci = out / ".github" / "workflows" / "ci.yml"
        assert ci.exists()
        content = ci.read_text()
        assert "Python" in content
        assert "ruff" in content.lower() or "Ruff" in content

    def test_ci_no_typescript_jobs(self, render):
        out = render(lang_python="true")
        content = (out / ".github" / "workflows" / "ci.yml").read_text()
        assert "TypeScript" not in content

    def test_pre_commit_has_ruff(self, render):
        out = render(lang_python="true")
        content = (out / ".pre-commit-config.yaml").read_text()
        assert "ruff" in content

    def test_no_jinja_in_ci(self, render):
        out = render(lang_python="true")
        _assert_no_jinja_artifacts(out / ".github" / "workflows" / "ci.yml")

    def test_valid_yaml(self, render):
        out = render(lang_python="true")
        _assert_valid_yaml(out / ".github" / "workflows" / "ci.yml")
        _assert_valid_yaml(out / ".pre-commit-config.yaml")


class TestTypescriptOnly:
    def test_ci_has_ts_jobs(self, render):
        out = render(lang_typescript="true")
        content = (out / ".github" / "workflows" / "ci.yml").read_text()
        assert "TypeScript" in content
        assert "npm ci" in content

    def test_ci_no_python(self, render):
        out = render(lang_typescript="true")
        content = (out / ".github" / "workflows" / "ci.yml").read_text()
        assert "bandit" not in content.lower()


class TestJavaOnly:
    def test_ci_has_java_jobs(self, render):
        out = render(lang_java="true")
        ci = out / ".github" / "workflows" / "ci.yml"
        content = ci.read_text()
        assert "Java" in content
        assert "maven" in content.lower() or "mvn" in content

    def test_pre_commit_has_java_hook(self, render):
        out = render(lang_java="true")
        content = (out / ".pre-commit-config.yaml").read_text()
        assert "java" in content.lower()


class TestMultiLanguage:
    def test_ci_has_all_enabled(self, render):
        out = render(lang_python="true", lang_typescript="true", lang_go="true")
        content = (out / ".github" / "workflows" / "ci.yml").read_text()
        for lang in ["Python", "TypeScript", "Go"]:
            assert lang in content
        assert "Rust" not in content
        assert "PHP" not in content

    def test_contributing_mentions_enabled(self, render):
        out = render(lang_python="true", lang_go="true")
        content = (out / "CONTRIBUTING.md").read_text()
        assert "Python" in content
        assert "Go" in content
        assert "PHP" not in content


class TestAllLanguages:
    def test_ci_has_all_jobs(self, render):
        out = render(
            lang_python="true", lang_typescript="true", lang_go="true",
            lang_rust="true", lang_php="true", lang_elixir="true",
            lang_java="true",
        )
        content = (out / ".github" / "workflows" / "ci.yml").read_text()
        for lang in ["Python", "TypeScript", "Go", "Rust", "PHP", "Elixir", "Java"]:
            assert lang in content, f"Missing {lang} in CI"

    def test_no_jinja_artifacts(self, render):
        out = render(
            lang_python="true", lang_typescript="true", lang_go="true",
            lang_rust="true", lang_php="true", lang_elixir="true",
            lang_java="true",
        )
        for f in (out / ".github" / "workflows").glob("*.yml"):
            _assert_no_jinja_artifacts(f)
        _assert_no_jinja_artifacts(out / ".pre-commit-config.yaml")
        _assert_no_jinja_artifacts(out / "CONTRIBUTING.md")

    def test_valid_yaml_all(self, render):
        out = render(
            lang_python="true", lang_typescript="true", lang_go="true",
            lang_rust="true", lang_php="true", lang_elixir="true",
            lang_java="true",
        )
        _assert_valid_yaml(out / ".github" / "workflows" / "ci.yml")
        _assert_valid_yaml(out / ".pre-commit-config.yaml")


# ── Methodology tests ────────────────────────────────────────────────────────

class TestCustomMethodology:
    def test_no_tier_table(self, render):
        out = render(lang_python="true", custom_methodology="true")
        content = (out / "CONTRIBUTING.md").read_text()
        assert "S/A/B/C" not in content

    def test_no_conventional_commits(self, render):
        out = render(lang_python="true", custom_methodology="true")
        content = (out / "CONTRIBUTING.md").read_text()
        assert "Conventional Commits" not in content

    def test_skip_agent_instructions(self, render):
        out = render(lang_python="true", custom_methodology="true",
                     skip_agent_instructions="true")
        contrib = (out / "CONTRIBUTING.md").read_text()
        assert "S/A/B/C" not in contrib

    def test_claude_md_no_methodology_leak(self, render):
        out = render(lang_python="true", custom_methodology="true",
                     skip_agent_instructions="false")
        claude = out / "CLAUDE.md"
        if claude.exists():
            content = claude.read_text()
            assert "S/A/B/C" not in content


# ── Branching model tests ────────────────────────────────────────────────────

class TestBranchingModels:
    def test_simple(self, render):
        out = render(lang_python="true", branching_model="simple")
        content = (out / ".pre-commit-config.yaml").read_text()
        assert "main" in content

    def test_gitflow(self, render):
        out = render(lang_python="true", branching_model="gitflow")
        content = (out / ".pre-commit-config.yaml").read_text()
        assert "develop" in content

    def test_trunk(self, render):
        out = render(lang_python="true", branching_model="trunk")
        content = (out / ".pre-commit-config.yaml").read_text()
        assert "main" in content


# ── Stack integration tests ──────────────────────────────────────────────────

class TestMemPalace:
    def test_ci_has_context_sync(self, render):
        out = render(lang_python="true", mempalace_enabled="true")
        content = (out / ".github" / "workflows" / "ci.yml").read_text()
        assert "MemPalace" in content

    def test_contributing_mentions_mempalace(self, render):
        out = render(lang_python="true", mempalace_enabled="true")
        content = (out / "CONTRIBUTING.md").read_text()
        assert "MemPalace" in content

    def test_mcp_json_exists(self, render):
        out = render(lang_python="true", mempalace_enabled="true")
        assert (out / ".mcp.json").exists()


class TestRenovate:
    def test_renovate_json_when_selected(self, render):
        out = render(lang_python="true", dependency_updates="renovate")
        assert (out / "renovate.json").exists()

    def test_dependabot_yml_when_selected(self, render):
        out = render(lang_python="true", dependency_updates="dependabot")
        assert (out / ".github" / "dependabot.yml").exists()


class TestCodeGuard:
    def test_no_semgrep_when_codeguard(self, render):
        out = render(lang_python="true", codeguard_enabled="true")
        content = (out / ".pre-commit-config.yaml").read_text()
        assert "semgrep" not in content.lower() or "codeguard" in content.lower()


# ── File presence tests ──────────────────────────────────────────────────────

class TestExpectedFiles:
    def test_core_files_exist(self, render):
        out = render(lang_python="true")
        for f in ["keel.yml", "keel", "CONTRIBUTING.md", ".pre-commit-config.yaml",
                   ".github/workflows/ci.yml", ".github/PULL_REQUEST_TEMPLATE.md",
                   ".github/instructions/guardrails.md",
                   ".github/instructions/code-review.md"]:
            assert (out / f).exists(), f"Missing: {f}"

    def test_no_makefile(self, render):
        out = render(lang_python="true")
        assert not (out / "Makefile").exists()

    def test_agent_files(self, render):
        out = render(lang_python="true", agent_claude_code="true",
                     agent_codex="true", agent_cursor="true",
                     agent_github_copilot="true")
        assert (out / "CLAUDE.md").exists()
        assert (out / "AGENTS.md").exists()
        assert (out / ".cursor" / "rules" / "keel.mdc").exists()
        assert (out / ".github" / "copilot-instructions.md").exists()

    def test_keel_script_executable(self, render):
        out = render(lang_python="true")
        keel = out / "keel"
        assert keel.exists()
        assert os.access(str(keel), os.X_OK)

    def test_keel_yml_has_project_name(self, render):
        out = render(lang_python="true")
        content = (out / "keel.yml").read_text()
        assert "Test Project" in content


# ── No Jinja artifacts across all rendered files ─────────────────────────────

class TestNoJinjaArtifacts:
    def test_all_md_files(self, render):
        out = render(lang_python="true", lang_typescript="true")
        for md in out.rglob("*.md"):
            _assert_no_jinja_artifacts(md)

    def test_all_yml_files(self, render):
        out = render(lang_python="true", lang_typescript="true")
        for yml in out.rglob("*.yml"):
            _assert_no_jinja_artifacts(yml)
        for yml in out.rglob("*.yaml"):
            _assert_no_jinja_artifacts(yml)
