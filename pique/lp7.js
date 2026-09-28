/* ============================================================
   PIQUE LP v7
   Dit bestand verplaatst voorwerpen en zet toestanden aan. Verder
   niets. Zonder JavaScript staat de hele pagina er gewoon.

   De regel die bepaalt wat je gebruikt:
     beweegt het omdat HIJ beweegt   -> scrollafstand is de klok
     beweegt het omdat de TIJD loopt -> alleen waar scrollen op slot
                                        staat, dus in de kaartlaag
     hoeft het alleen te ARRIVEREN   -> de ene reveal, en niets anders

   Pagina-instellingen (in een <script> hierboven):
     window.PQ7 = { slug, bedrijf, klant, campagne, cal, video,
                    video540, poster, meetUrl, terugbelUrl, logo,
                    kaart:{regels,ja,sub,lees} }
   ============================================================ */
(function () {
  'use strict';
  var C = window.PQ7 || {};
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches ||
             location.search.indexOf('statisch') > -1;
  var EASE = 'cubic-bezier(.16,1,.3,1)';

  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return [].slice.call(document.querySelectorAll(s)); };

  var gezien = {};
  function meet(stap, extra) {
    if (gezien[stap]) return; gezien[stap] = 1;
    var lading = JSON.stringify({ slug: C.slug || location.pathname, klant: C.klant || 'pique',
      campagne: C.campagne || '', stap: stap, extra: extra == null ? null : String(extra) });
    if (C.meetUrl && navigator.sendBeacon) navigator.sendBeacon(C.meetUrl, lading);
    else if (window.console && console.debug) console.debug('[pique]', stap, extra == null ? '' : extra);
  }
  window.pqMeet = meet;

  /* FLIP. Breekt alleen af als de BREEDTE verandert, dus bij draaien.
     Op iOS vuurt resize ook als de adresbalk inklapt. */
  function flip(el, van, ms, klaar) {
    var naar = el.getBoundingClientRect();
    if (!naar.width || !van.width) { if (klaar) klaar(); return; }
    var breed = innerWidth, af = false;
    el.style.transition = 'none';
    el.style.transform = 'translate(' +
      ((van.left + van.width / 2) - (naar.left + naar.width / 2)).toFixed(1) + 'px,' +
      ((van.top + van.height / 2) - (naar.top + naar.height / 2)).toFixed(1) + 'px) scale(' +
      (van.width / naar.width).toFixed(3) + ')';
    el.getBoundingClientRect();
    function stop() {
      if (af) return; af = true;
      removeEventListener('resize', bijDraai);
      el.style.transition = ''; el.style.transform = '';
      if (klaar) klaar();
    }
    function bijDraai() { if (innerWidth !== breed) stop(); }
    addEventListener('resize', bijDraai);
    requestAnimationFrame(function () {
      if (af) return;
      el.style.transition = 'transform ' + ms + 'ms ' + EASE;
      el.style.transform = '';
      setTimeout(stop, ms);
    });
  }

  function maakVideo() {
    var v = document.createElement('video');
    v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'auto';
    if (C.poster) v.poster = C.poster;
    var klein = C.video540 && matchMedia('(max-width:759px)').matches;
    v.src = klein ? C.video540 : C.video;
    return v;
  }
  function ontgrendel() {
    document.documentElement.className =
      document.documentElement.className.replace(' kaart-aan', '');
  }

  /* ── 00. DE KAARTLAAG ───────────────────────────────────── */
  function kaartlaag(klaar) {
    if (!C.kaart || location.search.indexOf('nokaart') > -1) return klaar(false);
    document.documentElement.className += ' kaart-aan';

    var regels = C.kaart.regels.map(function (r, i) {
      var stuk = r.split('*').map(function (seg, si) {
        return si % 2 ? '<span class="hl">' + seg + '</span>' : seg;
      }).join('');
      return '<span class="rg" style="--i:' + i + '">' + stuk + '</span>';
    }).join('');

    var el = document.createElement('div');
    el.id = 'kl';
    /* .klaarzetten wordt hier gezet, dus voordat er iets op het scherm
       staat. Zonder die klasse is het handschrift gewoon leesbaar. */
    el.innerHTML =
      '<div class="kl-podium">' +
        '<div class="pap' + (rust ? '' : ' klaarzetten') + '" id="dekaart">' +
          '<div class="kl-merk">' + (C.logo || '') + '<span>Persoonlijk</span></div>' +
          '<div class="inkt">' + regels + '</div></div>' +
        '<div class="kl-keuze" id="dekeuze">' +
          '<button class="knop" id="kja" type="button">' + C.kaart.ja + '</button>' +
          '<span class="kl-sub">' + C.kaart.sub + '</span></div>' +
        '<button class="kl-lees" id="klees" type="button">' + C.kaart.lees + '</button>' +
      '</div>';

    function inhangen() { document.body.appendChild(el); begin(); }
    if (document.body) inhangen(); else document.addEventListener('DOMContentLoaded', inhangen);

    function begin() {
      var kaart = el.querySelector('#dekaart'), keuze = el.querySelector('#dekeuze');
      var lees = el.querySelector('#klees'), af = false;
      var aantal = C.kaart.regels.length;

      /* De kaart landt nergens. In v6 vloog hij naar een nagemaakte map
         in de hero, en dan ligt er daarna een beige rechthoek op je
         scherm die niets voorstelt. Hier wordt hij weggelegd: hij komt
         een fractie naar je toe en verdwijnt, en daarachter staat de
         pagina. Het voorwerp blijft in zijn hand en niet op het scherm. */
      function sluit(metVideo, vEl) {
        if (af) return; af = true;
        meet(metVideo ? 'kaart-video' : 'kaart-lezen');
        el.classList.add('weg');
        el.style.pointerEvents = 'none';
        var gemeld = false;
        function afronden() {
          if (gemeld) return; gemeld = true;
          if (el.parentNode) el.parentNode.removeChild(el);
          if (metVideo && vEl) videolaag(vEl, function () { ontgrendel(); klaar(true); });
          else { ontgrendel(); klaar(false); }
        }
        if (!rust) {
          kaart.classList.add('weglegen');
          setTimeout(afronden, 620);
        } else {
          setTimeout(afronden, 60);
        }
      }

      /* Het geluid hangt aan de ontgrendeling binnen de klik zelf:
         play() gevolgd door pause() in het gebaar, want daarna mag het
         niet meer van iOS. */
      el.querySelector('#kja').addEventListener('click', function () {
        var v = null;
        if (C.video) {
          v = maakVideo();
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
        setTimeout(function () {
          keuze.classList.add('er'); meet('kaart-af');
        }, 420 + 200 + aantal * 340 + 420);
      }
      if (document.fonts && document.fonts.load) document.fonts.load('600 2rem Caveat').then(start, start);
      setTimeout(start, 1200);
    }
  }

  /* ── 01. DE VIDEOLAAG ───────────────────────────────────── */
  function videolaag(v, klaar) {
    meet('video-start');
    var el = document.createElement('div');
    el.id = 'vl';
    el.innerHTML =
      '<div class="doek"><img src="' + (C.poster || '') + '" alt=""></div>' +
      '<div class="v-bed"><span class="tel" id="vtel">0:00</span><span class="rek"></span>' +
        '<button class="v-over" id="vover" type="button">Overslaan</button></div>' +
      '<div class="v-balk" id="vbalk"></div>' +
      '<button class="v-geluid" id="vgel" type="button"><span>Tik voor geluid</span></button>';
    el.insertBefore(v, el.querySelector('.v-bed'));
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('er'); });

    var balk = el.querySelector('#vbalk'), tel = el.querySelector('#vtel');
    var over = el.querySelector('#vover'), gel = el.querySelector('#vgel');
    var weg = false;

    function mmss(s) { var m = Math.floor(s / 60), r = Math.floor(s % 60); return m + ':' + (r < 10 ? '0' : '') + r; }
    v.addEventListener('timeupdate', function () {
      if (!v.duration) return;
      balk.style.width = (v.currentTime / v.duration * 100) + '%';
      tel.textContent = mmss(v.duration - v.currentTime);
      if (v.currentTime > 60 && over.textContent === 'Overslaan') over.textContent = 'Verder lezen';
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
      el.classList.remove('er'); el.classList.add('weg');
      setTimeout(function () {
        if (el.parentNode) el.parentNode.removeChild(el);
        klaar();
      }, 440);
    }
  }

  /* ── 03. DE DATUM DIE BLIJFT STAAN ─────────────────────── */
  /* Het enige dat hier op scroll verandert is een cijfer. De balk
     kleeft onder de nav en de vondsten lopen eronder langs; op de
     derde slaat de datum terug naar 2023. Dat is de sprong in de tijd,
     en hij staat er als typografie in plaats van als een getekende lus.
     Geen scrub, dus een flick van 2000 px kan niets breken: elke
     eindtoestand is compleet. */
  function datumbalk() {
    var balk = $('.datumbalk'); if (!balk) return;
    var groot = balk.querySelector('.grootdatum'), wat = balk.querySelector('.wat');
    var vondsten = $$('.vondst');
    if (!groot || !vondsten.length) return;

    function zet(el) {
      var d = el.dataset.datum || '', w = el.dataset.wat || '';
      if (groot.textContent === d && wat.textContent === w) return;
      if (rust) { groot.textContent = d; wat.textContent = w; return; }
      balk.classList.add('wissel');
      setTimeout(function () {
        groot.textContent = d; wat.textContent = w;
        balk.classList.remove('wissel');
      }, 280);
    }
    zet(vondsten[0]);
    if (rust) return;

    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        zet(e.target);
        if (vondsten.indexOf(e.target) === vondsten.length - 1) meet('vondsten-uit');
      });
    }, { threshold: 0, rootMargin: '-38% 0px -46% 0px' });
    vondsten.forEach(function (v) { io.observe(v); });
  }

  /* ── 05. DE VIDEOREGEL BIJ DE ASK ───────────────────────── */
  /* Voor wie gelezen heeft in plaats van gekeken. Het geluid wordt ook
     hier binnen de klik ontgrendeld. */
  function videoregel() {
    var b = $('.videoregel'); if (!b || !C.video) { if (b) b.remove(); return; }
    b.addEventListener('click', function () {
      var v = maakVideo();
      try { var p = v.play(); if (p && p.then) p.then(function () { v.pause(); }, function () {}); } catch (e) {}
      meet('video-vanaf-ask');
      document.documentElement.className += ' kaart-aan';
      videolaag(v, function () { ontgrendel(); });
    });
  }

  /* ── DE ENE REVEAL ──────────────────────────────────────── */
  function onthullen() {
    var blokken = $$('.op');
    blokken.forEach(function (b) {
      [].slice.call(b.children).forEach(function (k, i) {
        k.style.setProperty('--dl', (Math.min(i, 2) * 90) + 'ms');
      });
    });
    var extra = $$('.namen, .hero');
    if (rust) {
      blokken.forEach(function (b) { b.classList.add('in'); });
      extra.forEach(function (b) { b.classList.add('in'); });
      warm(); return;
    }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        e.target.classList.add('in');
        /* De agenda laadt zodra het scharnier in beeld komt, ruim
           voordat hij op een knop kan drukken. */
        if (e.target.closest('.scharnier') || e.target.classList.contains('scharnier')) warm();
      });
    }, { threshold: 0, rootMargin: '0px 0px -12% 0px' });
    blokken.concat(extra).forEach(function (b) { io.observe(b); });
  }
  function warm() { if (window.pqWarmCal) window.pqWarmCal(); }

  /* ── DE NAV ─────────────────────────────────────────────── */
  function navigatie() {
    var nav = $('nav'), scharnier = $('.scharnier');
    var wacht = false;
    function meten() {
      wacht = false;
      var y = pageYOffset || document.documentElement.scrollTop;
      if (nav) {
        nav.classList.toggle('vast', y > innerHeight * .76);
        if (scharnier) nav.classList.toggle('toon',
          scharnier.getBoundingClientRect().bottom < innerHeight * .5);
      }
    }
    function tik() { if (wacht) return; wacht = true; requestAnimationFrame(meten); }
    addEventListener('scroll', tik, { passive: true });
    addEventListener('resize', tik);
    meten();
    /* Na een herlaad halverwege de pagina vuurt er geen scroll-event. */
    setTimeout(meten, 400); setTimeout(meten, 1200);
  }

  /* ── DE SHEET ───────────────────────────────────────────── */
  function sheet() {
    var sh = $('#sheet'); if (!sh) return;
    var calGeladen = false;

    function skeletWeg() { var s = $('#calskel'); if (s) s.classList.add('weg'); }
    function geenAgenda() {
      var tab = sh.querySelector('.sheet-tabs button[data-tab="plan"]');
      var pane = $('#pane-plan');
      if (tab) tab.remove(); if (pane) pane.remove();
      var tabs = sh.querySelector('.sheet-tabs'); if (tabs) tabs.style.display = 'none';
      var bel = $('#pane-bel'); if (bel) bel.classList.add('on');
    }
    function laadCal() {
      if (!C.cal) { geenAgenda(); return; }
      if (calGeladen) return; calGeladen = true;
      (function (X, A, L) { var p = function (a, ar) { a.q.push(ar); }; var d = X.document;
        X.Cal = X.Cal || function () { var cal = X.Cal; var ar = arguments;
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
    window.pqWarmCal = function () {
      if (calGeladen || !C.cal) return;
      if (window.requestIdleCallback) requestIdleCallback(laadCal, { timeout: 1500 });
      else setTimeout(laadCal, 400);
    };

    function tab(naam) {
      sh.querySelectorAll('.sheet-tabs button').forEach(function (b) {
        b.classList.toggle('on', b.dataset.tab === naam);
      });
      var p = $('#pane-plan'), b = $('#pane-bel');
      if (p) p.classList.toggle('on', naam === 'plan');
      if (b) b.classList.toggle('on', naam === 'bel');
      if (naam === 'plan') laadCal();
    }
    function open(welke) {
      sh.classList.add('open'); sh.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      tab(welke || 'plan'); meet('sheet-geopend', welke || 'plan');
    }
    function dicht() {
      sh.classList.remove('open'); sh.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
    window.pqOpenSheet = open;
    $$('[data-open="sheet"]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault(); meet('klik', b.dataset.doel || ''); open(b.dataset.tab);
      });
    });
    sh.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', dicht); });
    sh.querySelectorAll('.sheet-tabs button').forEach(function (b) {
      b.addEventListener('click', function () { tab(b.dataset.tab); });
    });
    addEventListener('keydown', function (e) { if (e.key === 'Escape' && sh.classList.contains('open')) dicht(); });

    var gekozen = '';
    var slots = $('#slots');
    if (slots) slots.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      [].slice.call(this.children).forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on'); gekozen = b.dataset.v;
    });
    var form = $('#belform');
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      var naam = (($('#bn') || {}).value || '').trim();
      var tel = (($('#bt') || {}).value || '').trim();
      if (!tel) return;
      meet('terugbelverzoek', tel);
      var lading = JSON.stringify({ naam: naam, tel: tel, wanneer: gekozen,
        bedrijf: C.bedrijf || '', slug: C.slug || '', klant: C.klant || 'pique',
        campagne: C.campagne || '' });
      /* Bewust text/plain: daarmee is het een simpele request en vraagt
         de browser geen preflight, die een Apps Script-webapp niet
         beantwoordt. */
      if (C.terugbelUrl) {
        fetch(C.terugbelUrl, { method: 'POST', body: lading, keepalive: true,
          headers: { 'Content-Type': 'text/plain;charset=utf-8' } }).catch(function () {
            if (navigator.sendBeacon) navigator.sendBeacon(C.terugbelUrl, new Blob([lading], { type: 'text/plain' }));
          });
      } else if (window.console && console.debug) console.debug('[pique] terugbelverzoek', lading);
      var voor = naam ? naam.split(' ')[0] : 'top';
      $('#pane-bel').innerHTML = '<div class="sheet-ok"><div class="hand">Genoteerd, ' + voor + '.</div>' +
        '<p>Ik bel je ' + (gekozen ? gekozen.toLowerCase() : 'zo snel als het schikt') + ' op ' + tel + '.</p></div>';
    });
  }

  /* ── OPSTARTEN ──────────────────────────────────────────── */
  function opstarten() {
    sheet();
    onthullen();
    videoregel();
    datumbalk();
    navigatie();
    kaartlaag(function (naVideo) {
      meet('pagina-open', naVideo ? 'na-video' : 'direct');
    });
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var t = document.querySelector(a.getAttribute('href')); if (!t) return;
        e.preventDefault();
        t.scrollIntoView({ behavior: rust ? 'auto' : 'smooth', block: 'start' });
      });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', opstarten);
  else opstarten();
})();
