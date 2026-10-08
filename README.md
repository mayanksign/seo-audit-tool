# SEO Score – Free SEO Audit Tool

SEO Score is a free website SEO audit tool. Enter one or more domains and get an instant technical SEO snapshot in a
single table. No signup, nothing is stored.

Live site: https://www.freeseoaudit.site/

## What it checks

For every domain you enter, the report shows:

| Column | Meaning |
|---|---|
| Status | HTTP status code of the homepage (redirects are followed) |
| Title | Page `<title>` |
| Meta Desc | Meta description (`NA` if missing) |
| Words | Visible word count |
| H1 / H2 | Number of H1 and H2 headings |
| Links | Number of internal links |
| Robots | Whether `/robots.txt` exists |
| Sitemap | Whether `/sitemap.xml` exists |

A site that can't be reached or times out is shown as `Error` instead of failing the whole report. You can audit
several domains at once (one per line, up to 5 per audit) and download the results as a CSV file.

Each audit also collects the final URL after redirects, response size, canonical URL and image count.
Request them as JSON with:

```bash
curl -H "Accept: application/json" -d "domains=example.com" https://www.freeseoaudit.site/
```

## Pages

- **Home** – the audit tool, features, how it works, FAQ
- **Blog** – SEO guides: free SEO audit tool, SEO tips for beginners, improving your SEO score, on-page SEO checklist
- **About**, **Contact**, **Privacy Policy**, **Terms & Conditions**

The design is responsive: the results table becomes stacked cards on phones.

## Project structure

```
app.py                  Web app and routes
src/
  seo_core.py           HTML analysis: title, meta, words, headings, links, canonical, images
  security.py           Content-Security-Policy (with a nonce) for HTML pages
templates/              Page templates; index.html is the home page, _header.html / _footer.html are shared
static/                 site.css, site.js, logo and preview image
security-headers.json   Security headers added to every response
tests/                  Unit tests
requirements-local.txt  Python dependencies
```

## Run locally

You need Python 3.13 or newer.

```bash
python -m venv .venv
.venv\Scripts\activate                 # macOS/Linux: source .venv/bin/activate
pip install -r requirements-local.txt
python app.py
```

Open http://localhost:10000 and enter a domain such as `example.com`.

## Run the tests

```bash
python -m unittest discover -s tests
```

## Security

Every response carries `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` and
`Permissions-Policy`. HTML pages also get a `Content-Security-Policy` with a fresh nonce on each response. The simple
headers are edited in `security-headers.json`. The policy is written to keep Google AdSense and Google Analytics working,
so avoid changing it to a plain domain list.

Only public hostnames are audited when running in production. IP addresses and `localhost` are rejected.

## Limits

- Up to 5 domains per audit; extra lines are shown as `Skipped`.
- Only the first 400,000 characters of a page's HTML are analysed.
- Requests to other websites time out after 8 seconds (5 seconds for `robots.txt` and `sitemap.xml`).

## Author

Built by Mayank.
