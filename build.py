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
       ("better-sleep.html", "Sleep map"), ("about.html", "About"), ("contact.html", "Contact")]

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


def icon_at(key, x, y, size, color):
    """Place one of the line icons inside a larger SVG."""
    return f'<g color="{color}">' + I[key].replace('<svg viewBox="0 0 24 24"', f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24"', 1) + '</g>'


NAVY, TEAL, AMBER, INK, INK2, PAPER2, WHITE, SUCCESS, ROAD = "#14324F", "#0E5E6F", "#F4B860", "#172033", "#3B4453", "#F3EEE4", "#FFFFFF", "#166534", "#2F3A4A"
FONT = "Atkinson Hyperlegible Next, Atkinson Hyperlegible, Arial, sans-serif"
SERIF = "Source Serif 4, Georgia, serif"


def road_svg(stops):
    """The map as a winding road, portrait, 720 units wide. Stops alternate sides; the road ends in a sunrise.
    Steps Kasim handles show his photo; each step is a button that opens its details card (site.js)."""
    import math
    W, top, gap = 720, 190, 180
    xs = [200, 520]
    pts = [(xs[i % 2], top + i * gap) for i in range(len(stops))]
    xe, ye = pts[-1]
    H = ye + 300
    d = f"M {pts[0][0]} 80 L {pts[0][0]} {pts[0][1]}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ym = (y0 + y1) / 2
        d += f" C {x0} {ym} {x1} {ym} {x1} {y1}"
    d += f" L {xe} {ye+40} C {xe} {ye+170} 360 {ye+110} 360 {H-78}"
    short_title = {5: "Get your CPAP", 9: "A better night's sleep"}
    short_sub = {1: "Tired? Snoring? Gasping for air?", 2: "One night at home, small device", 3: "We go over it in plain words",
                 4: "I write it myself, as your physician", 5: "from your supply company (DME)", 6: "I fit your mask by video and coach you",
                 7: "Pressure, humidity, ramp, mask", 8: "Until we get it right", 9: "Congratulations. You made it."}
    out = [f'<svg class="infographic road" viewBox="-110 0 {W+170} {H+50}" role="group" aria-label="The map to a better night\'s sleep. Nine steps; select a step to read about it." xmlns="http://www.w3.org/2000/svg">',
           '<defs><clipPath id="c40"><circle r="40"/></clipPath><clipPath id="c16"><circle r="16"/></clipPath></defs>',
           f'<style>.rt{{font-family:{FONT};font-weight:700;font-size:30px;fill:{INK}}}.rs{{font-family:{FONT};font-size:21px;fill:{INK2}}}.rn{{font-family:{SERIF};font-weight:700;font-size:20px;fill:{WHITE}}}.rl{{font-family:{FONT};font-weight:700;font-size:22px;fill:{INK2}}}.rf{{font-family:{SERIF};font-weight:700;font-size:30px;fill:{NAVY}}}.bk{{font-family:{FONT};font-weight:700;font-size:24px;fill:{TEAL}}}</style>',
           # legend: photo = with Dr. Hassen
           f'<g aria-hidden="true"><g transform="translate(470 34)"><image href="{PHOTO}" x="-16" y="-16" width="32" height="32" clip-path="url(#c16)"/><circle r="16" fill="none" stroke="{NAVY}" stroke-width="3"/></g><text x="496" y="42" class="rl">With Dr. Hassen</text>',
           f'<circle cx="470" cy="78" r="12" fill="#9AA3B2"/><text x="496" y="86" class="rl">With a partner</text>',
           f'<g transform="translate(360 {H-54})"><path d="M -170 0 A 170 170 0 0 1 170 0 Z" fill="{AMBER}" opacity="0.3"/><path d="M -110 0 A 110 110 0 0 1 110 0 Z" fill="{AMBER}"/>'
           + "".join(f'<line x1="{140*math.cos(a):.0f}" y1="{-140*math.sin(a):.0f}" x2="{190*math.cos(a):.0f}" y2="{-190*math.sin(a):.0f}" stroke="{AMBER}" stroke-width="9" stroke-linecap="round"/>' for a in [0.3, 0.75, 1.2, 1.94, 2.39, 2.84]) + '</g>',
           f'<path d="{d}" fill="none" stroke="{ROAD}" stroke-width="46" stroke-linecap="round"/>',
           f'<path d="{d}" fill="none" stroke="{AMBER}" stroke-width="5" stroke-dasharray="26 22" stroke-linecap="round"/>',
           f'<rect x="150" y="{H-58}" width="420" height="10" rx="5" fill="{ROAD}"/>',
           f'<text x="360" y="{H-10}" text-anchor="middle" class="rf">Better sleep</text>',
           f'<line x1="{pts[0][0]+34}" y1="84" x2="{pts[0][0]+34}" y2="144" stroke="{INK}" stroke-width="5"/>',
           f'<path d="M {pts[0][0]+37} 86 h 72 l -16 17 16 17 h -72 z" fill="{SUCCESS}"/><text x="{pts[0][0]+118}" y="116" class="rl">Start here</text>']
    y6, y8 = pts[5][1], pts[7][1]
    out.append(f'<path d="M -30 {y6-40} h -14 v {y8-y6+80} h 14" fill="none" stroke="{TEAL}" stroke-width="5" stroke-linecap="round"/>')
    out.append(f'<text transform="translate(-62 {(y6+y8)/2}) rotate(-90)" text-anchor="middle" class="bk">Same doctor · no hand-offs</text></g>')
    for (n, key, title, text, with_me, partner), (x, y) in zip(stops, pts):
        left = x == xs[0]
        ttl = short_title.get(n, title); sub = short_sub.get(n, "")
        out.append(f'<g class="mstop" data-n="{n}" tabindex="0" role="button" aria-controls="mdetail" aria-label="Step {n}: {ttl}. Show details">')
        out.append(f'<rect class="hit" x="{x-60 if left else x-560}" y="{y-58}" width="620" height="116" rx="20"/>')
        out.append(stop_marker(n, x, y, with_me, 40))
        if left:
            out.append(icon_at(key, x + 62, y - 24, 46, TEAL))
            out.append(f'<text x="{x+122}" y="{y+2}" class="rt">{ttl}</text><text x="{x+122}" y="{y+34}" class="rs">{sub}</text>')
        else:
            out.append(icon_at(key, x - 108, y - 24, 46, TEAL))
            out.append(f'<text x="{x-122}" y="{y+2}" text-anchor="end" class="rt">{ttl}</text><text x="{x-122}" y="{y+34}" text-anchor="end" class="rs">{sub}</text>')
        out.append('</g>')
    out.append('</svg>')
    return "\n".join(out)


PHOTO = "assets/dr-hassen-square.jpg"


def stop_marker(n, x, y, with_me, r):
    """Kasim's photo for his steps (numbered badge), gray dot for partner steps, a sun-gold dot for the finish."""
    if n == 9:
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{AMBER}" stroke="{WHITE}" stroke-width="6"/><text x="{x}" y="{y+r*0.3:.0f}" text-anchor="middle" style="font-family:{SERIF};font-weight:700;font-size:{r*0.85:.0f}px;fill:{NAVY}">{n}</text>'
    if with_me:
        br = r * 0.43
        return (f'<g transform="translate({x} {y})"><circle r="{r+6}" fill="{WHITE}"/>'
                f'<image href="{PHOTO}" x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" clip-path="url(#c{r})"/>'
                f'<circle r="{r}" fill="none" stroke="{NAVY}" stroke-width="{max(3, r//8)}"/>'
                f'<circle cx="{r*0.75:.0f}" cy="{r*0.75:.0f}" r="{br:.0f}" fill="{NAVY}" stroke="{WHITE}" stroke-width="3"/>'
                f'<text x="{r*0.75:.0f}" y="{r*0.75+br*0.42:.0f}" text-anchor="middle" style="font-family:{SERIF};font-weight:700;font-size:{br*1.15:.0f}px;fill:{WHITE}">{n}</text></g>')
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9AA3B2" stroke="{WHITE}" stroke-width="6"/><text x="{x}" y="{y+r*0.3:.0f}" text-anchor="middle" style="font-family:{SERIF};font-weight:700;font-size:{r*0.85:.0f}px;fill:{WHITE}">{n}</text>'


def road_svg_phone(stops):
    """Phone layout: drawn at 420 units wide so it renders near 1:1. Road hugs the left, labels on the right."""
    import math
    W, top, gap = 420, 110, 132
    pts = [((60 if i % 2 == 0 else 100), top + i * gap) for i in range(len(stops))]
    xe, ye = pts[-1]
    H = ye + 250
    d = f"M {pts[0][0]} 20 L {pts[0][0]} {pts[0][1]}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ym = (y0 + y1) / 2
        d += f" C {x0} {ym} {x1} {ym} {x1} {y1}"
    d += f" L {xe} {ye+30} C {xe} {ye+120} 210 {ye+80} 210 {H-70}"
    short_title = {5: "Get your CPAP", 9: "A better night's sleep"}
    sub = {1: "Tired? Snoring? Gasping?", 2: "One night at home", 3: "Explained in plain words",
           4: "Written by me", 5: "From your supply company", 6: "Mask fit by video",
           7: "Pressure, mask, comfort", 8: "Until we get it right", 9: "Congratulations!"}
    out = [f'<svg class="infographic road-phone" viewBox="0 0 {W} {H}" role="group" aria-label="The map to a better night\'s sleep. Nine steps; tap a step to read about it." xmlns="http://www.w3.org/2000/svg">',
           '<defs><clipPath id="c28"><circle r="28"/></clipPath></defs>',
           f'<style>.pt{{font-family:{FONT};font-weight:700;font-size:25px;fill:{INK}}}.ps{{font-family:{FONT};font-size:20px;fill:{INK2}}}.pn{{font-family:{SERIF};font-weight:700;font-size:26px;fill:{WHITE}}}.pf{{font-family:{SERIF};font-weight:700;font-size:26px;fill:{NAVY}}}</style>',
           f'<g transform="translate(210 {H-50})"><path d="M -150 0 A 150 150 0 0 1 150 0 Z" fill="{AMBER}" opacity="0.3"/><path d="M -95 0 A 95 95 0 0 1 95 0 Z" fill="{AMBER}"/>'
           + "".join(f'<line x1="{120*math.cos(a):.0f}" y1="{-120*math.sin(a):.0f}" x2="{160*math.cos(a):.0f}" y2="{-160*math.sin(a):.0f}" stroke="{AMBER}" stroke-width="8" stroke-linecap="round"/>' for a in [0.3, 0.75, 1.2, 1.94, 2.39, 2.84])
           + '</g>',
           f'<path d="{d}" fill="none" stroke="{ROAD}" stroke-width="34" stroke-linecap="round"/>',
           f'<path d="{d}" fill="none" stroke="{AMBER}" stroke-width="4" stroke-dasharray="18 16" stroke-linecap="round"/>',
           f'<rect x="40" y="{H-54}" width="340" height="8" rx="4" fill="{ROAD}"/>',
           f'<text x="210" y="{H-14}" text-anchor="middle" class="pf">Better sleep</text>']
    for (n, key, title, text, with_me, partner), (x, y) in zip(stops, pts):
        ttl = short_title.get(n, title)
        out.append(f'<g class="mstop" data-n="{n}" tabindex="0" role="button" aria-controls="mdetail" aria-label="Step {n}: {ttl}. Show details">')
        out.append(f'<rect class="hit" x="20" y="{y-50}" width="390" height="100" rx="16"/>')
        out.append(stop_marker(n, x, y, with_me, 28))
        out.append(f'<text x="150" y="{y-2}" class="pt">{ttl}</text>')
        out.append(f'<text x="150" y="{y+26}" class="ps">{sub[n]}</text>')
        out.append('</g>')
    out.append('</svg>')
    return "\n".join(out)


def sun_svg_phone():
    """Phone layout: sun on top, a beam down the left, benefits reading left to right. 420 units wide."""
    W, top, gap = 420, 130, 104
    H = top + 300 + len(BENEFIT_STATS) * gap
    bx = 44
    out = [f'<svg class="infographic sun-phone" viewBox="0 0 {W} {H}" role="img" aria-labelledby="sunp-t sunp-d" xmlns="http://www.w3.org/2000/svg">',
           '<title id="sunp-t">What a better night\'s sleep means: ten benefits</title>',
           f'<desc id="sunp-d">{" ".join(s + " " + " ".join(l) + "." for _, s, l in BENEFIT_STATS)}</desc>',
           f'<style>.st{{font-family:{SERIF};font-weight:700;font-size:30px;fill:{NAVY}}}.ss{{font-family:{FONT};font-weight:700;font-size:20px;fill:{NAVY}}}'
           f'.bn{{font-family:{SERIF};font-weight:700;font-size:30px;fill:{NAVY}}}.bl{{font-family:{FONT};font-size:21px;fill:{INK2}}}</style>',
           f'<rect x="{bx-6}" y="{top}" width="12" height="{H-top-40}" rx="6" fill="{AMBER}" opacity="0.6"/>']
    import math
    cx, cy, r = 210, top - 10, 96
    rays = "".join(f'<line x1="{cx+(r+12)*math.cos(a):.0f}" y1="{cy+(r+12)*math.sin(a):.0f}" x2="{cx+(r+34)*math.cos(a):.0f}" y2="{cy+(r+34)*math.sin(a):.0f}" stroke="{AMBER}" stroke-width="7" stroke-linecap="round"/>' for a in [i*math.pi/8 for i in range(16)])
    out.append(f'<g transform="translate(0 {r+40})"><circle cx="{cx}" cy="{cy}" r="{r+48}" fill="{AMBER}" opacity="0.18"/>{rays}<circle cx="{cx}" cy="{cy}" r="{r}" fill="{AMBER}"/>'
               f'<text x="{cx}" y="{cy-10}" text-anchor="middle" class="st">A better</text><text x="{cx}" y="{cy+24}" text-anchor="middle" class="st">night\'s sleep</text>'
               f'<text x="{cx}" y="{cy+54}" text-anchor="middle" class="ss">means…</text></g>')
    for i, (key, stat, lines) in enumerate(BENEFIT_STATS):
        y = top + r + 230 + i * gap
        out.append(f'<circle cx="{bx}" cy="{y}" r="30" fill="{WHITE}" stroke="{TEAL}" stroke-width="4"/>')
        out.append(icon_at(key, bx - 17, y - 17, 34, TEAL))
        out.append(f'<text x="{bx+48}" y="{y-4}" class="bn">{stat}</text>')
        out.append(f'<text x="{bx+48}" y="{y+26}" class="bl">{lines[0]} {lines[1]}</text>')
    out.append('</svg>')
    return "\n".join(out)


BENEFIT_STATS = [
    ("car",     "70%",       ["fewer crashes", "behind the wheel"]),
    ("bp",      "2–7",       ["points lower", "blood pressure"]),
    ("night",   "1 fewer",   ["bathroom trip", "a night"]),
    ("mood",    "6 months",  ["or less to", "a better mood"]),
    ("energy",  "3 points",  ["less sleepy", "during the day"]),
    ("partner", "Quieter",   ["nights for", "your partner"]),
    ("brain",   "Clearer",   ["thinking", "and memory"]),
    ("head",    "Fewer",     ["morning", "headaches"]),
    ("rhythm",  "Steadier",  ["heart rhythm", "(AFib)"]),
    ("shield",  "Better",    ["quality", "of life"]),
]


def sun_core(cx, cy, r):
    import math
    rays = "".join(f'<line x1="{cx+ (r+18)*math.cos(a):.0f}" y1="{cy+(r+18)*math.sin(a):.0f}" x2="{cx+(r+48)*math.cos(a):.0f}" y2="{cy+(r+48)*math.sin(a):.0f}" stroke="{AMBER}" stroke-width="9" stroke-linecap="round"/>'
                   for a in [i * math.pi / 8 for i in range(16)])
    return (f'<circle cx="{cx}" cy="{cy}" r="{r+70}" fill="{AMBER}" opacity="0.18"/>{rays}'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{AMBER}"/>'
            f'<text x="{cx}" y="{cy-22}" text-anchor="middle" class="st">A better</text>'
            f'<text x="{cx}" y="{cy+18}" text-anchor="middle" class="st">night\'s sleep</text>'
            f'<text x="{cx}" y="{cy+56}" text-anchor="middle" class="ss">means…</text>')


SUN_STYLE = (f'<style>.st{{font-family:{SERIF};font-weight:700;font-size:38px;fill:{NAVY}}}.ss{{font-family:{FONT};font-weight:700;font-size:24px;fill:{NAVY}}}'
             f'.bn{{font-family:{SERIF};font-weight:700;font-size:44px;fill:{NAVY}}}.bl{{font-family:{FONT};font-size:28px;fill:{INK2}}}</style>')


def sun_svg_radial():
    """Wide screens: the sun in the middle, ten benefits around it."""
    import math
    W, H, cx, cy, R = 1400, 1000, 700, 500, 150
    out = [f'<svg class="infographic sun-radial" viewBox="-60 -20 {W+120} {H+40}" role="img" aria-labelledby="sunr-t sunr-d" xmlns="http://www.w3.org/2000/svg">',
           '<title id="sunr-t">What a better night\'s sleep means: ten benefits around a rising sun</title>',
           f'<desc id="sunr-d">{" ".join(s + " " + " ".join(l) + "." for _, s, l in BENEFIT_STATS)}</desc>', SUN_STYLE]
    n = len(BENEFIT_STATS)
    for i, (key, stat, lines) in enumerate(BENEFIT_STATS):
        a = -math.pi / 2 + i * 2 * math.pi / n
        ix, iy = cx + 330 * math.cos(a), cy + 330 * math.sin(a)
        out.append(f'<line x1="{cx + (R+20)*math.cos(a):.0f}" y1="{cy+(R+20)*math.sin(a):.0f}" x2="{ix:.0f}" y2="{iy:.0f}" stroke="{AMBER}" stroke-width="6" stroke-dasharray="2 12" stroke-linecap="round"/>')
        out.append(f'<circle cx="{ix:.0f}" cy="{iy:.0f}" r="38" fill="{WHITE}" stroke="{TEAL}" stroke-width="4"/>')
        out.append(icon_at(key, f"{ix-22:.0f}", f"{iy-22:.0f}", 44, TEAL))
        c = math.cos(a)
        if abs(c) < 0.2:  # top or bottom: centre the text above/below
            anchor, tx = "middle", ix
            ty = iy - 60 if math.sin(a) < 0 else iy + 96
            out.append(f'<text x="{tx:.0f}" y="{ty:.0f}" text-anchor="{anchor}" class="bn">{stat}</text>')
            out.append(f'<text x="{tx:.0f}" y="{ty+30:.0f}" text-anchor="{anchor}" class="bl">{lines[0]} {lines[1]}</text>')
        else:
            anchor = "start" if c > 0 else "end"
            tx = ix + (56 if c > 0 else -56)
            out.append(f'<text x="{tx:.0f}" y="{iy-4:.0f}" text-anchor="{anchor}" class="bn">{stat}</text>')
            out.append(f'<text x="{tx:.0f}" y="{iy+30:.0f}" text-anchor="{anchor}" class="bl">{lines[0]}</text>')
            out.append(f'<text x="{tx:.0f}" y="{iy+62:.0f}" text-anchor="{anchor}" class="bl">{lines[1]}</text>')
    out.append(sun_core(cx, cy, R))
    out.append('</svg>')
    return "\n".join(out)


def sun_svg_stacked():
    """Phones: the sun on top, a sunbeam down the middle, benefits alternating left and right."""
    W, top, gap = 720, 200, 196
    n = len(BENEFIT_STATS)
    H = top + 190 + n * gap
    cx = 360
    out = [f'<svg class="infographic sun-stacked" viewBox="-40 0 {W+80} {H+30}" role="img" aria-labelledby="suns-t suns-d" xmlns="http://www.w3.org/2000/svg">',
           '<title id="suns-t">What a better night\'s sleep means: ten benefits along a sunbeam</title>',
           f'<desc id="suns-d">{" ".join(s + " " + " ".join(l) + "." for _, s, l in BENEFIT_STATS)}</desc>', SUN_STYLE.replace("font-size:44px","font-size:62px").replace("font-size:24px;fill:"+INK2,"font-size:38px;fill:"+INK2),
           f'<rect x="{cx-8}" y="{top+150}" width="16" height="{H-top-190}" fill="{AMBER}" opacity="0.6"/>',
           sun_core(cx, top, 130)]
    for i, (key, stat, lines) in enumerate(BENEFIT_STATS):
        y = top + 240 + i * gap
        left = i % 2 == 0
        out.append(f'<circle cx="{cx}" cy="{y}" r="36" fill="{WHITE}" stroke="{TEAL}" stroke-width="4"/>')
        out.append(icon_at(key, cx - 21, y - 21, 42, TEAL))
        if left:
            out.append(f'<text x="{cx-56}" y="{y-2}" text-anchor="end" class="bn">{stat}</text>')
            out.append(f'<text x="{cx-56}" y="{y+40}" text-anchor="end" class="bl">{lines[0]}</text>')
            out.append(f'<text x="{cx-56}" y="{y+80}" text-anchor="end" class="bl">{lines[1]}</text>')
        else:
            out.append(f'<text x="{cx+56}" y="{y-2}" class="bn">{stat}</text>')
            out.append(f'<text x="{cx+56}" y="{y+40}" class="bl">{lines[0]}</text>')
            out.append(f'<text x="{cx+56}" y="{y+80}" class="bl">{lines[1]}</text>')
    out.append('</svg>')
    return "\n".join(out)


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
    (1, "doctor", "Visit your doctor", "Do you feel tired when you wake up, a headache that lingers, problems concentrating? Snoring, drooling, gasping for air? Talk to your doctor. These are signs and symptoms of sleep apnea.", True, None),
    (2, "study", "Get a sleep study", "Usually a one-night test at home with a small device. I can arrange it and explain the result.", False, "Home sleep test provider"),
    (3, "dx", "Diagnosis", "The test shows whether you have sleep apnea and how much. We go over it together in plain words.", True, None),
    (4, "rx", "Get your prescription", "As your physician I write the CPAP prescription: the pressure, the type of machine, and the mask.", True, None),
    (5, "dme", "Get your CPAP from your supply company", "Your DME company delivers the machine, mask, and supplies, usually through your insurance.", False, "Your DME company"),
    (6, "monitor", "Mask fit + coaching", "I review your nightly use data as it comes in. Most modern machines send it over the internet every morning. If I see things are not going in the right direction, I may call you before you do to discuss changes.", True, None),
    (7, "adjust", "Adjust", "Pressure, humidity, ramp, mask. I make the changes myself, then we see what the next nights say.", True, None),
    (8, "repeat", "Sleep, sleep, repeat", "Until we get it right. Most people need two or three rounds. That is normal, and it is what I'm here for.", True, None),
    (9, "sun", "Congratulations. A better night's sleep.", "You wake up rested. Your bed partner sleeps too. Now we keep it that way.", True, None),
]

