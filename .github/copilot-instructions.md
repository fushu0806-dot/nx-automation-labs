# nx-automation-labs 共通ルール

## 言語
- 推論の説明、計画、質問、確認、進捗報告は **すべて日本語** で行う。
- コード内の識別子は英語、コメントは日本語でよい。
- ユーザーへの質問が必要な場合は、選択肢を示して日本語で聞く。

## 作業の進め方
- 変更前に、何をどう変更するかを日本語で短く説明する。
- 大きな変更(複数ファイル、仕様変更、削除)は、実行前に計画を提示して確認を取る。
- 不明点は推測で進めず、日本語で質問する。
- `index.html` は `index.src.html` をもとに `build.py` で生成される。生成物を直接編集せず、必ずソースを編集し、必要に応じて `python build.py` を実行する。
- `build.py` は `index.src.html` に加えて `nx-journal-generator.template.html` を使い、`index.html`、`tolerance-tool-offline.html`、`nx-journal-generator.html`、`SHA256SUMS.txt` を生成する。生成物を更新した場合は、対象を確認して同じコミットに含める。

## Git 運用
- 詳細は `.github/instructions/git-workflow.instructions.md` に従う。

## ルール自体の更新
- ユーザーが「ルールに追加して」「ルールを更新して」と言った場合は、
  該当する `.github/` 配下のファイルを編集し、変更内容を日本語で報告する。
- ルールを変更したら `docs/rules-changelog.md` に日付と変更内容を追記する。
- ルール変更も Git でコミットする(`docs:` プレフィックス)。
