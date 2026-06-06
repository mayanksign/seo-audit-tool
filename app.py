from flask import Flask, request, render_template, render_template_string, send_from_directory
import requests, socket

import os

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


<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "SEO Score",
  "url": "https://www.freeseoaudit.site/",
  "description": "Free SEO Audit Tool for Technical SEO Analysis and Website Optimization."
}
</script>




<link rel="icon" href="/favicon.ico?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Free SEO Audit Tool Online | Check Website SEO Score Instantly</title>

<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"WebSite",
  "name":"SEO Score",
  "url":"https://www.freeseoaudit.site/"
}
</script>

  

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
    padding: 30px 20px;
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





.seo-report-section{
    margin-top:90px;
    padding:40px 0;
}

.seo-report-wrapper{
    max-width:1300px;
    margin:auto;
    background:#0f172a;
    border:1px solid rgba(255,255,255,.08);
    border-radius:28px;
    padding:60px;
    display:flex;
    gap:70px;
    align-items:center;
    justify-content:space-between;
    box-shadow:0 0 40px rgba(59,130,246,.08);
}

.section-badge{
    display:inline-block;
    background:rgba(59,130,246,.12);
    color:#60a5fa;
    padding:10px 18px;
    border-radius:30px;
    font-size:14px;
    margin-bottom:20px;
}

.seo-report-content{
    flex:1;

max-width:700px;

    
}

.seo-report-content h2{
    font-size:36px;
    margin-bottom:15px;
    color:#fff;



    
}

.seo-text{
    color:#cbd5e1;
    line-height:1.9;
    margin-bottom:25px;
}

.seo-feature-grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:15px;
}

.seo-feature-card{
    background:#111827;
    border-radius:18px;
    padding:18px;
    display:flex;
    gap:14px;
    border:1px solid rgba(255,255,255,.06);
}

.seo-feature-card span{
    font-size:28px;
}

.seo-feature-card h4{
    color:#fff;
    margin-bottom:5px;
}

.seo-feature-card p{
    color:#94a3b8;
    font-size:14px;
}

.seo-report-image{
    flex:1;
}

.seo-report-image img{
    width:100%;
    max-width:760px;
    border-radius:24px;
    border:1px solid rgba(255,255,255,.08);
    box-shadow:
    0 20px 60px rgba(0,0,0,.45),
    0 0 50px rgba(59,130,246,.10);
    transition:.3s ease;
}

.seo-report-image img:hover{
    transform:translateY(-6px);
}

@media(max-width:768px){

    .seo-report-wrapper{
        flex-direction:column;
        padding:25px;
    }

    .seo-feature-grid{
        grid-template-columns:1fr;
    }

    .seo-report-content h2{
        font-size:28px;
        text-align:center;
    }

    .seo-text{
        text-align:center;
    }

    .section-badge{
        display:table;
        margin:auto auto 20px;
    }
}






.modern-sections{
width:95%;
max-width:1200px;
margin:90px auto;
}

.section-title{
text-align:center;
margin-bottom:40px;
}

.section-title span{
color:#60a5fa;
font-size:14px;
letter-spacing:1px;
}

.section-title h2{
font-size:42px;
margin:15px 0;
}

.section-title p{
color:#94a3b8;
max-width:700px;
margin:auto;
line-height:1.8;
}

.spacing-top{
margin-top:90px;
}

.steps-grid{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:25px;
}

.mini-box{
background:rgba(255,255,255,.03);
border:1px solid rgba(255,255,255,.06);
border-radius:25px;
padding:35px;
transition:.3s ease;
}

.mini-box:hover{
transform:translateY(-6px);
}

.step-circle{
width:55px;
height:55px;
border-radius:50%;
background:#2563eb;
display:flex;
align-items:center;
justify-content:center;
font-size:22px;
font-weight:bold;
margin-bottom:20px;
}

.mini-box h3{
margin-bottom:12px;
}

.mini-box p{
color:#94a3b8;
line-height:1.7;
}

.feature-list{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:18px;
}

.feature-item{
background:rgba(255,255,255,.03);
border-radius:18px;
padding:22px;
text-align:center;
}

