import os
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse, urljoin

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from seo_core import parse_page, normalize_domain  # noqa: E402

try:
    from bs4 import BeautifulSoup
except ImportError:  # parity checks need `pip install beautifulsoup4`
    BeautifulSoup = None


def reference(html, base):
    """The original app.py logic (BeautifulSoup), used as the oracle."""
    soup = BeautifulSoup(html, "html.parser")
    meta = soup.find("meta", attrs={"name": "description"})
    host = urlparse(base).netloc
    return {
        "title": soup.title.string.strip() if soup.title and soup.title.string else "NA",
        "meta": meta["content"].strip() if meta and meta.get("content") else "NA",
        "words": len(soup.get_text().split()),
        "h1": len(soup.find_all("h1")),
        "h2": len(soup.find_all("h2")),
        "links": sum(1 for a in soup.find_all("a", href=True)
                     if urlparse(urljoin(base, a["href"])).netloc == host),
        "images": len(soup.find_all("img")),
    }


SNIPPETS = [
    "<html><head><title> Hi &amp; bye </title><meta name='description' content='d &quot;x&quot;'>"
    "<link rel='canonical' href='https://e.com/'></head><body><h1>A</h1><H2>b</H2><h2 class=x>c</h2>"
    "<a href='/a'>1</a><a href=\"https://e.com/b\">2</a><a href='//e.com/c'>3</a>"
    "<a href='https://other.com/'>4</a><a href='mailto:a@b.c'>5</a><a href='javascript:void(0)'>6</a>"
    "<a href='#top'>7</a><a href='page.html'>8</a><a>none</a><img src=a><img src=b/></body></html>",
    "<p>foo<b>bar</b> baz&nbsp;qux</p><script>var a='<h1>x</h1> w w w';</script><style>p{}</style>"
    "<!-- <h1>c</h1> words words --><template><p>t t t</p></template><p>end</p>",
    "<title></title><meta name=description><p>x</p>",
    "<a title='a>b' href='/x'>l</a><div data-href='/no'>t</div>",
    "",
]


class ParseTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize_domain(" https://example.com "), "example.com")

    def test_basic_signals(self):
        d = parse_page(SNIPPETS[0], "https://e.com")
        self.assertEqual(d["title"], "Hi & bye")
        self.assertEqual(d["meta"], 'd "x"')
        self.assertEqual((d["h1"], d["h2"], d["images"]), (1, 2, 2))
        self.assertEqual(d["canonical"], "https://e.com/")
        self.assertEqual(d["links"], 5)  # /a, e.com/b, //e.com/c, #top, page.html

    def test_missing_everything(self):
        d = parse_page("", "https://e.com")
        self.assertEqual((d["title"], d["meta"], d["canonical"], d["words"]), ("NA", "NA", "NA", 0))


@unittest.skipIf(BeautifulSoup is None, "beautifulsoup4 not installed")
class ParityTests(unittest.TestCase):
    def check(self, html, base="https://e.com"):
        got, want = parse_page(html, base), reference(html, base)
        for k, v in want.items():
            self.assertEqual(got[k], v, f"{k} differs")

    def test_snippets(self):
        for s in SNIPPETS:
            with self.subTest(s[:40]):
                self.check(s)

    def test_site_templates(self):
        for f in sorted((ROOT / "templates").glob("*.html")):
            with self.subTest(f.name):
                self.check(f.read_text(encoding="utf-8"), "https://www.freeseoaudit.site")

    def test_extra_corpus(self):
        # Optional: SEO_CORPUS=dir/with/*.html to compare against saved real-world pages.
        d = os.environ.get("SEO_CORPUS")
        if not d:
            self.skipTest("SEO_CORPUS not set")
        for f in sorted(Path(d).glob("*.html")):
            with self.subTest(f.name):
                self.check(f.read_text(encoding="utf-8", errors="replace"), "https://" + f.stem)


if __name__ == "__main__":
    unittest.main()
