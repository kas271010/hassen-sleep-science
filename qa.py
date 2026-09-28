#!/usr/bin/env python3
"""Headless QA: every page at desktop + phone, axe-core (WCAG 2.2 AA), target sizes, labels, links.
Run with the local server up: python3 -m http.server 8765 --bind 127.0.0.1"""
import json, sys, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765"
PAGES = ["index.html", "cpap-users.html", "professionals.html", "better-sleep.html", "about.html", "pricing.html", "contact.html", "404.html"]
OUT = Path(".playwright-mcp/qa"); OUT.mkdir(parents=True, exist_ok=True)
AXE = urllib.request.urlopen("https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js").read().decode()

CHECK = """async () => {
  const r = await axe.run(document, {runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}});
  await document.fonts.ready;
  const ia=[...document.querySelectorAll('a,button,input,select,textarea,summary')].filter(e=>!e.closest('.hp'))
    .map(e=>{const b=e.getBoundingClientRect();return {t:(e.textContent||e.name||'').trim().slice(0,30),h:Math.round(b.height)}}).filter(x=>x.h>0);
  const under44 = ia.filter(x=>x.h<44);
  const unlabeled=[...document.querySelectorAll('input:not([type=hidden]):not([name=botcheck]),select,textarea')].filter(i=>!document.querySelector('label[for="'+i.id+'"]')).length;
  const op0=[...document.querySelectorAll('body *')].filter(e=>getComputedStyle(e).opacity==='0').length;
  const overflow = document.documentElement.scrollWidth > innerWidth + 1;
  const links=[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'));
  return {violations:r.violations.map(v=>v.id+'('+v.impact+' x'+v.nodes.length+' '+v.nodes[0].target[0]+')'),
          bodyFs:getComputedStyle(document.body).fontSize, fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family).filter((v,i,a)=>a.indexOf(v)===i),
          targets:ia.length, under44, unlabeled, op0, overflow, links};
}"""

problems = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36")
    page = ctx.new_page()
    all_links = set()
    for vp, tag in [((1440, 900), "desktop"), ((390, 844), "phone")]:
        page.set_viewport_size({"width": vp[0], "height": vp[1]})
        for path in PAGES:
            page.goto(f"{BASE}/{path}", wait_until="networkidle")
            page.add_script_tag(content=AXE)
            res = page.evaluate(CHECK)
            page.screenshot(path=str(OUT / f"{tag}-{path.replace('.html','')}.jpeg"), full_page=True, type="jpeg", quality=70)
            all_links.update(l for l in res["links"] if not l.startswith(("http", "mailto:", "tel:")))
            bad = res["violations"] or res["under44"] or res["unlabeled"] or res["op0"] or res["overflow"] or res["bodyFs"] != "19px"
            problems += bool(bad)
            print(f"[{tag}] {path:20s} axe={len(res['violations'])} targets={res['targets']} under44={res['under44']} "
                  f"unlabeled={res['unlabeled']} op0={res['op0']} overflow={res['overflow']} fs={res['bodyFs']} fonts={res['fonts']}")
            for v in res["violations"]: print("     VIOLATION", v)
    # internal links resolve?
    for l in sorted(all_links):
        target = l.split("#")[0] or "index.html"
        code = page.request.get(f"{BASE}/{target}").status
        if code != 200: problems += 1; print("BROKEN LINK", l, code)
    b.close()
print("PROBLEM PAGES:", problems)
