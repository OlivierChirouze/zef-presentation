#!/usr/bin/env python3
import re
import sys
from bs4 import BeautifulSoup

def main(path):
    html = open(path, 'r', encoding='utf-8').read()

    # Preserve empty lines by replacing them with a placeholder
    html = re.sub(r'\n\s*\n', '\n__EMPTY_LINE__\n', html)

    # 1) Extract only the inner content and attributes of each <aside>…</aside>
    aside_contents = []
    def mask_aside(m):
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)

        # Extract attributes from the opening tag
        attributes = re.search(r'<aside\b([^>]*)>', open_tag).group(1) or ""

        # Ensure attributes have a leading space if not empty
        attributes = f" {attributes.strip()}" if attributes.strip() else ""

        # Preserve original inner content
        idx = len(aside_contents)
        aside_contents.append((attributes, inner))
        return f"<aside{attributes}>__ASIDE_CONTENT_{idx}__</aside>"

    aside_re = re.compile(r'(<aside\b[^>]*>)(.*?)(</aside>)', re.DOTALL)
    masked = aside_re.sub(mask_aside, html)

    # 2) Pretty‐print everything (so all tags get indented), preserve original entities
    soup = BeautifulSoup(masked, 'html.parser')
    pretty = soup.prettify(formatter=None)

    # Restore empty lines from the placeholder
    pretty = pretty.replace('__EMPTY_LINE__', '')

    # 3) Collapse back any tags that only wrap a single text node
    one_line = re.compile(
        r'^([ \t]*)<(\w+)([^>]*)>\s*\n\s*([^<\n]+?)\s*\n\s*</\2>',
        re.MULTILINE
    )
    while True:
        new_pretty = one_line.sub(r'\1<\2\3>\4</\2>', pretty)
        if new_pretty == pretty:
            break
        pretty = new_pretty

    # 4) Remove ="" from empty attributes (e.g. data-markdown="")
    pretty = re.sub(r'\s([\w:-]+)=""', r' \1', pretty)

    # 5) Re-inject each aside’s original attributes and inner content
    for i, (attributes, content) in enumerate(aside_contents):
        pretty = pretty.replace(f"__ASIDE_CONTENT_{i}__", content)

    # 6) Fix indentation of </aside> tags
    def fix_aside_closing_tag(m):
        opening_tag_indent = m.group(1)
        attributes = m.group(2)
        content = m.group(3)
        return f"{opening_tag_indent}<aside{attributes}>{content}</aside>"

    pretty = re.sub(
        r'^([ \t]*)<aside\b([^>]*)>(.*?)</aside>',
        fix_aside_closing_tag,
        pretty,
        flags=re.DOTALL | re.MULTILINE
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(pretty)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} slides.html", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])