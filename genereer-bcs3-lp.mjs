// BCS Batch 3 - persoonlijke landingspagina's (journey / verhaallijn-model, 1:1 design van bcs2)
// Output: bcs3/[slug].html -> intro-pique.agency/bcs3/[slug]
// Bron: bcs3-base.json + bcs3-content.json (geschreven per prospect) + bcs3-favicons/
// Video Jeffrey bovenaan. Merk-favicon per merk. WebwinkelKeur-partnerblok bij merken met wwk=true.
// Schrijfregels: geen em-dashes, geen zin die met "Geen" begint, geen emojis.

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';

const base = JSON.parse(readFileSync(new URL('./bcs3-base.json', import.meta.url)));
const content = JSON.parse(readFileSync(new URL('./bcs3-content.json', import.meta.url)));
const css = readFileSync(new URL('./bcs3-style.css', import.meta.url), 'utf8');
const wwkSvg = readFileSync(new URL('./webwinkel-keur-logo.svg', import.meta.url), 'utf8')
  .replace(/<\?xml[^>]*\?>/, '').replace(/<!DOCTYPE[^>]*>/i, '').trim();

const clean = s => (s || '')
  .replace(/⚠️?\s*/g, 'Let op: ')
  .replace(/\s*—\s*/g, ', ')
  .replace(/–/g, '-')
  .replace(/\s*[↗→›►]\s*/g, ' ')
  .replace(/\s{2,}/g, ' ')
  .trim();
