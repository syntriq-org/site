from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote

root = Path(__file__).resolve().parent.parent
class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f"Duplicate id: {a['id']}"
            self.ids.add(a['id'])
        for name in ('src', 'href'):
            if name in a: self.links.append(a[name])
        if tag == 'img': assert 'alt' in a, 'Image requires alt text'

pages = [root / 'index.html', *sorted((root / 'insights').glob('*.html'))]
parsers = {}
for page in pages:
    parser = SiteParser()
    parser.feed(page.read_text())
    parsers[page.resolve()] = parser
for page, parser in parsers.items():
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (page.parent / unquote(url.path)).resolve() if url.path else page
        assert target.is_relative_to(root), f'Link escapes public root: {link}'
        assert target.is_file(), f'Missing asset in {page.name}: {link}'
        if url.fragment:
            assert target in parsers and unquote(url.fragment) in parsers[target].ids, f'Broken anchor in {page.name}: {link}'
for asset in re.findall(r"url\(['\"]?([^)'\"]+)", (root / 'style.css').read_text()):
    assert (root / asset).is_file(), f'Missing CSS asset: {asset}'
print(f'Validated {len(pages)} pages: cross-page anchors, IDs, image alternatives and local assets.')
