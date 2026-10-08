import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from security import add_nonce, content_security_policy, html_response_parts  # noqa: E402

HEADERS = json.loads((ROOT / "security-headers.json").read_text(encoding="utf-8"))
REQUIRED = ["Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options",
            "Referrer-Policy", "Permissions-Policy"]


class SecurityTests(unittest.TestCase):
    def test_static_headers_present(self):
        for h in REQUIRED:
            self.assertTrue(HEADERS.get(h), h)
        self.assertEqual(HEADERS["X-Content-Type-Options"], "nosniff")

    def test_csp_is_strict_where_it_matters(self):
        csp = content_security_policy("abc")
        for part in ("default-src 'self'", "script-src 'nonce-abc' 'strict-dynamic'", "object-src 'none'",
                     "base-uri 'none'", "frame-ancestors 'self'", "form-action 'self'"):
            self.assertIn(part, csp)

    def test_nonce_on_every_script_once(self):
        html = '<script>a</script><SCRIPT src="x"></SCRIPT><script nonce="keep">b</script>'
        out = add_nonce(html, "N1")
        self.assertEqual(out.count('nonce="N1"'), 2)
        self.assertEqual(out.count("nonce="), 3)

    def test_nonce_is_fresh_and_matches_csp(self):
        page = "<script>x</script>"
        (b1, h1), (b2, h2) = html_response_parts(page, HEADERS), html_response_parts(page, HEADERS)
        n1 = re.search(r'nonce="([^"]+)"', b1).group(1)
        n2 = re.search(r'nonce="([^"]+)"', b2).group(1)
        self.assertNotEqual(n1, n2)
        self.assertIn(f"'nonce-{n1}'", h1["Content-Security-Policy"])
        for k, v in HEADERS.items():
            self.assertEqual(h1[k], v)


if __name__ == "__main__":
    unittest.main()