const esc = s => clean(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const slug = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’'.]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
const mono = n => n.replace(/[^A-Za-z ]/g, '').split(/\s+/).filter(Boolean).slice(0, 2).map(w => w[0].toUpperCase()).join('');
const firstName = naam => {
  if (!naam) return '';
  const t = String(naam).trim().split(/[\s,&]+/)[0];
  if (/^[A-Za-z]\.?$/.test(t)) return '';
  return t;
};

const favDir = new URL('./bcs3-favicons/', import.meta.url);
const favData = (s, naam) => {
  const f = new URL(`${s}.png`, favDir);
  if (existsSync(f) && readFileSync(f).length >= 120) {
    const uri = `data:image/png;base64,${readFileSync(f).toString('base64')}`;
    return { logo: `<div class="bt-logo bt-img"><img src="${uri}" alt="${esc(naam)}"></div>`, icon: uri };
  }
  return { logo: `<div class="bt-logo">${esc(mono(naam))}</div>`, icon: null };
};

const findingChapters = (findings) => (findings || []).map((f, i) => {
  const side = i % 2 === 0 ? 'right' : 'left';
  const strong = f.strong ? ` <strong>${esc(f.strong)}</strong>` : '';
  const bron = f.src ? `<div class="ch-bron">${esc(f.src)}</div>` : '';
  return `
    <section class="chapter ${side}">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="ch-num">${String(i + 1).padStart(2, '0')}</div><h2 class="ch-kop">${esc(f.h)}</h2><p class="ch-text">${esc(f.body)}${strong}</p>${bron}</div>
      </div>
    </section>`;
}).join('');

const betekenisParas = (paras) => (paras || []).map(p => `<p class="ch-text">${esc(p)}</p>`).join('');

const wwkChapter = (naam) => `
    <section class="chapter right phase-wwk ch-wwk">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="wwk-logo">${wwkSvg}</div><div class="ch-eyebrow">En dit sluit precies aan</div><h2 class="ch-kop">Jullie WebwinkelKeur blijft staan.</h2><p class="ch-text">Jullie werken met WebwinkelKeur. Backbone is officieel WebwinkelKeur-partner. We handelen klantvragen en geschillen af volgens het WebwinkelKeur-beleid, dus de manier waarop wij jouw klanten te woord staan telt gewoon mee voor je keurmerk. <strong>De service die je klanten al van je gewend zijn, blijft precies zo staan.</strong></p><div class="ch-bron">Bron: webwinkelkeur.nl/partner/backbonecustomerservice</div></div>
      </div>
    </section>`;

const nkey=s=>(s||"").toLowerCase().replace(/\(.*?\)/g,"").normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[^a-z0-9]/g,"");
const contentNorm={}; for(const k of Object.keys(content)) contentNorm[nkey(k)]=content[k];
const page = p => {
  const naam = p.bedrijf;
  const c = content[naam] || contentNorm[nkey(naam)];
  if (!c) return null;
  const s = p.slug;
  const fn = firstName(p.beslisser);
  const h1 = fn
    ? `Hé ${esc(fn)},<br>dit is waarom je m'n brief hebt ontvangen.`
    : `Dit is waarom je<br>m'n brief hebt ontvangen.`;
  const meta = [p.plaats, '2026'].filter(Boolean).map(esc).join(' &middot; ');
  const fav = favData(s, naam);
  const iconLink = fav.icon
    ? `<link rel="icon" type="image/png" href="${fav.icon}">\n<link rel="apple-touch-icon" href="${fav.icon}">`
    : `<link rel="icon" type="image/png" href="favicon.png">`;

  return `<!DOCTYPE html>
<html lang="nl">
<head>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-NVMXNZ26');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Backbone CS - Voorbereid voor ${esc(naam)}</title>
<meta name="robots" content="noindex, nofollow">
${iconLink}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
${css}
</style>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NVMXNZ26" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

<div class="topbar">
  <span class="tb-brand">Backbone Customer Service</span>
  <span class="tb-label">Vertrouwelijk &middot; Voorbereid voor ${esc(naam)}</span>
</div>

<header class="intro" id="top">
  <div class="intro-grid"></div>
  <div class="intro-inner">
    <div class="intro-eyebrow">Voorbereid voor ${esc(naam)}</div>
    <div class="brand-tile">
      ${fav.logo}
      <div class="bt-text"><span class="bt-name">${esc(naam)}</span><span class="bt-meta">${meta}</span></div>
    </div>
    <div class="vframe"><video src="video.mp4#t=0.1" controls preload="metadata" playsinline></video></div>
    <div class="vlabel">Jeffrey, mede-oprichter van Backbone, over wat we bij ${esc(naam)} zagen.</div>
    <h1 class="intro-h1">${h1}</h1>
    <p class="intro-sub">Neem even de tijd. We nemen je stap voor stap mee.</p>
    <div class="scrollcue"><span>Volg de lijn</span><i></i></div>
  </div>
</header>

<main class="journey" id="journey">
  <svg class="journey-path" id="jpath" preserveAspectRatio="none" aria-hidden="true">
    <path class="jp-base" id="jp-base"></path>
    <path class="jp-prog" id="jp-prog"></path>
  </svg>

    <section class="chapter left">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="ch-eyebrow">Voor jou</div><h2 class="ch-kop">Waarom je dit ziet.</h2><p class="ch-text">${esc(c.lead)}</p><p class="ch-text">Juist daarom viel ons iets op. We zagen een paar dingen die bij elkaar horen, en we nemen je er even in mee.</p><div class="ch-sign"><strong>Jeffrey</strong>, mede-oprichter Backbone</div></div>
      </div>
    </section>

    <section class="chapter center phase">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="ch-eyebrow">Wat we zagen</div><h2 class="ch-kop ch-head">Bij ${esc(naam)}.</h2><p class="ch-sub">Een paar dingen die ons opvielen. Ze horen bij elkaar.</p></div>
      </div>
    </section>
${findingChapters(c.findings)}

    <section class="chapter center pivot">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="ch-eyebrow">Waar het op uitkomt</div><p class="ch-pivot">${esc(c.pivot)}</p></div>
      </div>
    </section>

    <section class="chapter left">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="ch-eyebrow">Wat dit betekent</div><h2 class="ch-kop">De prijs van stilzitten.</h2>${betekenisParas(c.betekenis)}${c.pull ? `<p class="ch-pull">${esc(c.pull)}</p>` : ''}${c.imagine ? `<p class="ch-text" style="margin-top:1.4rem;">${esc(c.imagine)}</p>` : ''}</div>
      </div>
    </section>

    <section class="chapter center phase">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="ch-eyebrow">Wat Backbone doet</div><h2 class="ch-kop ch-head">En dit is precies wat wij doen.</h2><p class="ch-sub">We nemen dat klantcontact over. Volledig uitbesteed, zo ingericht dat het klinkt alsof het intern bij ${esc(naam)} zit.</p></div>
      </div>
    </section>

    <section class="chapter right">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="ch-num">01</div><h2 class="ch-kop">Jouw toon, altijd</h2><p class="ch-text">We leren het merk kennen voor het eerste ticket. Voor ${esc(naam)} klinkt het als ${esc(naam)}, klanten merken het verschil niet met een intern team. <strong>Jouw toon. Jouw naam. Jouw tempo.</strong></p></div>
      </div>
    </section>

    <section class="chapter left">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body"><div class="ch-num">02</div><h2 class="ch-kop">Vaste EU-agents</h2><p class="ch-text">Mensen die de merken kennen waarvoor ze werken. Meerdere talen, in Zendesk. Zodat de belofte naar je klanten blijft staan, juist als het druk wordt.</p></div>
      </div>
    </section>
${c.wwk ? wwkChapter(naam) : ''}
</main>

<section class="proof" id="founders">
  <div class="proof-eyebrow reveal">De mensen achter Backbone</div>
  <h2 class="proof-head reveal">Twee Zendesk-professionals, bewust klein gehouden.</h2>
  <p class="proof-sub reveal">Jeffrey en Dylan richtten Backbone op vanuit hun achtergrond als Zendesk-specialisten. Ze werken uitsluitend met D2C-merken en houden het team bewust klein genoeg om kwaliteit te garanderen.</p>
  <div class="team-card reveal">
    <div class="tc-photo">
      <img src="jeff-dylan.jpg" alt="Jeffrey en Dylan, mede-oprichters Backbone Customer Service">
      <div class="tc-photo-overlay"></div>
      <div class="tc-photo-names">
        <strong>Jeffrey &amp; Dylan</strong>
        <span>Mede-oprichters &middot; Backbone CS &middot; Woerden</span>
      </div>
    </div>
    <div class="tc-body">
      <div class="tc-bio">Twee Zendesk-professionals die hun e-commerce-ervaring omzetten in een sterke D2C-klantenservice. Snelheid waar het kan, mensen waar het telt.</div>
      <div class="tc-facts">
        <div class="tf-item"><div class="tf-val">1M+ tickets</div><div class="tf-lbl">afgehandeld</div></div>
        <div class="tf-item"><div class="tf-val">20+ agents</div><div class="tf-lbl">EU-based, meerdere talen</div></div>
        <div class="tf-item"><div class="tf-val">Vaste prijs</div><div class="tf-lbl">per ticket, geen verrassingen</div></div>
      </div>
    </div>
  </div>
</section>

<section class="cta" id="gesprek">
  <div class="cta-inner">
    <div class="cta-eyebrow reveal">Volgende stap</div>
    <h2 class="cta-h reveal">Even kennismaken?</h2>
    <p class="cta-sub reveal">Dit wordt geen verkoopgesprek. Gewoon kijken hoe wij naar de klantenservice van ${esc(naam)} kijken, en of die belofte naar je klanten steviger kan. Kies hieronder een moment dat je uitkomt.</p>
    <div class="cta-embed reveal"><div id="my-cal-inline-30min"></div></div>
  </div>
</section>

<footer>
  <div class="ft-meta">
    Backbone Customer Service &middot; Voorbereid voor ${esc(naam)} &middot; Vertrouwelijk<br>
    <a href="mailto:info@backbonecustomerservice.com">info@backbonecustomerservice.com</a>
  </div>
</footer>

<script>
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.18});
document.querySelectorAll('.chapter,.reveal').forEach(el=>io.observe(el));
const journey=document.getElementById('journey'),svg=document.getElementById('jpath');
const base=document.getElementById('jp-base'),prog=document.getElementById('jp-prog');
const dots=[...journey.querySelectorAll('.ch-dot')];
let total=0;
function build(){
  const W=journey.clientWidth,H=journey.clientHeight,jr=journey.getBoundingClientRect();
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const pts=dots.map(x=>{const r=x.getBoundingClientRect();return{x:r.left+r.width/2-jr.left,y:r.top+r.height/2-jr.top};});
  if(pts.length<2)return;
  let dd='M '+pts[0].x.toFixed(1)+' '+pts[0].y.toFixed(1);
  for(let i=1;i<pts.length;i++){const a=pts[i-1],c=pts[i],my=((a.y+c.y)/2).toFixed(1);
    dd+=' C '+a.x.toFixed(1)+' '+my+', '+c.x.toFixed(1)+' '+my+', '+c.x.toFixed(1)+' '+c.y.toFixed(1);}
  base.setAttribute('d',dd);prog.setAttribute('d',dd);
  total=prog.getTotalLength();prog.style.strokeDasharray=total;
  onScroll();
}
function onScroll(){
  if(!total)return;
  const jr=journey.getBoundingClientRect(),trig=window.innerHeight*.52;
  const frac=Math.max(0,Math.min(1,(trig-jr.top)/journey.clientHeight));
  prog.style.strokeDashoffset=total*(1-frac);
  dots.forEach(x=>{const r=x.getBoundingClientRect();x.parentElement.parentElement.classList.toggle('reached',r.top+r.height/2<trig);});
}
addEventListener('scroll',onScroll,{passive:true});
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(build,120);});
build();addEventListener('load',build);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(build);
const vid=document.querySelector('.vframe video');if(vid)vid.addEventListener('loadedmetadata',build);
setTimeout(build,400);setTimeout(build,1200);
if(window.ResizeObserver)new ResizeObserver(()=>build()).observe(journey);
(function(C,A,L){let p=function(a,ar){a.q.push(ar)};let d=C.document;C.Cal=C.Cal||function(){let cal=C.Cal;let ar=arguments;if(!cal.loaded){cal.ns={};cal.q=cal.q||[];d.head.appendChild(d.createElement("script")).src=A;cal.loaded=true}if(ar[0]===L){const api=function(){p(api,arguments)};const namespace=ar[1];api.q=api.q||[];if(typeof namespace==="string"){cal.ns[namespace]=cal.ns[namespace]||api;p(cal.ns[namespace],ar);p(cal,["initNamespace",namespace])}else p(cal,ar);return}p(cal,ar)}})(window,"https://app.cal.com/embed/embed.js","init");
Cal("init","30min",{origin:"https://app.cal.com"});
Cal.ns["30min"]("inline",{elementOrSelector:"#my-cal-inline-30min",config:{"layout":"month_view","useSlotsViewOnSmallScreen":"true"},calLink:"jeffrey-backbone-cs/30min"});
Cal.ns["30min"]("ui",{"hideEventTypeDetails":false,"layout":"month_view"});
</script>
</body>
</html>`;
};

mkdirSync(new URL('./bcs3/', import.meta.url), { recursive: true });
const index = [];
let written = 0, skipped = [];
for (const p of base) {
  const html = page(p);
  if (!html) { skipped.push(p.bedrijf); continue; }
  writeFileSync(new URL(`./bcs3/${p.slug}.html`, import.meta.url), html);
  index.push({ bedrijf: p.bedrijf, slug: p.slug, url: `intro-pique.agency/bcs3/${p.slug}`, beslisser: p.beslisser, wwk: !!((content[p.bedrijf]||contentNorm[nkey(p.bedrijf)]||{}).wwk) });
  written++;
}
writeFileSync(new URL('./bcs3-index.json', import.meta.url), JSON.stringify(index, null, 1));
console.log(`Gegenereerd: ${written} landingspagina's in bcs3/. Overgeslagen (geen content): ${skipped.length}${skipped.length ? ' -> ' + skipped.slice(0,15).join(', ') : ''}`);
