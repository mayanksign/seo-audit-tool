from flask import Flask, request, render_template_string
import requests, socket
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>SEO Audit Tool</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Segoe UI', sans-serif;
    color: #fff;
}

.card {
    width: 95%;
    max-width: 1100px;
    background: #111827;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.6);
}

h1 {
    font-size: 28px;
    margin-bottom: 20px;
    text-align: center;
}

textarea {
    width: 100%;
    height: 120px;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 15px;
    color: white;
    font-size: 15px;
    outline: none;
}

textarea:focus {
    border-color: #38bdf8;
}

button {
    width: 100%;
    margin-top: 15px;
    padding: 14px;
    background: linear-gradient(135deg, #38bdf8, #3b82f6);
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(56,189,248,0.4);
}

table {
    width: 100%;
    margin-top: 25px;
    border-collapse: collapse;
    overflow: hidden;
    border-radius: 12px;
}

th {
    background: #1e293b;
    padding: 12px;
    font-size: 14px;
}

td {
    background: #0f172a;
    padding: 12px;
    font-size: 14px;
    text-align: center;
    border-top: 1px solid #1f2937;
}

tr:hover td {
    background: #111827;
}

.footer {
    margin-top: 20px;
    text-align: center;
    opacity: 0.6;
    font-size: 13px;
}
</style>
</head>

<body>
<div class="card">

<h1>🚀 Professional SEO Audit Tool</h1>

<form method="post">
    <textarea name="domains" placeholder="Enter domains (one per line)..."></textarea>
    <button>Run SEO Audit</button>
</form>

{% if results %}
<table>
    <tr>
        <th>Domain</th>
        <th>Status</th> 
        <th>Title</th>
        <th>Meta Desc</th>
        <th>Words</th>
        <th>H1</th>
        <th>H2</th>
        <th>Links</th>
        <th>Robots</th>
        <th>Sitemap</th>
    </tr>

    {% for r in results %}
    <tr>
        <td>{{r.domain}}</td>
        <td>{{r.status}}</td>
        <td>{{r.title}}</td>
        <td>{{r.meta}}</td>
        <td>{{r.words}}</td>
        <td>{{r.h1}}</td>
        <td>{{r.h2}}</td>
        <td>{{r.links}}</td>
        <td>{{r.robots}}</td>
        <td>{{r.sitemap}}</td>
    </tr>
    {% endfor %}
</table>
{% endif %}


<div class="footer">
    Built By Mayank | SEO Automation Tool
</div>

</div>
</body>
</html>
"""

def analyze(domain):
    data = {"domain": domain}

    domain = domain.replace("https://", "").replace("http://", "").strip()
    base = "https://" + domain


    try:
        r = requests.get(base, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")

        data["status"] = r.status_code
        data["title"] = soup.title.string.strip() if soup.title else "NA"

        meta = soup.find("meta", attrs={"name": "description"})
        data["meta"] = meta["content"][:60] if meta else "NA"

        text = soup.get_text()
        data["words"] = len(text.split())

        data["h1"] = len(soup.find_all("h1"))
        data["h2"] = len(soup.find_all("h2"))

        # Internal links count
        parsed = urlparse(base)
        internal_links = 0
        for a in soup.find_all("a", href=True):
            link = urljoin(base, a["href"])
            if urlparse(link).netloc == parsed.netloc:
                internal_links += 1
        data["links"] = internal_links

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

    return render_template_string(HTML, results=results)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=10000)


