from html.parser import HTMLParser
from pathlib import Path
import re

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

parser = SiteParser()
parser.feed((root / 'index.html').read_text())
for link in parser.links:
    if link.startswith('#'):
        assert link == '#' or link[1:] in parser.ids, f'Broken anchor: {link}'
    elif not link.startswith(('https:', 'http:', 'mailto:', 'data:')):
        assert (root / link).is_file(), f'Missing asset: {link}'
for asset in re.findall(r"url\(['\"]?([^)'\"]+)", (root / 'style.css').read_text()):
    assert (root / asset).is_file(), f'Missing CSS asset: {asset}'
print('Validated page anchors, IDs, image alternatives and local assets.')
