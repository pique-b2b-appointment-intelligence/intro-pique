#!/usr/bin/env python3
"""
TextInc Business LP Generator
Reads copy-data.json, generates one HTML file per prospect.
"""

import json, re, sys, os

def fmt(text):
    if not text:
        return ''
    text = text.replace('—', ',').replace('–', '-')
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return text

def esc(text):
    if not text:
        return ''
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def screen_google(url, query, results=None):
    if not results:
        results = []
    rows = ''
    for r in results[:3]:
        rows += f'''<div style="margin-bottom:16px">
          <div style="font-size:.72rem;color:#1a0dab;font-weight:600;margin-bottom:1px">{esc(r.get("title",""))}</div>
          <div style="font-size:.64rem;color:#006621;margin-bottom:2px">{esc(r.get("url",""))}</div>
          <div style="font-size:.72rem;color:#545454;line-height:1.5">{fmt(r.get("snippet",""))}</div>
        </div>'''
    return f'''<div class="screen r d1">
    <div class="screen-bar">
      <span class="sd sd1"></span><span class="sd sd2"></span><span class="sd sd3"></span>
      <span class="screen-url">google.nl &nbsp;&rsaquo;&nbsp; {esc(query)}</span>
    </div>
    <div class="screen-body">
      <div style="font-size:.67rem;color:#70757a;margin-bottom:10px">Ongeveer 12.400.000 resultaten (0,42 seconden)</div>
      {rows}
    </div>
  </div>'''

def screen_website(url, title='', excerpt=''):
    return f'''<div class="screen r d1">
    <div class="screen-bar">
      <span class="sd sd1"></span><span class="sd sd2"></span><span class="sd sd3"></span>
      <span class="screen-url">{esc(url)}</span>
    </div>
    <div class="screen-body">
      {f'<div style="font-size:.92rem;font-weight:700;color:#111;margin-bottom:7px;font-family:Georgia,serif">{fmt(title)}</div>' if title else ''}
      {f'<div style="font-size:.76rem;color:#444;line-height:1.6">{fmt(excerpt)}</div>' if excerpt else ''}
    </div>
  </div>'''

def build_obs_html(obs_list):
    html = ''
    for i, obs in enumerate(obs_list[:3]):
        aankondiging = fmt(obs.get('aankondiging', ''))
        body = fmt(obs.get('body', ''))
        screen_type = obs.get('screen_type', 'none')
        screen_url = obs.get('screen_url', '')
        google_query = obs.get('google_query', '')
        google_results = obs.get('google_results', [])
        screen_title = obs.get('screen_title', '')
        screen_excerpt = obs.get('screen_excerpt', '')

        html += f'<p class="r" style="margin-top:{32 if i > 0 else 0}px"><strong>{aankondiging}</strong></p>\n'
        html += f'<p class="r">{body}</p>\n'

        if screen_type == 'google' and google_query:
            html += screen_google(screen_url, google_query, google_results) + '\n'
        elif screen_type == 'website' and screen_url:
            html += screen_website(screen_url, screen_title, screen_excerpt) + '\n'

    return html

def make_lp(c):
    company   = esc(c['company'])
    slug      = c['slug']
    domain    = c.get('domain', '')
    naam      = esc(c.get('naam', ''))
    voornaam  = esc(c.get('voornaam', ''))
    functie   = esc(c.get('functie', ''))
    tier      = c.get('tier', 1)

    # Variable sections from copy
    s1_p1     = fmt(c.get('s1_p1', ''))
    s1_p2     = fmt(c.get('s1_p2', ''))
    s1_p3     = fmt(c.get('s1_p3', ''))
    pivot_h2  = fmt(c.get('pivot_h2', ''))
    s3_p1     = fmt(c.get('s3_p1', ''))
    s3_p2     = fmt(c.get('s3_p2', ''))
    pull_quote = fmt(c.get('pull_quote', ''))
    s2_obs    = build_obs_html(c.get('obs', []))

    logo_src = f'https://logo.clearbit.com/{domain}' if domain else ''
    logo_html = f'<img src="{logo_src}" alt="{company}" onerror="this.style.display=\'none\'">' if logo_src else ''

    tier_label = {1: 'Tier 1', 2: 'Tier 2', 3: 'Tier 3'}.get(tier, '')

    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-NVMXNZ26');</script>
