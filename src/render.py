"""Minimal renderer for templates/index.html, used by the Worker instead of Jinja2.

index.html only uses one `{% if results %}` block wrapping one
`{% for r in results %}` loop with `{{r.field}}` substitutions. Handling just
that keeps the Worker free of third-party runtime dependencies (Jinja2 pulls in
MarkupSafe, a compiled package). Output is identical to Jinja2 with autoescape
on (tests/test_render.py checks this). The pattern is checked at import time,
so a template change that this renderer can't handle fails the deploy instead
of serving a broken page.
"""
import re

_BLOCK = re.compile(
    r"\{%\s*if results\s*%\}(.*?)\{%\s*for r in results\s*%\}(.*?)\{%\s*endfor\s*%\}(.*?)\{%\s*endif\s*%\}",
    re.DOTALL,
)
_VAR = re.compile(r"\{\{\s*r\.(\w+)\s*\}\}")
_ESCAPES = {"&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&#34;"}
_ESCAPE_RE = re.compile("[&<>'\"]")


def escape(value):
    return _ESCAPE_RE.sub(lambda m: _ESCAPES[m.group()], str(value))


class HomeTemplate:
    def __init__(self, source):
        blocks = _BLOCK.findall(source)
        if len(blocks) != 1:
            raise ValueError("index.html: expected exactly one if/for results block")
        m = _BLOCK.search(source)
        self.before = source[:m.start()]
        self.head, self.row, self.tail = m.group(1), m.group(2), m.group(3)
        self.after = source[m.end():]
        if self.after.endswith("\n"):  # Jinja2 drops a single trailing newline
            self.after = self.after[:-1]
        for part in (self.before, self.head, self.tail, self.after):
            if "{%" in part or "{{" in part:
                raise ValueError("index.html: unsupported template syntax outside the results block")
        if "{%" in self.row:
            raise ValueError("index.html: unsupported statement inside the results loop")
        # alternating [text, field, text, field, ..., text]
        self._row_parts = _VAR.split(self.row)
        if any("{{" in p for p in self._row_parts[::2]):
            raise ValueError("index.html: unsupported expression inside the results loop")

    def render(self, results):
        out = [self.before]
        if results:
            out.append(self.head)
            for r in results:
                parts = self._row_parts[:]
                for i in range(1, len(parts), 2):
                    parts[i] = escape(r.get(parts[i], ""))
                out.append("".join(parts))
            out.append(self.tail)
        out.append(self.after)
        return "".join(out)
