// BCS Batch 2 - Tier 1 prospectlijst generator (v2, met diep geverifieerd onderzoek)
// Voegt basisgegevens (bcs-batch2-base.json) samen met het research-dossier (bcs-batch2-research.json).
// Per bedrijf: geverifieerde beslisser, contactkanalen, echte trigger en een openingshoek.
// Regels: geen em-dashes, geen zinnen die met "Geen" beginnen, geen emojis/symbolen.

import { readFileSync, writeFileSync } from 'node:fs';

const base = JSON.parse(readFileSync(new URL('./bcs-batch2-base.json', import.meta.url)));
const research = JSON.parse(readFileSync(new URL('./bcs-batch2-research.json', import.meta.url)));

// bedrijven die niet meer actief zijn of buiten scope vallen
const oldDrop = new Set(['Amsterdenim', 'Posie Beauty', 'Willicroft', 'The Limonaderij']);

// Pique-schrijfregels
const clean = s => (s || '')
  .replace(/⚠️?\s*/g, 'Let op: ')
  .replace(/\s*—\s*/g, ', ')
  .replace(/–/g, '-')
  .replace(/\s*[↗→›►]\s*/g, ' ')
  .replace(/\s{2,}/g, ' ')
  .trim();
const esc = s => clean(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// samenvoegen
const rows = base
  .filter(p => !oldDrop.has(p.bedrijf))
  .map(p => ({ ...p, r: research[p.bedrijf] || null }))
  .filter(p => p.r && p.r.conf !== 'DROP');

// tier op basis van verificatie-confidence
const tierOf = r => {
  if (!r) return 'geen';
  if (r.conf === 'HARD') return 'hard';
  if (r.conf === 'LEAD') return 'lead';
  return 'geen'; // GEEN of leeg
};
rows.forEach(p => { p.tier = tierOf(p.r); });

const catMap = { Fashion: 'Fashion & apparel', Home: 'Home & interior', Beauty: 'Beauty & skincare', Supplements: 'Supplements & health', Food: 'Food & beverage', Accessoires: 'Accessoires & sieraden', Kids: 'Kids, baby & maternity', Baby: 'Kids, baby & maternity', 'Baby/kids': 'Kids, baby & maternity', Maternity: 'Kids, baby & maternity', Cycling: 'Sport, outdoor & pets', Sport: 'Sport, outdoor & pets', Outdoor: 'Sport, outdoor & pets', Fitness: 'Sport, outdoor & pets', Pets: 'Sport, outdoor & pets' };
const catOf = r => catMap[r.vert.split(' · ')[0]] || r.vert.split(' · ')[0];
rows.forEach(r => { r._cat = catOf(r); });
const verticals = [...new Set(rows.map(r => r._cat))];

const total = rows.length;
const nHard = rows.filter(p => p.tier === 'hard').length;
const nLead = rows.filter(p => p.tier === 'lead').length;
const nGeen = rows.filter(p => p.tier === 'geen').length;

// ---- CSV ----
const csvHeader = ['Bedrijf', 'Website', 'Stad', 'Verticaal', 'Omzet_est', 'Pijnprofiel', 'Beslisser_naam', 'Beslisser_functie', 'LinkedIn', 'Verificatie', 'Bron', 'Contactkanalen', 'Trigger', 'Openingshoek', 'Zoekopdracht_LinkedIn'];
const tierLabel = { hard: 'Geverifieerd', lead: 'Lead - checken', geen: 'Naam te vinden' };
const csv = [csvHeader.join(',')].concat(rows.map(p => [
  p.bedrijf, p.web, p.stad, p.vert, p.omzet, p.r.pp, p.r.naam, p.r.functie, p.r.li || '', tierLabel[p.tier], p.r.bron, p.r.kanalen, p.r.trigger, p.r.obs, p.hoek
].map(v => `"${clean(v).replace(/"/g, '""')}"`).join(','))).join('\n');
writeFileSync(new URL('./BCS-Prospects-Batch2.csv', import.meta.url), csv);

// ---- HTML ----
const cardHTML = p => {
  const r = p.r;
  const tiers = {
    hard: { cls: 'conf-ok', txt: 'Geverifieerd' },
    lead: { cls: 'conf-check', txt: 'Lead, checken' },
    geen: { cls: 'conf-none', txt: 'Naam te vinden' },
  };
  const t = tiers[p.tier];
  const ppBadge = r.pp ? `<span class="pp pp-${r.pp}">Pijn ${r.pp}</span>` : '';
  const liLink = r.li ? `<a class="besl-li" href="${esc(r.li)}" target="_blank">LinkedIn</a>` : '';
  const besl = r.naam
    ? `<div class="besl-naam">${esc(r.naam)}</div><div class="besl-functie">${esc(r.functie)}</div>${liLink}`
    : `<div class="besl-naam besl-leeg">Doelrol: ${esc(r.functie || 'beslisser te vinden')}</div>`;
  const bron = r.bron ? `<div class="besl-note">Bron: ${esc(r.bron)}</div>` : '';
  const check = (p.tier !== 'hard' && p.hoek) ? `<div class="dl"><span class="dl-k">Checken</span><span class="dl-v mono-sm">${esc(p.hoek)}</span></div>` : '';
  return `<div class="card">
    <div class="card-top">
      <div>
        <div class="card-name">${esc(p.bedrijf)}</div>
        <a class="card-web" href="https://${esc(p.web)}" target="_blank">${esc(p.web)}</a>
      </div>
      <span class="conf ${t.cls}">${esc(t.txt)}</span>
    </div>
    <div class="card-meta">
      <span>${esc(p.stad)}</span><span class="dot">·</span><span>${esc(p.vert)}</span><span class="dot">·</span><span>${esc(p.omzet)}</span>${ppBadge}
    </div>
    <div class="card-besl">
      <div class="besl-label">Beslisser</div>
      ${besl}${bron}
    </div>
    <div class="card-detail">
      <div class="dl"><span class="dl-k">Kanalen</span><span class="dl-v">${esc(r.kanalen)}</span></div>
      <div class="dl"><span class="dl-k">Trigger</span><span class="dl-v">${esc(r.trigger)}</span></div>
      <div class="dl"><span class="dl-k">Opening</span><span class="dl-v dl-obs">${esc(r.obs)}</span></div>
      ${check}
    </div>
  </div>`;
};

const sections = verticals.map(v => {
  const items = rows.filter(r => r._cat === v);
  return `<section class="sec">
    <div class="sec-head"><span class="sec-title">${esc(v)}</span><span class="sec-count">${items.length}</span></div>
    <div class="grid">${items.map(cardHTML).join('')}</div>
  </section>`;
}).join('');

const html = `<!DOCTYPE html>
<html lang="nl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BCS · Prospectlijst Batch 2 · Tier 1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#F8F6F2;--navy:#0F172A;--amber:#D4943A;--white:#FFFFFF;--text:#1E2433;--muted:rgba(30,36,51,.48);--border:rgba(15,23,42,.09);--red:#dc2626;--green:#16a34a;--serif:'Playfair Display',Georgia,serif;--sans:'Inter',system-ui,sans-serif;--mono:'DM Mono',monospace}
body{font-family:var(--sans);background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;line-height:1.6}
.topbar{background:var(--navy);padding:.7rem 2.5rem;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
.topbar-l{display:flex;align-items:center;gap:1rem}
.topbar-logo{font-family:var(--serif);font-size:.95rem;font-weight:600;color:var(--white);letter-spacing:-.02em}
.topbar-sep{width:1px;height:12px;background:rgba(255,255,255,.12)}
.topbar-title{font-family:var(--mono);font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.35)}
.topbar-badge{background:rgba(212,148,58,.15);border:1px solid rgba(212,148,58,.3);border-radius:100px;padding:.22rem .65rem;font-family:var(--mono);font-size:.56rem;letter-spacing:.1em;text-transform:uppercase;color:var(--amber)}
.wrap{max-width:1100px;margin:0 auto;padding:0 2.5rem}
.ey{font-family:var(--mono);font-size:.58rem;letter-spacing:.2em;text-transform:uppercase;color:var(--amber);margin-bottom:.75rem;display:flex;align-items:center;gap:.5rem}
.ey::before{content:'';width:10px;height:1px;background:var(--amber);opacity:.7}
h1{font-family:var(--serif);font-size:clamp(2rem,3vw,2.8rem);font-weight:600;line-height:1.1;letter-spacing:-.03em;color:var(--navy)}
.sub{font-size:.9rem;color:var(--muted);line-height:1.7;margin-top:.7rem;max-width:680px}
.hero{padding:3.5rem 0 2.5rem;border-bottom:1px solid var(--border)}
.hero-g{display:grid;grid-template-columns:1fr 320px;gap:3.5rem;align-items:start}
.hcard{background:var(--navy);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,.06)}
.hcard-label{font-family:var(--mono);font-size:.56rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(212,148,58,.6);margin-bottom:1rem;display:block}
.hcard-stats{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:rgba(255,255,255,.06);border-radius:10px;overflow:hidden;margin-bottom:1.1rem}
.hs{background:rgba(255,255,255,.03);padding:.85rem;text-align:center}
.hs-n{font-family:var(--serif);font-size:1.5rem;font-weight:700;color:var(--white);line-height:1}
.hs-n .a{color:var(--amber)}
.hs-l{font-size:.6rem;color:rgba(255,255,255,.3);margin-top:.25rem}
.hcard-note{font-size:.74rem;color:rgba(255,255,255,.4);line-height:1.55;border-top:1px solid rgba(255,255,255,.06);padding-top:.9rem}
.hcard-note strong{color:rgba(255,255,255,.7)}
.callout{margin-top:1.75rem;background:rgba(212,148,58,.06);border:1px solid rgba(212,148,58,.18);border-radius:12px;padding:1.1rem 1.3rem;font-size:.82rem;color:rgba(30,36,51,.66);line-height:1.6}
.callout strong{color:var(--navy)}
.sec{padding:2.75rem 0 .5rem}
.sec-head{display:flex;align-items:center;gap:.8rem;margin-bottom:1.25rem}
.sec-title{font-family:var(--serif);font-size:1.45rem;font-weight:600;color:var(--navy);letter-spacing:-.02em}
.sec-count{font-family:var(--mono);font-size:.6rem;color:var(--muted);border:1px solid var(--border);border-radius:100px;padding:.15rem .55rem}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.card{background:var(--white);border:1.5px solid var(--border);border-radius:14px;padding:1.2rem 1.35rem;transition:border-color .2s}
.card:hover{border-color:rgba(212,148,58,.3)}
.card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:1rem}
.card-name{font-size:1rem;font-weight:600;color:var(--navy);letter-spacing:-.01em}
.card-web{font-family:var(--mono);font-size:.66rem;color:var(--muted);text-decoration:none}
.card-web:hover{color:var(--amber)}
.conf{font-family:var(--mono);font-size:.52rem;letter-spacing:.08em;text-transform:uppercase;padding:.24rem .55rem;border-radius:100px;white-space:nowrap;flex-shrink:0}
.conf-ok{background:rgba(22,163,74,.1);color:var(--green);border:1px solid rgba(22,163,74,.2)}
.conf-check{background:rgba(212,148,58,.08);color:var(--amber);border:1px solid rgba(212,148,58,.2)}
.conf-none{background:rgba(15,23,42,.05);color:var(--muted);border:1px solid var(--border)}
.card-meta{display:flex;align-items:center;flex-wrap:wrap;gap:.4rem;margin-top:.55rem;font-size:.72rem;color:var(--muted)}
.card-meta .dot{opacity:.4}
.pp{font-family:var(--mono);font-size:.54rem;letter-spacing:.05em;padding:.1rem .45rem;border-radius:100px;margin-left:.25rem}
.pp-A{background:rgba(220,38,38,.07);color:rgba(220,38,38,.8)}
.pp-B{background:rgba(15,23,42,.06);color:rgba(30,36,51,.55)}
.card-besl{margin-top:.9rem;padding:.75rem .9rem;background:rgba(15,23,42,.025);border-radius:10px;border:1px solid var(--border)}
.besl-label{font-family:var(--mono);font-size:.52rem;letter-spacing:.12em;text-transform:uppercase;color:rgba(212,148,58,.7);margin-bottom:.35rem}
.besl-naam{font-size:.86rem;font-weight:600;color:var(--navy)}
.besl-leeg{color:var(--muted);font-weight:500;font-style:italic}
.besl-functie{font-size:.74rem;color:var(--muted);margin-top:.1rem}
.besl-li{display:inline-block;margin-top:.35rem;font-family:var(--mono);font-size:.6rem;color:var(--amber);text-decoration:none}
.besl-note{font-size:.66rem;color:rgba(30,36,51,.42);margin-top:.3rem;line-height:1.4;font-style:italic}
.card-detail{margin-top:.85rem;display:flex;flex-direction:column;gap:.5rem}
.dl{display:grid;grid-template-columns:66px 1fr;gap:.6rem;align-items:start}
.dl-k{font-family:var(--mono);font-size:.55rem;letter-spacing:.06em;text-transform:uppercase;color:rgba(30,36,51,.38);padding-top:.1rem}
.dl-v{font-size:.76rem;color:rgba(30,36,51,.72);line-height:1.5}
.dl-obs{color:var(--navy);font-style:italic}
.mono-sm{font-family:var(--mono);font-size:.64rem;color:rgba(30,36,51,.5);word-break:break-word}
.doc-footer{background:var(--navy);padding:1.5rem 2.5rem;display:flex;align-items:center;justify-content:space-between;margin-top:3.5rem}
.df-l{font-family:var(--mono);font-size:.58rem;color:rgba(255,255,255,.25);letter-spacing:.06em}
.df-r{font-family:var(--mono);font-size:.56rem;color:rgba(255,255,255,.18);letter-spacing:.06em}
@media(max-width:880px){.hero-g,.grid{grid-template-columns:1fr}.wrap{padding:0 1.3rem}.topbar{padding:.7rem 1.3rem}}
</style></head>
<body>
<div class="topbar">
  <div class="topbar-l"><span class="topbar-logo">Pique</span><span class="topbar-sep"></span><span class="topbar-title">Prospectlijst · Backbone CS</span></div>
  <span class="topbar-badge">Batch 2 · Tier 1 · Geverifieerd</span>
</div>
<div class="wrap">
  <section class="hero">
    <div class="hero-g">
      <div>
        <div class="ey">Prospectlijst · Batch 2 · Onderzoeksronde</div>
        <h1>${total} Tier 1 bedrijven.<br>Beslisser en trigger onderzocht.</h1>
        <p class="sub">Elk bedrijf is opnieuw diep onderzocht via de eigen contact-, team- en klantenservicepagina, plus reviews. Per bedrijf staat de beslisser met betrouwbaarheidsniveau, welke contactkanalen ze de klant echt bieden, een verifieerbare trigger op basis van hun klantenservicesituatie, en een openingshoek voor het eerste contact.</p>
        <div class="callout">
          <strong>Betrouwbaarheid van de beslisser.</strong> <strong>Geverifieerd</strong> (${nHard}): naam en rol staan op de eigen site of zijn in meerdere bronnen bevestigd, hier sta ik achter. <strong>Lead, checken</strong> (${nLead}): de naam komt uit een LinkedIn-zoekresultaat of externe database die ik niet kon openen, controleer die in een ingelogde sessie voordat je benadert. <strong>Naam te vinden</strong> (${nGeen}): geen bereikbare beslisser gevonden, alleen een algemeen adres of een naam achter een betaald KvK-uittreksel. Er is geen naam verzonnen. Bedrijven die niet meer actief of niet in Nederland bleken, zijn onderweg verwijderd.
        </div>
      </div>
      <div class="hcard">
        <span class="hcard-label">Stand na onderzoek</span>
        <div class="hcard-stats">
          <div class="hs"><div class="hs-n">${total}</div><div class="hs-l">Actieve Tier 1</div></div>
          <div class="hs"><div class="hs-n"><span class="a">${nHard}</span></div><div class="hs-l">Beslisser geverifieerd</div></div>
          <div class="hs"><div class="hs-n">${nLead}</div><div class="hs-l">Lead, checken</div></div>
          <div class="hs"><div class="hs-n">${nGeen}</div><div class="hs-l">Naam te vinden</div></div>
        </div>
        <div class="hcard-note"><strong>Pijnprofiel A</strong> = overbelaste founder/insider doet CS erbij. <strong>Pijnprofiel B</strong> = onbetrouwbare part-timer/junior-opzet. De trigger en opening sluiten aan op het zichtbare profiel.</div>
      </div>
    </div>
  </section>
  ${sections}
</div>
<div class="doc-footer">
  <span class="df-l">Pique × Backbone CS · Prospectlijst Batch 2 · Onderzoeksronde</span>
  <span class="df-r">Volgende stap: leads bevestigen, daarna assets</span>
</div>
</body></html>`;

writeFileSync(new URL('./BCS-Prospects-Batch2.html', import.meta.url), html);

// ---- Verificatielijst (Markdown) om af te lopen ----
const byTier = t => rows.filter(p => p.tier === t);
const hardRow = p => `- **${p.bedrijf}**: ${clean(p.r.naam)}, ${clean(p.r.functie)} (${clean(p.r.bron)})`;
const leadRow = (p, i) => `${i + 1}. [ ] **${p.bedrijf}** -> ${clean(p.r.naam || '(naam te vinden)')}, ${clean(p.r.functie)}\n` +
  `    Bron: ${clean(p.r.bron)}\n` +
  (p.hoek ? `    Zoek: \`${clean(p.hoek)}\`\n` : '') +
  `    Trigger: ${clean(p.r.trigger)}\n` +
  `    Bevinding: \n`;

const md = `# BCS Batch 2 verificatielijst beslissers (na onderzoeksronde)

Doel: de "Lead" en "Naam te vinden" beslissers bevestigen in een ingelogde LinkedIn-sessie of via KvK. Vul achter "Bevinding" in: klopt / klopt niet / juiste naam.

Stand: ${total} actieve bedrijven. ${nHard} geverifieerd, ${nLead} lead te checken, ${nGeen} naam te vinden. New Optimist (failliet) en TakeDaily (opgeheven) zijn verwijderd.

---

## A. Geverifieerd (${nHard}): naam op eigen site of in meerdere bronnen bevestigd
${byTier('hard').map(hardRow).join('\n')}

---

## B. Lead, checken (${nLead}): naam uit LinkedIn-zoekresultaat of database, nog niet hard bevestigd
${byTier('lead').map(leadRow).join('\n')}
---

## C. Naam te vinden (${nGeen}): geen publieke naam, doelrol bekend
${byTier('geen').map(leadRow).join('\n')}`;

writeFileSync(new URL('./BCS-Batch2-Verificatielijst.md', import.meta.url), md);

console.log(`Gegenereerd: ${total} actieve bedrijven. Geverifieerd ${nHard}, lead ${nLead}, naam te vinden ${nGeen}. ${verticals.length} verticals.`);
