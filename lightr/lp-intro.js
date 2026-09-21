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
  var traag = false; /* demo: schrijfanimatie altijd afspelen, ook bij 'verklein beweging' */
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
  /* Pagina afdekken vóór de eerste paint. Zonder dit zie je eerst een split
     second de pagina zelf en pas daarna de kaart, en precies dat moment is wat
     de hele laag probeert te voorkomen. De laag zelf blijft zichtbaar. */
  document.documentElement.className += ' pq-on';
  var dek = document.createElement('style');
  dek.textContent = 'html.pq-on{background:var(--donker,#0E1526)}' +
                    'html.pq-on body{visibility:hidden}' +
                    'html.pq-on #pq{visibility:visible}';
  (document.head || document.documentElement).appendChild(dek);
  /* Vangnet: gaat er hierna iets mis, dan mag de pagina niet onzichtbaar
     blijven. Na drie seconden gaat de afdekking eraf, of de kaart er nu is
     of niet. */
  setTimeout(function () {
    if (!document.getElementById('pq')) {
      document.documentElement.className =
        document.documentElement.className.replace(' pq-on', '');
    }
  }, 3000);

  /* Is er geen opname, dan is één knop genoeg. Anders beloven we
     een video die er niet is. Zet cfg.video op false op zo'n pagina. */
  var heeftVideo = cfg.video !== false && !!window.PQ_VIDEO;
  var el = document.createElement('div');
  el.id = 'pq';
  el.innerHTML =
    '<div class="pq-glow"></div><div class="pq-stage">' +
      '<div class="pq-card" id="pqcard">' + (merk ? '<div class="pq-brand"><span>' + label + '</span></div>' : '') + '<div class="pq-ink" id="pqink"></div></div>' +
      '<div class="pq-choice" id="pqchoice"><button class="pq-btn" id="pqgo" type="button">' + (heeftVideo ? cta : (cfg.ctaZonderVideo || 'Laat maar zien')) + ' <span class="pq-arw">&#8594;</span></button>' + (heeftVideo ? '<span class="pq-btn-sub">' + ctaSub + '</span>' : '') + '</div>' +
      (heeftVideo ? '<button class="pq-read" id="pqread" type="button">' + lezen + '</button>' : '') +
    '</div>';
  /* Dit bestand hangt in de <head>, dus de body bestaat hier nog niet en appendChild
     gooit een fout. De laag werd daardoor nooit ingehangen, terwijl pq-on wel op <html>
     bleef staan: elke v2-pagina opende zonder kaart en met een lege plek in de hero.
     De laag is los van het document al compleet, dus inhangen mag ook later. */
  function inhangen(){
    /* Het logo pas hier ophalen. Dit bestand hangt in de <head>, dus bij het
       opbouwen van de kaart bestaat de nav nog niet en zou het leeg blijven. */
    var merkblok = el.querySelector('.pq-brand');
    var navlogo = document.querySelector('nav .logo');
    if (merkblok && navlogo) merkblok.insertAdjacentHTML('afterbegin', navlogo.innerHTML);
    document.body.appendChild(el);
    /* pq-vlot: de kaart komt op zodra hij echt in de pagina hangt, en niet pas
       als het handschrift binnen is. Twee frames, anders staat hij er in een
       keer zonder de opkomst. */
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ card.classList.add('in'); }); });
  }
  /* Zodra <body> bestaat inhangen, niet pas bij DOMContentLoaded. Op een zware
     pagina scheelt dat honderden milliseconden waarin er niets te zien is.
     Kan hier veilig, omdat de videocheck uit window.PQ_VIDEO komt en niet uit
     een element dat nog geparsed moet worden. */
  (function wacht() {
    if (document.body) { inhangen(); return; }
    setTimeout(wacht, 4);
  })();

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

  /* pq-vlot: elk teken had een eigen setTimeout. Op een telefoon die nog staat
     te laden schuiven die timers achter elkaar aan, en dan hapert precies de
     eerste regel, het moment waarop iemand kijkt. Nu loopt er een lus mee met
     het beeldscherm: alles wat op dit frame aan de beurt is gaat in een keer
     aan, en na een traag frame haalt hij de achterstand in plaats van hem op
     te tellen. Het tempo van de kaart blijft daardoor precies gelijk. */
  var plan = [], klok = 0;
  perRegel.forEach(function(chars, r){
    chars.forEach(function(s){ plan.push({s:s, t:klok}); klok += (s.textContent===' '?Math.round(tempo*.45):tempo); });
    if (r < perRegel.length-1) klok += pauze;
  });
  function schrijf(){
    var start = performance.now(), i = 0;
    requestAnimationFrame(function frame(nu){
      var verstreken = nu - start;
      while (i < plan.length && plan[i].t <= verstreken) { plan[i].s.classList.add('on'); i++; }
      if (i < plan.length) { requestAnimationFrame(frame); return; }
      choice.classList.add('in'); if (read) read.classList.add('in');
      if (typeof pqTrack === 'function') pqTrack('kaart-uitgeschreven');
    });
  }

  /* De kaart vliegt naar zijn plek in de hero. Dat is het hele punt:
     het voorwerp in hun hand wordt het voorwerp op het scherm. */
  function sluit(metVideo){
    if (klaar) return; klaar = true;
    /* pq-vlot: lp-v2.js hangt onderaan de pagina. Wie op een trage telefoon
       meteen tikt, liep tegen een pqTrack die er nog niet was, en dan deed
       de knop niets. */
    if (typeof pqTrack === 'function') pqTrack(metVideo ? 'intro-video' : 'intro-lezen');
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
  /* pq-vlot: de kaart zelf hoeft niet op het handschrift te wachten, alleen de
     inkt. Hij komt dus op zodra hij in de pagina hangt, en het schrijven begint
     zodra Caveat binnen is. Dat lettertype staat nu naast de pagina, dus dat is
     in de praktijk meteen. De 700 ms eronder is het vangnet als het bestand er
     niet komt; daar stond 1200, en dat was zuiver wachttijd op een telefoon. */
  var gestart = false;
  function begin(){
    if (gestart) return; gestart = true;
    setTimeout(schrijf, 380);
  }
  if (document.fonts && document.fonts.load) document.fonts.load('600 2rem Caveat').then(begin, begin);
  setTimeout(begin, 700);
})();
