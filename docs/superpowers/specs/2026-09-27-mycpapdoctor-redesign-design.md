# mycpapdoctor.com redesign — design spec (2026-09-27)

Approved by Kasim in chat 2026-09-27 ("Go with your recommendations"): masthead A, booking A, pricing B, real photo from files.

## Intent
A telehealth CPAP practice site whose median reader is 60, skewed to the 70s, plus four professional referrer types
(CDL/DOT medical examiners, skilled nursing facilities, DME companies, sleep centers). Success = a 70-year-old finds the
phone number or the request form within one screen, understands the price, and trusts the doctor's face and licence.
Professionals find their own door and a referral path in one click.

## Constraints (from memory)
- Static site on GitHub Pages, repo kas271010/hassen-sleep-science, domain mycpapdoctor.com. No framework, no build step.
- Contact via Web3Forms (key already on site) → kasimmisak@hotmail.com. Forms carry NO PHI (decision 2026-09-19).
- No scheduler or payment yet (booking option A). Phone-first.
- Price shown: $89/month, everything included, first visit is the full evaluation, cancel anytime (pricing option B).
- Credentials line: "Kasim Hassen, MD, RCP". MI physician licence #4301518506, MI RCP #4401010875.
- No AI-generated imagery. Portrait = health-amharic/assets/real_seeds/seedA_hires.jpg (real photo).
- No payments from DMEs (Stark / 42 CFR 424.57(f)); referral-only relationship language.

## Accessibility bar (WCAG 2.2 AA + senior guidelines)
Body 19px / line-height 1.6 / max 65ch · contrast ≥7:1 for body text, ≥4.5:1 everywhere · all targets ≥48px tall ·
no hover-only menus · no scroll animation, `prefers-reduced-motion` respected · visible focus rings · every input has a
visible `<label>` · skip link · logical heading order · phone number in header as tel: link · fixed Call/Request bar on
phones · visited links distinct · plain-language copy at roughly 8th-grade level.

## Site map
1. `index.html` Home — masthead, two doors (I use a CPAP / I refer patients), 3-step how it works, doctor + credentials,
   price card, phone, footer.
2. `cpap-users.html` For CPAP users — what I fix, what a visit looks like, what to have ready, FAQ.
3. `professionals.html` For professionals — four sections (DOT examiners, SNFs, DMEs, sleep centers), referral form
   (no patient details), what I send back.
4. `about.html` About Dr. Hassen — RT-to-MD story, licences, research, approach.
5. `pricing.html` Pricing — one card, what's included, what's not, FAQ.
6. `contact.html` Contact / Request a visit — phone first, labeled form, hours.
7. `404.html`, `favicon.svg`, `robots.txt`, `sitemap.xml`.

## Design system
- Type: Atkinson Hyperlegible Next (body, UI), Source Serif 4 (display headings). Google Fonts, `display=swap`.
- Palette: paper `#FBF8F3`, ink `#172033`, navy action `#14324F`, teal accent `#0E5E6F`, amber highlight `#B45309`
  (used on dark only), success `#166534`, rule `#D9D2C5`. Visited link `#5B3A8C`.
- Buttons: 56px min height, 20px text, 12px radius, navy fill/white text (primary) or 2px navy outline (secondary).
- Cards: paper-2 `#F3EEE4` background, 1px rule border, 16px radius, no shadows needed.
- Layout: 1120px max, 24px gutters, single column below 720px.

## Components
- Header: logo text "Dr. Kasim Hassen" + "The CPAP Doctor" small caps, nav (For CPAP users · For professionals · About ·
  Pricing · Contact), phone link, primary button "Request a visit". Mobile: `<button aria-expanded>` toggles the nav list.
- Mobile bottom bar: two 56px buttons, Call and Request a visit; hidden ≥720px.
- Forms: Web3Forms POST via fetch with real UA (browser), honeypot `botcheck`, success/error text in `aria-live` region,
  fallback instruction with phone + email on error. Patient form: name, phone, email, best time to call, short note.
  Professional form: name, organization, role select, phone, email, note. Both say: no patient information here.
- Footer: legal name Hassen Sleep Science, licences, email, phone, "Telehealth for Michigan residents".

## Testing / QA
Local `python3 -m http.server`; Playwright at 1440×900 and 390×844 for every page; axe-core injected from cdnjs, zero
serious/critical violations; programmatic checks: min target height ≥48, body font ≥19px, all inputs labelled, no
element with opacity 0, `prefers-reduced-motion` present; every internal link resolves; one live Web3Forms submission
after deploy (Kasim deletes the test email). Then push to main and re-verify on https://mycpapdoctor.com.
