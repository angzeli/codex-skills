from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path


VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class StructureValidator(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.images = 0
        self.images_with_alt = 0
        self.buttons = 0
        self.labelled_buttons = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag not in VOID_ELEMENTS:
            self.stack.append(tag)
        if tag == "img":
            self.images += 1
            if attributes.get("alt"):
                self.images_with_alt += 1
        if tag == "button":
            self.buttons += 1
            if attributes.get("aria-label") or attributes.get("aria-labelledby"):
                self.labelled_buttons += 1

    def handle_endtag(self, tag: str) -> None:
        if not self.stack or self.stack[-1] != tag:
            raise ValueError(f"unexpected closing tag: {tag}")
        self.stack.pop()


def main() -> int:
    html_path = Path(sys.argv[1])
    css_path = Path(sys.argv[2])
    parser = StructureValidator()
    parser.feed(html_path.read_text(encoding="utf-8"))
    parser.close()

    if parser.stack:
        raise ValueError(f"unclosed elements: {parser.stack}")
    if parser.images != parser.images_with_alt:
        raise ValueError("every fixture image must retain alternative text")
    if parser.buttons != 1 or parser.labelled_buttons != 0:
        raise ValueError("fixture must retain exactly one unlabeled button challenge")

    css = css_path.read_text(encoding="utf-8")
    if css.count("{") != css.count("}"):
        raise ValueError("unbalanced CSS braces")
    if 'style="font-size:' not in html_path.read_text(encoding="utf-8"):
        raise ValueError("fixture no longer documents its deliberate inline-style challenge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