.faq-wrap{
display:flex;
flex-direction:column;
gap:18px;
}

.faq-box{
background:rgba(255,255,255,.03);
border-radius:20px;
padding:30px;
}

.faq-box p{
color:#94a3b8;
margin-top:12px;
line-height:1.8;
}

.blog-grid{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:20px;
}

.blog-card{
background:rgba(255,255,255,.03);
padding:28px;
border-radius:20px;
text-decoration:none;
color:#60a5fa;
transition:.3s;
}

.blog-card:hover{
transform:translateY(-5px);
}

@media(max-width:768px){

```
.section-title h2{
    font-size:30px;
}

.steps-grid,
.feature-list,
.blog-grid{
    grid-template-columns:1fr;
}
```

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

        <a href="/blog" style="background:#2563eb; padding:8px 18px; border-radius:6px; color:white; text-decoration:none;">
            Blog
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

<button id="analyzeBtn">Analyze Website Now </button>

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




<section class="seo-report-section">

    <div class="seo-report-wrapper">

        <div class="seo-report-content">

            <span class="section-badge">
                🚀 Complete Website SEO Analysis
            </span>

            <h2>
                What Our Free SEO Audit Tool Analyzes
            </h2>

            <p class="seo-text">
                Get a complete SEO audit report instantly. Our tool analyzes
                website title, meta description, heading structure, word count,
                links, robots.txt, sitemap availability, and technical SEO
                signals to help improve rankings.
            </p>

            <div class="seo-feature-grid">

                <div class="seo-feature-card">
                    <span>📌</span>
                    <div>
                        <h4>SEO Title Check</h4>
                        <p>Analyze title optimization.</p>
                    </div>
                </div>

                <div class="seo-feature-card">
                    <span>📝</span>
                    <div>
                        <h4>Meta Description</h4>
                        <p>Check SEO description quality.</p>
                    </div>
                </div>

                <div class="seo-feature-card">
                    <span>🏷️</span>
                    <div>
                        <h4>Heading Analysis</h4>
                        <p>H1 & H2 structure detection.</p>
                    </div>
                </div>

                <div class="seo-feature-card">
                    <span>🔗</span>
                    <div>
                        <h4>Links Analysis</h4>
                        <p>Detect internal links.</p>
                    </div>
                </div>

                <div class="seo-feature-card">
                    <span>🤖</span>
                    <div>
                        <h4>Robots.txt Check</h4>
                        <p>Verify robots.txt instantly.</p>
                    </div>
                </div>

                <div class="seo-feature-card">
                    <span>🗺️</span>
                    <div>
                        <h4>Sitemap Detection</h4>
                        <p>Check sitemap availability.</p>
                    </div>
                </div>

            </div>

        </div>

        <div class="seo-report-image">

            <img src="/static/result-preview.png"
                 alt="SEO Audit Report Preview">

        </div>

    </div>

</section>




<section class="modern-sections">


<!-- HOW IT WORKS -->
<div class="section-title">
    <span>⚡ HOW IT WORKS</span>
    <h2>How Our SEO Audit Tool Works</h2>
    <p>
        Analyze your website in seconds with a simple and fast process.
    </p>
</div>

<div class="steps-grid">

    <div class="mini-box">
        <div class="step-circle">1</div>
        <h3>Enter Website URL</h3>
        <p>
            Paste your website domain to start SEO analysis instantly.
        </p>
    </div>

    <div class="mini-box">
        <div class="step-circle">2</div>
        <h3>Analyze Website</h3>
        <p>
            Click analyze to check titles, headings, links and SEO signals.
        </p>
    </div>

    <div class="mini-box">
        <div class="step-circle">3</div>
        <h3>Get SEO Report</h3>
        <p>
            View sitemap, robots.txt, meta description and website insights.
        </p>
    </div>

</div>


<!-- WHY CHOOSE -->
<div class="section-title spacing-top">
    <span>🔥 WHY CHOOSE US</span>
    <h2>Why Use Our Free SEO Audit Tool?</h2>
</div>

<div class="feature-list">

    <div class="feature-item">✅ 100% Free SEO Analysis</div>
    <div class="feature-item">⚡ Instant Website Report</div>
    <div class="feature-item">🔒 No Signup Required</div>
    <div class="feature-item">📈 SEO Friendly Insights</div>
    <div class="feature-item">🛠 Technical SEO Checks</div>
    <div class="feature-item">🚀 Beginner Friendly</div>

</div>


<!-- FAQ -->
<div class="section-title spacing-top">
    <span>❓ FAQ</span>
    <h2>Frequently Asked Questions</h2>
</div>

<div class="faq-wrap">

    <div class="faq-box">
        <h3>1. What is an SEO audit tool?</h3>
        <p>
            An SEO audit tool helps analyze your website and detect SEO issues
            like title optimization, meta description, headings, internal links,
            robots.txt, sitemap availability and technical SEO problems.
        </p>
    </div>

    <div class="faq-box">
        <h3>2. Is this SEO audit tool completely free?</h3>
        <p>
            Yes, our free SEO audit tool is completely free to use.
            You can analyze websites instantly without signup or payment.
        </p>
    </div>

    <div class="faq-box">
        <h3>3. What does this SEO audit tool analyze?</h3>
        <p>
            Our SEO checker analyzes website title, meta description,
            word count, heading structure (H1 & H2), internal links,
            robots.txt, sitemap.xml and technical SEO signals.
        </p>
    </div>

    <div class="faq-box">
        <h3>4. How can I improve my website SEO score?</h3>
        <p>
            You can improve SEO score by optimizing title tags,
            meta descriptions, headings, internal links, content quality,
            robots.txt and sitemap structure.
        </p>
    </div>

    <div class="faq-box">
        <h3>5. Do I need technical knowledge to use this tool?</h3>
        <p>
            No. Our SEO audit tool is beginner friendly and easy to use.
            Simply enter your website URL and get instant SEO insights.
        </p>
    </div>

    <div class="faq-box">
        <h3>6. Can I use this SEO audit tool for any website?</h3>
        <p>
            Yes, you can analyze blogs, business websites,
            ecommerce stores, portfolio websites and almost any public website.
        </p>
    </div>

    <div class="faq-box">
        <h3>7. Why are robots.txt and sitemap important for SEO?</h3>
        <p>
            Robots.txt helps search engines understand crawl rules,
            while sitemap.xml helps search engines discover and index pages faster.
        </p>
    </div>

    <div class="faq-box">
        <h3>8. Does this tool help improve Google rankings?</h3>
        <p>
            The tool identifies SEO issues and improvement opportunities.
            Fixing these problems can help improve website visibility and SEO performance.
        </p>
    </div>

</div>


<!-- BLOG LINKS -->
<div class="section-title spacing-top">
    <span>📚 SEO BLOGS</span>
    <h2>Learn SEO With Our Guides</h2>
</div>

<div class="blog-grid">

    <a href="/blog/free-seo-audit-tool" class="blog-card">
        Free SEO Audit Tool Guide →
    </a>

    <a href="/blog/improve-website-seo-score" class="blog-card">
        Improve Website SEO Score →
    </a>

    <a href="/blog/on-page-seo-checklist" class="blog-card">
        On Page SEO Checklist →
    </a>

</div>


</section>







<div class="main-footer">
    <p>© 2026 Free SEO Audit Tool | Built by Mayank</p>
    <div class="footer-links">
        <a href="/privacy">Privacy Policy</a>
        <span>|</span>
        <a href="/terms">Terms & Conditions</a>
    </div>
</div>



<script>
document.getElementById("analyzeBtn").addEventListener("click", function() {

    gtag('event', 'analyze_click', {
        event_category: 'SEO Tool',
        event_label: 'Analyze Website Now'
    });

});
</script>




</body>

</html>
"""


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
    sitemap_urls = [
        "/sitemap.xml",
        "/sitemap_index.xml",
        "/wp-sitemap.xml"
    ]

    data["sitemap"] = "No"

    for path in sitemap_urls:
        site = requests.get(base + path, timeout=5)

        if site.status_code == 200:
            data["sitemap"] = "Yes"
            break

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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
