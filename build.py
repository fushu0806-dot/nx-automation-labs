from hashlib import sha256
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "index.src.html"


def remove_section(source: str, name: str) -> str:
    pattern = rf"<!--{name}_START-->.*?<!--{name}_END-->\s*"
    return re.sub(pattern, "", source, flags=re.DOTALL)


def remove_markers(source: str, name: str) -> str:
    return re.sub(rf"<!--{name}_(?:START|END)-->", "", source)


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    web = remove_markers(remove_section(source, "OFFLINE_ONLY"), "WEB_ONLY")
    offline = remove_markers(remove_section(source, "WEB_ONLY"), "OFFLINE_ONLY")

    (ROOT / "index.html").write_text(web, encoding="utf-8", newline="\n")
    offline_path = ROOT / "cad-workbench-offline.html"
    offline_path.write_text(offline, encoding="utf-8", newline="\n")

    digest = sha256(offline_path.read_bytes()).hexdigest()
    (ROOT / "SHA256SUMS.txt").write_text(
        f"{digest}  {offline_path.name}\n", encoding="ascii", newline="\n"
    )
    print("Generated index.html, cad-workbench-offline.html, and SHA256SUMS.txt")


if __name__ == "__main__":
    main()
