/* SEO SCORE – progressive enhancement only; every page works without this file. */
(function () {
  "use strict";

  // Highlight the current page in the navigation.
  var path = location.pathname.replace(/\/$/, "") || "/";
  document.querySelectorAll(".nav-links a[href]").forEach(function (a) {
    var href = a.getAttribute("href");
    if (href === path || (href !== "/" && path.indexOf(href + "/") === 0)) a.setAttribute("aria-current", "page");
  });

  // Audit form: busy state while the (server-side) audit runs.
  var form = document.getElementById("auditForm");
  var btn = document.getElementById("analyzeBtn");
  if (form && btn) {
    form.addEventListener("submit", function () {
      var ta = form.querySelector("textarea");
      if (ta && !ta.value.trim()) return;
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner" aria-hidden="true"></span> Analyzing…';
    });
    btn.addEventListener("click", function () {
      if (typeof gtag === "function") {
        gtag("event", "analyze_click", { event_category: "SEO Tool", event_label: "Analyze Website Now" });
      }
    });
  }

  // Results: status pills and CSV export.
  var results = document.getElementById("results");
  if (results) {
    var cls = function (v, col) {
      v = v.trim();
      if (col === 1) { // HTTP status
        if (/^2/.test(v)) return "ok";
        if (/^3/.test(v)) return "warn";
        return "bad";
      }
      if (v === "Yes") return "ok";
      if (v === "No") return "warn";
      if (v === "Error") return "bad";
      return "";
    };
    results.querySelectorAll("tbody tr").forEach(function (tr) {
      tr.querySelectorAll("td").forEach(function (td, i) {
        if (i === 1 || i === 8 || i === 9 || td.textContent.trim() === "Error") {
          var c = cls(td.textContent, i);
          if (c) td.innerHTML = '<span class="pill ' + c + '">' + td.innerHTML + "</span>";
        }
      });
    });
    var csvBtn = document.getElementById("csvBtn");
    if (csvBtn) {
      csvBtn.addEventListener("click", function () {
        var rows = [];
        results.querySelectorAll("tr").forEach(function (tr) {
          var cells = [];
          tr.querySelectorAll("th,td").forEach(function (c) {
            cells.push('"' + c.textContent.trim().replace(/"/g, '""') + '"');
          });
          if (cells.length) rows.push(cells.join(","));
        });
        var a = document.createElement("a");
        a.href = URL.createObjectURL(new Blob([rows.join("\r\n")], { type: "text/csv" }));
        a.download = "seo-audit.csv";
        document.body.appendChild(a);
        a.click();
        a.remove();
      });
    }
  }
})();
