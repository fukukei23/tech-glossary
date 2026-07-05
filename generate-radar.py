"""radar-spec.yaml -> レーダーチャート SVG 断片を生成（index.html.j2 に埋め込み）"""
import math
import yaml
from pathlib import Path

ROOT = Path(__file__).parent
CENTER = 70.0
UNIT = 10.64  # 1評価あたりのpx（Task2実測）
# 軸角度（上起点・時計回り 60°間隔、SVG y 下+なので 90°起点・−60°刻みで減算）
ANGLES_DEG = [90, 30, 330, 270, 210, 150]
RINGS = [1, 2, 3, 4, 5]


def _point(angle_deg: float, radius: float) -> tuple[float, float]:
    """上起点・時計回り。SVG座標系は y 下+なので sin の符号反転"""
    rad = math.radians(angle_deg)
    return (CENTER + radius * math.cos(rad), CENTER - radius * math.sin(rad))


def _ring_polygon(rating: int) -> str:
    pts = [_point(a, UNIT * rating) for a in ANGLES_DEG]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def _axis_lines() -> str:
    lines = []
    for a in ANGLES_DEG:
        x, y = _point(a, UNIT * 5)
        lines.append(
            f'<line x1="{CENTER}" y1="{CENTER}" x2="{x:.1f}" y2="{y:.1f}" '
            f'stroke="rgba(255,255,255,0.12)" stroke-width="0.8"/>'
        )
    return "\n".join(lines)


def _rings_svg() -> str:
    parts = [f'<polygon points="{_ring_polygon(r)}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.8"/>' for r in RINGS]
    parts.append(_axis_lines())
    return "\n".join(parts)


def _lang_svg(lang: dict) -> str:
    pts = [_point(ANGLES_DEG[i], UNIT * lang["ratings"][i]) for i in range(6)]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    color = lang["color"]
    out = [f'<polygon points="{poly}" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="1.5"/>']
    for x, y in pts:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{color}"/>')
    return "\n".join(out)


def _card_svg(lang: dict) -> str:
    """index.html.j2 の radar-card 1枚分"""
    return (
        f'      <div class="radar-card">\n'
        f'        <div class="radar-lang">{lang["icon"]} {lang["name"]}</div>\n'
        f'        <svg width="140" height="140" viewBox="0 0 140 140">\n'
        f'{_rings_svg()}\n'
        f'{_lang_svg(lang)}\n'
        f'</svg>\n'
        f'        <div class="radar-labels"><span class="radar-label">{lang["label"]}</span></div>\n'
        f'      </div>'
    )


def _load_spec() -> dict:
    """YAML読込。バリデーション付きで空構造を返すと import や build 全体が止まるので明示的に例外。"""
    path = ROOT / "radar-spec.yaml"
    if not path.exists():
        raise FileNotFoundError(f"radar-spec.yaml が見つかりません: {path}")
    try:
        with open(path, encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise RuntimeError(f"radar-spec.yaml のパースに失敗: {e}") from e
    if not isinstance(spec, dict) or "languages" not in spec:
        raise ValueError("radar-spec.yaml に 'languages:' キーが必要です")
    return spec


def _validate_lang(lang: dict, idx: int) -> dict:
    """個別言語の必須キーを .get() でデフォルト補完（labels 欠如・ratings 長さ不一致）"""
    ratings = lang.get("ratings", [1] * 6)
    if not isinstance(ratings, list) or len(ratings) != 6:
        raise ValueError(f"languages[{idx}].ratings は長さ6のリストが必要（{len(ratings)} given）")
    return {
        "id": lang.get("id", f"unknown-{idx}"),
        "name": lang.get("name", f"Unknown-{idx}"),
        "icon": lang.get("icon", "📊"),
        "color": lang.get("color", "#888888"),
        "ratings": ratings,
        "label": lang.get("label", ""),
    }


def main() -> int:
    spec = _load_spec()
    langs = [_validate_lang(lang, i) for i, lang in enumerate(spec["languages"])]
    out = "\n".join(_card_svg(lang) for lang in langs)
    out_path = ROOT / "templates" / "_radar_cards.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"完了: {len(langs)}言語 → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())