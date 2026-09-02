/* ============================================================
   PIQUE LP v2 — gedrag
   Journeylijn, voortgangsrail, dock, boeksheet, videolaag en de
   leesdiepte-signalen. Onderaan de <body> insluiten, na lp-intro.js.

   Pagina-instellingen (optioneel, in een <script> ervoor):
     window.PQ_TRACK_URL    = '/api/t';       // leesdiepte en klikken
     window.PQ_TERUGBEL_URL = '<apps script>';// terugbelverzoeken
     window.PQ_BEDRIJF      = 'Odido Zakelijk';
     window.PQ_KLANT        = 'pique';        // sleutel uit KLANTEN in Terugbelverzoek.gs
     window.PQ_CAMPAGNE     = 'grote-merken'; // vrije naam, om later op te filteren
     window.PQ_SCHRIJF      = false;          // briefje halverwege uitzetten (staat standaard aan)
     window.PQ_DOCK_NA      = 0.75;           // deel van de pagina waarna de dock komt
     window.PQ_CAL          = 'simon-kempers/belafspraak-pique';
     window.PQ_VIDEO        = 'simon-staand.mp4';
     window.PQ_POSTER       = 'simon-staand-poster.jpg';
   ============================================================ */
/* ══ 0. SIGNAAL. Elke stap die de prospect zet is een belsignaal voor Timon.
   /api/t vangt het profiel op en Belcockpit weet wie tot het eind las zonder te boeken. ══ */
var PQ_SLUG = location.pathname.split('/').pop().replace('.html','');
/* Endpoint voor terugbelverzoeken. Zie Dashboard/Terugbelverzoek.gs voor het opzetten.
   Zolang dit leeg is, laat het formulier de bevestiging zien en logt het naar de console. */
window.PQ_TERUGBEL_URL = window.PQ_TERUGBEL_URL || '';
window.PQ_BEDRIJF  = window.PQ_BEDRIJF  || '';
/* Zonder klant komt het verzoek bij Pique terecht. Dat is de veilige terugval:
   liever bij de verkeerde persoon dan nergens. Zet hem dus altijd op een
   klantpagina, anders belt Murphy niet en jij ook niet. */
window.PQ_KLANT    = window.PQ_KLANT    || 'pique';
window.PQ_CAMPAGNE = window.PQ_CAMPAGNE || '';
/* Meten staat aan tenzij een pagina hem expliciet op '' zet. Het endpoint staat op
   hetzelfde domein als de pagina, dus geen extra script van derden en geen cookie. */
window.PQ_TRACK_URL = (typeof window.PQ_TRACK_URL === 'string') ? window.PQ_TRACK_URL : '/api/t';

/* Eén bezoek levert één event op, geen twaalf. De ringbuffer in Belcockpit is 4.000 events
   groot; twaalf losse stappen per scan vaagt de historie binnen twee batches weg. Daarom
   telt de pagina alles zelf op en stuurt hij een profiel: hoe lang, hoe diep, waar bleef
   hij hangen. Meerdere flushes van hetzelfde bezoek overschrijven elkaar op de sessie-id.

   Alleen actieve tijd telt. Een tabblad dat een uur op de achtergrond staat is geen
   aandacht, en zonder deze correctie is elke vergeten tab een tophit op het belbord. */
var pqSessie = String(Date.now().toString(36) + Math.random().toString(36).slice(2, 8));
var pqGezien = {};      // stap -> 1, zodat elke stap maar één keer telt
var pqStappen = [];     // in de volgorde waarin het gebeurde
var pqSecties = {};     // blok -> seconden werkelijk in beeld
var pqActief  = 0;      // seconden met de pagina zichtbaar
var pqDiep    = 0;      // hoogste scrolldiepte in procenten
var pqVideoSec = 0;     // verst bekeken punt in de video
var pqVorige  = '';     // vingerafdruk van de vorige flush, tegen dubbel verkeer

/* Welke blokken we los volgen. Dezelfde ids als de journeylijn verderop. */
var PQ_BLOKKEN = [['s2','bevinding-1'],['s3','kantelpunt'],['ask','belaanbod'],['s4','voorstel'],['gesprek','cta']];

