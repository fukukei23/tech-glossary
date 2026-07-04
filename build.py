"""tech-glossary ビルドスクリプト: languages/*.yaml -> 01_languages/*.html + index.html"""
import sys
from pathlib import Path

import yaml
import mistune
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
LANG_DIR = ROOT / "languages"
TEMPLATE_DIR = ROOT / "templates"
BUILD_DIR = ROOT / "01_languages"
INDEX_DIR = ROOT  # index.html はルート

LANGUAGES = ["typescript", "go", "rust", "sql", "python"]
_md = mistune.create_markdown(escape=False)


def render_terms(body: str, terms: list) -> str:
    """body内の **用語** を terms の定義で展開（tooltip用）。

    mistune前後に適用。今回は **用語** を <strong>用語</strong> のまま残す
    （tooltip未実装はPhase2以降）。
    """
    # Phase1 は **用語** -> <strong>用語</strong> の標準Markdown変換のみ
    return body


def load_language(name: str) -> dict:
    """YAML読込 + body を Markdown->HTML 化して summary.body_md に格納"""
    with open(LANG_DIR / f"{name}.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    body = render_terms(data["summary"]["body"], data.get("terms", []))
    data["summary"]["body_md"] = _md(body)
    return data


def build_language_html(name: str, env: Environment) -> None:
    """1言語のHTML生成"""
    data = load_language(name)
    tmpl = env.get_template("language.html.j2")
    html = tmpl.render(lang=data)
    BUILD_DIR.mkdir(exist_ok=True)
    (BUILD_DIR / f"{name}.html").write_text(html, encoding="utf-8")


def build_index(env: Environment, langs: list) -> None:
    """一覧ページ生成"""
    tmpl = env.get_template("index.html.j2")
    html = tmpl.render(languages=langs)
    (INDEX_DIR / "index.html").write_text(html, encoding="utf-8")


def main() -> int:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=True)
    langs = []
    for name in LANGUAGES:
        build_language_html(name, env)
        langs.append(load_language(name))
    build_index(env, langs)
    print(f"完了: {len(LANGUAGES)}言語 + index → {BUILD_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
