from html.parser import HTMLParser
from pathlib import Path
import re
import struct
import zlib
import json
from urllib.parse import urlsplit, unquote

root = Path(__file__).resolve().parent.parent
class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.meta = {}
        self.title = False
        self.h1 = 0
        self.canonical = False
        self.images = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title': self.title = True
        if tag == 'h1': self.h1 += 1
        if tag == 'meta': self.meta[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = True
        if tag == 'img':
            assert a.get('width') and a.get('height'), 'Image dimensions required'
            self.images.append(a)
            for candidate in a.get('srcset', '').split(','):
                if candidate.strip(): self.links.append(candidate.strip().split()[0])
        if 'id' in a:
            assert a['id'] not in self.ids, f"Duplicate id: {a['id']}"
            self.ids.add(a['id'])
        for name in ('src', 'href'):
            if name in a: self.links.append(a[name])
        if tag == 'img': assert 'alt' in a, 'Image requires alt text'

pages = [*sorted(root.glob('*.html')), *sorted((root / 'insights').glob('*.html'))]
parsers = {}
for page in pages:
    parser = SiteParser()
    parser.feed(page.read_text())
    assert parser.title and parser.h1 == 1, f'Title/H1 missing or duplicated: {page}'
    assert parser.canonical, f'Canonical missing: {page}'
    for key in ('description', 'viewport', 'og:title', 'og:description', 'og:image', 'og:url', 'twitter:card'):
        assert parser.meta.get(key), f'Missing metadata {key}: {page}'
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

for page, parser in parsers.items():
    for img in parser.images:
        asset = (page.parent / img['src']).resolve()
        if asset.suffix == '.png':
            data = asset.read_bytes()
            assert data[:8] == b'\x89PNG\r\n\x1a\n', f'Invalid PNG: {asset}'
            width, height = struct.unpack('>II', data[16:24])
            assert width == int(img['width']) and height == int(img['height']), f'Incorrect dimensions: {asset}'
for article in json.loads((root / 'content/articles.json').read_text()):
    for suffix in ('.svg', '.png', '-preview.png'):
        assert (root / 'assets/diagrams' / (article['slug'] + suffix)).is_file()
import xml.etree.ElementTree as ET
sitemap = ET.parse(root / 'sitemap.xml')
assert len(sitemap.getroot()) == len(pages), 'Sitemap does not match page count'
print('Validated metadata, PNG dimensions, ten article asset sets and sitemap.')

# Check all PNG chunks and compressed image streams, not only header dimensions.
for asset in (root / 'assets').rglob('*.png'):
    data = asset.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', f'Invalid PNG signature: {asset}'
    offset = 8
    compressed = b''
    ended = False
    while offset < len(data):
        assert offset + 12 <= len(data), f'Truncated PNG chunk: {asset}'
        length = struct.unpack('>I', data[offset:offset+4])[0]
        kind = data[offset+4:offset+8]
        payload = data[offset+8:offset+8+length]
        crc = data[offset+8+length:offset+12+length]
        assert len(payload) == length and len(crc) == 4, f'Truncated PNG payload: {asset}'
        assert zlib.crc32(kind + payload) & 0xffffffff == struct.unpack('>I', crc)[0], f'PNG CRC mismatch: {asset}'
        if kind == b'IDAT': compressed += payload
        offset += length + 12
        if kind == b'IEND':
            ended = True
            break
    assert ended, f'PNG missing end chunk: {asset}'
    decoder = zlib.decompressobj()
    decoder.decompress(compressed)
    assert decoder.eof, f'Truncated PNG image stream: {asset}'
print('Validated integrity of every PNG asset.')
