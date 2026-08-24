/* ============================================================
   PIQUE — intro-laag na de scan (gedeeld)
   Per pagina in de <head>, boven dit bestand:

     <script>window.PIQUE_INTRO = {
       voornaam: "Bram",
       bedrijf: "Alva Charging"
     };<\/script>

   Alleen voornaam is verplicht. Eigen regels kan met:
       regels: ["Hoi {voornaam}.", "Ik zag iets bij *{bedrijf}*."]
   Tekst tussen sterretjes wordt amber. Een | forceert een regelafbreking.

   Zonder JS verschijnt de laag niet, dus de pagina blijft altijd bereikbaar.
   ============================================================ */

(function () {
  var cfg = window.PIQUE_INTRO;
  if (!cfg) return;

  /* De laag speelt standaard bij elk bezoek. Een kaart gaat rond op kantoor
     en wordt door meerdere mensen gescand, dus iedereen hoort hem te zien.
     Alleen met eenmalig: true slaat hij een tweede bezoek over. */
  var KEY = 'pq-intro:' + location.pathname;
  var eenmalig = cfg.eenmalig === true;
  try { if (eenmalig && localStorage.getItem(KEY)) return; } catch (e) {}

  var traag = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bedrijf = cfg.bedrijf || 'je bedrijf';

  /* Bij een deel van de prospects kennen we de voornaam niet.
     Die krijgen dezelfde kaart zonder aanhef. */
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
  /* Op klantpagina's staat er geen afzenderregel boven de kaart:
     alleen het handschrift. Zet daar merk: false. */
  var merk   = cfg.merk !== false;
  var label  = cfg.label  || 'Persoonlijk';
  var vidSel = cfg.video     || '#reelvid';
  var vidWrap = cfg.videoWrap || '#reel';

  var tempo = cfg.tempo || 30;   // ms per teken
  var pauze = cfg.pauze || 340;  // ms tussen zinnen

  var LOGO = '<svg viewBox="0 0 929.98 302.23" xmlns="http://www.w3.org/2000/svg" aria-label="Pique"><path fill="currentColor" d="M0,268v-3.83l7.66-2.68q7.65-2.29,10.14-6.89t2.49-12.26V41.73q0-7.65-2.68-12.25T7.27,22.21L0,19.14V15.32H93q57,0,82.51,20.86t25.46,55a78.41,78.41,0,0,1-10.53,40Q180,149.32,155.83,160T90.74,170.77h-13v70.45q0,14.92,14.93,19.52l11.48,3.45V268ZM77.73,163.11H92.27q18.77,0,30.64-6.13t17.61-21.44q5.74-15.31,5.74-42.5,0-27.57-6.32-42.88T121.37,28.91Q109.12,23,90.74,23h-13Z"/><path fill="currentColor" d="M216.32,268v-3.83l5.36-1.53c5.11-1.54,8.62-3.83,10.53-6.9s2.88-7.14,2.88-12.25V123.67q0-8-2.88-12.06t-10.53-5.55l-5.36-1.15v-3.83l70.07-22.59,3.83,3.83-1.15,54.37V243.9q0,7.65,2.87,12.25T302.09,263l3.83,1.15V268ZM261.5,58.2q-13,0-22-8.23a27.06,27.06,0,0,1-9-20.87q0-13,9-21.06t22-8q13,0,21.83,8t8.8,21.06q0,12.63-8.8,20.87T261.5,58.2Z"/><path fill="currentColor" d="M503.21,119.57a87.17,87.17,0,0,0-33.76-35.13q-21.76-12.69-50.16-12.68T369.4,84.44a90,90,0,0,0-33.8,35.13q-12.27,22.45-12.24,52t12.24,52a90.24,90.24,0,0,0,33.8,35.16q21.5,12.68,49.89,12.66c3.83,0,7.54-.2,11.18-.53,2.21-.22,4.4-.48,6.53-.83-2-4.41-4.22-9.33-6.59-14.54a28.4,28.4,0,0,1-11.08,2.17c-.83,0-1.64,0-2.43-.1q-11.26-.92-19.81-10.52-9.51-10.64-14.72-29.79t-5.17-45.7q0-26.55,5.17-45.71t14.72-29.58c6.3-7,13.72-10.41,22.24-10.41,8.75,0,16.29,3.45,22.53,10.41S453,113,456.44,125.77s5.21,28,5.21,45.71q0,24.09-4.28,42.05c10.39,11.85,21.09,23.82,29.21,32.21a89,89,0,0,0,16.63-22.24q12-22.49,12-52T503.21,119.57Z"/><path fill="currentColor" d="M608.74,273.76A64.49,64.49,0,0,1,581.37,268a42.21,42.21,0,0,1-19.53-18.57q-7.1-12.82-6.7-33.89l1.15-98.4q0-8.8-3.06-12.63t-9.58-5.36l-4.59-1.53V93.81l68.54-13.4,3.82,3.82-1.91,54.37v92.28q0,12.26,7.08,18t17.81,5.75a55.62,55.62,0,0,0,19.14-3.07,68.65,68.65,0,0,0,16.85-9.19l1.53-124.82q0-8.79-2.68-12.44t-10-5.17l-3.82-1.15V95l67-14.54,3.83,3.82-1.15,54.37V242.36q0,8.43,2.3,13t9.95,7.66l3.83,1.15V268l-67,3.83-3.45-22.59a136.35,136.35,0,0,1-27.37,17.42Q628.66,273.76,608.74,273.76Z"/><path fill="currentColor" d="M851.11,78.11q24.89,0,42.5,10.14a69.39,69.39,0,0,1,27,27.57Q930,133.25,930,155.45q0,4.22-.38,8.62a34.71,34.71,0,0,1-1.53,7.84H814q.38,41.35,14.74,59.54t42.69,18.19q19.14,0,31-6.13a75.81,75.81,0,0,0,22.21-18l3.83,3.44a88.14,88.14,0,0,1-31.59,32.93q-19.73,11.87-47.29,11.87-27.18,0-48.24-11.68a82.38,82.38,0,0,1-32.93-33.5q-11.86-21.83-11.87-52.07,0-31.39,13.79-53.41t35.41-33.51A95.54,95.54,0,0,1,851.11,78.11ZM850,85.77a28.2,28.2,0,0,0-19,6.7q-7.85,6.7-12.25,23.73T814,164.26h65.47q3.82-41.73-3.06-60.12T850,85.77Z"/><path fill="#C6893C" d="M400.7,166s35.83,78.88,49.46,109c13.39,29.63,51.1,46.89,84.54-12.47a1,1,0,0,0-1.35-1.37c-7.45,4.12-26.71,12.89-41.07,3.1C474.11,251.94,395,153.48,400.7,166Z"/></svg>';

  /* Pagina afdekken vóór de eerste paint. Zonder dit zie je eerst een split
     second de pagina zelf en pas daarna de kaart, en precies dat moment is wat
     de hele laag probeert te voorkomen. De laag zelf blijft zichtbaar. */
  document.documentElement.className += ' pq-on';
  var dek = document.createElement('style');
  dek.textContent = 'html.pq-on{background:var(--navy,#0E1526)}' +
                    'html.pq-on body{visibility:hidden}' +
                    'html.pq-on #pq-intro{visibility:visible}';
  (document.head || document.documentElement).appendChild(dek);
  /* Vangnet: gaat er hierna iets mis, dan mag de pagina niet onzichtbaar
     blijven. Na drie seconden gaat de afdekking eraf, of de kaart er nu is
     of niet. */
  setTimeout(function () {
    if (!document.getElementById('pq-intro')) {
      document.documentElement.className =
        document.documentElement.className.replace(' pq-on', '');
    }
  }, 3000);

  var f = document.createElement('link');
  f.rel = 'stylesheet';
  f.href = 'https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&display=swap';
  document.head.appendChild(f);

  function start() {
    /* Staat er geen video op de pagina, dan is één knop genoeg. Anders
       beloven we een video die er niet is. Komt voor op pagina's waar de
       opname nog moet worden gedraaid. */
    var heeftVideo = cfg.video !== false && !!document.querySelector(vidSel);
    var knop = heeftVideo ? cta : (cfg.ctaZonderVideo || 'Laat maar zien');

    var el = document.createElement('div');
    el.id = 'pq-intro';
    el.innerHTML =
      '<div class="pq-glow"></div>' +
      '<div class="pq-stage">' +
        '<div class="pq-card" id="pq-card">' +
          (merk ? '<div class="pq-brand">' + LOGO + '<span>' + label + '</span></div>' : '') +
          '<div class="pq-ink" id="pq-ink"></div>' +
        '</div>' +
        '<div class="pq-choice" id="pq-choice">' +
          '<button class="pq-btn" id="pq-go" type="button">' + knop + ' <span class="pq-arw">&#8594;</span></button>' +
          (heeftVideo ? '<span class="pq-btn-sub">' + ctaSub + '</span>' : '') +
        '</div>' +
        (heeftVideo ? '<button class="pq-read" id="pq-read" type="button">' + lezen + '</button>' : '') +
      '</div>';
    document.body.appendChild(el);

    var card   = document.getElementById('pq-card');
    var ink    = document.getElementById('pq-ink');
    var choice = document.getElementById('pq-choice');
    var read   = document.getElementById('pq-read');
    var klaar  = false;

    /* Alle regels staan er meteen in, alleen nog onzichtbaar.
       Daardoor heeft de kaart vanaf het begin zijn eindhoogte
       en verspringt er niets tijdens het schrijven. */
    var perRegel = regels.map(function (tekst) {
      var lijn = document.createElement('span');
      lijn.className = 'pq-line';
      var chars = [];
      tekst.split('|').forEach(function (deel, di) {
        if (di > 0) lijn.appendChild(document.createElement('br'));

        var tekens = [];
        deel.split('*').forEach(function (seg, si) {
          for (var i = 0; i < seg.length; i++) tekens.push({ c: seg[i], hl: si % 2 === 1 });
        });

        /* Elk teken is een eigen span, dus zonder woordomhulsel mag de
           browser midden in een woord afbreken. Woorden krijgen daarom
           een nowrap-wikkel en breken alleen op de spaties. */
        var woord = null;
        tekens.forEach(function (t) {
          var s = document.createElement('span');
          s.className = 'pq-ch' + (t.hl ? ' hl' : '');
          s.textContent = t.c;
          if (t.c === ' ') {
            woord = null;
            lijn.appendChild(s);
          } else {
            if (!woord) {
              woord = document.createElement('span');
              woord.className = 'pq-w';
              lijn.appendChild(woord);
            }
            woord.appendChild(s);
          }
          chars.push(s);
        });
      });
      ink.appendChild(lijn);
      return chars;
    });

    function wacht(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

    async function schrijf() {
      for (var r = 0; r < perRegel.length; r++) {
        var chars = perRegel[r];
        for (var i = 0; i < chars.length; i++) {
          chars[i].classList.add('on');
          await wacht(chars[i].textContent === ' ' ? Math.round(tempo * .45) : tempo);
        }
        if (r < perRegel.length - 1) await wacht(pauze);
      }
      choice.classList.add('in');
      if (read) read.classList.add('in');
    }

    function alles() {
      perRegel.forEach(function (c) { c.forEach(function (s) { s.classList.add('on'); }); });
      card.classList.add('in');
      choice.classList.add('in');
      if (read) read.classList.add('in');
    }

    function sluit(metVideo) {
      if (klaar) return;
      klaar = true;
      try { if (eenmalig) localStorage.setItem(KEY, '1'); } catch (e) {}
      el.classList.add('pq-out');
      document.documentElement.className = document.documentElement.className.replace(' pq-on', '');
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 650);

      if (!metVideo) return;
      var v = document.querySelector(vidSel);
      var w = document.querySelector(vidWrap);
      if (!v) return;
      if (w) w.classList.add('playing');
      v.setAttribute('controls', '');
      v.muted = false;
      try { v.currentTime = 0; } catch (e) {}
      var p = v.play();
      if (p && p.catch) {
        p.catch(function () {
          v.removeAttribute('controls');
          if (w) w.classList.remove('playing');
        });
      }
      setTimeout(function () { v.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 100);
    }

    document.getElementById('pq-go').addEventListener('click', function () { sluit(true); });
    if (read) read.addEventListener('click', function () { sluit(false); });

    if (traag) { alles(); return; }

    /* Wachten tot Caveat binnen is. Anders staat de tekst eerst in een
       vervangende letter en verspringt de kaart halverwege het schrijven,
       precies wat je op een trage mobiele verbinding zou zien. */
    var gestart = false;
    function begin() {
      if (gestart) return;
      gestart = true;
      setTimeout(function () { card.classList.add('in'); }, 60);
      setTimeout(function () { if (read) read.classList.add('in'); }, 900);
      setTimeout(schrijf, 620);
    }
    if (document.fonts && document.fonts.load) {
      document.fonts.load('600 2rem Caveat').then(begin, begin);
    }
    setTimeout(begin, 1200);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
