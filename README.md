# 📖 テクニカルアーキテクト語彙帳 (tech-glossary)

> **「書けなくていい。会議で使える知識を持つ。」**
> 個人開発者が実務で触れる主要領域を **9 言語 × 8 セクション** にまとめた、データ駆動の技術語彙集。

🔗 **公開サイト**: <https://fukukei23.github.io/tech-glossary/>

![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)
![pytest](https://img.shields.io/badge/pytest-65%20pass-blue)
![Languages](https://img.shields.io/badge/languages-9-orange)

---

## 🎯 なぜこの 9 言語か（選定基準）

個人開発者が実務で触れる主要領域を、過不足なく **9 言語** でカバーしました。網羅主義ではなく「実務で話せる」を最適化した選定です。

| 言語 | カバーする領域 | 一行で |
|---|---|---|
| **TypeScript** | モダン Web / フルスタック | 型安全なフロント＆バックエンドの現在の標準 |
| **Go** | インフラ・高トラフィック API | クラウドネイティブの担い手（Docker/Kubernetes/Terraform 全部 Go） |
| **Rust** | 高信頼性・システムプログラミング | メモリ安全性と速度を両立する次世代の低レイヤ |
| **Python** | データ・AI / RAG | 機械学習・LLM 周辺の事実上の標準言語 |
| **SQL** | データ・モデリング | すべてのアプリケーションの根底にある問い合わせ言語 |
| **Java** | エンタープライズ基幹 | 大企業・銀行系の安定バックエンド |
| **C#** | .NET / ゲーム (Unity) | Windows 圏エンタープライズとゲーム業界の中軸 |
| **Bash** | 運用自動化・CI/CD | すべての Linux 環境で動く最古の接着剤 |
| **Kotlin** | Android モダン | Google 公式の Android 推奨言語 |

### 📐 スコープ管理志向（差別化ストーリー）

**「膨らませず 9 言語 × 8 セクションで止める」** — これが本プロジェクトの設計判断です。

- 言語を無限に増やさない（9 言語で実務カバレッジ 80% を押さえる）
- セクション構成を全言語で統一（比較の fairness を担保）
- 「知的な完了」を見える化する（TODO で膨張させない）

これはポートフォリオにおける **スコープ管理能力** のアピールでもあります。多くの個人プロジェクトが「あれもこれも」と膨らんで unfinished になる中、**明確なストップ条件** を設定して完成させた点が技術選定者としての差別化軸です。

---

## 📚 各言語ページの構成（共通 8 セクション）

全 9 言語が**同じ 8 セクション構成**を持ち、言語間の比較可能性を担保しています。

| # | セクション | 内容 |
|---|---|---|
| 1 | 📌 **一言で言うと** | 用語の quote ＋ body（専門用語は tooltip 付き） |
| 2 | 🎯 **得意な用途** | その言語が最適なユースケース一覧 |
| 3 | ⚖️ **他言語との比較** | 比較テーブル（軸 × 値 × マーク） |
| 4 | ✅ **選ぶ / ⚠ 選ばない理由** | pros / cons |
| 5 | 💬 **会議 Q&A** | その言語に関して会議で聞かれる典型的問と答 |
| 6 | 🌐 **エコシステム** | パッケージマネージャ・FW・主要ライブラリ・ランタイム |
| 7 | 💻 **コード例** | highlight.js 11.9.0 (CDN) によるシンタックスハイライト |
| 8 | 📚 **学習ロードマップ** | 初級 / 中級 / 上級 ＋ 期間目安 |

---

## 🛠️ データ駆動ビルド

本プロジェクトは **YAML データ → HTML** のデータ駆動ビルドを採用しており、コンテンツ追加コストを最小化しています。

### ビルドスタック

- **Python 3.11** / Jinja2 / PyYAML / mistune / pytest
- **highlight.js 11.9.0**（CDN・SRI 付き）

### ビルド手順

> ⚠ PEP 668 によりシステム pip はブロックされます。必ず `.venv` を使用してください。

```bash
# 初回のみ
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# ビルド
.venv/bin/python build.py
# → 01_languages/*.html (9言語) + index.html が生成される

# レーダーチャート SVG 再生成
.venv/bin/python generate-radar.py
# → radar-spec.yaml (9言語×6軸) から index.html に埋め込み

# テスト（スキーマ検証・65 pass）
.venv/bin/pytest test_build.py -q
```

### 生成物

- `01_languages/<lang>.html`（9 言語分・8 セクションフル実装）
- `index.html`（レーダーチャート 9 言語比較・検索・アコーディオン展開）

### CI

`.github/workflows/build.yml` にて push / PR 時に `build + pytest + snapshot diff` を実行し、生成物の健全性を担保しています。

---

## 📐 YAML スキーマ（貢献者向け）

各言語は `languages/<lang>.yaml` に定義されます。主要フィールド:

```yaml
id: typescript              # ファイル名と一致
name: TypeScript            # 表示名
icon: "🔷"                  # アイコン絵文字
tagline: "型安全なWeb開発の標準"

tags:
  fit_for: ["Web API", "SPA"]
  avoid_for: ["組込", "低レイヤ"]

summary:
  quote: "JavaScriptに型を"
  body: |

use_cases:
  - title: Web API
    desc:

compare:
  headers: [...]
  rows:
    - axis: 実行速度
      values: [...]
      marks: [...]

pros_cons:
  choose: [...]
  avoid: [...]

qa:
  - q: 質問
    a: 回答

ecosystem:
  package_manager:
    - { name: npm, desc: ... }
  frameworks: [{ name, desc }]
  major_libs:   [{ name, desc }]
  runtimes:     [{ name, desc }]

code_examples:
  - title: Hello World
    code: |
      console.log("hi");

learning_roadmap:
  beginner_period: "1-2週"
  beginner:        [{ topic, desc }]
  intermediate_period: "1-2月"
  intermediate:    [{ topic, desc }]
  advanced_period: "3-6月"
  advanced:        [{ topic, desc }]

terms:                       # tooltip 用語定義
  - word: 型推論
    def: 型を明示せずとも...
```

### 新規言語の追加ステップ

1. `languages/<newlang>.yaml` を作成（既存 YAML をテンプレートに）
2. `build.py` の `LANGUAGES` リストに追加
3. `test_build.py` の `EXPECTED_LANGS` に追加
4. `radar-spec.yaml` に 6 軸評価を追加（軸順序: 実行速度 / AI&ML / 学習容易さ / 型安全性 / フロント対応 / スケーラビリティ）
5. ビルド＆テストで検証:
   ```bash
   .venv/bin/python build.py && .venv/bin/pytest test_build.py -q
   ```

---

## 🗂️ ディレクトリ構造

```
tech-glossary/
├── languages/                 # 9言語のソースデータ (YAML)
│   ├── typescript.yaml
│   ├── go.yaml
│   ├── rust.yaml
│   ├── sql.yaml
│   ├── python.yaml
│   ├── java.yaml
│   ├── csharp.yaml
│   ├── bash.yaml
│   └── kotlin.yaml
├── templates/                 # Jinja2 テンプレート
│   ├── language.html.j2
│   └── index.html.j2
├── assets/                    # 静的アセット
│   ├── style.css
│   ├── tooltip.js
│   └── theme.js
├── 01_languages/              # ビルド生成物（9言語HTML・gitignore対象外）
├── build.py                   # ビルドスクリプト
├── generate-radar.py          # レーダーSVG生成
├── radar-spec.yaml            # レーダー9言語×6軸 評価データ
├── test_build.py              # スキーマ検証 (65 pass)
├── requirements.txt
├── scripts/diff_check.py      # スナップショット差分チェック
└── .github/workflows/
    ├── build.yml              # CI: build + pytest + diff
    └── deploy.yml             # GitHub Pages デプロイ
```

---

## 💡 設計思想

### なぜ語彙帳なのか

「コードを手書きしなくても、技術選定の場で説明できる」ことを目標にした語彙帳です。読者は **面接官** と **未来の自分（知識の整理）** の二重。だからこそ「書き方」より「会議で使える説明」に軸を置いています。

### なぜデータ駆動か

コンテンツ（YAML）と表示（Jinja2 テンプレート）を分離することで、
- 新言語追加が YAML 1 ファイル＋リスト登録だけで済む
- デザイン変更が全言語に一括反映される
- スキーマ検証によるデータ品質の自動担保

を実現しています。

### セキュリティ

- **XSS 対策**: mistune `escape=True` ＋ `html.escape` でユーザ入力（YAML 内コード等）をエスケープ
- **CDN SRI**: highlight.js は CDN 配信＋SRI ハッシュで改ざん検知

---

## 📜 ライセンス・クレジット

- **ライセンス**: MIT（個人ポートフォリオとして公開）
- **作者**: fukukei23

### 参考にした公式ドキュメント

各言語の記述は以下の公式ドキュメントを裏取りしています:

- **TypeScript**: <https://www.typescriptlang.org/docs/>
- **Go**: <https://go.dev/doc/>
- **Rust**: <https://www.rust-lang.org/learn>
- **Python**: <https://docs.python.org/3/>
- **SQL**: <https://www.postgresql.org/docs/>
- **Java**: <https://docs.oracle.com/en/java/> / <https://spring.io/>
- **C#**: <https://learn.microsoft.com/dotnet/csharp/>
- **Bash**: <https://www.gnu.org/software/bash/manual/>
- **Kotlin**: <https://kotlinlang.org/docs/home.html>

---

> Build with Python 3 + Jinja2 + PyYAML + mistune + pytest + highlight.js
