"""Runtime-independent SEO parsing shared by the Flask app and the Cloudflare Worker.

Nothing here does network I/O, so it runs unchanged under CPython (Flask,
`requests`) and Pyodide (Cloudflare Python Workers, `fetch`).

It uses only the standard library. The Free Workers plan allows ~10 ms of CPU
per request, and building a BeautifulSoup tree for every page is several times
slower than the regex scan below. Results match
`BeautifulSoup(html, "html.parser")` for the signals the audit reports
(see tests/test_seo_core.py for the parity check).
"""
import html as _html
import re
from urllib.parse import urlparse, urljoin

_F = re.IGNORECASE
_FS = re.IGNORECASE | re.DOTALL

# One left-to-right pass that drops comments and <script>/<style> bodies (their
# contents are never markup). <template> bodies still contain real elements
# (counted as headings/images/links) but their text is not part of get_text().
_DROP = re.compile(r"<!--.*?-->|<(script|style)\b[^>]*>.*?</\1\s*>", _FS)
_TEMPLATE = re.compile(r"<template\b[^>]*>.*?</template\s*>", _FS)
# Any tag / doctype / processing instruction, tolerating '>' inside quoted attributes.
_TAG = re.compile(
    r"<(?:/?[a-zA-Z][^>\"']*(?:(?:\"[^\"]*\"|'[^']*')[^>\"']*)*|[!?][^>]*)>"
)
_ATTRS = r"((?:[^>\"']|\"[^\"]*\"|'[^']*')*)"
_TITLE = re.compile(r"<title\b[^>]*>(.*?)</title\s*>", _FS)
_META = re.compile(r"<meta\b" + _ATTRS + ">", _F)
_LINK = re.compile(r"<link\b" + _ATTRS + ">", _F)
_A_HREF = re.compile(
    r"<a\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*?\shref\s*=\s*"
    r"(?:\"([^\"]*)\"|'([^']*)'|([^\s>\"']+))", _F
)
_ATTR = re.compile(
    r"([^\s=/\"'>]+)(?:\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>\"']*)))?"
)
_H1 = re.compile(r"<h1(?![\w:-])", _F)
_H2 = re.compile(r"<h2(?![\w:-])", _F)
_IMG = re.compile(r"<img(?![\w:-])", _F)


def normalize_domain(domain):
    return domain.replace("https://", "").replace("http://", "").strip()


def _attrs(raw):
    out = {}
    for m in _ATTR.finditer(raw):
        name = m.group(1).lower()
        if name in out:  # first occurrence wins, like html.parser
            continue
        val = m.group(2)
        if val is None:
            val = m.group(3)
        if val is None:
            val = m.group(4)
        out[name] = _html.unescape(val) if val and "&" in val else (val or "")
    return out


_NETLOC_END = re.compile(r"[/?#]")
_NON_HTTP = ("mailto:", "tel:", "javascript:", "sms:", "data:")


def _is_internal(href, host):
    h = href.strip()
    # Fast paths for the common absolute forms (urljoin/urlparse are slow in bulk).
    low = h[:11].lower()
    if low.startswith(("https://", "http://")):
        rest = h[h.index("//") + 2:]
        end = _NETLOC_END.search(rest)
        return (rest[:end.start()] if end else rest) == host
    if low.startswith(_NON_HTTP):
        return False
    # Relative references ("/x", "page", "#top", "?q=1") can never leave the host.
    if h[:2] != "//":
        first = h.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
        if ":" not in first:
            return True
    return urlparse(urljoin("https://" + host + "/", h)).netloc == host


def parse_page(html, base):
    """Extract the on-page SEO signals from an HTML document fetched from `base`."""
    clean = _DROP.sub("", html)
    data = {}

    m = _TITLE.search(clean)
    title = _html.unescape(m.group(1)).strip() if m else ""
    data["title"] = title or "NA"

    data["meta"] = "NA"
    for m in _META.finditer(clean):
        a = _attrs(m.group(1))
        if a.get("name") == "description":
            data["meta"] = a.get("content", "").strip() or "NA"
            break

    text = _TAG.sub("", _TEMPLATE.sub("", clean) if "<template" in clean else clean)
    if "&" in text:
        text = _html.unescape(text)
    data["words"] = len(text.split())

    data["h1"] = len(_H1.findall(clean))
    data["h2"] = len(_H2.findall(clean))

    # Internal links count
    host = urlparse(base).netloc
    internal_links = 0
    for m in _A_HREF.finditer(clean):
        href = m.group(1)
        if href is None:
            href = m.group(2)
        if href is None:
            href = m.group(3)
        if "&" in href:
            href = _html.unescape(href)
        if _is_internal(href, host):
            internal_links += 1
    data["links"] = internal_links

    # Extra signals (collected for API consumers; not shown in the table)
    data["canonical"] = "NA"
    for m in _LINK.finditer(clean):
        a = _attrs(m.group(1))
        if "canonical" in a.get("rel", "").lower().split() and a.get("href"):
            data["canonical"] = a["href"].strip()
            break
    data["images"] = len(_IMG.findall(clean))

    return data
