"""tech-glossary ビルドスクリプト: languages/*.yaml -> 01_languages/*.html + index.html"""
import html as _html
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
# escape=True: YAML内の生HTMLをエスケープ（XSS対策）。**太字**等のMarkdown変換は維持される
# ため apply_tooltips の <strong>用語</strong> 置換も機能する
_md = mistune.create_markdown(escape=True)


def apply_tooltips(content: str, terms: list) -> str:
    """mistune出力の <strong>用語</strong> を tooltip span に置換（現行HTML同等）。

    word/def は html.escape でエスケープ（XSS対策）。mistune も escape=True で
    body 側をエスケープしているので、word もエスケープして突合せる。
    """
    for t in terms:
        word = _html.escape(t["word"], quote=False)
        defn = _html.escape(t["def"], quote=False)
        content = content.replace(
            f"<strong>{word}</strong>",
            f'<span class="term">{word}<span class="term-popup">{defn}</span></span>',
        )
    return content


def load_language(name: str) -> dict:
    """YAML読込 + body を Markdown->HTML 化して summary.body_md に格納"""
    with open(LANG_DIR / f"{name}.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    body_md = _md(data["summary"]["body"])
    data["summary"]["body_md"] = apply_tooltips(body_md, data.get("terms", []))
    # pros_cons も Markdown 変換（choose/avoid 内の **太字** 等を反映）
    pc = data["pros_cons"]
    pc["choose_md"] = _md(pc["choose"])
    pc["avoid_md"] = _md(pc["avoid"]) if pc.get("avoid") else ""
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
