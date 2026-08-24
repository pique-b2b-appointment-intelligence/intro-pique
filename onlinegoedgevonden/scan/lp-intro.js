/* ============================================================
   PIQUE LP v2 — de kaartlaag na de scan
   De kaart die ze net vasthielden schrijft zichzelf en vliegt daarna
   naar zijn plek in de hero. Dat voorwerp is de hele brug tussen het
   ding op hun bureau en deze pagina, dus die laag hoort er altijd op.

   Per pagina, in de <head>, boven dit bestand:

     <script>window.PIQUE_INTRO = {
       voornaam: "Bram",            // laat weg als je hem niet zeker weet
       bedrijf:  "Alva Charging",
       ctaSub:   "Video van Murphy \u00b7 1 min 20",
       merk:     false              // false op een klantpagina
     };<\/script>
     <script src="lp-intro.js"><\/script>

   Eigen regels kan met  regels: ["Hoi {voornaam}.", "Ik zag iets bij *{bedrijf}*."]
   Tekst tussen sterretjes wordt accentkleur, een | forceert een regelafbreking.
   Zonder JS verschijnt de laag niet, dus de pagina blijft altijd bereikbaar.
   De vormgeving zit in lp.css onder 'INTRO-LAAG'.
   ============================================================ */
/* ══ 1. INTRO-LAAG. De kaart verdwijnt niet, hij landt in de pagina. ══ */
(function(){
  /* ?nointro slaat de kaartlaag over. Handig voor QC en screenshots. */
  /* ?nointro slaat de kaartlaag over. Voor QC en screenshots.
     Dit bestand hangt in de <head>, dus de hero bestaat hier nog niet. */
  if (location.search.indexOf('nointro') > -1) {
    var toon = function () {
      var sc = document.getElementById('slotcard');
      if (sc) sc.classList.add('show');
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', toon);
    else toon();
    return;
  }
  var cfg = window.PIQUE_INTRO;
  if (!cfg) return;
  var traag = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bedrijf = cfg.bedrijf || 'je bedrijf';
  /* Zonder voornaam vervalt de aanhef. Een kaart die '[Voornaam]'
     uitschrijft is meteen ontmaskerd. */
  var standaard = cfg.voornaam ? [
    'Hoi {voornaam}.',
    'Deze kaart lag niet toevallig|op je bureau.',
    'Ik keek een tijd naar {bedrijf}.',
    '*Wil je weten wat ik zag?*'
  ] : [
    'Deze kaart lag niet toevallig|op je bureau.',
    'Ik keek een tijd naar {bedrijf}.',
    '*Wil je weten wat ik zag?*'
  ];
  var regels = (cfg.regels && cfg.regels.length ? cfg.regels : standaard).map(function (r) {
    return r.replace(/\{voornaam\}/g, cfg.voornaam || '').replace(/\{bedrijf\}/g, bedrijf);
  });
  var cta    = cfg.cta    || 'Ja, laat maar zien';
  var ctaSub = cfg.ctaSub || 'Video van Simon &middot; 1 min 20';
  var lezen  = cfg.lezen  || 'Ik lees liever eerst';
  var label  = cfg.label  || 'Persoonlijk';
  var merk   = cfg.merk !== false;
  var tempo  = cfg.tempo || 30;
  var pauze  = cfg.pauze || 340;
  /* Op een kaart die rondgaat op kantoor hoort iedereen de laag te zien.
     Alleen met eenmalig:true slaat hij een tweede bezoek over. */
  var KEY = 'pq-intro:' + location.pathname;
  var eenmalig = cfg.eenmalig === true;
  try { if (eenmalig && localStorage.getItem(KEY)) return; } catch (e) {}
  var nl = document.querySelector('nav .logo');
  var LOGO = nl ? nl.innerHTML : '';
  document.documentElement.className += ' pq-on';

  /* Is er geen opname, dan is één knop genoeg. Anders beloven we
     een video die er niet is. Zet cfg.video op false op zo'n pagina. */
  var heeftVideo = cfg.video !== false && !!window.PQ_VIDEO;
  var el = document.createElement('div');
  el.id = 'pq';
  el.innerHTML =
    '<div class="pq-glow"></div><div class="pq-stage">' +
      '<div class="pq-card" id="pqcard">' + (merk ? '<div class="pq-brand">' + LOGO + '<span>' + label + '</span></div>' : '') + '<div class="pq-ink" id="pqink"></div></div>' +
      '<div class="pq-choice" id="pqchoice"><button class="pq-btn" id="pqgo" type="button">' + (heeftVideo ? cta : (cfg.ctaZonderVideo || 'Laat maar zien')) + ' <span class="pq-arw">&#8594;</span></button>' + (heeftVideo ? '<span class="pq-btn-sub">' + ctaSub + '</span>' : '') + '</div>' +
      (heeftVideo ? '<button class="pq-read" id="pqread" type="button">' + lezen + '</button>' : '') +
    '</div>';
  /* Dit bestand hangt in de <head>, dus de body bestaat hier nog niet en appendChild
     gooit een fout. De laag werd daardoor nooit ingehangen, terwijl pq-on wel op <html>
     bleef staan: elke v2-pagina opende zonder kaart en met een lege plek in de hero.
     De laag is los van het document al compleet, dus inhangen mag ook later. */
  function inhangen(){ document.body.appendChild(el); }
  if (document.body) inhangen();
  else document.addEventListener('DOMContentLoaded', inhangen);

  var card = el.querySelector('#pqcard'), ink = el.querySelector('#pqink');
  var choice = el.querySelector('#pqchoice'), read = el.querySelector('#pqread');
  var klaar = false;

  var perRegel = regels.map(function(tekst){
    var lijn = document.createElement('span'); lijn.className = 'pq-line'; var chars = [];
    tekst.split('|').forEach(function(deel, di){
      if (di > 0) lijn.appendChild(document.createElement('br'));
      var tekens = [];
      deel.split('*').forEach(function(seg, si){ for (var i=0;i<seg.length;i++) tekens.push({c:seg[i], hl:si%2===1}); });
      var woord = null;
      tekens.forEach(function(t){
        var s = document.createElement('span'); s.className = 'pq-ch' + (t.hl?' hl':''); s.textContent = t.c;
        if (t.c === ' ') { woord = null; lijn.appendChild(s); }
        else { if (!woord) { woord = document.createElement('span'); woord.className='pq-w'; lijn.appendChild(woord); } woord.appendChild(s); }
        chars.push(s);
      });
    });
    ink.appendChild(lijn); return chars;
  });

  function wacht(ms){ return new Promise(function(r){ setTimeout(r, ms); }); }
  async function schrijf(){
    for (var r=0; r<perRegel.length; r++){
      var chars = perRegel[r];
      for (var i=0;i<chars.length;i++){ chars[i].classList.add('on'); await wacht(chars[i].textContent===' '?Math.round(tempo*.45):tempo); }
      if (r < perRegel.length-1) await wacht(pauze);
    }
    choice.classList.add('in'); if (read) read.classList.add('in');
    pqTrack('kaart-uitgeschreven');
  }

  /* De kaart vliegt naar zijn plek in de hero. Dat is het hele punt:
     het voorwerp in hun hand wordt het voorwerp op het scherm. */
  function sluit(metVideo){
    if (klaar) return; klaar = true;
    pqTrack(metVideo ? 'intro-video' : 'intro-lezen');
    var slot = document.getElementById('slot');
    var slotcard = document.getElementById('slotcard');
    el.classList.add('gone');
    /* Zonder landingsplek in de hero fade't de laag gewoon weg. */
    if (!slot) {
      el.style.opacity = '0';
      setTimeout(function(){ ontgrendel(el); if (metVideo && window.pqVideo) window.pqVideo(); }, 620);
      return;
    }
    var a = card.getBoundingClientRect(), s = slot.getBoundingClientRect();
    var sc = s.width / a.width;
    var dx = (s.left + s.width/2) - (a.left + a.width/2);
    var dy = (s.top + s.height/2) - (a.top + a.height/2);
    card.classList.add('fly');
    card.style.transform = 'translate('+dx.toFixed(1)+'px,'+dy.toFixed(1)+'px) scale('+sc.toFixed(3)+') rotate(-2.6deg)';
    card.style.opacity = '0';
    setTimeout(function(){ if (slotcard) slotcard.classList.add('show'); }, 620);
    setTimeout(function(){
      ontgrendel(el);
      if (metVideo && window.pqVideo) window.pqVideo();
    }, 980);
  }

  function ontgrendel(laag){
    try { if (eenmalig) localStorage.setItem(KEY, '1'); } catch (e) {}
    document.documentElement.className = document.documentElement.className.replace(' pq-on','');
    if (laag && laag.parentNode) laag.parentNode.removeChild(laag);
  }
  el.querySelector('#pqgo').addEventListener('click', function(){ sluit(heeftVideo); });
  if (read) read.addEventListener('click', function(){ sluit(false); });

  if (traag){
    perRegel.forEach(function(c){ c.forEach(function(s){ s.classList.add('on'); }); });
    card.classList.add('in'); choice.classList.add('in'); if (read) read.classList.add('in');
    return;
  }
  var gestart = false;
  function begin(){
    if (gestart) return; gestart = true;
    setTimeout(function(){ card.classList.add('in'); }, 60);
    setTimeout(function(){ read.classList.add('in'); }, 900);
    setTimeout(schrijf, 620);
  }
  if (document.fonts && document.fonts.load) document.fonts.load('600 2rem Caveat').then(begin, begin);
  setTimeout(begin, 1200);
})();
