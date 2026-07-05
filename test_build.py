# test_build.py
import pytest
import yaml
from pathlib import Path

LANG_DIR = Path(__file__).parent / "languages"
EXPECTED_LANGS = ["typescript", "go", "rust", "sql", "python"]
REQUIRED_FIELDS = ["id", "name", "icon", "tagline", "tags", "summary",
                   "use_cases", "compare", "pros_cons", "qa"]


def load_yaml(name):
    path = LANG_DIR / f"{name}.yaml"
    if not path.exists():
        pytest.skip(f"{name}.yaml not yet created")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.mark.parametrize("lang", EXPECTED_LANGS)
def test_required_fields(lang):
    data = load_yaml(lang)
    for field in REQUIRED_FIELDS:
        assert field in data, f"{lang}.yaml に必須フィールド '{field}' がない"


@pytest.mark.parametrize("lang", EXPECTED_LANGS)
def test_tags_structure(lang):
    data = load_yaml(lang)
    tags = data["tags"]
    assert "fit_for" in tags, f"{lang}.yaml tags に fit_for がない"
    assert "avoid_for" in tags, f"{lang}.yaml tags に avoid_for がない"
    assert isinstance(tags["fit_for"], list)
    assert isinstance(tags["avoid_for"], list)


@pytest.mark.parametrize("lang", EXPECTED_LANGS)
def test_compare_headers_rows_consistency(lang):
    data = load_yaml(lang)
    compare = data["compare"]
    headers = compare["headers"]
    for row in compare["rows"]:
        assert len(row["values"]) == len(headers), \
            f"{lang}.yaml compare: values数({len(row['values'])}) != headers数({len(headers)})"
        assert len(row.get("marks", [])) == len(headers) or not row.get("marks"), \
            f"{lang}.yaml compare: marks数がheaders数と不一致を許容しない"


@pytest.mark.parametrize("lang", EXPECTED_LANGS)
def test_summary_quote_body(lang):
    data = load_yaml(lang)
    summary = data["summary"]
    assert "quote" in summary
    assert "body" in summary
    assert isinstance(summary["quote"], str)
    assert isinstance(summary["body"], str)


# === ビルド関数テスト（Task 7 追記）===
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).parent))
from build import load_language, build_language_html  # noqa: E402
from jinja2 import Environment, FileSystemLoader  # noqa: E402


def _env():
    return Environment(
        loader=FileSystemLoader(str(_Path(__file__).parent / "templates")),
        autoescape=True,
    )


def test_load_language_typescript():
    data = load_language("typescript")
    assert data["name"] == "TypeScript"
    assert "fit_for" in data["tags"]
    assert "body_md" in data["summary"]


def test_build_language_html_generates_file():
    build_language_html("typescript", _env())
    out = _Path(__file__).parent / "01_languages" / "typescript.html"
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "<title>TypeScript" in content
    assert "assets/style.css" in content
    assert "assets/tooltip.js" in content


# === Phase2a: 新3セクション検証（存在時のみ・任意） ===

@pytest.mark.parametrize("lang", EXPECTED_LANGS)
def test_ecosystem_structure_when_present(lang):
    data = load_yaml(lang)
    if "ecosystem" not in data:
        pytest.skip(f"{lang}.yaml に ecosystem 未登録（Phase2aでは任意）")
    eco = data["ecosystem"]
    assert "package_manager" in eco, f"{lang}.yaml ecosystem に package_manager がない"
    for fw in eco.get("frameworks", []):
        assert "name" in fw and "desc" in fw, f"{lang}.yaml ecosystem.frameworks に name/desc が必要"
    # major_libs/runtimes も name+desc 構造を推奨（文字列も許容・後方互換）
    for lib in eco.get("major_libs", []):
        if isinstance(lib, dict):
            assert "name" in lib and "desc" in lib, f"{lang}.yaml ecosystem.major_libs dictには name/desc が必要"
    for rt in eco.get("runtimes", []):
        if isinstance(rt, dict):
            assert "name" in rt and "desc" in rt, f"{lang}.yaml ecosystem.runtimes dictには name/desc が必要"


@pytest.mark.parametrize("lang", EXPECTED_LANGS)
def test_code_examples_structure_when_present(lang):
    data = load_yaml(lang)
    if "code_examples" not in data:
        pytest.skip(f"{lang}.yaml に code_examples 未登録（Phase2aでは任意）")
    for ex in data["code_examples"]:
        assert "title" in ex and "code" in ex, f"{lang}.yaml code_examples に title/code が必要"


@pytest.mark.parametrize("lang", EXPECTED_LANGS)
def test_learning_roadmap_structure_when_present(lang):
    data = load_yaml(lang)
    if "learning_roadmap" not in data:
        pytest.skip(f"{lang}.yaml に learning_roadmap 未登録（Phase2aでは任意）")
    lr = data["learning_roadmap"]
    for level in ["beginner", "intermediate", "advanced"]:
        assert level in lr, f"{lang}.yaml learning_roadmap に {level} がない"
        assert isinstance(lr[level], list), f"{lang}.yaml learning_roadmap.{level} はlistであること"
