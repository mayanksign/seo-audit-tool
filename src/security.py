"""Security headers shared by the Flask app and the Cloudflare Worker.

The simple headers (HSTS, nosniff, X-Frame-Options, Referrer-Policy,
Permissions-Policy) live in security-headers.json. The Content-Security-Policy
is built per response because it carries a fresh nonce.

The home page loads Google AdSense and Google Analytics. Google does not
support domain allow-lists for AdSense (its domains change), only a strict,
nonce-based policy: nonce + 'strict-dynamic' + 'unsafe-eval' (needed by the ad
code) and https:/http: as the fallback for browsers without strict-dynamic.
"""
import re
import secrets

_SCRIPT_TAG = re.compile(r"<script\b(?![^>]*\bnonce=)", re.IGNORECASE)


def new_nonce():
    return secrets.token_urlsafe(16)


def content_security_policy(nonce):
    return "; ".join([
        "default-src 'self'",
        f"script-src 'nonce-{nonce}' 'strict-dynamic' 'unsafe-inline' 'unsafe-eval' https: http:",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: https:",
        "font-src 'self' data:",
        "connect-src 'self' https:",
        "frame-src https:",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'self'",
        "frame-ancestors 'self'",
        "upgrade-insecure-requests",
    ])


def add_nonce(html, nonce):
    """Put the nonce on every <script> tag so the CSP lets them run."""
    return _SCRIPT_TAG.sub(f'<script nonce="{nonce}"', html)


def html_response_parts(html, static_headers):
    """(body_with_nonces, headers) for an HTML page."""
    nonce = new_nonce()
    headers = dict(static_headers)
    headers["Content-Security-Policy"] = content_security_policy(nonce)
    return add_nonce(html, nonce), headers