function pqTrack(stap, extra){
  if (pqGezien[stap]) return; pqGezien[stap] = 1;
  pqStappen.push(extra ? stap + ':' + String(extra).slice(0, 24) : stap);
  /* Deze drie mogen niet wachten op het verlaten van de pagina: daarna belt of mailt
     er iemand, en dan moet het signaal er al zijn. */
  if (stap === 'terugbelverzoek' || stap === 'afspraak-geboekt' || stap === 'video-uitgekeken') pqFlush(stap);
}

/* Eén tik per seconde, alleen als de pagina echt in beeld staat. Een blok telt mee zolang
   het het midden van het scherm raakt; dat is dichter bij lezen dan 'is een pixel zichtbaar'. */
setInterval(function(){
  if (document.hidden) return;
  pqActief++;
  PQ_BLOKKEN.forEach(function(b){
    var el = document.getElementById(b[0]); if (!el) return;
    var r = el.getBoundingClientRect();
    if (r.top < innerHeight * 0.75 && r.bottom > innerHeight * 0.25) pqSecties[b[1]] = (pqSecties[b[1]] || 0) + 1;
  });
}, 1000);

function pqDiepteMeten(){
  var h = document.body.scrollHeight - innerHeight;
  var pct = h > 0 ? Math.round((scrollY / h) * 100) : 100;
  if (pct > pqDiep) pqDiep = Math.min(100, pct);
}

function pqFlush(reden){
  /* De vingerafdruk laat tijd en reden bewust weg: anders stuurt elke trigger opnieuw
     hetzelfde profiel en telt Belcockpit bezoeken die er niet waren. */
  var vinger = pqActief + '|' + pqDiep + '|' + pqStappen.join(',') + '|' + JSON.stringify(pqSecties);
  if (vinger === pqVorige) return;
  pqVorige = vinger;
  var lading = JSON.stringify({
    v: 2, slug: PQ_SLUG, sessie: pqSessie, reden: reden || '',
    sec: pqActief, diep: pqDiep, secties: pqSecties, stappen: pqStappen,
    video: Math.round(pqVideoSec), bedrijf: window.PQ_BEDRIJF,
    klant: window.PQ_KLANT, campagne: window.PQ_CAMPAGNE, t: Date.now()
  });
  if (!window.PQ_TRACK_URL) { if (console && console.debug) console.debug('[pique] bezoek', lading); return; }
  var blob = new Blob([lading], {type: 'text/plain;charset=UTF-8'});
  if (navigator.sendBeacon && navigator.sendBeacon(window.PQ_TRACK_URL, blob)) return;
  fetch(window.PQ_TRACK_URL, {method: 'POST', body: lading, keepalive: true,
    headers: {'Content-Type': 'text/plain;charset=utf-8'}}).catch(function(){});
}

/* Een tik bij binnenkomst en daarna een hartslag, zodat het bord kan laten zien wie er
   nu op zijn pagina zit en niet pas na afloop. Alle tikken dragen dezelfde sessie-id en
   smelten server-side samen tot één bezoek, dus dit kost geen extra opslag.
   De hartslag staat stil zolang het tabblad op de achtergrond staat, want dan telt de
   tijd ook niet mee. Een tabblad dat hard wordt afgesloten stuurt niets meer; door de
   hartslag ben je dan hooguit een halve minuut kwijt in plaats van het hele bezoek. */
setTimeout(function(){ pqFlush('binnen'); }, 3000);
setInterval(function(){ if (!document.hidden) pqFlush('bezig'); }, 30000);
addEventListener('visibilitychange', function(){ pqFlush(document.hidden ? 'weg' : 'terug'); });
addEventListener('pagehide', function(){ pqFlush('einde'); });

/* ══ 2. VIDEO-OVERLAY. Video is een aanbod, geen blokkade. ══
   De kleuren komen uit tokens, net als in lp.css. Ze stonden hier hard in het navy
   van Pique, waardoor de overlay op een OGG-pagina blauw opende terwijl de rest groen
   is. Een controle op vaste kleuren moet dus ook langs dit bestand. */
