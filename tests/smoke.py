"""Live smoke test for a running Worker (local `wrangler dev` or a deployed URL).

    python tests/smoke.py                       # http://127.0.0.1:8787
    python tests/smoke.py https://seo.example.com

Needs internet access from the Worker (it audits example.com). Exit code 0 = pass.
"""
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8787").rstrip("/")
failures = []


def req(path, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    r = urllib.request.Request(BASE + path, data=body, headers={"User-Agent": "smoke-test"})
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def rows(html):
    """Table rows as lists of cell text (domain, status, title, meta, words, h1, h2, links, robots, sitemap)."""
    return [re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S) for tr in re.findall(r"<tr>(.*?)</tr>", html, re.S) if "<td" in tr]


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail and not ok else ""))
    if not ok:
        failures.append(name)


s, h = req("/")
check("GET / -> 200 with form", s == 200 and 'name="domains"' in h and "Free SEO Audit Tool" in h and not rows(h), s)

for path in ["/about", "/contact", "/blog", "/blog/free-seo-audit-tool", "/blog/seo-tips-for-beginners",
             "/blog/improve-website-seo-score", "/blog/on-page-seo-checklist", "/privacy", "/terms"]:
    s, _ = req(path)
    check(f"GET {path} -> 200", s == 200, s)

for path in ["/robots.txt", "/sitemap.xml", "/llms.txt", "/favicon.ico", "/static/logo.png"]:
    s, _ = req(path)
    check(f"GET {path} -> 200 (static asset)", s == 200, s)

s, _ = req("/does-not-exist")
check("GET unknown path -> 404", s == 404, s)

s, h = req("/", {"domains": "example.com"})
r = rows(h)
ok = s == 200 and len(r) == 1 and r[0][0] == "example.com" and r[0][1] == "200" and r[0][2] == "Example Domain"
check("POST / example.com -> status 200, title 'Example Domain'", ok, r)

s, h = req("/", {"domains": "https://google.com\nthis-domain-does-not-exist-12345.invalid\nlocalhost\n127.0.0.1"})
r = rows(h)
check("POST / redirecting domain (google.com) -> 200", len(r) == 4 and r[0][1] == "200", r[:1])
check("POST / unresolvable domain -> Error row, page still renders", len(r) == 4 and r[1][1:4] == ["Error"] * 3, r[1:2])
check("POST / localhost / IP rejected -> Error rows", len(r) == 4 and r[2][1] == "Error" and r[3][1] == "Error", r[2:])

many = "\n".join(f"example{i}.com" for i in range(30))
s, h = req("/", {"domains": many})
r = rows(h)
check("POST / over the limit -> extras reported as Skipped", s == 200 and len(r) == 30 and "Skipped" in r[-1][1], (s, len(r)))

# Security headers on pages, static assets and error responses.
SEC = ["Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy", "Permissions-Policy"]


def headers_of(path):
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + path, headers={"User-Agent": "smoke-test"}), timeout=60) as r:
            return r.headers, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.headers, ""


for path in ["/", "/about", "/blog/free-seo-audit-tool", "/static/site.css", "/static/logo.png", "/robots.txt", "/nope"]:
    h, _ = headers_of(path)
    missing = [k for k in SEC if not h.get(k)]
    check(f"security headers on {path}", not missing, missing)

h1, b1 = headers_of("/")
h2, b2 = headers_of("/")
n1 = re.search(r'nonce="([^"]+)"', b1)
n2 = re.search(r'nonce="([^"]+)"', b2)
csp = h1.get("Content-Security-Policy", "")
check("CSP present with nonce that matches the page's scripts",
      bool(n1) and f"'nonce-{n1.group(1)}'" in csp and "object-src 'none'" in csp, csp[:120])
check("CSP nonce changes on every response", bool(n1 and n2) and n1.group(1) != n2.group(1))
check("every <script> on / carries the nonce", len(re.findall(r"<script\b(?![^>]*nonce=)", b1)) == 0)

# Opt-in JSON view (Accept: application/json) exposes the signals the table doesn't show.
import json  # noqa: E402

r = urllib.request.Request(BASE + "/", data=urllib.parse.urlencode({"domains": "google.com\nexample.com"}).encode(),
                           headers={"Accept": "application/json", "User-Agent": "smoke-test"})
with urllib.request.urlopen(r, timeout=90) as resp:
    js = json.loads(resp.read())
g, e = js[0], js[1]
check("JSON: redirect detected + final URL (google.com)", g.get("redirected") is True and "google" in g.get("final_url", ""), g)
check("JSON: response size > 0", isinstance(g.get("size_bytes"), int) and g["size_bytes"] > 0, g.get("size_bytes"))
check("JSON: example.com title/meta/canonical/images/links",
      e["title"] == "Example Domain" and e["meta"] == "NA" and e["canonical"] == "NA" and e["images"] == 0
      and e["links"] == 0 and e["redirected"] is False and e["robots"] == "No", e)

s, h = req("/", {"domains": ""})
check("POST / empty input -> 200, no rows", s == 200 and not rows(h), s)

print("\nFAILED: " + ", ".join(failures) if failures else "\nAll smoke checks passed.")
sys.exit(1 if failures else 0)
