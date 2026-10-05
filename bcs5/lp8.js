/* ============================================================
   PIQUE LP v8 — drie gedragingen, meer niet.

   1 de vraagbalk komt op zodra de opening voorbij is
   2 de bron klapt open als hij hem aanraakt (het enige dat op HEM
     reageert in plaats van op scroll)
   3 de convergentie scrubt een keer, halverwege

   Zonder JavaScript staat de hele pagina er: de balk is dan gewoon
   zichtbaar, de bronnen staan open en de twee fragmenten staan naast
   elkaar met de conclusie eronder.
   ============================================================ */
(function () {
  'use strict';
  var C = window.PQ8 || {};
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches ||
             location.search.indexOf('statisch') > -1;
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return [].slice.call(document.querySelectorAll(s)); };

  var gezien = {};
  function meet(stap, extra) {
    if (gezien[stap]) return; gezien[stap] = 1;
    var lading = JSON.stringify({ slug: C.slug || location.pathname, klant: C.klant || '',
      campagne: C.campagne || '', stap: stap, extra: extra == null ? null : String(extra) });
    if (C.meetUrl && navigator.sendBeacon) navigator.sendBeacon(C.meetUrl, lading);
    else if (window.console && console.debug) console.debug('[pq8]', stap, extra || '');
  }

  /* ── 1. de vraagbalk ────────────────────────────────────── */
  function vraagbalk() {
    var balk = $('.vraagbalk'), opening = $('.opening');
    if (!balk || !opening) return;
    if (rust) { balk.classList.add('er'); return; }
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { balk.classList.toggle('er', !e.isIntersecting); });
    }, { threshold: 0, rootMargin: '-72px 0px 0px 0px' }).observe(opening);
  }

  /* ── 2. de bron die opengaat ────────────────────────────── */
  /* Alles op elke andere pagina reageert op scroll. Dit reageert op
     hem, en het zegt precies wat de pagina claimt: je kunt me
     controleren. */
  function bronnen() {
    $$('.bronknop').forEach(function (knop) {
      var doel = document.getElementById(knop.getAttribute('aria-controls'));
      if (!doel) return;
      knop.setAttribute('aria-expanded', 'false');
      knop.addEventListener('click', function () {
        var open = doel.classList.toggle('open');
        knop.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (open) meet('bron-geopend', knop.dataset.dom || '');
      });
    });
  }

  /* ── 3. de convergentie ─────────────────────────────────── */
  function samenkomen() {
    var sec = $('.samen'), pin = $('.samen-pin');
    if (!sec || !pin || rust) return;
    var wacht = false;
    function meten() {
      wacht = false;
      var r = sec.getBoundingClientRect();
      /* Een sticky kind scrubt over sectiehoogte min stickyhoogte, en
         dat wordt per frame gemeten omdat svh met de adresbalk meebeweegt. */
      var reis = sec.offsetHeight - pin.offsetHeight;
      if (reis <= 0) return;
      var f = -r.top / reis;
      f = f < 0 ? 0 : f > 1 ? 1 : f;
      /* De beweging is klaar op 62 procent, zodat de conclusie daarna
         nog even stil in beeld staat voordat hij doorscrolt. */
      var uit = 1 - Math.min(1, f / 0.62);
      pin.style.setProperty('--uit', uit.toFixed(3));
      if (uit < .05) meet('convergentie');
    }
    function tik() { if (wacht) return; wacht = true; requestAnimationFrame(meten); }
    addEventListener('scroll', tik, { passive: true });
    addEventListener('resize', tik);
    meten(); setTimeout(meten, 400);
  }

  /* ── de sheet ───────────────────────────────────────────── */
  function sheet() {
    var sh = $('#sheet'); if (!sh) return;
    var geladen = false;
    function skeletWeg() { var s = $('#calskel'); if (s) s.classList.add('weg'); }
    function laadCal() {
      if (geladen || !C.cal) { if (!C.cal) geenAgenda(); return; }
      geladen = true;
      (function (X, A, L) { var p = function (a, ar) { a.q.push(ar); }; var d = X.document;
        X.Cal = X.Cal || function () { var cal = X.Cal, ar = arguments;
          if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement('script')).src = A; cal.loaded = true; }
          if (ar[0] === L) { var api = function () { p(api, arguments); }; var ns = ar[1]; api.q = api.q || [];
            if (typeof ns === 'string') { cal.ns[ns] = cal.ns[ns] || api; p(cal.ns[ns], ar); p(cal, ['initNamespace', ns]); }
            else p(cal, ar); return; } p(cal, ar); };
      })(window, 'https://app.cal.com/embed/embed.js', 'init');
      Cal('init', 'pq', { origin: 'https://cal.com' });
      Cal.ns.pq('inline', { elementOrSelector: '#cal-embed', config: { layout: 'month_view' }, calLink: C.cal });
      Cal.ns.pq('on', { action: 'bookingSuccessful', callback: function () { meet('afspraak-geboekt'); } });
      Cal.ns.pq('on', { action: 'linkReady', callback: skeletWeg });
      setTimeout(skeletWeg, 12000);
    }
    function geenAgenda() {
      var t = sh.querySelector('.tabs'); if (t) t.style.display = 'none';
      var p = $('#pane-plan'); if (p) p.remove();
      var b = $('#pane-bel'); if (b) b.classList.add('on');
    }
    function tab(n) {
      sh.querySelectorAll('.tabs button').forEach(function (b) { b.classList.toggle('on', b.dataset.tab === n); });
      var p = $('#pane-plan'), b = $('#pane-bel');
      if (p) p.classList.toggle('on', n === 'plan');
      if (b) b.classList.toggle('on', n === 'bel');
      if (n === 'plan') laadCal();
    }
    function open(w) {
      sh.classList.add('open'); sh.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden'; tab(w || 'plan'); meet('sheet', w || 'plan');
    }
    function dicht() {
      sh.classList.remove('open'); sh.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
    $$('[data-open]').forEach(function (b) {
      b.addEventListener('click', function () { open(b.dataset.open); });
    });
    sh.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', dicht); });
    sh.querySelectorAll('.tabs button').forEach(function (b) {
      b.addEventListener('click', function () { tab(b.dataset.tab); });
    });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') dicht(); });

    /* De agenda laadt zodra de ask in beeld komt, ruim voordat hij kan klikken. */
    var ask = $('.ask');
    if (ask && C.cal && !rust) new IntersectionObserver(function (es, io) {
      if (!es[0].isIntersecting) return; io.disconnect();
      if (window.requestIdleCallback) requestIdleCallback(laadCal, { timeout: 1500 });
      else setTimeout(laadCal, 400);
    }, { threshold: 0 }).observe(ask);
    if (!C.cal) geenAgenda();

    var wanneer = '';
    var slots = $('#slots');
    if (slots) slots.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      [].slice.call(this.children).forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on'); wanneer = b.dataset.v;
    });
    var form = $('#belform');
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      var naam = (($('#bn') || {}).value || '').trim(), tel = (($('#bt') || {}).value || '').trim();
      if (!tel) return;
      meet('terugbelverzoek', tel);
      var lading = JSON.stringify({ naam: naam, tel: tel, wanneer: wanneer,
        bedrijf: C.bedrijf || '', slug: C.slug || '', klant: C.klant || '', campagne: C.campagne || '' });
      /* text/plain, anders vraagt de browser een preflight die een Apps
         Script-webapp niet beantwoordt. */
      if (C.terugbelUrl) fetch(C.terugbelUrl, { method: 'POST', body: lading, keepalive: true,
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } }).catch(function () {
          if (navigator.sendBeacon) navigator.sendBeacon(C.terugbelUrl, new Blob([lading], { type: 'text/plain' }));
        });
      $('#pane-bel').innerHTML = '<div class="ok"><p class="disp">Genoteerd, ' +
        (naam ? naam.split(' ')[0] : 'top') + '.</p><p>Ik bel je ' +
        (wanneer ? wanneer.toLowerCase() : 'zo snel als het schikt') + ' op ' + tel + '.</p></div>';
    });
  }

  function video() {
    var b = $('.videorij'); if (!b) return;
    if (!C.video) { b.remove(); return; }
    b.addEventListener('click', function () {
      meet('video');
      var l = document.createElement('div'); l.className = 'vlaag';
      l.innerHTML = '<video playsinline controls autoplay src="' + C.video + '"' +
        (C.poster ? ' poster="' + C.poster + '"' : '') + '></video>' +
        '<button class="vdicht" type="button" aria-label="Sluiten">&times;</button>';
      document.body.appendChild(l);
      document.body.style.overflow = 'hidden';
      l.querySelector('.vdicht').addEventListener('click', function () {
        l.remove(); document.body.style.overflow = '';
      });
    });
  }

  function start() { vraagbalk(); bronnen(); samenkomen(); sheet(); video(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