<!-- End Google Tag Manager -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TextInc Business - Voorbereid voor {company}</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#F6F5F2;--paper:#FFFFFF;--ink:#161614;--body:#383834;
  --muted:#888880;--faint:#AEADA6;--line:rgba(0,0,0,.07);--line2:rgba(0,0,0,.12);
  --accent:#1B4F8A;--sans:'Inter',system-ui,sans-serif;--serif:'Lora',Georgia,serif;--r:8px;
}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--sans);background:var(--bg);color:var(--body);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
img{{display:block;max-width:100%}}
.wrap{{max-width:680px;margin:0 auto;padding:0 28px}}
.topbar{{background:var(--ink);padding:12px 28px;display:flex;align-items:center;justify-content:space-between;gap:16px;position:sticky;top:0;z-index:20}}
.tb-brand{{font-size:.78rem;font-weight:600;color:rgba(255,255,255,.9);letter-spacing:.01em}}
.tb-label{{font-size:.68rem;color:rgba(255,255,255,.35);letter-spacing:.04em}}
h1{{font-family:var(--serif);font-size:clamp(2rem,5vw,3rem);font-weight:500;color:var(--ink);line-height:1.12;letter-spacing:-.03em}}
h2{{font-family:var(--serif);font-size:clamp(1.4rem,3vw,1.9rem);font-weight:500;color:var(--ink);line-height:1.2;letter-spacing:-.025em}}
h3{{font-size:.82rem;font-weight:700;color:var(--ink);letter-spacing:.06em;text-transform:uppercase}}
p{{font-size:.96rem;line-height:1.82;color:var(--body);margin-bottom:18px}}
p:last-child{{margin-bottom:0}}
p strong{{color:var(--ink);font-weight:600}}
.sec{{padding:80px 0;border-bottom:1px solid var(--line)}}
.sec:last-of-type{{border-bottom:none}}
.lbl{{display:inline-flex;align-items:center;gap:8px;font-size:.62rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:28px}}
.lbl::before{{content:'';width:18px;height:1px;background:var(--faint);flex-shrink:0}}
.pull{{font-family:var(--serif);font-style:italic;font-size:clamp(1.18rem,2.5vw,1.45rem);color:var(--ink);line-height:1.55;border-left:2px solid var(--ink);padding:4px 0 4px 22px;margin:36px 0}}
.prospect-mark{{display:flex;align-items:center;gap:14px;padding-bottom:28px;border-bottom:1px solid var(--line);margin-bottom:40px}}
.pm-logo{{width:44px;height:44px;background:var(--paper);border:1px solid var(--line2);border-radius:10px;overflow:hidden;flex-shrink:0;display:flex;align-items:center;justify-content:center}}
.pm-logo img{{width:36px;height:36px;object-fit:contain}}
.pm-name{{font-size:.78rem;font-weight:600;color:var(--ink);display:block;margin-bottom:1px}}
.pm-meta{{font-size:.68rem;color:var(--muted)}}
.screen{{border-radius:var(--r);overflow:hidden;border:1px solid var(--line2);box-shadow:0 4px 20px rgba(0,0,0,.08);margin:24px 0;background:var(--paper)}}
.screen-bar{{background:#ECEAE6;padding:9px 14px;display:flex;align-items:center;gap:5px;border-bottom:1px solid var(--line2)}}
.sd{{width:9px;height:9px;border-radius:50%}}
.sd1{{background:#E06C5A}}.sd2{{background:#E0C05A}}.sd3{{background:#5ABE6E}}
.screen-url{{flex:1;margin-left:10px;background:rgba(0,0,0,.07);border-radius:4px;height:20px;display:flex;align-items:center;padding:0 10px;font-size:.62rem;color:var(--muted);letter-spacing:.01em}}
.screen-body{{padding:20px 22px}}
.stat-row{{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}}
.chip{{display:inline-flex;flex-direction:column;padding:14px 18px;background:var(--paper);border:1px solid var(--line2);border-radius:var(--r)}}
.chip-val{{font-family:var(--serif);font-size:1.5rem;font-weight:500;color:var(--ink);line-height:1;margin-bottom:3px}}
.chip-lbl{{font-size:.65rem;color:var(--muted);line-height:1.35;max-width:100px}}
.pivot{{padding:52px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:48px 0;text-align:center}}
.pivot-pre{{font-size:.62rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:16px}}
.pivot h2{{text-align:center;max-width:480px;margin:0 auto}}
.ti-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line2);border-radius:var(--r);overflow:hidden;margin-top:32px}}
.ti-item{{background:var(--paper);padding:24px 22px}}
.ti-tag{{font-size:.6rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:8px}}
.ti-title{{font-size:.9rem;font-weight:600;color:var(--ink);margin-bottom:6px}}
.ti-desc{{font-size:.82rem;color:var(--muted);line-height:1.6}}
.team-card{{display:grid;grid-template-columns:1fr 1fr;gap:0;background:var(--paper);border:1px solid var(--line2);border-radius:14px;overflow:hidden;margin-top:32px}}
.tc-photo{{position:relative;overflow:hidden;background:#2A2A27;min-height:300px;display:flex;align-items:center;justify-content:center}}
.tc-photo img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 15%}}
.tc-photo-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(22,22,20,.6) 0%,transparent 50%)}}
.tc-photo-names{{position:absolute;bottom:18px;left:20px;color:#fff}}
.tc-photo-names strong{{display:block;font-size:1rem;font-weight:600;letter-spacing:-.01em;margin-bottom:3px}}
.tc-photo-names span{{font-size:.66rem;color:rgba(255,255,255,.55);letter-spacing:.05em;text-transform:uppercase}}
.tc-initials{{font-family:var(--serif);font-size:3rem;font-weight:500;color:rgba(255,255,255,.4)}}
.tc-body{{padding:28px 26px;display:flex;flex-direction:column;justify-content:space-between;gap:24px}}
.tc-bio{{font-size:.86rem;color:var(--body);line-height:1.75}}
.tc-facts{{display:flex;flex-direction:column;gap:14px;margin-top:auto}}
.tf-item{{border-left:2px solid var(--line2);padding-left:12px}}
.tf-val{{font-size:.86rem;font-weight:600;color:var(--ink);margin-bottom:1px}}
.tf-lbl{{font-size:.68rem;color:var(--muted)}}
.cta-sec{{background:var(--ink);border-radius:14px;padding:44px 40px;margin:48px 0;color:#fff}}
.cta-eyebrow{{font-size:.62rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.4);margin-bottom:14px}}
.cta-sec h2{{color:#fff;margin-bottom:14px}}
.cta-sec > p{{color:rgba(255,255,255,.6);font-size:.9rem;margin-bottom:0}}
.cta-cols{{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:36px;align-items:start}}
.cta-col-label{{font-size:.6rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.35);margin-bottom:14px}}
.cf{{display:flex;flex-direction:column;gap:9px}}
.cf input,.cf textarea{{width:100%;padding:11px 13px;border-radius:7px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.06);color:#fff;font-family:var(--sans);font-size:.84rem;outline:none;transition:border-color .2s}}
.cf input::placeholder,.cf textarea::placeholder{{color:rgba(255,255,255,.28)}}
.cf input:focus,.cf textarea:focus{{border-color:rgba(255,255,255,.3);background:rgba(255,255,255,.09)}}
.cf textarea{{height:100px;resize:none}}
.cf-btn{{width:100%;padding:12px;border-radius:7px;background:#fff;color:var(--ink);font-family:var(--sans);font-size:.84rem;font-weight:700;border:none;cursor:pointer;transition:opacity .18s}}
.cf-btn:hover{{opacity:.9}}
.cal-wrap{{border-radius:var(--r);overflow:hidden;border:1px solid rgba(255,255,255,.1);min-height:420px;background:rgba(255,255,255,.04)}}
#my-cal-inline-belafspraak-textinc{{width:100%;min-height:420px}}
.footer{{padding:28px 0 44px;text-align:center}}
.footer p{{font-size:.68rem;color:var(--faint);margin:0}}
.r{{opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s ease}}
.r.v{{opacity:1;transform:translateY(0)}}
.r.d1{{transition-delay:.08s}}.r.d2{{transition-delay:.16s}}.r.d3{{transition-delay:.24s}}
@media(max-width:600px){{
  .wrap{{padding:0 20px}}.sec{{padding:56px 0}}
  .ti-grid{{grid-template-columns:1fr}}
  .team-card{{grid-template-columns:1fr}}
  .tc-photo{{min-height:220px}}
  .cta-cols{{grid-template-columns:1fr}}
  .cta-sec{{padding:32px 22px}}
  .topbar{{padding:12px 20px}}
}}
</style>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NVMXNZ26" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

<div class="topbar">
  <span class="tb-brand">TextInc Business</span>
  <span class="tb-label">Vertrouwelijk &middot; Voorbereid voor {company}</span>
</div>

<div class="wrap">

<!-- S1: OPENING -->
<section class="sec">
  <div class="prospect-mark r">
    <div class="pm-logo">{logo_html}</div>
    <div>
      <span class="pm-name">{company}</span>
      <span class="pm-meta">{domain} &middot; {tier_label} &middot; Juni 2026</span>
    </div>
  </div>
  <h1 class="r">H&eacute; {voornaam}, dit is waarom<br>je mijn brief hebt ontvangen.</h1>
  <div style="margin-top:28px">
    <p class="r d1">{s1_p1}</p>
    <p class="r d2">{s1_p2}</p>
    {f'<p class="r d3">{s1_p3}</p>' if s1_p3 else ''}
  </div>
</section>

<!-- S2: OBSERVATIES -->
<section class="sec">
  <div class="lbl r">Hoe ik naar {company} keek</div>
  {s2_obs}
</section>

<!-- PIVOT -->
<div class="pivot r">
  <div class="pivot-pre">Waar het op uitkomt</div>
  <h2>{pivot_h2}</h2>
</div>

<!-- S3: ANALYSE -->
<section class="sec" style="padding-top:0;border-top:none">
  <div class="lbl r">Wat ik denk dat hierachter zit</div>
  <p class="r">{s3_p1}</p>
  {f'<p class="r">{s3_p2}</p>' if s3_p2 else ''}
  <div class="pull r">{pull_quote}</div>
</section>

<!-- S4: TEXTINC BUSINESS -->
<section class="sec">
  <div class="lbl r">TextInc Business</div>
  <h2 class="r">Wat wij doen.</h2>
  <p class="r" style="margin-top:14px">Wij helpen bedrijven meer doen met het websiteverkeer dat al binnenkomt. Via SEO-content die organisch bereik opbouwt, en via conversiegerichte teksten die bezoekers omzetten in klanten. <strong>Jouw propositie. Jouw toon. Jouw doelgroep.</strong></p>
  <div class="ti-grid r d1">
    <div class="ti-item">
      <div class="ti-tag">SEO-content</div>
      <div class="ti-title">Organisch bereik dat groeit</div>
      <div class="ti-desc">Pagina's die scoren op de zoektermen die je klanten gebruiken. Geen willekeurige content, maar gerichte autoriteitsopbouw.</div>
    </div>
    <div class="ti-item">
      <div class="ti-tag">Conversiegerichte copy</div>
      <div class="ti-title">Bezoekers die klant worden</div>
      <div class="ti-desc">Teksten die twijfel wegnemen en de volgende stap duidelijk maken. Van productpagina tot landingspagina.</div>
    </div>
    <div class="ti-item">
      <div class="ti-tag">Content architectuur</div>
      <div class="ti-title">Structuur die autoriteit opbouwt</div>
      <div class="ti-desc">Niet zomaar blogartikelen. Maar een contentstructuur die zoekmachines en beslissers begrijpen.</div>
    </div>
    <div class="ti-item">
      <div class="ti-tag">CRO &amp; tekst</div>
      <div class="ti-title">Meer uit bestaand verkeer</div>
      <div class="ti-desc">Je kunt meer verkeer binnenhalen. Of je kunt meer doen met het verkeer dat er al is. Dat is onze specialiteit.</div>
    </div>
  </div>
</section>

<!-- S5: SIMON KEMPERS -->
<section class="sec">
  <div class="lbl r">De persoon achter TextInc Business</div>
  <p class="r">Simon Kempers richtte TextInc Business op vanuit zijn achtergrond in SEO, copywriting en conversieoptimalisatie. Hij werkt met bedrijven die serieus verkeer binnenhalen maar meer willen doen met dat verkeer. Schrijven, structuur en de combinatie van beide.</p>
  <div class="team-card r d1">
    <div class="tc-photo">
      <img src="/textinc/simon.jpg" alt="Simon Kempers, TextInc Business" onerror="this.style.display='none'">
      <div class="tc-photo-overlay"></div>
      <div class="tc-photo-names">
        <strong>Simon Kempers</strong>
        <span>Oprichter &middot; TextInc Business &middot; Amsterdam</span>
      </div>
    </div>
    <div class="tc-body">
      <div class="tc-bio">SEO-strateeg en conversiespecialist. Helpt B2B-bedrijven en webshops structureel meer halen uit hun bestaande websiteverkeer. Combineert contentstrategie met conversiegerichte copy.</div>
      <div class="tc-facts">
        <div class="tf-item"><div class="tf-val">100+</div><div class="tf-lbl">content audits uitgevoerd</div></div>
        <div class="tf-item"><div class="tf-val">NL &amp; BE</div><div class="tf-lbl">B2B SaaS, e-commerce, platforms</div></div>
        <div class="tf-item"><div class="tf-val">SEO + CRO</div><div class="tf-lbl">Altijd in combinatie, nooit los</div></div>
      </div>
    </div>
  </div>
</section>

<!-- S6: CTA -->
<section class="sec" style="border-bottom:none;padding-bottom:0">
  <div class="cta-sec r">
    <div class="cta-eyebrow">Volgende stap</div>
    <h2>Plan een kennismaking in.</h2>
    <p>Als je benieuwd bent hoe wij hiernaar kijken: stuur een bericht of kies direct een moment dat past.</p>
    <div class="cta-cols">
      <div>
        <div class="cta-col-label">Stuur een bericht</div>
        <form class="cf" action="https://formspree.io/f/simon@textinc.nl" method="POST">
          <input type="hidden" name="prospect" value="{company}">
          <input type="text" name="naam" placeholder="Naam" required>
          <input type="email" name="email" placeholder="E-mailadres" required>
          <input type="text" name="bedrijf" placeholder="Bedrijf" value="{company}">
          <textarea name="bericht" placeholder="Korte vraag of opmerking"></textarea>
          <button class="cf-btn" type="submit">Verstuur bericht</button>
        </form>
      </div>
      <div>
        <div class="cta-col-label">Plan direct een belafspraak</div>
        <div class="cal-wrap">
          <div style="width:100%;height:100%;overflow:scroll" id="my-cal-inline-belafspraak-textinc"></div>
        </div>
      </div>
    </div>
  </div>
</section>

</div>

<footer class="footer">
  <p>TextInc Business &middot; Voorbereid voor {company} &middot; Vertrouwelijk</p>
</footer>

<script>
var P = {{ key: 'textinc_lp_{slug}' }};
(function() {{
  var els = document.querySelectorAll('.r');
  if (!('IntersectionObserver' in window)) {{ els.forEach(function(e) {{ e.classList.add('v'); }}); return; }}
  var io = new IntersectionObserver(function(entries) {{
    entries.forEach(function(e) {{ if (e.isIntersecting) {{ e.target.classList.add('v'); io.unobserve(e.target); }} }});
  }}, {{ rootMargin: '0px 0px -32px 0px', threshold: 0.04 }});
  els.forEach(function(el) {{ io.observe(el); }});
}})();
(function (C, A, L) {{ let p = function (a, ar) {{ a.q.push(ar); }}; let d = C.document; C.Cal = C.Cal || function () {{ let cal = C.Cal; let ar = arguments; if (!cal.loaded) {{ cal.ns = {{}}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; }} if (ar[0] === L) {{ const api = function () {{ p(api, arguments); }}; const namespace = ar[1]; api.q = api.q || []; if(typeof namespace === "string"){{cal.ns[namespace] = cal.ns[namespace] || api;p(cal.ns[namespace], ar);p(cal, ["initNamespace", namespace]);}} else p(cal, ar); return;}} p(cal, ar); }}; }})(window, "https://app.cal.com/embed/embed.js", "init");
Cal("init", "belafspraak-textinc", {{origin:"https://app.cal.com"}});
Cal.config = Cal.config || {{}};
Cal.config.forwardQueryParams = true;
Cal.ns["belafspraak-textinc"]("inline", {{
  elementOrSelector:"#my-cal-inline-belafspraak-textinc",
  config: {{"layout":"month_view","useSlotsViewOnSmallScreen":"true"}},
  calLink: "simon-kempers/belafspraak-textinc",
}});
Cal.ns["belafspraak-textinc"]("ui", {{"hideEventTypeDetails":false,"layout":"month_view"}});
</script>
</body>
</html>'''


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    copy_file = os.path.join(base_dir, '_copy-data.json')

    # Also write to TextInc Business/Outreach
    outreach_dir = os.path.join(
        os.path.dirname(os.path.dirname(base_dir)),
        'TextInc Business', 'Outreach'
    )
    os.makedirs(outreach_dir, exist_ok=True)

    if not os.path.exists(copy_file):
        print(f"ERROR: {copy_file} niet gevonden. Workflow eerst uitvoeren.", file=sys.stderr)
        sys.exit(1)

    with open(copy_file, encoding='utf-8') as f:
        companies = json.load(f)

    generated = 0
    errors = []
    for c in companies:
        slug = c.get('slug', '')
        if not slug:
            errors.append(f"Geen slug voor {c.get('company','?')}")
            continue
        try:
            html = make_lp(c)
            # Write to BCS/textinc/ (deploy root)
            out_path = os.path.join(base_dir, f'{slug}.html')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            # Also write to TextInc Business/Outreach/
            out_path2 = os.path.join(outreach_dir, f'{slug}.html')
            with open(out_path2, 'w', encoding='utf-8') as f:
                f.write(html)
            generated += 1
            print(f"  OK  {slug}.html  ({c.get('company','')})")
        except Exception as e:
            errors.append(f"{c.get('company','?')}: {e}")
            print(f"  ERR {slug}: {e}")

    print(f"\nGegenereerd: {generated}/{len(companies)}")
    if errors:
        print(f"Fouten: {len(errors)}")
        for e in errors:
            print(f"  - {e}")

if __name__ == '__main__':
    main()
