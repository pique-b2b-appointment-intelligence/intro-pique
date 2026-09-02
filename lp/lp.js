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
     window.PQ_CAL          = 'simon-kempers/belafspraak-pique';
     window.PQ_VIDEO        = 'simon-staand.mp4';
     window.PQ_POSTER       = 'simon-staand-poster.jpg';
   ============================================================ */
/* ══ 0. SIGNAAL. Elke stap die de prospect zet is een belsignaal voor Timon.
   Wire dit op /api/t en Belcockpit weet wie tot het eind las zonder te boeken. ══ */
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
var pqGezien = {};
function pqTrack(stap, extra){
  if (pqGezien[stap]) return; pqGezien[stap] = 1;
  var body = JSON.stringify({slug:PQ_SLUG, stap:stap, extra:extra||null, t:Date.now()});
  if (window.PQ_TRACK_URL && navigator.sendBeacon) navigator.sendBeacon(window.PQ_TRACK_URL, body);
  else if (console && console.debug) console.debug('[pique]', stap, extra||'');
}

/* ══ 2. VIDEO-OVERLAY. Video is een aanbod, geen blokkade. ══ */
window.pqVideo = function(){
  pqTrack('video-gestart');
  var o = document.createElement('div');
  o.style.cssText = 'position:fixed;inset:0;z-index:300;background:rgba(10,15,26,.88);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;transition:opacity .35s ease';
  o.innerHTML = '<video playsinline controls autoplay src="' + (window.PQ_VIDEO || 'video.mp4') + '" poster="' + (window.PQ_POSTER || 'video-poster.jpg') + '" style="width:min(330px,80vw);max-height:88vh;border-radius:20px;box-shadow:0 40px 90px rgba(0,0,0,.6);background:#0c1116"></video>' +
    '<button aria-label="Sluiten" style="position:absolute;top:18px;right:18px;width:38px;height:38px;border-radius:50%;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff;font-size:1.2rem;cursor:pointer">&times;</button>';
  document.body.appendChild(o);
  requestAnimationFrame(function(){ o.style.opacity = '1'; });
  function dicht(){ o.style.opacity='0'; setTimeout(function(){ o.remove(); }, 350); }
  o.querySelector('button').addEventListener('click', dicht);
  o.addEventListener('click', function(e){ if (e.target === o) dicht(); });
  o.querySelector('video').addEventListener('ended', function(){ pqTrack('video-uitgekeken'); dicht(); });
};
(function(){ var v = document.getElementById('vrow'); if (v) v.addEventListener('click', window.pqVideo); })();

/* ══ 3. REVEALS + JOURNEYLIJN ══ */
var io = new IntersectionObserver(function(es){
  es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
}, {threshold:.18});
document.querySelectorAll('.chapter,.founder,.reveal,.ask,.toon').forEach(function(el){ io.observe(el); });

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
  var na = pivot.getBoundingClientRect().bottom < innerHeight * .5;
  if (na && window.pqWarmCal) window.pqWarmCal();
  if (dockWeg || document.getElementById('sheet').classList.contains('open')) { dock.classList.remove('up'); return; }
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
  requestAnimationFrame(function(){ bijScroll(); railUpdate(); dockUpdate(); diepteUpdate(); tikt = false; });
}, {passive:true});
addEventListener('scroll', function(){
  document.getElementById('nav').classList.toggle('solid', scrollY > innerHeight * .6);
}, {passive:true});

var rt; addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(bouw, 120); });
bouw(); addEventListener('load', bouw);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(bouw);
setTimeout(bouw, 400); setTimeout(bouw, 1200);
if (window.ResizeObserver) paden.forEach(function(p){ new ResizeObserver(bouw).observe(p.wrap); });

document.getElementById('askread').addEventListener('click', function(){
  pqTrack('leest-eerst-voorstel');
  document.getElementById('s4').scrollIntoView({behavior:'smooth', block:'start'});
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

    var lading = JSON.stringify({
      naam: naam, tel: tel, wanneer: gekozen,
      bedrijf: window.PQ_BEDRIJF, slug: PQ_SLUG,
      klant: window.PQ_KLANT, campagne: window.PQ_CAMPAGNE
    });

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
