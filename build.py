#!/usr/bin/env python3
"""Assembles the static pages from one shared header/footer. Output is plain HTML committed to the repo.
Run: python3 build.py   (no dependencies)"""
from pathlib import Path

PHONE_TEL = "tel:+18105238233"
PHONE = "(810) 523-8233"
EMAIL = "khassen@mycpapdoctor.com"
SITE = "https://mycpapdoctor.com"
W3F_KEY = "2942bb44-82bb-416e-ae02-0df36865d919"

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6.2 6.2l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'

NAV = [("cpap-users.html", "For CPAP users"), ("professionals.html", "For professionals"),
       ("better-sleep.html", "Sleep map"), ("about.html", "About"), ("pricing.html", "Pricing"), ("contact.html", "Contact")]

# Simple line icons for the map stops and benefit tiles (stroke inherits currentColor)
def ico(paths):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'

I = {
    "doctor":  ico('<path d="M9 3v4a3 3 0 0 0 6 0V3"/><path d="M6 7v3a6 6 0 0 0 12 0V7"/><circle cx="18" cy="17" r="3"/><path d="M12 16v1a3 3 0 0 0 3 3"/>'),
    "study":   ico('<path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/><path d="M3 20h8"/>'),
    "dx":      ico('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3h6v3H9z"/><path d="M9 12h6M9 16h4"/>'),
    "rx":      ico('<path d="M6 3h6a4 4 0 0 1 0 8H6z"/><path d="M6 3v18"/><path d="M12 11l7 10"/><path d="M19 11l-7 10"/>'),
    "dme":     ico('<path d="M3 7h11v10H3z"/><path d="M14 10h4l3 3v4h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>'),
    "monitor": ico('<path d="M2 9a14 14 0 0 1 20 0"/><path d="M6 13a9 9 0 0 1 12 0"/><path d="M9.5 16.5a4 4 0 0 1 5 0"/><circle cx="12" cy="20" r="1"/>'),
    "adjust":  ico('<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="9" cy="6" r="2" fill="currentColor"/><circle cx="15" cy="12" r="2" fill="currentColor"/><circle cx="8" cy="18" r="2" fill="currentColor"/>'),
    "repeat":  ico('<path d="M17 2l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>'),
    "sun":     ico('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    "energy":  ico('<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>'),
    "heart":   ico('<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>'),
    "car":     ico('<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11"/><path d="M3 11h18v6H3z"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>'),
    "mood":    ico('<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><path d="M9 9h.01M15 9h.01"/>'),
    "brain":   ico('<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3h1V4z"/><path d="M15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3h-1V4z"/>'),
    "bp":      ico('<path d="M3 12h4l2-5 4 10 2-5h6"/>'),
    "partner": ico('<path d="M3 18v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6"/><path d="M3 18h18"/><path d="M5 10V7a2 2 0 0 1 2-2h4v5"/>'),
    "night":   ico('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/><path d="M5 20h6"/>'),
    "head":    ico('<circle cx="12" cy="8" r="5"/><path d="M12 13v8"/><path d="M8 17h8"/>'),
    "rhythm":  ico('<path d="M2 12h4l2-4 3 8 3-10 2 6h6"/>'),
    "reflux":  ico('<path d="M12 21V9"/><path d="M8 13l4-4 4 4"/><path d="M5 21h14"/>'),
    "shield":  ico('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
}


def map_stop(n, key, title, text, with_me=True, partner=None):
    tag = '<span class="stop-tag">The CPAP Doctor is with you here</span>' if with_me else f'<span class="stop-tag partner">{partner}</span>'
    return f"""<li class="stop">
  <div class="stop-num" aria-hidden="true">{n}</div>
  <div class="stop-card">
    <div class="stop-icon">{I[key]}</div>
    <h3><span class="visually-hidden">Step {n}: </span>{title}</h3>
    <p>{text}</p>
    {tag}
  </div>
</li>"""


def benefit(key, title, text):
    return f'<li class="benefit"><div class="benefit-icon">{I[key]}</div><h3>{title}</h3><p>{text}</p></li>'


MAP_STOPS = [
    (1, "doctor", "Visit your doctor", "Tell your doctor you snore, wake up tired, or stop breathing at night. That doctor can be me.", True, None),
    (2, "study", "Get a sleep study", "Usually a one-night test at home with a small device. I can arrange it and explain the result.", False, "Home sleep test provider"),
    (3, "dx", "Diagnosis", "The test shows whether you have sleep apnea and how much. We go over it together in plain words.", True, None),
    (4, "rx", "Get your prescription", "As your physician I write the CPAP prescription: the pressure, the type of machine, and the mask.", True, None),
    (5, "dme", "Get your CPAP from your supply company", "Your DME company delivers the machine, mask, and supplies, usually through your insurance.", False, "Your DME company"),
    (6, "monitor", "Get the coaching you need", "I watch your nightly use data as it comes in. Most modern machines send it to the network every morning. We talk about what it shows.", True, None),
    (7, "adjust", "Adjust", "Pressure, humidity, ramp, mask. I make the changes myself, then we see what the next nights say.", True, None),
    (8, "repeat", "Sleep, sleep, repeat", "Until we get it right. Most people need two or three rounds. That is normal, and it is what I'm here for.", True, None),
    (9, "sun", "Congratulations. A better night's sleep.", "You wake up rested. Your bed partner sleeps too. Now we keep it that way.", True, None),
]

BENEFITS_PROVEN = [
    ("energy", "Less daytime sleepiness", "The best-proven benefit. People stay awake through the afternoon, the TV, and the drive home."),
    ("mood", "Better mood", "Depression scores fell within six months in a large trial of people with heart disease who used CPAP."),
    ("partner", "Quieter nights for your partner", "Snoring drops sharply. Many couples get back into the same bedroom."),
    ("bp", "Lower blood pressure", "A modest drop on average, and larger for people whose pressure was hard to control."),
    ("car", "Safer driving", "In studies of regular users, car crashes fell by about two thirds."),
    ("shield", "A better quality of life", "Sleep-related quality of life improves. This is one of the reasons doctors prescribe it."),
]
BENEFITS_LIKELY = [
    ("night", "Fewer bathroom trips at night", "Untreated apnea makes the body shed fluid at night. Treatment often cuts the trips."),
    ("head", "Fewer morning headaches", "Low oxygen overnight is a common cause. Steady breathing usually ends them."),
    ("brain", "Clearer thinking", "Concentration and memory tend to improve, especially when sleepiness was the problem."),
    ("rhythm", "A steadier heart rhythm", "In people with atrial fibrillation who use CPAP regularly, the rhythm problem comes back less often."),
    ("reflux", "Less nighttime heartburn", "Reflux at night improves for many people once the airway stays open."),
    ("heart", "Lower heart risk, for regular users", "Trials are not settled. Studies of people who use CPAP most of the night point to lower risk. Using it matters."),
]


def head(title, desc, path):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{'' if path == 'index.html' else path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/dr-hassen-square.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Physician","name":"Dr. Kasim Hassen, MD, RCP","alternateName":"The CPAP Doctor","url":"{SITE}/","telephone":"+1-810-523-8233","email":"{EMAIL}","image":"{SITE}/assets/dr-hassen-square.jpg","areaServed":{{"@type":"State","name":"Michigan"}},"medicalSpecialty":"Sleep apnea and CPAP therapy management","availableService":{{"@type":"MedicalTherapy","name":"CPAP prescription and management by telehealth"}},"parentOrganization":{{"@type":"MedicalBusiness","name":"Hassen Sleep Science"}}}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
"""


def header(current):
    items = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a></li>'
        for href, label in NAV)
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="Dr. Kasim Hassen, The CPAP Doctor, home">
      <span class="name">Dr. Kasim Hassen</span>
      <span class="tag">The CPAP Doctor</span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{ICON_MENU}<span class="label">Menu</span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{items}</ul>
      <a class="phone" href="{PHONE_TEL}">{PHONE}</a>
      <a class="btn primary" href="contact.html">Request a visit</a>
    </nav>
  </div>
</header>
<main id="main">
"""


FOOTER = f"""</main>
<nav class="call-bar" aria-label="Quick actions">
  <a class="btn secondary" href="{PHONE_TEL}">{ICON_PHONE}Call</a>
  <a class="btn primary" href="contact.html">Request a visit</a>
</nav>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h2>Dr. Kasim Hassen, MD, RCP</h2>
        <p>The CPAP Doctor. A Michigan-licensed physician and respiratory therapist who fixes CPAP therapy by video or phone, for patients anywhere in Michigan.</p>
        <p class="mb-0">Practice name: Hassen Sleep Science</p>
      </div>
      <div>
        <h2>Pages</h2>
        <ul>
          <li><a href="cpap-users.html">For CPAP users</a></li>
          <li><a href="professionals.html">For professionals</a></li>
          <li><a href="better-sleep.html">Your sleep map</a></li>
          <li><a href="about.html">About Dr. Hassen</a></li>
          <li><a href="pricing.html">Pricing</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Reach me</h2>
        <ul>
          <li><a href="{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Westland, Michigan. Visits by video or phone.</li>
        </ul>
      </div>
    </div>
    <p class="legal">Michigan Physician License #4301518506 &middot; Michigan Respiratory Care License #4401010875 &middot; &copy; 2026 Hassen Sleep Science. Telehealth for Michigan residents. This website does not provide emergency care. If you are having trouble breathing right now, call 911.</p>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


def check_item(text):
    return f"<li>{ICON_CHECK}<span>{text}</span></li>"


def faq(items):
    out = ['<div class="faq">']
    for q, a in items:
        out.append(f"<details><summary>{q}</summary><div class=\"answer\"><p>{a}</p></div></details>")
    out.append("</div>")
    return "\n".join(out)


def patient_form():
    return f"""<form data-web3forms method="post" action="https://api.web3forms.com/submit" novalidate>
  <input type="hidden" name="access_key" value="{W3F_KEY}">
  <input type="hidden" name="subject" value="New patient request from mycpapdoctor.com">
  <input type="hidden" name="from_name" value="mycpapdoctor.com">
  <div class="hp" aria-hidden="true"><input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></div>
  <p class="form-note">Please do not put medical details in this form. Just tell me how to reach you. We will talk about your CPAP on the call.</p>
  <div class="field"><label for="p-name">Your name</label><input id="p-name" name="name" type="text" autocomplete="name" required></div>
  <div class="field"><label for="p-phone">Phone number <span class="hint">Any format is fine.</span></label><input id="p-phone" name="phone" type="tel" autocomplete="tel" required></div>
  <div class="field"><label for="p-email">Email <span class="hint">Optional. Leave blank if you prefer a call.</span></label><input id="p-email" name="email" type="email" autocomplete="email"></div>
  <div class="field"><label for="p-time">Best time to call</label>
    <select id="p-time" name="best_time"><option>Morning</option><option>Afternoon</option><option>Evening</option><option>Any time</option></select></div>
  <div class="field"><label for="p-note">Anything you want me to know before I call? <span class="hint">Optional. For example: "new to CPAP" or "mask leaks".</span></label><textarea id="p-note" name="message"></textarea></div>
  <button class="btn primary" type="submit">Send my request</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>"""


def pro_form():
    return f"""<form data-web3forms method="post" action="https://api.web3forms.com/submit" novalidate>
  <input type="hidden" name="access_key" value="{W3F_KEY}">
  <input type="hidden" name="subject" value="Professional referral inquiry from mycpapdoctor.com">
  <input type="hidden" name="from_name" value="mycpapdoctor.com">
  <div class="hp" aria-hidden="true"><input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></div>
  <p class="form-note">No patient information here, please. Tell me who you are and I will send you a secure referral form and my fax number.</p>
  <div class="field"><label for="r-name">Your name</label><input id="r-name" name="name" type="text" autocomplete="name" required></div>
  <div class="field"><label for="r-org">Organization</label><input id="r-org" name="organization" type="text" autocomplete="organization" required></div>
  <div class="field"><label for="r-role">I am a</label>
    <select id="r-role" name="role"><option>DOT / CDL medical examiner</option><option>Skilled nursing or post-acute facility</option><option>DME company</option><option>Sleep center</option><option>Primary care or other clinician</option><option>Other</option></select></div>
  <div class="field"><label for="r-phone">Phone number</label><input id="r-phone" name="phone" type="tel" autocomplete="tel" required></div>
  <div class="field"><label for="r-email">Email</label><input id="r-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="r-note">What do you need? <span class="hint">Optional.</span></label><textarea id="r-note" name="message"></textarea></div>
  <button class="btn primary" type="submit">Send</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>"""


CTA_BAND = f"""<section class="section dark">
  <div class="wrap center">
    <h2>Ready when you are.</h2>
    <p class="lead">Call me, or send a short request and I will call you within one business day.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn secondary" href="{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
      <a class="btn primary" href="contact.html">Request a visit</a>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------- pages
PAGES = {}

PAGES["index.html"] = dict(
    title="The CPAP Doctor | Dr. Kasim Hassen, Michigan telehealth CPAP care",
    desc="Michigan-licensed physician and respiratory therapist who fixes CPAP problems by video or phone. Prescriptions, settings, masks, and monthly follow-up. $89 a month.",
    body=f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Michigan telehealth &middot; Physician and respiratory therapist</p>
      <h1>Your CPAP should feel right. I'm the doctor who makes it right.</h1>
      <p class="lead">I'm Dr. Kasim Hassen. I fix leaking masks, wrong pressures, and machines that still leave you tired. By video or phone, from your home, anywhere in Michigan.</p>
      <div class="btn-row">
        <a class="btn primary" href="contact.html">Request a visit</a>
        <a class="btn secondary" href="{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
      </div>
      <ul class="trust">
        <li>{ICON_CHECK}Michigan-licensed physician</li>
        <li>{ICON_CHECK}10+ years as a respiratory therapist</li>
        <li>{ICON_CHECK}3,200+ CPAP patients helped</li>
      </ul>
    </div>
    <div class="portrait"><img src="assets/dr-hassen.jpg" width="800" height="1000" alt="Dr. Kasim Hassen in a white coat with a stethoscope" fetchpriority="high"></div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>Which one are you?</h2>
    <div class="grid two">
      <a class="door" href="cpap-users.html">
        <h3>I use a CPAP, or I'm about to</h3>
        <p>Masks, pressure, dry mouth, feeling tired, or just getting started. I sort it out with you and write the changes myself.</p>
        <span class="go">See how I help &rarr;</span>
      </a>
      <a class="door" href="professionals.html">
        <h3>I refer patients</h3>
        <p>DOT medical examiners, nursing facilities, DME companies, and sleep centers. A CPAP physician your patients can reach this week.</p>
        <span class="go">Referral details &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>How it works</h2>
    <ol class="steps">
      <li><span class="num">1</span><h3>Call or send a request</h3><p>Tell me how to reach you. I call you back within one business day and we pick a time.</p></li>
      <li><span class="num">2</span><h3>We meet by video or phone</h3><p>I look at your machine's data, your mask, and how you actually sleep. Bring your questions.</p></li>
      <li><span class="num">3</span><h3>I make the changes myself</h3><p>Pressure, settings, mask, prescription, supplies. Then I check on you every month until it feels right.</p></li>
    </ol>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>Your map to a better night's sleep</h2>
    <p class="lead">Nine stops, from the first visit to waking up rested. I am with you at seven of them.</p>
    <ol class="mini-map">
      {"".join(f'<li><span class="mini-num" aria-hidden="true">{n}</span>{title}</li>' for n,_,title,_,_,_ in MAP_STOPS)}
    </ol>
    <div class="btn-row"><a class="btn primary" href="better-sleep.html">See the whole map</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Problems I fix most often</h2>
    <ul class="chips">
      <li>Mask leaks and marks</li><li>Dry mouth or nose</li><li>Pressure feels too strong</li><li>Still tired after months</li>
      <li>The screen says my AHI is high</li><li>Swallowing air</li><li>Can't fall asleep with it on</li><li>New to CPAP and lost</li>
    </ul>
  </div>
</section>

<section class="section alt">
  <div class="wrap doctor-grid">
    <img src="assets/dr-hassen-480.jpg" width="480" height="600" alt="Dr. Kasim Hassen in a white coat with a stethoscope">
    <div>
      <p class="eyebrow">About your doctor</p>
      <h2>A respiratory therapist first. A physician second. Both, for you.</h2>
      <p>I spent more than ten years at the bedside as a respiratory therapist, in intensive care units and in patients' homes, before I became a doctor. That is where I learned what actually makes CPAP work: the mask, the settings, and someone who listens.</p>
      <p>Now I hold a full Michigan physician license, so I can write and change your CPAP prescription myself. No waiting on another office.</p>
      <ul class="checklist">
        {check_item("Doctor of Medicine, Michigan Physician License #4301518506")}
        {check_item("Registered Respiratory Therapist, Michigan RCP #4401010875")}
        {check_item("Published researcher in sleep and respiratory care")}
      </ul>
      <p class="mt-0"><a href="about.html">Read more about Dr. Hassen</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid two">
      <div class="price-card">
        <p class="eyebrow">One simple price</p>
        <p class="amount">$89 <small>a month</small></p>
        <ul class="checklist">
          {check_item("Your first visit is a full evaluation")}
          {check_item("Prescription and settings changes, written by me")}
          {check_item("Monthly check-ins on your machine's data")}
          {check_item("Cancel any time. No contract.")}
        </ul>
        <p class="fine">Cash pay. No insurance billing. I can give you a receipt to send to your insurer.</p>
        <p class="mb-0"><a href="pricing.html">See what's included</a></p>
      </div>
      <div>
        <blockquote>
          <p>"I'd been ready to throw my CPAP in the closet. Dr. Hassen actually listened to what I was experiencing, adjusted my settings based on my data, and found me a mask that doesn't leak. For the first time in months, I'm sleeping through the night."</p>
          <cite>A CPAP patient, San Diego</cite>
        </blockquote>
      </div>
    </div>
  </div>
</section>
{CTA_BAND}
""")

PAGES["cpap-users.html"] = dict(
    title="For CPAP users | The CPAP Doctor",
    desc="What Dr. Hassen fixes, what a telehealth CPAP visit looks like, what to have ready, and answers to common questions.",
    body=f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">For people who use a CPAP</p>
    <h1>Help with the machine, the mask, and the sleep you're still not getting.</h1>
    <p class="lead">Most CPAP problems are fixable. They just need someone who knows the equipment and can change the prescription. I do both.</p>
    <div class="btn-row">
      <a class="btn primary" href="contact.html">Request a visit</a>
      <a class="btn secondary" href="{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>What I fix</h2>
    <div class="grid three">
      <div class="card"><h3>Mask trouble</h3><ul><li>Leaks that wake you up</li><li>Red marks and sore spots</li><li>Feeling closed in</li><li>The wrong size or style for your face</li></ul></div>
      <div class="card"><h3>Comfort and settings</h3><ul><li>Pressure that feels too strong or too weak</li><li>Dry mouth, dry nose, or a runny nose</li><li>Swallowing air and bloating</li><li>Humidity and ramp settings</li></ul></div>
      <div class="card"><h3>Still not better</h3><ul><li>Tired after months of use</li><li>The screen shows a high number (AHI)</li><li>Central events on your report</li><li>Not sure the machine is even helping</li></ul></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>What a visit looks like</h2>
    <ol class="steps">
      <li><span class="num">1</span><h3>A real conversation</h3><p>The first visit is 45 to 60 minutes by video or phone. I ask what bothers you and what you have already tried.</p></li>
      <li><span class="num">2</span><h3>I read your machine's data</h3><p>ResMed, Philips, or any brand. If your machine sends data online, I can see it. If not, I'll show you an easy way to share it.</p></li>
      <li><span class="num">3</span><h3>I make the changes</h3><p>As your treating physician I change the settings, order a new mask or supplies, and update your prescription. Then we check in monthly.</p></li>
    </ol>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>What to have ready</h2>
    <ul class="checklist">
      {check_item("Your machine and mask, within reach")}
      {check_item("Your sleep study report, if you can find it. If not, that's fine. Bring what you have.")}
      {check_item("The name of the company that supplies your equipment")}
      {check_item("A short list of what bothers you most")}
    </ul>
    <p>New to all this, or think you might have sleep apnea but never had a test? I can arrange a home sleep test and write the prescription that follows. Just call.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Common questions</h2>
    {faq([
        ("Do I need a referral from my doctor?", "No. You can call me directly. If you want, I will send a note to your regular doctor after we meet."),
        ("Can you really change my prescription?", "Yes. I hold a full Michigan physician license. I write and change CPAP and BiPAP prescriptions myself and send them to your supply company."),
        ("Do you take insurance?", "No. The price is $89 a month, paid by card. I can give you a receipt to send to your insurer for your own claim. Your CPAP machine and supplies still go through your supply company and your insurance as usual."),
        ("Will you work with my supply company?", "Yes. I send them the orders and the notes they need, including the follow-up visit paperwork many insurers ask for in the first 90 days."),
        ("I'm not good with computers. Can we do this by phone?", "Yes. Video is nice because I can see your mask, but a phone call works. I will walk you through anything technical, one step at a time."),
        ("What if I need something you don't do?", "If you need an in-lab sleep study, a specialist, or a different kind of machine, I will tell you plainly and point you to the right place."),
    ])}
  </div>
</section>
{CTA_BAND}
""")

PAGES["professionals.html"] = dict(
    title="For professionals | Refer a patient to The CPAP Doctor",
    desc="A Michigan-licensed CPAP physician for DOT medical examiners, skilled nursing facilities, DME companies, and sleep centers. Referral-only, telehealth, fast turnaround.",
    body=f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">For professionals</p>
    <h1>A CPAP physician your patients can reach this week.</h1>
    <p class="lead">I am a Michigan-licensed physician and a registered respiratory therapist. I manage PAP therapy by telehealth, write the orders myself, and send your documentation back fast. Referral only. No fees in either direction.</p>
    <div class="btn-row">
      <a class="btn primary" href="#refer">Start a referral</a>
      <a class="btn secondary" href="{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>Who I work with</h2>
    <div class="grid two">
      <div class="card">
        <h3>DOT and CDL medical examiners</h3>
        <p>Drivers you cannot certify until sleep apnea is addressed. I arrange home sleep testing, start therapy, and manage it. You get a letter for the file: test result, treatment started, and the compliance download when it's time.</p>
      </div>
      <div class="card">
        <h3>Skilled nursing and post-acute facilities</h3>
        <p>CPAP and BiPAP management for residents by telehealth. Settings orders, mask problems, questions from your nurses and therapists, and staff training on request.</p>
      </div>
      <div class="card">
        <h3>DME companies</h3>
        <p>The patient who is struggling in the first 90 days. I take the visit, fix the setup, document the re-evaluation your payer requires, and send the order back. Referral relationship only. No payments either way.</p>
      </div>
      <div class="card">
        <h3>Sleep centers</h3>
        <p>Overflow PAP management for patients you have already diagnosed. You keep the diagnostics. I keep the patient on therapy and send you notes.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>What you get back</h2>
    <ul class="checklist">
      {check_item("A visit note within two business days of each encounter")}
      {check_item("Signed orders and prescription changes, sent to the supplier you name")}
      {check_item("The 31-to-90-day re-evaluation note with objective adherence data")}
      {check_item("A monthly adherence summary, if you want one")}
    </ul>
    <p>Telehealth for patients located in Michigan. Cash-pay for the patient at $89 a month, or ask me about facility arrangements.</p>
  </div>
</section>

<section class="section alt" id="refer">
  <div class="wrap">
    <h2>Start a referral</h2>
    <p>Tell me who you are and I will send a secure referral form and my direct line. Or call {PHONE}.</p>
    {pro_form()}
  </div>
</section>
{CTA_BAND}
""")

PAGES["better-sleep.html"] = dict(
    title="Your map to a better night's sleep | The CPAP Doctor",
    desc="The nine stops from your first doctor visit to waking up rested, and what a better night's sleep does for your body, your mood, and your driving.",
    body=f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">The map</p>
    <h1>Your map to a better night's sleep.</h1>
    <p class="lead">Nine stops. Some take a week, some take a night. I am with you at seven of them, and I stay until we get it right.</p>
    <div class="btn-row">
      <a class="btn primary" href="contact.html">Start at stop 1</a>
      <a class="btn secondary" href="{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2 class="visually-hidden">The nine stops</h2>
    <ol class="map">
      {"".join(map_stop(*s) for s in MAP_STOPS)}
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">What you get at the end</p>
    <h2>What does a better night's sleep mean?</h2>
    <p class="lead">These are the benefits studies have found when people with sleep apnea use CPAP regularly. Results differ from person to person. Using the machine most of the night, most nights, is what makes them show up.</p>

    <h3 class="tier">Well proven</h3>
    <ul class="benefits">
      {"".join(benefit(*b) for b in BENEFITS_PROVEN)}
    </ul>

    <h3 class="tier">Likely, especially for regular users</h3>
    <ul class="benefits">
      {"".join(benefit(*b) for b in BENEFITS_LIKELY)}
    </ul>
    <p class="muted" style="font-size:1rem">Sources: American Academy of Sleep Medicine clinical practice guideline on PAP therapy (2019); the SAVE trial, New England Journal of Medicine (2016); meta-analysis of crash risk before and after CPAP, SLEEP (2010); reviews of CPAP and atrial fibrillation, blood pressure, and nocturia. Ask me and I will walk you through any of them.</p>
  </div>
</section>
{CTA_BAND}
""")

PAGES["about.html"] = dict(
    title="About Dr. Kasim Hassen | The CPAP Doctor",
    desc="Dr. Kasim Hassen, MD, RCP. Ten years as a respiratory therapist, then medical school. Michigan-licensed physician who manages CPAP therapy by telehealth.",
    body=f"""
<section class="hero">
  <div class="wrap doctor-grid">
    <img src="assets/dr-hassen.jpg" width="800" height="1000" alt="Dr. Kasim Hassen in a white coat with a stethoscope">
    <div>
      <p class="eyebrow">About</p>
      <h1>Dr. Kasim Hassen, MD, RCP</h1>
      <p class="lead">"I became a respiratory therapist because I believe breathing well is the foundation of living well. I became a doctor to deeply understand the disease processes behind it."</p>
      <ul class="checklist">
        {check_item("Doctor of Medicine")}
        {check_item("Michigan Physician License #4301518506")}
        {check_item("Registered Respiratory Therapist, Michigan RCP #4401010875")}
        {check_item("Intensive care, newborn intensive care, acute care, and home ventilator experience")}
      </ul>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>Why I do this</h2>
    <p>For more than ten years I was the respiratory therapist who set up the CPAP, fitted the mask, and got the phone call when it wasn't working. I saw the same thing over and over: the machine was rarely the problem. The details were. A mask that fit the face in the store but not on the pillow. A pressure that was right for the sleep study but wrong for real life. Nobody with the time to look.</p>
    <p>I went to medical school to understand the disease underneath all of it, and I finished my first year of residency training in internal medicine. Now, with a full Michigan physician license, I can do the thing I always wanted to do for my patients: look closely, and then actually change the prescription.</p>
    <p>I have worked with more than 3,200 CPAP patients and I have published research in respiratory and sleep care. Data informs my decisions. It does not replace listening.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>How I work</h2>
    <div class="grid three">
      <div class="card"><h3>Solutions over speed</h3><p>I take the time to find what actually works for you, not the fastest fix.</p></div>
      <div class="card"><h3>Guided by the science</h3><p>Every change is grounded in how your airway works and what your data shows.</p></div>
      <div class="card"><h3>A real partnership</h3><p>Your experience matters. I listen first, then we solve it together.</p></div>
    </div>
  </div>
</section>
{CTA_BAND}
""")

PAGES["pricing.html"] = dict(
    title="Pricing | The CPAP Doctor",
    desc="One simple price for CPAP management by telehealth: $89 a month, everything included, cancel any time.",
    body=f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1>One simple price. No surprises.</h1>
    <p class="lead">Every visit is one-on-one with me. No call center, no script, no runaround.</p>
  </div>
</section>

<section class="section alt">
  <div class="wrap grid two">
    <div class="price-card">
      <p class="eyebrow">CPAP care</p>
      <p class="amount">$89 <small>a month</small></p>
      <ul class="checklist">
        {check_item("A full first evaluation, 45 to 60 minutes, by video or phone")}
        {check_item("Review of your machine's data every month")}
        {check_item("Pressure, comfort, and mask changes, made by me")}
        {check_item("Prescription updates and supply orders sent to your supplier")}
        {check_item("A monthly check-in, and a way to reach me between visits")}
        {check_item("Cancel any time. No contract.")}
      </ul>
      <p class="fine">Paid by card after your first visit. Requesting a visit costs nothing.</p>
      <div class="btn-row"><a class="btn primary" href="contact.html">Request a visit</a></div>
    </div>
    <div>
      <h2>What's not included</h2>
      <ul>
        <li><strong>The machine and supplies.</strong> Those still come from your supply company or any retailer, using the prescription I write. Your insurance handles them as usual.</li>
        <li><strong>The sleep study itself.</strong> If you need one, I can arrange a home test. It is billed separately, usually around $190 cash.</li>
        <li><strong>Insurance billing.</strong> I don't bill insurers. I can give you a receipt for your own claim.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Questions about cost</h2>
    {faq([
        ("Why a monthly fee instead of one visit?", "Because CPAP problems are rarely fixed in one sitting. The first change usually helps. The second and third are what make it stick. Monthly care lets me follow your data and adjust without you starting over each time."),
        ("What if I only want one visit?", "Call me and tell me that. We will talk about what makes sense for you."),
        ("Can I stop whenever I want?", "Yes. There is no contract. Tell me and the monthly charge stops."),
        ("Do I pay before we talk?", "No. Requesting a visit and the first phone call cost nothing. You pay by card after your first full visit."),
    ])}
  </div>
</section>
{CTA_BAND}
""")

PAGES["contact.html"] = dict(
    title="Contact | Request a visit with The CPAP Doctor",
    desc="Call (810) 523-8233 or send a short request. Dr. Hassen returns calls within one business day. Telehealth for Michigan residents.",
    body=f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Call me, or send a short request.</h1>
    <p class="lead">I return calls and messages within one business day. If you get my voicemail, leave your name and number and I will call you back.</p>
    <p><a class="phone-big" href="{PHONE_TEL}">{ICON_PHONE}{PHONE}</a></p>
    <p>Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br>Visits by video or phone, for patients located in Michigan.</p>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>Request a visit</h2>
    {patient_form()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Referring a patient?</h2>
    <p>Medical examiners, facilities, suppliers, and sleep centers: use the <a href="professionals.html#refer">professional referral page</a>.</p>
  </div>
</section>
""")

PAGES["404.html"] = dict(
    title="Page not found | The CPAP Doctor",
    desc="That page does not exist.",
    body=f"""
<section class="hero">
  <div class="wrap">
    <h1>That page isn't here.</h1>
    <p class="lead">The link may be old. Try the home page, or call me and I will help.</p>
    <div class="btn-row">
      <a class="btn primary" href="index.html">Go to the home page</a>
      <a class="btn secondary" href="{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
    </div>
  </div>
</section>
""")


def build():
    root = Path(__file__).parent
    for path, page in PAGES.items():
        current = path if path in dict(NAV) else None
        html = head(page["title"], page["desc"], path) + header(current) + page["body"] + FOOTER
        (root / path).write_text(html, encoding="utf-8")
        print("wrote", path, len(html), "bytes")


if __name__ == "__main__":
    build()