window.pqVideo = function(){
  pqTrack('video-gestart');
  var o = document.createElement('div');
  o.style.cssText = 'position:fixed;inset:0;z-index:300;background:rgba(var(--dieper-rgb),.88);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;transition:opacity .35s ease';
  o.innerHTML = '<video playsinline controls autoplay src="' + (window.PQ_VIDEO || 'video.mp4') + '" poster="' + (window.PQ_POSTER || 'video-poster.jpg') + '" style="width:min(330px,80vw);max-height:88vh;border-radius:20px;box-shadow:0 40px 90px rgba(0,0,0,.6);background:var(--video-bg)"></video>' +
    '<button aria-label="Sluiten" style="position:absolute;top:18px;right:18px;width:38px;height:38px;border-radius:50%;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff;font-size:1.2rem;cursor:pointer">&times;</button>';
  document.body.appendChild(o);
  requestAnimationFrame(function(){ o.style.opacity = '1'; });
  function dicht(){ o.style.opacity='0'; setTimeout(function(){ o.remove(); }, 350); }
  o.querySelector('button').addEventListener('click', dicht);
  o.addEventListener('click', function(e){ if (e.target === o) dicht(); });
  var vid = o.querySelector('video');
  /* Hoe ver iemand keek zegt meer dan of hij op play drukte. Alleen het verste punt,
     want terugspoelen mag de teller niet verlagen. */
  vid.addEventListener('timeupdate', function(){ if (vid.currentTime > pqVideoSec) pqVideoSec = vid.currentTime; });
  vid.addEventListener('ended', function(){ pqTrack('video-uitgekeken'); dicht(); });
};
(function(){ var v = document.getElementById('vrow'); if (v) v.addEventListener('click', window.pqVideo); })();

/* ══ 3. REVEALS + JOURNEYLIJN ══ */
var io = new IntersectionObserver(function(es){
  es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
}, {threshold:.18});
/* .belofte hoorde hier niet bij, waardoor het garantieblok op de dossierpagina's
   nooit zichtbaar werd: de opmaak zet het op opacity 0 tot deze waarnemer de klasse
   'in' toevoegt. Een blok dat niet in deze lijst staat, blijft onzichtbaar. */
document.querySelectorAll('.chapter,.founder,.reveal,.ask,.toon,.belofte').forEach(function(el){ io.observe(el); });

var paden = [['journey','jp-base','jp-prog'],['journey2','jp-base2','jp-prog2']].map(function(x){
  var wrap = document.getElementById(x[0]);
  return {wrap:wrap, svg:wrap.querySelector('.jpath'), base:document.getElementById(x[1]), prog:document.getElementById(x[2]),
          dots:[].slice.call(wrap.querySelectorAll('.ch-dot')), total:0};
});
function bouw(){
  paden.forEach(function(p){
    var W = p.wrap.clientWidth, H = p.wrap.clientHeight, jr = p.wrap.getBoundingClientRect();
    p.svg.setAttribute('viewBox','0 0 '+W+' '+H);
    var pts = p.dots.map(function(d){ var r = d.getBoundingClientRect(); return {x:r.left+r.width/2-jr.left, y:r.top+r.height/2-jr.top}; });
    if (pts.length < 2) return;
    var dd = 'M '+pts[0].x.toFixed(1)+' '+pts[0].y.toFixed(1);
    for (var i=1;i<pts.length;i++){
      var a = pts[i-1], c = pts[i], my = ((a.y+c.y)/2).toFixed(1);
      dd += ' C '+a.x.toFixed(1)+' '+my+', '+c.x.toFixed(1)+' '+my+', '+c.x.toFixed(1)+' '+c.y.toFixed(1);
    }
    p.base.setAttribute('d', dd); p.prog.setAttribute('d', dd);
    p.total = p.prog.getTotalLength(); p.prog.style.strokeDasharray = p.total;
  });
  bijScroll();
}
function bijScroll(){
  var trig = innerHeight * .52;
  paden.forEach(function(p){
    if (!p.total) return;
    var jr = p.wrap.getBoundingClientRect();
    var frac = Math.max(0, Math.min(1, (trig - jr.top) / p.wrap.clientHeight));
    p.prog.style.strokeDashoffset = p.total * (1 - frac);
    p.dots.forEach(function(d){
      var r = d.getBoundingClientRect();
      d.closest('.chapter').classList.toggle('reached', r.top + r.height/2 < trig);
    });
  });
}

/* ══ 3b. HET KANTELPUNT ALS GESCHREVEN BRIEFJE ══
   Halverwege komt de kaart terug. Het donkere blok wordt papier, de zin komt
   in hetzelfde handschrift, en hij wordt geschreven terwijl je kijkt. Sneller
   dan bij binnenkomst, want daar had je nog niets gelezen en hier wil je door. */