ONE_DOC = {6: "Usually: the supply company's therapist fits the mask, and you call the sleep doctor's office if it isn't working. With me: I fit the mask with you on video, and I'm the one who sees your data.",
           7: "Usually: a request goes from the therapist to the doctor, who signs a new order, and the supply company changes the setting. That's days. With me: I see the problem and I make the change myself.",
           8: "Usually: each round of 'try this, then call us' restarts the chain. With me: it's one conversation with one doctor until it works."}
import json as _json
STOP_DATA_JSON = _json.dumps({n: {"title": t, "text": txt, "mine": mine, "partner": partner or "", "one": ONE_DOC.get(n, "")}
                              for n, _, t, txt, mine, partner in MAP_STOPS}).replace("</", "<\\/")

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
    desc="Michigan-licensed physician and respiratory therapist who fixes CPAP problems by video or phone. Prescriptions, settings, masks, and monthly follow-up.",
    body=f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Michigan telehealth &middot; Physician and respiratory therapist</p>
    <h1>Your CPAP should feel right. I'm the doctor who makes it right.</h1>
    <p class="lead">I fix leaking masks, wrong pressures, and machines that still leave you tired. By video or phone, from your home, anywhere in Michigan.</p>
    <div class="btn-row">
      <a class="btn primary" href="contact.html">Request a visit</a>
      <a class="btn secondary" href="{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
    </div>
    <div class="byline">
      <img src="assets/dr-hassen-square.jpg" width="600" height="600" alt="Dr. Kasim Hassen" fetchpriority="high">
      <div>
        <p class="byline-name">Dr. Kasim Hassen, MD, RCP</p>
        <ul class="trust">
          <li>{ICON_CHECK}Michigan-licensed physician</li>
          <li>{ICON_CHECK}10+ years as a respiratory therapist</li>
          <li>{ICON_CHECK}3,200+ CPAP patients helped</li>
        </ul>
      </div>
    </div>
  </div>
