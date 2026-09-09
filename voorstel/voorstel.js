/* ============================================================
   VOORSTEL-PAGINA — het gedrag
   Reveals, de rail, de pen die zichzelf tekent, de volumeschuif,
   de keuzeknoppen en het leesprofiel.

   Meten gebruikt hetzelfde profiel als lp-v2: één POST per bezoek
   naar /api/t, die het doorzet naar Belcockpit. Zo staat een
   voorstel dat drie keer geopend wordt op hetzelfde bord als een
   scan, en belt Timon erop na.
   ============================================================ */
(function () {
  'use strict';
  var $ = function (s, w) { return (w || document).querySelector(s); };
  var $$ = function (s, w) { return Array.prototype.slice.call((w || document).querySelectorAll(s)); };
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* De teller van het leesprofiel staat bovenaan omdat zetVolume() hem al tijdens het
     opbouwen aanroept. Stond hij lager, dan is `gezien` daar nog undefined en stopt het
     hele script stil bij de eerste tik. */
  var SLUG = window.PQ_SLUG || location.pathname.replace(/^\/+|\/+$/g, '');
  var TRACK = (typeof window.PQ_TRACK_URL === 'string') ? window.PQ_TRACK_URL : '/api/t';
  var sessie = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  var gezien = {}, stappen = [], secties = {}, actief = 0, diep = 0, vorige = '';


  /* ── 1. reveals ─────────────────────────────────────────── */
  var io = new IntersectionObserver(function (rijen) {
    rijen.forEach(function (r) {
      if (!r.isIntersecting) return;
      r.target.classList.add('in');
      io.unobserve(r.target);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
  $$('.op').forEach(function (el) { io.observe(el); });

  /* ── 2. de pen. de lengte van het pad hangt af van hoe breed de
        zin uitvalt, dus die meten we pas als de tekst staat. ── */
  function penMeten() {
    $$('.pen path, .door path').forEach(function (p) {
      var len = Math.ceil(p.getTotalLength()) + 4;
      p.style.setProperty('--len', len);
    });
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(penMeten);
  else addEventListener('load', penMeten);
  penMeten();

  /* ── 3. balk en rail ────────────────────────────────────── */
  var bar = $('.bar'), rail = $('.rail');
  var doelen = $$('section[id]');
  function bijScroll() {
    var y = scrollY;
    if (bar) {
      bar.classList.toggle('vast', y > 40);
      bar.classList.toggle('toon', y > innerHeight * 0.55);
    }
    if (rail) {
      var beste = null;
      doelen.forEach(function (s) {
        if (s.getBoundingClientRect().top < innerHeight * 0.4) beste = s.id;
      });
      $$('a', rail).forEach(function (a) {
        a.classList.toggle('aan', a.getAttribute('href') === '#' + beste);
      });
    }
    diepteMeten();
  }
  addEventListener('scroll', bijScroll, { passive: true });
  addEventListener('resize', bijScroll);

  /* ── 4. de volumeschuif ─────────────────────────────────── */
  var staffel = window.PQ_STAFFEL || {};
  var kiesKnoppen = $$('.kies button');
  function zetVolume(sleutel) {
    var d = staffel[sleutel];
    if (!d) return;
    kiesKnoppen.forEach(function (b) { b.classList.toggle('aan', b.dataset.v === sleutel); });
    Object.keys(d).forEach(function (k) {
      $$('[data-prijs="' + k + '"]').forEach(function (el) { el.textContent = d[k]; });
    });
    window.PQ_VOLUME = sleutel;
    tik('volume-' + sleutel);
  }
  kiesKnoppen.forEach(function (b) {
    b.addEventListener('click', function () { zetVolume(b.dataset.v); });
  });
  if (window.PQ_ADVIES) zetVolume(String(window.PQ_ADVIES));

  /* ── 5. trechterbalken vullen zodra ze in beeld komen ───── */
  var ioTr = new IntersectionObserver(function (rijen) {
    rijen.forEach(function (r) {
      if (!r.isIntersecting) return;
      $$('.tr-f', r.target).forEach(function (f) { f.style.width = f.dataset.w + '%'; });
      ioTr.unobserve(r.target);
    });
  }, { threshold: 0.3 });
  $$('.trechter').forEach(function (el) { ioTr.observe(el); });
  function vulBalken(w) { $$('.tr-f', w).forEach(function (f) { f.style.width = f.dataset.w + '%'; }); }

  /* ── 6. de keuze ────────────────────────────────────────── */
  $$('[data-keuze]').forEach(function (b) {
    b.addEventListener('click', function () {
      var soort = b.dataset.keuze;
      tik('keuze-' + soort);
      flush('keuze');
      var dank = $('.dank');
      if (dank) {
        $('[data-dank-kop]', dank).textContent = b.dataset.dankKop || 'Genoteerd.';
        $('[data-dank-tekst]', dank).textContent = b.dataset.dankTekst || '';
        dank.classList.add('toon');
        dank.scrollIntoView({ behavior: rust ? 'auto' : 'smooth', block: 'center' });
      }
      if (b.dataset.href) setTimeout(function () { location.href = b.dataset.href; }, 900);
    });
  });
  $$('.bar-knop, [data-spring]').forEach(function (b) {
    b.addEventListener('click', function () {
      var d = $('#keuze');
      if (d) d.scrollIntoView({ behavior: rust ? 'auto' : 'smooth' });
      tik('naar-keuze');
    });
  });
  $$('.klap').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      tik('open-' + (d.dataset.k || 'cijfers'));
      vulBalken(d);
    });
  });
  $$('a[data-dossier]').forEach(function (a) {
    a.addEventListener('click', function () { tik('dossier-' + a.dataset.dossier); flush('dossier'); });
  });

  /* ── 7. leesprofiel. zelfde vorm als lp-v2, zie Klanten/BCS/api/t.js ── */
  function tik(stap) {
    if (gezien[stap]) return;
    gezien[stap] = 1;
    stappen.push(stap);
  }
  function diepteMeten() {
    var h = document.body.scrollHeight - innerHeight;
    var pct = h > 0 ? Math.round((scrollY / h) * 100) : 100;
    if (pct > diep) diep = Math.min(100, pct);
  }
  setInterval(function () {
    if (document.hidden) return;
    actief++;
    doelen.forEach(function (s) {
      var r = s.getBoundingClientRect();
      if (r.top < innerHeight * 0.75 && r.bottom > innerHeight * 0.25) {
        secties[s.id] = (secties[s.id] || 0) + 1;
      }
    });
  }, 1000);

  function flush(reden) {
    var vinger = actief + '|' + diep + '|' + stappen.join(',') + '|' + JSON.stringify(secties);
    if (vinger === vorige) return;
    vorige = vinger;
    var lading = JSON.stringify({
      v: 2, soort: 'voorstel', slug: SLUG, sessie: sessie, reden: reden || '',
      sec: actief, diep: diep, secties: secties, stappen: stappen,
      bedrijf: window.PQ_BEDRIJF, klant: window.PQ_KLANT,
      campagne: window.PQ_CAMPAGNE || 'voorstel', t: Date.now()
    });
    if (!TRACK) { if (console && console.debug) console.debug('[pique] voorstel', lading); return; }
    var blob = new Blob([lading], { type: 'text/plain;charset=UTF-8' });
    if (navigator.sendBeacon && navigator.sendBeacon(TRACK, blob)) return;
    fetch(TRACK, { method: 'POST', body: lading, keepalive: true,
      headers: { 'Content-Type': 'text/plain;charset=utf-8' } }).catch(function () {});
  }
  setTimeout(function () { flush('binnen'); }, 3000);
  setInterval(function () { if (!document.hidden) flush('bezig'); }, 30000);
  addEventListener('visibilitychange', function () { flush(document.hidden ? 'weg' : 'terug'); });
  addEventListener('pagehide', function () { flush('einde'); });

  bijScroll();
})();
