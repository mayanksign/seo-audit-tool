import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from render import HomeTemplate  # noqa: E402

try:
    import jinja2
except ImportError:  # `pip install -r requirements-local.txt` brings Flask + Jinja2
    jinja2 = None

# The Worker renders the build output (partials already inlined by scripts/build.mjs).
subprocess.run(["node", str(ROOT / "scripts" / "build.mjs")], check=True, capture_output=True)
from templates_bundle import TEMPLATES  # noqa: E402

SOURCE = TEMPLATES["index.html"]
ROWS = [
    {"domain": "example.com", "status": 200, "title": "Example Domain", "meta": "NA", "words": 26,
     "h1": 1, "h2": 0, "links": 0, "robots": "No", "sitemap": "No", "final_url": "ignored"},
    {"domain": "<b>x</b>&\"'", "status": "Error", "title": "Error", "meta": "Error", "words": "-",
     "h1": "-", "h2": "-", "links": "-", "robots": "Error", "sitemap": "Error"},
]


class RenderTests(unittest.TestCase):
    def test_empty_has_no_table(self):
        out = HomeTemplate(SOURCE).render([])
        self.assertNotIn("<table", out)
        self.assertNotIn("{%", out)
        self.assertIn('name="domains"', out)

    def test_rows_are_escaped(self):
        out = HomeTemplate(SOURCE).render(ROWS)
        self.assertIn("<td data-label=\"Domain\">example.com</td>", out)
        self.assertIn("<td data-label=\"Domain\">&lt;b&gt;x&lt;/b&gt;&amp;&#34;&#39;</td>", out)
        self.assertNotIn("{{", out)

    def test_rejects_unsupported_syntax(self):
        with self.assertRaises(ValueError):
            HomeTemplate(SOURCE.replace("</body>", "{% if x %}y{% endif %}</body>"))

    @unittest.skipIf(jinja2 is None, "jinja2 not installed")
    def test_matches_jinja2(self):
        env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(str(ROOT / "templates")))
        tpl = env.get_template("index.html")
        mine = HomeTemplate(SOURCE)
        for results in ([], ROWS[:1], ROWS):
            self.assertEqual(mine.render(results), tpl.render(results=results))


if __name__ == "__main__":
    unittest.main()