</section>
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
    <p>Never had a sleep test? Do you feel tired when you wake up, a headache that lingers, problems concentrating? Snoring, drooling, gasping for air? These are signs and symptoms of sleep apnea. I can arrange a home sleep test and write the prescription that follows. Just call.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>Common questions</h2>
    {faq([
        ("Do I need a referral from my doctor?", "No. You can call me directly. If you want, I will send a note to your regular doctor after we meet."),
        ("Can you really change my prescription?", "Yes. I hold a full Michigan physician license. I write and change CPAP and BiPAP prescriptions myself and send them to your supply company."),
        ("Do you take insurance?", "No. I am a cash-pay practice, and we go over the cost on our first call before anything is charged. I can give you a receipt to send to your insurer for your own claim. Your CPAP machine and supplies still go through your supply company and your insurance as usual."),
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
    <p>Telehealth for patients located in Michigan. Cash-pay for the patient, or ask me about facility arrangements.</p>
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
    <h2 class="visually-hidden">The map</h2>
    <div class="compare">
      <div class="compare-card usual"><p class="compare-k">The usual way</p><p class="compare-h">4–5 different people</p>
        <p>Sleep doctor → supply company → their therapist for the mask → back to the doctor for changes. Each hand-off adds days. It can take weeks, sometimes months.</p>
        <p class="compare-stat">At one major U.S. sleep center, patients waited a median of <strong>113 days</strong> (almost 4 months) from referral to being offered treatment.<sup>1</sup></p></div>
      <div class="compare-card me"><p class="compare-k">With me</p><p class="compare-h">One doctor, start to finish</p>
        <p>I'm a physician <strong>and</strong> a respiratory therapist. The same person fits your mask, coaches you, and adjusts your settings, so fixes happen sooner.</p></div>
    </div>
    <p class="map-hint">Tap any step to learn more.</p>
    <div class="info-wrap">{road_svg(MAP_STOPS)}{road_svg_phone(MAP_STOPS)}</div>
    <div id="mdetail" class="mdetail" hidden>
      <button type="button" class="md-close" aria-label="Close step details">×</button>
      <p class="md-num"></p><h3 class="md-title"></h3><p class="md-who"></p><p class="md-text"></p><p class="md-one"></p>
      <a class="btn primary md-book" href="contact.html">Book this step</a>
    </div>
    <script type="application/json" id="stop-data">{STOP_DATA_JSON}</script>
    <p class="muted source-note"><sup>1</sup> Morgan, Ramar, Morgenthaler (Mayo Clinic). <em>Journal of Clinical Sleep Medicine</em>, February 2026.</p>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <p class="eyebrow">What you get at the end</p>
    <h2>What does a better night's sleep mean?</h2>
    <p class="lead">What studies have found when people with sleep apnea use CPAP regularly. Results differ from person to person. Using the machine most of the night, most nights, is what makes them show up.</p>
    <div class="info-wrap wide">{sun_svg_radial()}{sun_svg_phone()}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
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