(function(){
  if (window.PQ_SCHRIJF === false) return;
  var blok = document.querySelector('.chapter.pivot');
  var zin = blok && blok.querySelector('.ch-pivot');
  if (!zin) return;
  blok.classList.add('brief');

  /* De tijdlijn hoort niet ín een handgeschreven briefje. Die gaat eronder,
     buiten het papier, en krijgt daar de lichte kleuren. */
  var tl = blok.querySelector('.tl');
  if (tl) { tl.classList.add('los'); blok.querySelector('.ch-inner').appendChild(tl); }

  var traag = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (traag) { blok.classList.add('klaar'); return; }

  /* Elk teken een eigen span, maar woorden in een nowrap-wikkel. Zonder die
     wikkel mag de browser midden in een woord afbreken. Alle spans staan er
     meteen in, alleen nog onzichtbaar, zodat het papier vanaf het begin zijn
     eindhoogte heeft en er niets verspringt tijdens het schrijven. */
  var tekst = zin.textContent;
  zin.textContent = '';
  var tekens = [], woord = null;
  for (var i = 0; i < tekst.length; i++) {
    var c = tekst[i];
    var sp = document.createElement('span');
    sp.className = 'pc'; sp.textContent = c;
    if (c === ' ' || c === '\n') { woord = null; zin.appendChild(sp); }
    else {
      if (!woord) { woord = document.createElement('span'); woord.className = 'pw'; zin.appendChild(woord); }
      woord.appendChild(sp);
    }
    tekens.push(sp);
  }

  var tempo = window.PQ_SCHRIJF_TEMPO || 13;   // ms per teken; de kaart doet 30
  var bezig = false;

  function schrijf(){
    var i = 0;
    (function stap(){
      /* Per beurt een paar tekens, anders zet je honderden timers aan. */
      var eind = Math.min(tekens.length, i + Math.max(1, Math.round(16 / tempo)));
      for (; i < eind; i++) tekens[i].classList.add('aan');
      if (i < tekens.length) setTimeout(stap, tempo);
      else setTimeout(function(){ blok.classList.add('klaar'); pqTrack('kantelpunt-gelezen'); }, 300);
    })();
  }
  function alles(){
    tekens.forEach(function(t){ t.classList.add('aan'); });
    blok.classList.add('klaar');
  }

  /* Geen drempel op het blok zelf: met de tijdlijn eronder is het kantelpunt op
     een laptop hoger dan het venster, en dan wordt een percentage nooit gehaald.
     Een marge die alleen de middenband van het scherm overhoudt werkt bij elke
     hoogte, want daar komt het blok altijd doorheen. */
  var io2 = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if (!e.isIntersecting || bezig) return;
      bezig = true; io2.disconnect(); schrijf();
    });
  }, {threshold:0, rootMargin:'-30% 0px -30% 0px'});
  io2.observe(blok);

  /* Vangnet. Scrollt iemand er in een ruk voorbij, of levert de waarnemer om
     wat voor reden dan ook niets, dan blijft het papier anders leeg. */
  addEventListener('scroll', function vangnet(){
    if (bezig) { removeEventListener('scroll', vangnet); return; }
    if (blok.getBoundingClientRect().bottom < 0) {
      bezig = true; io2.disconnect();
      removeEventListener('scroll', vangnet);
      alles();
    }
  }, {passive:true});
})();

/* ══ 4. RAIL + VOORTGANGSBALK. Weten waar je bent halveert het wegklikken. ══ */
var rail = document.getElementById('rail'), railLinks = [].slice.call(rail.querySelectorAll('a'));
var mbar = document.getElementById('mbar');
var doelen = railLinks.map(function(a){ return document.querySelector(a.getAttribute('href')); });
function railUpdate(){
  var y = scrollY + innerHeight * .4, act = -1;
  doelen.forEach(function(d, i){ if (d && d.getBoundingClientRect().top + scrollY <= y) act = i; });
  railLinks.forEach(function(a, i){ a.classList.toggle('act', i === act); });
  rail.classList.toggle('on', scrollY > innerHeight * .7);
  var h = document.documentElement.scrollHeight - innerHeight;
  mbar.style.width = (h > 0 ? Math.min(100, scrollY / h * 100) : 0) + '%';
}

