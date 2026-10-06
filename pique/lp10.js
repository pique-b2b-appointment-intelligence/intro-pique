/* ============================================================
   PIQUE LP v10
   Boven de waterlijn klikt elke sectie vast: een scherm, een ding.
   De rail links laat zien waar je bent en hoeveel vegen er nog zijn.

   Vier gedragingen, meer niet:
     de kaartlaag, de video, de rail, de bron die opengaat.
   ============================================================ */
(function () {
  'use strict';
  var C = window.PQ10 || {};
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches ||
             location.search.indexOf('statisch') > -1;
  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return [].slice.call(document.querySelectorAll(s)); };

  var gezien = {};
  function meet(stap, extra) {
    if (gezien[stap]) return; gezien[stap] = 1;
    var l = JSON.stringify({ slug: C.slug || location.pathname, klant: C.klant || 'pique',
      campagne: C.campagne || '', stap: stap, extra: extra == null ? null : String(extra) });
    if (C.meetUrl && navigator.sendBeacon) navigator.sendBeacon(C.meetUrl, l);
    else if (window.console && console.debug) console.debug('[pq10]', stap, extra || '');
  }
  window.pqMeet = meet;

  /* ── de kaartlaag ───────────────────────────────────────── */
  function kaartlaag(klaar) {
    if (!C.kaart || location.search.indexOf('nokaart') > -1) {
      var sc = $('#slotcard'); if (sc) sc.classList.add('toon');
      return klaar(false);
    }
    document.documentElement.classList.add('kaart-aan');
    var regels = C.kaart.regels.map(function (r, i) {
      var stuk = r.split('*').map(function (seg, si) {
        return si % 2 ? '<span class="hl">' + seg + '</span>' : seg;
      }).join('');
      return '<span class="rg" style="--i:' + i + '">' + stuk + '</span>';
    }).join('');
    var el = document.createElement('div');
    el.id = 'kl';
    el.innerHTML = '<div class="kl-mid">' +
      '<div class="pap' + (rust ? '' : ' klaarzetten') + '" id="dekaart">' +
        '<div class="kl-merk">' + (C.logo || '') + '<span>Persoonlijk</span></div>' +
        '<div class="inkt">' + regels + '</div></div>' +
      '<div class="kl-keuze" id="keuze">' +
        '<button class="knop groot" id="kja" type="button">' + C.kaart.ja + '</button>' +
        '<span class="kl-sub">' + C.kaart.sub + '</span></div>' +
      '<button class="kl-lees" id="klees" type="button">' + C.kaart.lees + '</button></div>';
    document.body.appendChild(el);

    var kaart = el.querySelector('#dekaart'), keuze = el.querySelector('#keuze');
    var lees = el.querySelector('#klees'), af = false;

    function sluit(metVideo, vEl) {
      if (af) return; af = true;
      meet(metVideo ? 'kaart-video' : 'kaart-lezen');
      var slot = $('#slotcard'), gemeld = false;
      function klaarmee() {
        if (gemeld) return; gemeld = true;
        if (el.parentNode) el.parentNode.removeChild(el);
        document.documentElement.classList.remove('kaart-aan');
        if (slot) slot.classList.add('toon');
        if (metVideo && vEl) videolaag(vEl, function () { klaar(true); });
        else klaar(false);
      }
      el.classList.add('weg');
      setTimeout(klaarmee, rust ? 40 : 560);
    }

    /* het geluid wordt binnen de klik ontgrendeld, daarna mag het niet meer van iOS */
    el.querySelector('#kja').addEventListener('click', function () {
      var v = null;
      if (C.video) {
        v = document.createElement('video');
        v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'auto';
        if (C.poster) v.poster = C.poster;
        v.src = C.video;
        try { var p = v.play(); if (p && p.then) p.then(function () { v.pause(); }, function () {}); } catch (e) {}
      }
      sluit(!!v, v);
    });
    lees.addEventListener('click', function () { sluit(false); });

    if (rust) { kaart.classList.add('er'); keuze.classList.add('er'); lees.classList.add('er'); return; }
    var gestart = false;
    function start() {
      if (gestart) return; gestart = true;
      setTimeout(function () { kaart.classList.add('er'); }, 60);
      setTimeout(function () { kaart.classList.add('schrijf'); }, 420);
      setTimeout(function () { lees.classList.add('er'); }, 900);
      setTimeout(function () { keuze.classList.add('er'); meet('kaart-af'); },
                 620 + C.kaart.regels.length * 340 + 400);
    }
    if (document.fonts && document.fonts.load) document.fonts.load('600 2rem Caveat').then(start, start);
    setTimeout(start, 1200);
  }

  /* ── de videolaag ───────────────────────────────────────── */
  function videolaag(v, klaar) {
    meet('video-start');
    var el = document.createElement('div');
    el.id = 'vl';
    el.innerHTML = '<div class="v-bed"><span class="tel" id="vtel">0:00</span>' +
      '<span class="rek"></span><button class="v-over" id="vover" type="button">Overslaan</button></div>' +
      '<div class="v-balk" id="vbalk"></div>' +
      '<button class="v-geluid" id="vgel" type="button"><span>Tik voor geluid</span></button>';
    el.insertBefore(v, el.firstChild);
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('er'); });
    var balk = el.querySelector('#vbalk'), tel = el.querySelector('#vtel');
    var over = el.querySelector('#vover'), gel = el.querySelector('#vgel'), weg = false;
    function mmss(s) { var m = Math.floor(s / 60), r = Math.floor(s % 60); return m + ':' + (r < 10 ? '0' : '') + r; }
    v.addEventListener('timeupdate', function () {
      if (!v.duration) return;
      balk.style.width = (v.currentTime / v.duration * 100) + '%';
      tel.textContent = mmss(v.duration - v.currentTime);
      if (v.currentTime > 55 && over.textContent === 'Overslaan') over.textContent = 'Verder lezen';
    });
    v.addEventListener('ended', function () { dicht('uitgekeken'); });
    over.addEventListener('click', function () { dicht('overgeslagen'); });
    gel.addEventListener('click', function () { v.muted = false; v.play(); gel.classList.remove('er'); });
    v.muted = false;
    var p = v.play();
    if (p && p.catch) p.catch(function () {
      v.muted = true;
      v.play().then(function () { gel.classList.add('er'); }, function () { dicht('geblokkeerd'); });
    });
    function dicht(reden) {
      if (weg) return; weg = true;
      meet('video-' + reden, v.currentTime ? Math.round(v.currentTime) : 0);
      el.classList.remove('er');
      setTimeout(function () {
        if (el.parentNode) el.parentNode.removeChild(el);
        document.documentElement.classList.remove('kaart-aan');
        klaar();
      }, 420);
    }
  }

  /* ── de rail: waar ben ik, en hoeveel vegen nog ─────────── */
  /* De rail bestaat omdat elke sectie het scherm vult: zonder hem weet
     je niet of je bij veeg twee of veeg vijf bent. */
  function rail() {
    var rail = $('.rail'), secties = $$('.s');
    if (!rail || !secties.length) return;
    var vol = rail.querySelector('.vol');
    var dots = secties.map(function (_, i) {
      var d = document.createElement('i');
      d.style.top = 'calc(22svh + ' + (i / (secties.length - 1) * 100) + '% * (56svh / 100))';
      rail.appendChild(d);
      return d;
    });
    /* de dots staan op gelijke afstand over het spoor */
    dots.forEach(function (d, i) {
      d.style.top = 'calc(22svh + (56svh / ' + (secties.length - 1) + ') * ' + i + ')';
    });
    if (rust) { rail.classList.add('er'); dots.forEach(function (d) { d.classList.add('aan'); }); return; }

    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var i = secties.indexOf(e.target);
        dots.forEach(function (d, j) {
          d.classList.toggle('aan', j <= i);
          d.classList.toggle('nu', j === i);
        });
        vol.style.height = 'calc((56svh / ' + (secties.length - 1) + ') * ' + i + ')';
        if (i === secties.length - 1) meet('ask-gezien');
      });
    }, { threshold: .5 });
    secties.forEach(function (s) { io.observe(s); });

    /* de rail verschijnt pas als de eerste sectie voorbij is en
       verdwijnt onder de waterlijn, want daar is hij niets meer waard */
    var onder = $('.onder');
    new IntersectionObserver(function (es) {
      rail.classList.toggle('er', !es[0].isIntersecting);
    }, { threshold: 0 }).observe(onder || secties[secties.length - 1]);
  }

  /* ── de bron die opengaat ───────────────────────────────── */
  function bronnen() {
    $$('.bronknop').forEach(function (k) {
      var d = document.getElementById(k.getAttribute('aria-controls'));
      if (!d) return;
      k.addEventListener('click', function () {
        var open = d.classList.toggle('open');
        k.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (open) meet('bron-geopend', k.dataset.dom || '');
      });
    });
  }

  /* ── de VSL onderaan ────────────────────────────────────── */
  function vsl() {
    var b = $('.vslbox'); if (!b) return;
    if (!C.vsl) { var sec = b.closest('section'); if (sec) sec.remove(); return; }
    b.addEventListener('click', function () {
      meet('vsl');
      var l = document.createElement('div'); l.id = 'vlaag';
      l.innerHTML = '<video playsinline controls autoplay src="' + C.vsl + '"></video>' +
        '<button class="vdicht" type="button" aria-label="Sluiten">&times;</button>';
      document.body.appendChild(l);
      document.documentElement.classList.add('kaart-aan');
      l.querySelector('.vdicht').addEventListener('click', function () {
        l.remove(); document.documentElement.classList.remove('kaart-aan');
      });
    });
  }

  /* ── de ene reveal, en de nav ───────────────────────────── */
  function rest() {
    var blokken = $$('.op, .bewijs');
    if (rust) { blokken.forEach(function (b) { b.classList.add('in'); }); }
    else {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          io.unobserve(e.target); e.target.classList.add('in');
        });
      }, { threshold: 0, rootMargin: '0px 0px -10% 0px' });
      blokken.forEach(function (b) {
        [].slice.call(b.children).forEach(function (k, i) {
          k.style.setProperty('--dl', (Math.min(i, 2) * 80) + 'ms');
        });
        io.observe(b);
      });
    }
    var nav = $('nav'), wacht = false;
    function tik() {
      if (wacht) return; wacht = true;
      requestAnimationFrame(function () {
        wacht = false;
        if (nav) nav.classList.toggle('vast', (pageYOffset || 0) > 24);
      });
    }
    addEventListener('scroll', tik, { passive: true });
    tik();
  }

  /* ── de sheet ───────────────────────────────────────────── */
  function sheet() {
    var sh = $('#sheet'); if (!sh) return;
    var geladen = false;
    function skeletWeg() { var x = $('#calskel'); if (x) x.classList.add('weg'); }
    function geenAgenda() {
      var t = sh.querySelector('.tabs'); if (t) t.style.display = 'none';
      var p = $('#pane-plan'); if (p) p.remove();
      var b = $('#pane-bel'); if (b) b.classList.add('on');
    }
    function laadCal() {
      if (!C.cal) { geenAgenda(); return; }
      if (geladen) return; geladen = true;
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
    function tab(n) {
      sh.querySelectorAll('.tabs button').forEach(function (b) { b.classList.toggle('on', b.dataset.tab === n); });
      var p = $('#pane-plan'), b = $('#pane-bel');
      if (p) p.classList.toggle('on', n === 'plan');
      if (b) b.classList.toggle('on', n === 'bel');
      if (n === 'plan') laadCal();
    }
    window.pqOpenSheet = function (w) {
      sh.classList.add('open'); sh.setAttribute('aria-hidden', 'false');
      document.documentElement.classList.add('kaart-aan');
      tab(w || 'plan'); meet('sheet', w || 'plan');
    };
    function dicht() {
      sh.classList.remove('open'); sh.setAttribute('aria-hidden', 'true');
      document.documentElement.classList.remove('kaart-aan');
    }
    sh.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', dicht); });
    sh.querySelectorAll('.tabs button').forEach(function (b) {
      b.addEventListener('click', function () { tab(b.dataset.tab); });
    });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') dicht(); });
    if (!C.cal) geenAgenda();

    /* de agenda laadt zodra de ask in beeld komt, ruim voor de klik */
    var ask = $('.ask');
    if (ask && C.cal && !rust) new IntersectionObserver(function (es, io) {
      if (!es[0].isIntersecting) return; io.disconnect();
      if (window.requestIdleCallback) requestIdleCallback(laadCal, { timeout: 1500 });
      else setTimeout(laadCal, 400);
    }, { threshold: 0 }).observe(ask);

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
      var l = JSON.stringify({ naam: naam, tel: tel, wanneer: wanneer, bedrijf: C.bedrijf || '',
        slug: C.slug || '', klant: C.klant || 'pique', campagne: C.campagne || '' });
      /* text/plain: anders vraagt de browser een preflight die een Apps
         Script-webapp niet beantwoordt */
      if (C.terugbelUrl) fetch(C.terugbelUrl, { method: 'POST', body: l, keepalive: true,
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } }).catch(function () {
          if (navigator.sendBeacon) navigator.sendBeacon(C.terugbelUrl, new Blob([l], { type: 'text/plain' }));
        });
      $('#pane-bel').innerHTML = '<div class="ok"><p class="d">Genoteerd, ' +
        (naam ? naam.split(' ')[0] : 'top') + '.</p><p>Ik bel je ' +
        (wanneer ? wanneer.toLowerCase() : 'zo snel als het schikt') + ' op ' + tel + '.</p></div>';
    });
  }

  function start() {
    sheet(); bronnen(); vsl(); rail(); rest();
    kaartlaag(function (naVideo) { meet('pagina-open', naVideo ? 'na-video' : 'direct'); });
    $$('[data-open]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (window.pqOpenSheet) window.pqOpenSheet(b.dataset.open);
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
