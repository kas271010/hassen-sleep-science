#!/usr/bin/env python3
"""One live submission of the patient request form on the deployed site. Sends ONE real email to the inbox."""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://mycpapdoctor.com"
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36").new_page()
    page.goto(f"{BASE}/contact.html", wait_until="networkidle")
    page.fill("#p-name", "QA test (delete me)")
    page.fill("#p-phone", "000-000-0000")
    page.select_option("#p-time", "Any time")
    page.fill("#p-note", "Automated form test from the redesign QA. Please delete.")
    with page.expect_response(lambda r: "api.web3forms.com/submit" in r.url) as resp:
        page.click("form button[type=submit]")
    r = resp.value
    page.wait_for_function("document.querySelector('.form-status').textContent.length > 10")
    print("web3forms HTTP", r.status, "| status text:", page.inner_text(".form-status"))
    b.close()
