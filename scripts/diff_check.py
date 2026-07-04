"""生成HTML と snapshots/ の構造diff検証（Phase1同等性確認）

現行手書きHTML（snapshots/）とビルド生成HTML（01_languages/）の
クラス付きタグ構造を比較。許容差分（assets外部化）を除去して比較。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
GENERATED = ROOT / "01_languages"
SNAPSHOT = ROOT / "snapshots"
LANGS = ["typescript", "go", "rust", "sql", "python"]

# 許容差分: assets外部化による<link>/<script src>追加・<style>/<script>埋め込み削除
ALLOWED_PATTERNS = [
    r"<style>.*?</style>",
    r"<script>.*?</script>",
    r'<link rel="stylesheet" href="\.\./assets/style\.css">',
    r'<script src="\.\./assets/(tooltip|theme)\.js"></script>',
]


def normalize(html: str) -> set:
    """クラス付きタグを抽出（構造比較用）"""
    for p in ALLOWED_PATTERNS:
        html = re.sub(p, "", html, flags=re.DOTALL)
    tags = re.findall(r"<(\w+)[^>]*class=\"([^\"]+)\"", html)
    return set(tags)


def main() -> int:
    fails = []
    for name in LANGS:
        gen_path = GENERATED / f"{name}.html"
        snap_path = SNAPSHOT / f"{name}.html"
        if not gen_path.exists() or not snap_path.exists():
            fails.append(f"{name}: ファイル不在 (gen={gen_path.exists()}, snap={snap_path.exists()})")
            continue
        gen = gen_path.read_text(encoding="utf-8")
        snap = snap_path.read_text(encoding="utf-8")
        gen_struct = normalize(gen)
        snap_struct = normalize(snap)
        if gen_struct != snap_struct:
            missing = snap_struct - gen_struct
            extra = gen_struct - snap_struct
            detail = []
            if missing:
                detail.append(f"欠損{sorted(missing)}")
            if extra:
                detail.append(f"追加{sorted(extra)}")
            fails.append(f"{name}: 構造diff - {' / '.join(detail)}")
        else:
            print(f"✅ {name}: 構造同等")

    if fails:
        print("\n".join("❌ " + f for f in fails))
        print(f"\n{len(fails)}件の差分検出")
        return 1
    print("\n全言語 構造同等性: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