/* ══ 5. DOCK. Pas ná het kantelpunt, dus verdiend en niet opdringerig. ══ */
var dock = document.getElementById('dock'), pivot = document.getElementById('s3'), cta = document.getElementById('gesprek');
var dockWeg = false;
document.getElementById('dockx').addEventListener('click', function(){ dockWeg = true; dock.classList.remove('up'); pqTrack('dock-weggeklikt'); });
function dockUpdate(){
  /* De agenda alvast warm draaien mag zodra het kantelpunt voorbij is, want dat
     kost de bezoeker niets. De dock zelf komt later: op het kantelpunt heeft hij
     de vraag net gelezen en is een balk in beeld opdringerig. */
  if (pivot.getBoundingClientRect().bottom < innerHeight * .5 && window.pqWarmCal) window.pqWarmCal();
  if (dockWeg || document.getElementById('sheet').classList.contains('open')) { dock.classList.remove('up'); return; }
  /* Met PQ_DOCK_NA komt de dock op een deel van de paginahoogte. Zonder,
     op het oude moment: zodra het kantelpunt voorbij is. Zolang niet alle
     batches zijn nagelopen staan die twee naast elkaar. */
  var hoogte = document.documentElement.scrollHeight - innerHeight;
  var deel = hoogte > 0 ? scrollY / hoogte : 0;
  var na = deel >= (typeof window.PQ_DOCK_NA === 'number' ? window.PQ_DOCK_NA : 0.75);
  var bij = cta.getBoundingClientRect().top < innerHeight * .85;
  var aan = na && !bij;
  dock.classList.toggle('up', aan);
  document.documentElement.style.setProperty('--dock', aan ? '4.5rem' : '0px');
  if (aan) pqTrack('dock-getoond');
}

/* ══ 6. LEESDIEPTE ══ */
var diepte = [['s2','bevinding-1'],['s3','kantelpunt'],['ask','belaanbod-gezien'],['s4','voorstel'],['gesprek','cta-gezien']];
function diepteUpdate(){
  diepte.forEach(function(d){
    var el = document.getElementById(d[0]);
    if (el && el.getBoundingClientRect().top < innerHeight * .7) pqTrack(d[1]);
  });
}

var tikt = false;
addEventListener('scroll', function(){
  if (tikt) return; tikt = true;
  requestAnimationFrame(function(){ bijScroll(); railUpdate(); dockUpdate(); diepteUpdate(); pqDiepteMeten(); tikt = false; });
}, {passive:true});
addEventListener('scroll', function(){
  document.getElementById('nav').classList.toggle('solid', scrollY > innerHeight * .6);
}, {passive:true});

var rt; addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(bouw, 120); });
bouw(); addEventListener('load', bouw);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(bouw);
setTimeout(bouw, 400); setTimeout(bouw, 1200);
if (window.ResizeObserver) paden.forEach(function(p){ new ResizeObserver(bouw).observe(p.wrap); });

/* Deze knop staat niet op elke pagina. Zonder deze controle gooit de regel een fout
   op een pagina die hem mist, en dan draait alles hieronder niet meer: het belscherm,
   de agenda en het terugbelformulier. */
var askread = document.getElementById('askread');
if (askread) askread.addEventListener('click', function(){
  pqTrack('leest-eerst-voorstel');
  var doel = document.getElementById('s4');
  if (doel) doel.scrollIntoView({behavior:'smooth', block:'start'});
});

