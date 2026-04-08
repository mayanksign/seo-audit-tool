from flask import Flask, request, render_template, render_template_string, send_from_directory
import requests, socket
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-4N0SB8JHTS"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-4N0SB8JHTS');
</script>



<link rel="icon" href="/favicon.ico?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Free SEO Audit Tool Online | Check Website SEO Score Instantly</title>

  <meta name="description" content="Analyze your website SEO instantly with our free SEO audit tool. Get detailed reports, errors, and suggestions without signup.">

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}


body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    font-family: 'Segoe UI', sans-serif;
    color: #fff;
    margin: 0;
}



.page-wrap {
    flex: 1;
    padding: 150px 0 80px;
}


.card {
    width: 95%;
    max-width: 1100px;
    background: #111827;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.6);
    margin: 20px auto 0;
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




.main-footer {
    width: 100%;
    background: #020617;
    padding: 22px 20px;
    text-align: center;
    color: #cbd5e1;
    border-top: 1px solid #1f2937;
  
}



.footer-links {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
}

.footer-links a {
    color: #38bdf8;
    text-decoration: none;
    font-size: 14px;
}

.footer-links a:hover {
    color: #60a5fa;
    text-decoration: underline;
}




.subheading {
  font-size: 16px;
  color: #cbd5e1; /* light grey */
  text-align: center;
  margin-bottom: 15px;
}


.trust-lines {
  text-align: center;
  margin-top: 12px;
}

.trust-lines p {
  display: inline-block;
  margin: 5px 8px;
  padding: 6px 12px;
  background: rgba(255,255,255,0.1);
  border-radius: 20px;
  font-size: 13px;
  color: #fff;
}




@media (max-width: 768px) {

 body {
        padding: 0;
    }

    .page-wrap {
        flex: 1;
        padding: 110px 0 20px;
    }


    

    .card {
        width: calc(100% - 24px);
        padding: 18px;
        margin: 12px auto 0;
        border-radius: 16px;
    }

    h1 {
        font-size: 22px;
    }

    .subheading {
        font-size: 14px;
        line-height: 1.5;
    }

    textarea {
        height: 110px;
        font-size: 14px;
    }

    button {
        font-size: 15px;
        padding: 13px;
    }

    .trust-lines p {
        font-size: 12px;
        margin: 4px;
        padding: 6px 10px;
    }

.page-wrap {
    padding: 110px 0 20px;
}

    .main-footer {
        padding: 14px 10px;
    }

    .main-footer p,
    .footer-links a,
    .footer-links span {
        font-size: 13px;
    }

    nav {
        padding: 10px 14px !important;
        flex-wrap: wrap;
        gap: 10px;
    }
}



</style>
</head>

<body>

<nav style="
    width:100%;
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px 40px;
    background:#0f172a;
    color:white;
    position:fixed;
    top:0;
    left:0;
    z-index:1000;
">

    <!-- Logo LEFT -->
    <div>
        <a href="/" style="text-decoration:none;">
            <span style="font-size:25px; font-weight:500; letter-spacing:1px;">
                <span style="color:#2563eb;">SEO</span> 
                <span style="color:#cbd5e1;">SCORE</span>
            </span>
        </a>
    </div>

    <!-- Menu RIGHT -->
    <div style="display:flex; align-items:center; gap:30px;">
        <a href="/" style="color:white; text-decoration:none;">Home</a>
        <a href="/about" style="color:white; text-decoration:none;">About</a>
        <a href="/contact" style="color:white; text-decoration:none;">Contact</a>

        <a href="/" style="background:#2563eb; padding:8px 18px; border-radius:6px; color:white; text-decoration:none;">
            Analyze
        </a>
    </div>

</nav>


<div class="page-wrap">

<div class="card">

<h1>🚀 Free SEO Audit Tool</h1>

<p class="subheading">
  Check your website SEO score instantly & fix issues in seconds
</p>

<form method="post">
    <textarea name="domains" placeholder="Enter domains (one per line)..."></textarea>

<button>Analyze Website Now </button>

<div class="trust-lines">
  <p>✅ 1000+ Websites Analyzed</p>
  <p>✅ Free & Instant Report</p>
  <p>✅ No Signup Required</p>
</div>
   
</form>

{% if results %}
<div style="max-height:500px; overflow-y:auto; margin:20px 30px 0;">
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
</div>
{% endif %}



</div>

</div>

<div class="main-footer">
    <p>© 2026 Free SEO Audit Tool | Built by Mayank</p>
    <div class="footer-links">
        <a href="/privacy-policy">Privacy Policy</a>
        <span>|</span>
        <a href="/terms-and-conditions">Terms & Conditions</a>
    </div>
</div>





</body>

</html>
"""



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')
  

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico')





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
        data["meta"] = meta["content"][:160] if meta else "NA"

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
