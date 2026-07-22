// AUTO-AFGELEID van genereer-pique-batch3.mjs door build-batch4.mjs.
// AUTO-AFGELEID van genereer-pique-batch2.mjs door build-batch3.mjs.
// Genereert 25 persoonlijke franchise-LP's (batch 2) in ./pique/[slug].html
// Ontwerp: premium, minimalistisch "reveal journey". Een slingerend gestippeld pad (SVG, in JS
// door de echte hoofdstuk-ankers getekend) verbindt asymmetrische, alternerende hoofdstukken.
// Het pad inkt amber terwijl je scrolt; hoofdstukken onthullen zich subtiel. Chronologisch verhaal.
// Schrijfregels: geen em-dashes, geen 'Geen'-zinstart, geen 'niet x maar y', geen emojis, geen cursief.
import { writeFileSync, mkdirSync, readFileSync } from 'node:fs';
import { PROSPECTS } from './pique-batch4-data.mjs';

const CAL = 'https://cal.com/simon-kempers/belafspraak-pique';
const LOGO = readFileSync(new URL('../../Marketing/Logo Pique/SVG/Logo 1-01.svg', import.meta.url),'utf8').replace(/<defs>[\s\S]*?<\/defs>/,'').replace(/class=\"cls-1\"/g,'fill=\"currentColor\"').replace(/class=\"cls-2\"/g,'fill=\"#D4943A\"').replace(/\s+/g,' ');
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

function render(p){
  const objLower = p.object.charAt(0).toLowerCase()+p.object.slice(1);
  const founderText = p.founderText || `Ik bouw voor een handvol netwerken tegelijk een regionale acquisitiemachine. ${p.org} paste precies in dat beeld, dus nam ik de tijd om dit voorstel met de hand voor je uit te werken.`;
  const ctaSub = p.ctaSub || `We kiezen samen één regio en de droomklanten die daar zitten. Werkt het, dan rollen we het uit over ${p.structuur}.`;
  const org = esc(p.org);

  // Journey-hoofdstukken (alternerend links/rechts), chronologisch, met fase-koppen.
  const F = p.aannames;
  const C = [
    { side:'left', eyebrow:'Voor jou', kop:'Waarom je dit ziet.', body:`${p.persoonlijkeNoot}`, sign:true },
    { side:'center', header:true, eyebrow:'Wat ik zag', kop:`Bij ${org}.`, sub:`Drie dingen die me opvielen. Ze horen bij elkaar.` },
    { side:'right', num:'01', kop:F[0].kop, body:F[0].tekst },
    { side:'left', num:'02', kop:F[1].kop, body:F[1].tekst },
    { side:'right', num:'03', kop:F[2].kop, body:F[2].tekst },
    { side:'center', pivot:true, pre:'Waar het op uitkomt', kop:p.tension },
    { side:'left', eyebrow:'Wat dit betekent', kop:'De prijs van stilzitten.', body:p.consequence },
    { side:'center', header:true, eyebrow:'Wat ik doe', kop:'Pique, in het kort.', sub:`Ik regel gesprekken met de beslissers die je normaal niet warm te pakken krijgt. Eén strategie, per regio uitgevoerd, op naam en met een reden. Soms met iets tastbaars, zoals ${esc(objLower)} voor jouw droomklanten.` },
    { side:'right', num:'01', kop:'Eén strategie, lokaal uitgevoerd', body:`Jij bepaalt de lijn centraal. Ik voer 'm per regio uit, met beslissers en een toon die daar passen.` },
    { side:'left', num:'02', kop:'Exclusief, nooit je concurrent', body:`Wat ik voor een regio vind, is van ${org}. Nooit gedeeld, nooit doorverkocht.` },
    { side:'right', num:'03', kop:'Bewijs één regio, dan uitrollen', body:`We beginnen met één regio. Werkt het, dan rollen we uit over de rest.` },
  ];

  const chapterHTML = C.map(c => {
    let inner;
    if(c.pivot){ inner = `${c.pre?`<div class="ch-eyebrow">${c.pre}</div>`:``}<p class="ch-pivot">${c.kop}</p>`; }
    else if(c.header){ inner = `<div class="ch-eyebrow">${c.eyebrow}</div><h2 class="ch-kop ch-head">${c.kop}</h2>${c.sub?`<p class="ch-sub">${c.sub}</p>`:''}`; }
    else { inner = `${c.eyebrow?`<div class="ch-eyebrow">${c.eyebrow}</div>`:''}${c.num?`<div class="ch-num">${c.num}</div>`:''}<h2 class="ch-kop">${c.kop}</h2><p class="ch-text">${c.body}</p>${c.bron?`<div class="ch-bron">Bron: ${c.bron}</div>`:''}${c.sign?`<div class="ch-sign">Simon, oprichter Pique</div>`:''}`; }
    return `    <section class="chapter ${c.side}${c.pivot?' pivot':''}${c.header?' phase':''}">
      <div class="ch-inner">
        <span class="ch-dot"></span>
        <div class="ch-body">${inner}</div>
      </div>
    </section>`;
  }).join('\n');

  return `<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pique voor ${org}</title>
<meta name="description" content="Een persoonlijk voorstel voor ${org}. Eén aanpak, per regio, exclusief voor jou.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#FBFAF8;--ink:#141C33;--ink2:rgba(20,28,51,.66);--ink3:rgba(20,28,51,.42);
  --navy:#0E1526;--amber:#C6893C;--ambers:#E0AC66;--line:rgba(20,28,51,.13);--white:#fff;
  --serif:'Playfair Display',Georgia,serif;--sans:'Inter',system-ui,sans-serif;--ease:cubic-bezier(.16,1,.3,1);
  --fs-h:clamp(1.9rem,3vw,2.7rem);--fs-body:clamp(1.02rem,1.25vw,1.16rem);
}
html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
body{font-family:var(--sans);background:var(--bg);color:var(--ink);overflow-x:hidden;line-height:1.6}
::selection{background:rgba(198,137,60,.2)}

/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;justify-content:space-between;padding:1.5rem clamp(1.5rem,4vw,3rem);transition:background .5s var(--ease),backdrop-filter .5s,padding .4s}
nav.solid{background:rgba(251,250,248,.72);backdrop-filter:blur(16px) saturate(1.4);padding-top:1rem;padding-bottom:1rem}
.logo{color:var(--white);text-decoration:none;display:flex;align-items:center;transition:color .5s}
.logo svg{height:26px;width:auto;display:block}
nav.solid .logo{color:var(--ink)}
.logo-dot{width:6px;height:6px;border-radius:50%;background:var(--amber)}
.nav-cta{font-size:.78rem;font-weight:500;letter-spacing:.01em;color:rgba(255,255,255,.7);text-decoration:none;padding:.5rem .95rem;border-radius:100px;border:1px solid rgba(255,255,255,.16);transition:all .4s}
.nav-cta:hover{color:#fff;border-color:rgba(255,255,255,.4)}
nav.solid .nav-cta{color:var(--ink2);border-color:var(--line)}
nav.solid .nav-cta:hover{color:var(--ink);border-color:var(--ink3)}

/* INTRO / HERO */
.intro{position:relative;background:var(--navy);color:#fff;padding:clamp(6rem,12vh,8rem) clamp(1.5rem,4vw,3rem) clamp(4rem,9vh,6.5rem);overflow:hidden}
.intro-grid{position:absolute;inset:0;background-image:radial-gradient(circle at 50% 0,rgba(198,137,60,.1),transparent 55%);pointer-events:none}
.intro-inner{position:relative;max-width:940px;margin:0 auto;display:flex;flex-direction:column;align-items:center;text-align:center}
.intro-eyebrow{font-size:.7rem;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:rgba(224,172,102,.9);margin-bottom:2.25rem;opacity:0;animation:up 1s var(--ease) .15s forwards}
.vframe{width:100%;max-width:820px;border-radius:20px;overflow:hidden;border:1px solid rgba(255,255,255,.1);box-shadow:0 50px 130px rgba(0,0,0,.5);background:#000;aspect-ratio:16/9;opacity:0;animation:up 1.1s var(--ease) .3s forwards}
.vframe video{width:100%;height:100%;display:block;object-fit:cover}
.vlabel{font-size:.78rem;font-weight:500;letter-spacing:.02em;color:rgba(255,255,255,.42);margin-top:1rem;opacity:0;animation:up 1s var(--ease) .42s forwards}
.intro-h1{font-family:var(--serif);font-weight:500;font-size:clamp(2rem,4.2vw,3.3rem);line-height:1.12;letter-spacing:-.02em;margin-top:clamp(2.5rem,5vh,3.5rem);max-width:20ch;opacity:0;animation:up 1.1s var(--ease) .5s forwards}
.intro-sub{color:rgba(255,255,255,.55);font-size:1.05rem;font-weight:300;margin-top:1.25rem;max-width:44ch;opacity:0;animation:up 1s var(--ease) .68s forwards}
.scrollcue{margin-top:clamp(2.5rem,6vh,4rem);display:flex;flex-direction:column;align-items:center;gap:.6rem;opacity:0;animation:up 1s var(--ease) .9s forwards}
.scrollcue span{font-size:.62rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.3)}
.scrollcue i{display:block;width:1px;height:38px;background:linear-gradient(rgba(224,172,102,.7),transparent);animation:cue 2.2s ease-in-out infinite;transform-origin:top}
@keyframes cue{0%,100%{transform:scaleY(.5);opacity:.4}50%{transform:scaleY(1);opacity:1}}
@keyframes up{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:translateY(0)}}

/* JOURNEY */
.journey{position:relative;max-width:1180px;margin:0 auto;padding:clamp(4rem,9vh,7rem) clamp(1.25rem,3vw,2rem) clamp(3rem,7vh,5rem)}
.journey-path{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:visible}
.jp-base{fill:none;stroke:var(--line);stroke-width:2;stroke-linecap:round;stroke-dasharray:.5 11;animation:march 40s linear infinite}
@keyframes march{to{stroke-dashoffset:-92}}
.jp-prog{fill:none;stroke:var(--amber);stroke-width:2.4;stroke-linecap:round;filter:drop-shadow(0 0 6px rgba(198,137,60,.4))}
.chapter{position:relative;z-index:1;display:flex;padding:clamp(5.5vh,8vh,10vh) 0}
.chapter.left{justify-content:flex-start}
.chapter.right{justify-content:flex-end}
.chapter.center{justify-content:center}
.ch-inner{position:relative;width:min(400px,40%)}
.chapter.center .ch-inner{width:min(560px,78%);text-align:center}
.chapter.center .ch-body{background:var(--bg);padding:1.5rem 1.75rem;border-radius:16px;position:relative;z-index:1}
.ch-dot{position:absolute;top:-1.7rem;width:13px;height:13px;border-radius:50%;background:var(--bg);border:2px solid var(--line);z-index:2;transition:border-color .5s var(--ease),background .5s var(--ease),box-shadow .5s var(--ease)}
.chapter.left .ch-dot{right:-1.7rem}
.chapter.right .ch-dot{left:-1.7rem}
.chapter.center .ch-dot{left:50%;transform:translateX(-50%)}
.chapter.reached .ch-dot{border-color:var(--amber);background:var(--amber);box-shadow:0 0 0 6px rgba(198,137,60,.12)}
.ch-body{opacity:0;transform:translateY(30px);filter:blur(5px);transition:opacity 1s var(--ease),transform 1s var(--ease),filter 1s var(--ease)}
.chapter.in .ch-body{opacity:1;transform:none;filter:blur(0)}
.ch-eyebrow{font-size:.68rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--amber);margin-bottom:1.1rem}
.ch-num{font-size:.72rem;font-weight:600;letter-spacing:.1em;color:var(--ink3);margin-bottom:.9rem;font-variant-numeric:tabular-nums}
.ch-kop{font-family:var(--serif);font-weight:500;font-size:var(--fs-h);line-height:1.16;letter-spacing:-.015em;color:var(--ink);margin-bottom:.9rem}
.ch-head{font-size:clamp(2.1rem,3.6vw,3rem);margin-bottom:0}
.ch-sub{font-size:1.06rem;color:var(--ink2);line-height:1.7;margin-top:1rem;font-weight:300;max-width:34ch;margin-left:auto;margin-right:auto}
.ch-text{font-size:var(--fs-body);color:var(--ink2);line-height:1.75;font-weight:400}
.ch-extra{font-size:.96rem;color:var(--ink3);line-height:1.65;margin-top:1.1rem;padding-top:1.1rem;border-top:1px solid var(--line)}
.ch-bron{font-size:.72rem;color:var(--ink3);margin-top:.95rem;letter-spacing:.02em}
.ch-sign{font-size:.85rem;color:var(--ink3);margin-top:1.4rem;font-weight:500}
.chapter.pivot{padding:clamp(8vh,12vh,15vh) 0}
.ch-pivot{font-family:var(--serif);font-weight:500;font-size:clamp(1.35rem,2.1vw,1.75rem);line-height:1.42;letter-spacing:-.015em;color:var(--ink)}
.chapter.pivot .ch-dot{width:16px;height:16px;top:-2.1rem}
.chapter.pivot .ch-inner{width:min(680px,88%)}
.chapter.phase{padding-top:clamp(7vh,10vh,13vh)}
.chapter.phase .ch-dot{width:15px;height:15px;top:-2.1rem}

/* FOUNDER */
.founder{max-width:760px;margin:0 auto;padding:clamp(3rem,6vh,5rem) clamp(1.5rem,4vw,2rem) clamp(4rem,8vh,6rem);display:grid;grid-template-columns:auto 1fr;gap:clamp(1.75rem,4vw,3rem);align-items:center}
.founder .fr{opacity:0;transform:translateY(24px);filter:blur(4px);transition:all 1s var(--ease)}
.founder.in .fr{opacity:1;transform:none;filter:blur(0)}
.fo-photo{width:clamp(120px,16vw,150px);height:clamp(120px,16vw,150px);border-radius:50%;object-fit:cover;box-shadow:0 20px 50px rgba(20,28,51,.15)}
.fo-eyebrow{font-size:.68rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--amber);margin-bottom:1rem}
.fo-text{font-family:var(--sans);font-weight:400;font-size:1.02rem;line-height:1.72;color:var(--ink2);margin-bottom:1.1rem}
.fo-text p{margin-bottom:.7rem}
.fo-text p:last-child{margin-bottom:0}
.fo-name{font-size:.92rem;color:var(--ink2)}.fo-name strong{color:var(--ink);font-weight:600}
@media(max-width:600px){.founder{grid-template-columns:1fr;text-align:center;justify-items:center}}

/* CTA */
.cta{background:var(--navy);color:#fff;padding:clamp(4.5rem,10vh,7rem) clamp(1.5rem,4vw,2rem)}
.cta-inner{max-width:720px;margin:0 auto;text-align:center}
.cta-eyebrow{font-size:.7rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:rgba(224,172,102,.9);margin-bottom:1.25rem}
.cta-h{font-family:var(--serif);font-weight:500;font-size:clamp(1.9rem,3.4vw,2.7rem);line-height:1.15;letter-spacing:-.02em}
.cta-sub{color:rgba(255,255,255,.6);font-size:1.05rem;font-weight:300;margin:1.25rem auto 0;max-width:48ch}
.cta-embed{margin-top:clamp(2.5rem,5vh,3.5rem);background:#fff;border-radius:20px;box-shadow:0 40px 100px rgba(0,0,0,.4);overflow:hidden;min-height:640px}
#cal-embed{width:100%;min-height:640px}
.reveal{opacity:0;transform:translateY(24px);transition:opacity 1s var(--ease),transform 1s var(--ease)}
.reveal.in{opacity:1;transform:none}

/* REVIEWS */
.reviews{max-width:1000px;margin:0 auto;padding:clamp(4.5rem,9vh,7rem) clamp(1.5rem,4vw,2rem)}
.rv-eyebrow{text-align:center;font-size:.7rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--amber);margin-bottom:2.75rem}
.rv-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
.rv{background:var(--white);border:1px solid var(--line);border-radius:18px;padding:2.25rem;transition:transform .5s var(--ease),box-shadow .5s var(--ease)}
.rv:hover{transform:translateY(-4px);box-shadow:0 26px 60px rgba(20,28,51,.08)}
.rv-stars{color:var(--amber);font-size:.9rem;letter-spacing:.1em;margin-bottom:1.25rem}
.rv-q{font-family:var(--serif);font-weight:400;font-size:1.25rem;line-height:1.45;color:var(--ink);margin-bottom:1.5rem;letter-spacing:-.01em}
.rv-who{font-size:.85rem;color:var(--ink2)}.rv-who strong{color:var(--ink);font-weight:600}
@media(max-width:680px){.rv-grid{grid-template-columns:1fr}}

.guarantee{padding:clamp(2rem,5vh,4rem) clamp(1.5rem,4vw,2rem) clamp(3rem,6vh,5rem)}
.gr-card{max-width:720px;margin:0 auto;background:var(--white);border:1px solid rgba(198,137,60,.3);border-radius:20px;padding:clamp(2rem,4vw,3rem);box-shadow:0 24px 60px rgba(20,28,51,.07);position:relative}
.gr-card::before{content:'';position:absolute;top:0;left:clamp(2rem,4vw,3rem);right:clamp(2rem,4vw,3rem);height:2px;background:linear-gradient(90deg,transparent,var(--amber),transparent)}
.gr-eyebrow{font-size:.7rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--amber);margin-bottom:1.1rem}
.gr-head{font-family:var(--serif);font-weight:500;font-size:clamp(1.5rem,2.6vw,2rem);line-height:1.22;letter-spacing:-.02em;color:var(--ink);margin-bottom:1rem}
.gr-text{font-size:1.02rem;color:var(--ink2);line-height:1.72;font-weight:400}
.gr-text sup{color:var(--amber);font-weight:700;font-size:.7em}
.gr-note{font-size:.82rem;color:var(--ink3);line-height:1.6;margin-top:1.25rem;padding-top:1rem;border-top:1px solid var(--line)}
.gr-star{color:var(--amber);font-weight:700}
/* FOOTER */
footer{border-top:1px solid var(--line);padding:2.75rem 2rem;text-align:center}
.ft-logo{color:var(--ink);display:inline-flex;align-items:center;margin-bottom:.8rem}
.ft-logo svg{height:24px;width:auto}
.ft-meta{font-size:.74rem;color:var(--ink3);line-height:1.9}
.ft-meta a{color:var(--ink2);text-decoration:none}
.ft-cta{display:inline-flex;align-items:center;gap:.5rem;font-size:.92rem;font-weight:600;color:var(--ink);text-decoration:none;border-bottom:2px solid var(--amber);padding-bottom:3px;margin-bottom:2.25rem;transition:gap .3s var(--ease)}
.ft-cta:hover{gap:.85rem}
.ft-cta svg{width:15px;height:15px;stroke:var(--amber);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}

@media(max-width:800px){
  .chapter{justify-content:flex-start;padding:5.5vh 0 5.5vh 2.4rem}
  .chapter.center{justify-content:flex-start}
  .ch-inner,.chapter.center .ch-inner{width:100%;text-align:left}
  .ch-sub{margin-left:0;margin-right:0}
  .ch-dot,.chapter.left .ch-dot,.chapter.right .ch-dot,.chapter.center .ch-dot{left:-2.4rem;right:auto;top:.3rem;transform:none}
}
</style>
</head>
<body>
<nav id="nav">
  <a href="#top" class="logo" aria-label="Pique">${LOGO}</a>
  <a href="#gesprek" class="nav-cta">Plan een gesprek</a>
</nav>

<header class="intro" id="top">
  <div class="intro-grid"></div>
  <div class="intro-inner">
    <div class="intro-eyebrow">Persoonlijk voor ${org}</div>
    <div class="vframe"><video src="video-9juli.mp4" controls preload="metadata" playsinline></video></div>
    <div class="vlabel">Kort woord vooraf van Simon</div>
    <h1 class="intro-h1">${p.voornaam?`Hé ${esc(p.voornaam)}, dit`:`Dit`} is waarom je mijn brief hebt ontvangen.</h1>
    <p class="intro-sub">Neem even de tijd. Ik neem je stap voor stap mee.</p>
    <div class="scrollcue"><span>Volg de lijn</span><i></i></div>
  </div>
</header>

<main class="journey" id="journey">
  <svg class="journey-path" id="jpath" preserveAspectRatio="none" aria-hidden="true">
    <path class="jp-base" id="jp-base"></path>
    <path class="jp-prog" id="jp-prog"></path>
  </svg>
${chapterHTML}
</main>

<section class="founder" id="founder">
  <img class="fo-photo fr" src="simon.png" alt="Simon Kempers, oprichter Pique">
  <div class="fr">
    <div class="fo-eyebrow">De persoon achter dit voorstel</div>
    <div class="fo-text">
      <p>Ik ben Simon. Ik begon Pique omdat de inbox van elke beslisser vol zit met dezelfde geautomatiseerde berichten. Daar val je niet meer tussen op.</p>
      <p>Dus doe ik het omgekeerd. Een klein aantal bedrijven, per stuk het onderzoek dat je hierboven zag, en een kaart plus pagina die echt alleen over hen gaan.</p>
      <p>Volume is het doel niet. Aandacht wel.</p>
    </div>
    <p class="fo-name"><strong>Simon Kempers</strong>, oprichter Pique</p>
  </div>
</section>

<section class="guarantee">
  <div class="gr-card reveal">
    <div class="gr-eyebrow">Onze garantie</div>
    <p class="gr-head">Break-even binnen drie maanden, of we werken kosteloos door.</p>
    <p class="gr-text">We rekenen met de gemiddelde waarde van één klant over de volledige looptijd. Heb je na drie maanden je investering nog niet terugverdiend, dan zetten we de samenwerking kosteloos voort tot je dat punt bereikt.<sup>*</sup></p>
    <p class="gr-note"><span class="gr-star">*</span> De garantie vervalt wanneer je al in de eerste maand break-even draait.</p>
  </div>
</section>

<section class="cta" id="gesprek">
  <div class="cta-inner">
    <div class="cta-eyebrow reveal">De volgende stap</div>
    <h2 class="cta-h reveal">Even kennismaken?</h2>
    <p class="cta-sub reveal">Dit wordt geen verkoopgesprek. Gewoon kijken of dit bij ${org} past, en of dat koude stuk warmer kan.</p>
    <div class="cta-embed reveal"><div id="cal-embed"></div></div>
  </div>
</section>

<section class="reviews">
  <div class="rv-eyebrow reveal">Wat klanten zeggen</div>
  <div class="rv-grid">
    <figure class="rv reveal"><div class="rv-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><blockquote class="rv-q">&ldquo;Had oprecht niet gedacht dat de service zo uitgebreid was.&rdquo;</blockquote><figcaption class="rv-who"><strong>David Meeusen</strong><br>Azora Studio</figcaption></figure>
    <figure class="rv reveal"><div class="rv-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><blockquote class="rv-q">&ldquo;Professioneel, afspraken nagekomen en goede communicatie.&rdquo;</blockquote><figcaption class="rv-who"><strong>Jeffrey Roelands</strong><br>Backbone Customer Service</figcaption></figure>
  </div>
</section>

<footer>
  <a href="https://www.pique.agency/regional-growth" class="ft-cta">Meer weten over Regional Growth <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
  <div class="ft-logo">${LOGO}</div>
  <div class="ft-meta">
    Onderdeel van TextInc B2B Copywriting &nbsp;&middot;&nbsp; <a href="mailto:info@pique.agency">info@pique.agency</a><br>
    &copy; 2026 Pique
  </div>
</footer>

<script>
const nav=document.getElementById('nav');
addEventListener('scroll',()=>nav.classList.toggle('solid',scrollY>window.innerHeight*.6),{passive:true});

const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.2});
document.querySelectorAll('.chapter,.founder,.reveal').forEach(el=>io.observe(el));

const journey=document.getElementById('journey'),svg=document.getElementById('jpath');
const base=document.getElementById('jp-base'),prog=document.getElementById('jp-prog');
const dots=[...journey.querySelectorAll('.ch-dot')];
let total=0;
function build(){
  const W=journey.clientWidth,H=journey.clientHeight,jr=journey.getBoundingClientRect();
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  const pts=dots.map(d=>{const r=d.getBoundingClientRect();return{x:r.left+r.width/2-jr.left,y:r.top+r.height/2-jr.top};});
  if(pts.length<2)return;
  let d='M '+pts[0].x.toFixed(1)+' '+pts[0].y.toFixed(1);
  for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i],my=((a.y+b.y)/2).toFixed(1);
    d+=' C '+a.x.toFixed(1)+' '+my+', '+b.x.toFixed(1)+' '+my+', '+b.x.toFixed(1)+' '+b.y.toFixed(1);}
  base.setAttribute('d',d);prog.setAttribute('d',d);
  total=prog.getTotalLength();prog.style.strokeDasharray=total;
  onScroll();
}
function onScroll(){
  if(!total)return;
  const jr=journey.getBoundingClientRect(),trig=window.innerHeight*.52;
  const frac=Math.max(0,Math.min(1,(trig-jr.top)/journey.clientHeight));
  prog.style.strokeDashoffset=total*(1-frac);
  dots.forEach(d=>{const r=d.getBoundingClientRect();d.parentElement.parentElement.classList.toggle('reached',r.top+r.height/2<trig);});
}
addEventListener('scroll',onScroll,{passive:true});
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(build,120);});
build();
addEventListener('load',build);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(build);
const v=document.querySelector('.vframe video');if(v)v.addEventListener('loadedmetadata',build);
setTimeout(build,400);setTimeout(build,1200);
if(window.ResizeObserver)new ResizeObserver(()=>build()).observe(journey);

(function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if(typeof namespace === "string"){cal.ns[namespace] = cal.ns[namespace] || api;p(cal.ns[namespace], ar);p(cal, ["initNamespace", namespace]);} else p(cal, ar); return;} p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");
Cal("init","belafspraak-pique",{origin:"https://cal.com"});
Cal.ns["belafspraak-pique"]("inline",{elementOrSelector:"#cal-embed",config:{layout:"month_view"},calLink:"simon-kempers/belafspraak-pique"});
</script>
</body>
</html>`;
}

const outDir = `${import.meta.dirname}/pique`;
mkdirSync(outDir,{recursive:true});
let n=0;const slugs=new Set();
for(const p of PROSPECTS){
  if(slugs.has(p.slug)) throw new Error('Dubbele slug: '+p.slug);
  slugs.add(p.slug);
  writeFileSync(`${outDir}/${p.slug}.html`, render(p));
  n++;
}
console.log(`Gegenereerd: ${n} LP's in ${outDir}`);
