#!/usr/bin/env python3
"""index.src.html から Web版・オフライン版・NX専用版を生成する。

  入力  index.src.html                 … 計算機・NX UIと生成処理
        nx-journal-generator.template.html … NX専用版のページ枠・CSP・スタイル
  出力  index.html                     … Web版（広告枠・オフライン版ダウンロードリンクあり）
        tolerance-tool-offline.html    … オフライン版（広告なし・CSPで外部通信を遮断）
        nx-journal-generator.html      … NXジャーナル専用の単一HTML生成ツール
        SHA256SUMS.txt                 … オフライン版とNX専用版の SHA-256

使い方： python build.py
注意：index.html は毎回上書きされます。直接編集せず、index.src.html を編集してください。
"""
import re, hashlib, pathlib, sys

root = pathlib.Path(__file__).resolve().parent
src_path = root / "index.src.html"
if not src_path.exists():
    sys.exit("index.src.html が見つかりません（build.py と同じフォルダに置いてください）")
src = src_path.read_text(encoding="utf-8")

def strip(text, tag):
    return re.sub(r"<!--%s_START-->.*?<!--%s_END-->\n?" % (tag, tag), "", text, flags=re.S)
def keep(text, tag):
    return re.sub(r"<!--%s_(?:START|END)-->\n?" % tag, "", text)

def extract(text, tag):
    if tag == "NX_GENERATOR_SCRIPT":
        pattern = r"/\* %s_START \*/(.*?)/\* %s_END \*/" % (tag, tag)
    else:
        pattern = r"<!--%s_START-->(.*?)<!--%s_END-->" % (tag, tag)
    matches = re.findall(pattern, text, flags=re.S)
    if len(matches) != 1:
        sys.exit(f"{tag} の開始・終了マーカーが不正です")
    return matches[0]

def remove_config_io(text):
    text = re.sub(r"<!--NX_CONFIG_IO_START-->.*?<!--NX_CONFIG_IO_END-->", "", text, flags=re.S)
    return re.sub(r"// NX_CONFIG_IO_START.*?// NX_CONFIG_IO_END", "", text, flags=re.S)

offline = keep(strip(src, "WEB_ONLY"), "OFFLINE_ONLY")
offline_bytes = offline.encode("utf-8")
sha = hashlib.sha256(offline_bytes).hexdigest()
web = keep(strip(src, "OFFLINE_ONLY"), "WEB_ONLY").replace("{{OFFLINE_SHA256}}", sha)

template_path = root / "nx-journal-generator.template.html"
if not template_path.exists():
    sys.exit("nx-journal-generator.template.html が見つかりません")
template = template_path.read_text(encoding="utf-8")
markup = remove_config_io(extract(src, "NX_TOOL_MARKUP"))
panel = '<div class="panel" id="p-nx" role="tabpanel" aria-labelledby="t-nx" hidden>'
if markup.count(panel) != 1:
    sys.exit("NX専用版のパネル開始タグが不正です")
markup = markup.replace(panel, '<div class="panel" id="p-nx">')
script = remove_config_io(extract(src, "NX_GENERATOR_SCRIPT"))
journal = template.replace("{{NX_TOOL_MARKUP}}", markup).replace("{{NX_GENERATOR_SCRIPT}}", script)
if "{{NX_TOOL_MARKUP}}" in journal or "{{NX_GENERATOR_SCRIPT}}" in journal:
    sys.exit("NX専用版のテンプレートに未解決のマーカーがあります")
journal_bytes = journal.encode("utf-8")
journal_sha = hashlib.sha256(journal_bytes).hexdigest()
web = web.replace("{{NX_JOURNAL_SHA256}}", journal_sha)

(root / "tolerance-tool-offline.html").write_bytes(offline_bytes)
(root / "index.html").write_bytes(web.encode("utf-8"))
(root / "nx-journal-generator.html").write_bytes(journal_bytes)
(root / "SHA256SUMS.txt").write_bytes(
    f"{sha}  tolerance-tool-offline.html\n{journal_sha}  nx-journal-generator.html\n".encode("utf-8")
)
print("OK  offline sha256:", sha)
print("OK  NX journal sha256:", journal_sha)
