from flask import Flask, request, render_template, send_from_directory
import requests

import os

import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from seo_core import normalize_domain, parse_page

app = Flask(__name__)

# The home page markup now lives in templates/index.html (it used to be an
# inline HTML string here) so the Flask app and the Cloudflare Worker share it.


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/blog/free-seo-audit-tool')
def blog1():
    return render_template('blog1.html')

@app.route('/blog/seo-tips-for-beginners')
def blog2():
    return render_template('blog2.html')


@app.route('/blog/improve-website-seo-score')
def blog3():
    return render_template('blog3.html')

@app.route('/blog/on-page-seo-checklist')
def blog4():
    return render_template('blog4.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')



@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')


@app.route('/llms.txt')
def llms():
    return send_from_directory('.', 'llms.txt')



@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico')


def analyze(domain):
    data = {"domain": domain}

    base = "https://" + normalize_domain(domain)

    try:
        r = requests.get(base, timeout=8)
        data.update(parse_page(r.text, base))
        data["status"] = r.status_code
        data["final_url"] = r.url
        data["redirected"] = bool(r.history)
        data["size_bytes"] = len(r.content)

    except:
        data.update({"status":"Error","title":"Error","meta":"Error","words":"-","h1":"-","h2":"-","links":"-"})

    try:
        rob = requests.get(base + "/robots.txt", timeout=5)
        data["robots"] = "Yes" if rob.status_code == 200 else "No"
    except:
        data["robots"] = "Error"



    try:
        site = requests.get(base + "/sitemap.xml", timeout=5)
        data["sitemap"] = "Yes" if site.status_code == 200 else "No"
    except:
        data["sitemap"] = "Error"

    return data

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        domains = request.form["domains"].splitlines()

        for d in domains:
            d = d.strip()
            if d:
                results.append(analyze(d))

    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