/* ══ 7. SHEET. Cal.com laadt pas als iemand hem opent, niet bij elke scan. ══ */
(function(){
  var sheet = document.getElementById('sheet'), calGeladen = false;
  function tab(naam){
    sheet.querySelectorAll('.sheet-tabs button').forEach(function(b){ b.classList.toggle('on', b.dataset.tab === naam); });
    document.getElementById('pane-plan').classList.toggle('on', naam === 'plan');
    document.getElementById('pane-bel').classList.toggle('on', naam === 'bel');
    if (naam === 'plan') laadCal();
  }
  function laadCal(){
    if (calGeladen) return; calGeladen = true;
    (function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d2 = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d2.head.appendChild(d2.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");
    Cal("init","belafspraak-pique",{origin:"https://cal.com"});
    Cal.ns["belafspraak-pique"]("inline",{elementOrSelector:"#cal-embed",config:{layout:"month_view"},calLink:(window.PQ_CAL || "simon-kempers/belafspraak-pique")});
    Cal.ns["belafspraak-pique"]("on",{action:"bookingSuccessful",callback:function(){ pqTrack('afspraak-geboekt'); }});
    Cal.ns["belafspraak-pique"]("on",{action:"linkReady",callback:klaarMetLaden});
    /* Vangnet: reageert cal niet, dan gaat het skelet na 12s toch weg. */
    setTimeout(klaarMetLaden, 12000);
  }
  function klaarMetLaden(){
    var sk = document.getElementById('calskel');
    if (sk) sk.classList.add('weg');
  }
  /* De agenda begint met laden zodra iemand het kantelpunt passeert, dus
     ruim voordat hij op de knop kan drukken. Openen voelt daardoor direct.
     De sheet staat op dat moment nog buiten beeld, maar heeft wel afmetingen,
     dus cal kan gewoon renderen. */
  window.pqWarmCal = function(){
    if (calGeladen) return;
    var doe = function(){ laadCal(); };
    if (window.requestIdleCallback) requestIdleCallback(doe, {timeout:1500}); else setTimeout(doe, 400);
  };
  function open(welke){
    sheet.classList.add('open'); sheet.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
    tab(welke || 'plan'); dockUpdate();
    pqTrack('sheet-geopend', welke || 'plan');
  }
  function dicht(){
    sheet.classList.remove('open'); sheet.setAttribute('aria-hidden','true');
    document.body.style.overflow = ''; dockUpdate();
  }
  /* Ook bereikbaar voor knoppen die pas ná het laden ontstaan, zoals de bevestiging
     onder een verzonden formulier. */
  window.pqOpenSheet = open;
  document.querySelectorAll('[data-open="sheet"]').forEach(function(b){
    b.addEventListener('click', function(){ open(b.dataset.tab); });
  });
  sheet.querySelectorAll('[data-close]').forEach(function(b){ b.addEventListener('click', dicht); });
  sheet.querySelectorAll('.sheet-tabs button').forEach(function(b){ b.addEventListener('click', function(){ tab(b.dataset.tab); }); });
  addEventListener('keydown', function(e){ if (e.key === 'Escape' && sheet.classList.contains('open')) dicht(); });

  var gekozen = '';
  document.getElementById('slots').addEventListener('click', function(e){
    var b = e.target.closest('button'); if (!b) return;
    [].slice.call(this.children).forEach(function(x){ x.classList.remove('on'); });
    b.classList.add('on'); gekozen = b.dataset.v;
  });
  document.getElementById('belform').addEventListener('submit', function(e){
    e.preventDefault();
    var naam = document.getElementById('bn').value.trim();
    var tel  = document.getElementById('bt').value.trim();
    if (!tel) return;
    pqTrack('terugbelverzoek', tel);

    /* PQ_EXTRA vult een pagina zelf, bijvoorbeeld met de antwoorden uit een intake.
       Die gaan pas mee op het moment dat iemand zelf zijn nummer achterlaat. */
    var lading = JSON.stringify(Object.assign({
      naam: naam, tel: tel, wanneer: gekozen,
      bedrijf: window.PQ_BEDRIJF, slug: PQ_SLUG,
      klant: window.PQ_KLANT, campagne: window.PQ_CAMPAGNE
    }, window.PQ_EXTRA || {}));

    /* Bewust text/plain: daarmee is het een simpele request en vraagt de browser
       geen preflight, wat een Apps Script-webapp toch niet zou beantwoorden.
       Lukt fetch niet, dan gaat het alsnog met een beacon de deur uit. */
    var url = window.PQ_TERUGBEL_URL;
    if (url) {
      fetch(url, {
        method: 'POST', body: lading, keepalive: true,
        headers: {'Content-Type': 'text/plain;charset=utf-8'}
      }).catch(function(){
        if (navigator.sendBeacon) navigator.sendBeacon(url, new Blob([lading], {type:'text/plain'}));
      });
    } else if (console && console.debug) {
      console.debug('[pique] terugbelverzoek (nog geen endpoint ingesteld)', lading);
    }

    var voornaam = naam ? naam.split(' ')[0] : 'top';
    document.getElementById('pane-bel').innerHTML =
      '<div class="sheet-ok"><div class="hand">Genoteerd, ' + voornaam + '.</div>' +
      '<p>Ik bel je ' + (gekozen ? gekozen.toLowerCase() : 'zo snel als het schikt') + ' op ' + tel + '.</p>' +
      '<p style="margin-top:.9rem;font-size:.8rem;color:var(--ink3)">Komt het toch niet uit? Mail me op ' +
      '<a href="mailto:info@pique.agency" style="color:var(--amber)">info@pique.agency</a>.</p></div>';
  });
})();
