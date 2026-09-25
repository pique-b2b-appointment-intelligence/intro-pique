/* ============================================================
   PIQUE LP v5 — "Bewijsstuk"
   Dit bestand verplaatst één voorwerp en zet toestanden aan. Verder
   niets. Zonder JavaScript staat de hele pagina er gewoon: elke
   klasse hier voegt iets toe, niets verbergt tekst die er anders
   wel zou staan.

   De regel die bepaalt wat je gebruikt:
     beweegt het omdat HIJ beweegt  -> scrollafstand is de klok
     beweegt het omdat de TIJD loopt -> alleen waar scrollen op slot
                                        staat, dus in de kaartlaag
     hoeft het alleen te ARRIVEREN   -> de ene reveal, en niets anders

   Pagina-instellingen (in een <script> hierboven):
     window.PQ5 = { slug, bedrijf, klant, campagne, cal, video,
                    video540, poster, meetUrl, terugbelUrl, logo,
                    kaart:{regels,ja,sub,lees} }
   ============================================================ */
(function () {
  'use strict';
  var C = window.PQ5 || {};
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches ||
             location.search.indexOf('statisch') > -1;
  var EASE = 'cubic-bezier(.16,1,.3,1)';

  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return [].slice.call(document.querySelectorAll(s)); };

  /* ── meting ─────────────────────────────────────────────── */
  var gezien = {};
  function meet(stap, extra) {
    if (gezien[stap]) return; gezien[stap] = 1;
    var lading = JSON.stringify({ slug: C.slug || location.pathname, klant: C.klant || 'pique',
      campagne: C.campagne || '', stap: stap, extra: extra == null ? null : String(extra) });
    if (C.meetUrl && navigator.sendBeacon) navigator.sendBeacon(C.meetUrl, lading);
    else if (window.console && console.debug) console.debug('[pique]', stap, extra == null ? '' : extra);
  }
  window.pqMeet = meet;

  /* FLIP: meet waar iets staat, zet het terug naar waar het vandaan
     kwam, en laat het naar zijn eigen plek lopen. Breekt alleen af
     als de BREEDTE verandert, dus bij draaien. Op iOS vuurt resize
     ook als de adresbalk inklapt, en dat brak de vlucht in v4. */
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

  /* ── 1. DE KAARTLAAG ────────────────────────────────────── */
  /* Het enige moment op de pagina waarop wachten iets oplevert:
     scrollen staat op slot en hij kijkt naar het voorwerp dat op
     zijn bureau lag. De regels komen met een clip-path op, niet
     teken voor teken: vier animerende elementen in plaats van
     honderdveertig spans die elk een blur compositen. */
  function kaartlaag(klaar) {
    if (!C.kaart || location.search.indexOf('nokaart') > -1) {
      var sc = $('#slotcard'); if (sc) sc.classList.add('show');
      return klaar(false);
    }
    document.documentElement.className += ' kaart-aan';

    var regels = C.kaart.regels.map(function (r, i) {
      var stuk = r.split('*').map(function (seg, si) {
        return si % 2 ? '<span class="hl">' + seg + '</span>' : seg;
      }).join('');
      return '<span class="rg" style="--i:' + i + '">' + stuk + '</span>';
    }).join('');

    var el = document.createElement('div');
    el.id = 'kl';
    el.innerHTML =
      '<div class="waas"><img src="' + (C.poster || '') + '" alt=""></div>' +
      '<div class="kl-podium">' +
        '<div class="pap" id="dekaart"><div class="kl-merk">' + (C.logo || '') +
          '<span>Persoonlijk</span></div><div class="inkt" id="deinkt">' + regels + '</div></div>' +
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

      function sluit(metVideo, vEl) {
        if (af) return; af = true;
        meet(metVideo ? 'kaart-video' : 'kaart-lezen');
        el.classList.add('weg');
        el.style.pointerEvents = 'none';

        var slot = $('#slotcard'), plek = $('#slot');
        var klaarGemeld = false;
        function afronden() {
          if (klaarGemeld) return; klaarGemeld = true;
          if (el.parentNode) el.parentNode.removeChild(el);
          if (metVideo && vEl) videolaag(vEl, klaar);
          else { ontgrendel(); klaar(false); }
        }

        if (plek && !rust) {
          var a = kaart.getBoundingClientRect(), b = plek.getBoundingClientRect();
          kaart.classList.add('vlieg');
          kaart.style.transform = 'translate(' +
            ((b.left + b.width / 2) - (a.left + a.width / 2)).toFixed(1) + 'px,' +
            ((b.top + b.height / 2) - (a.top + a.height / 2)).toFixed(1) + 'px) scale(' +
            (b.width / a.width).toFixed(3) + ') rotate(-2.6deg)';
          kaart.style.opacity = '0';
          /* Ontgrendelen op transitionend, met een vangnet van 1200 ms.
             Alleen een timer die korter is dan de vlucht laat de pagina
             onder de bevroren transform wegschuiven; alleen transitionend
             laat de pagina permanent vastzitten als een frame mist. */
          kaart.addEventListener('transitionend', function (e) {
            if (e.propertyName === 'transform') afronden();
          });
          setTimeout(afronden, 1200);
        } else {
          el.style.opacity = '0'; el.style.transition = 'opacity .3s ease';
          setTimeout(afronden, rust ? 60 : 320);
        }
        setTimeout(function () { if (slot) slot.classList.add('show'); }, rust ? 0 : 600);
      }

      /* Het geluid hangt aan de ontgrendeling binnen de klik: play()
         gevolgd door pause() in het gebaar zelf, want daarna mag het
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
        /* De knoppen komen pas als de laatste letter staat: 200 ms
           aanloop plus 340 ms per regel plus 420 ms schrijftijd. */
        setTimeout(function () {
          keuze.classList.add('er'); meet('kaart-af');
        }, 420 + 200 + aantal * 340 + 420);
      }
      if (document.fonts && document.fonts.load) document.fonts.load('600 2rem Caveat').then(start, start);
      setTimeout(start, 1200);
    }
  }

  function ontgrendel() {
    document.documentElement.className =
      document.documentElement.className.replace(' kaart-aan', '');
  }

  function maakVideo() {
    var v = document.createElement('video');
    v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'auto';
    if (C.poster) v.poster = C.poster;
    var klein = C.video540 && matchMedia('(max-width:759px)').matches;
    v.src = klein ? C.video540 : C.video;
    return v;
  }

  /* ── 2. DE VIDEOLAAG ────────────────────────────────────── */
  /* Alle bediening in de onderste veilige zone, nooit bovenin: daar
     zit het eiland. Sluit met een fade, niet met een vlucht naar een
     portret: die rekenfout rekte het gezicht 42 procent uit. */
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
      /* Na een minuut is overslaan geen afhaken meer maar doorgaan. */
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
        ontgrendel(); klaar(true);
      }, 440);
    }
  }

  /* ── 3. DE PIN: het dossier gaat open ───────────────────── */
  /* Eén scrub (--open, één property, alleen transform) plus twee
     getrapte toestanden. Getrapt en niet gescrubd, want één flick op
     iOS legt 800 tot 2000 px af en slaat anders drie drempels tegelijk
     over. Elke eindtoestand is compleet op zichzelf, dus er gaat nooit
     informatie verloren aan scrollsnelheid. */
  function pin() {
    var sec = $('.vond'), box = $('.pin-box');
    if (!sec || !box) return null;
    box.classList.add('c');
    if (rust) {
      /* Zonder pin heeft de sectie geen scrollreis nodig. Dit is dezelfde
         lay-out als de reduced-motion-variant, zodat ?statisch laat zien
         wat iemand met bewegingsvoorkeur uit ook werkelijk krijgt. */
      box.style.setProperty('--open', 1);
      sec.style.height = 'auto';
      box.style.position = 'static'; box.style.height = 'auto';
      var la = $('.lade'); if (la) la.style.position = 'relative';
      return null;
    }
    if (matchMedia('(min-width:900px)').matches) {
      box.style.setProperty('--open', 1); return null;
    }
    box.classList.remove('c');
    var stand = '', vorigeF = 0, eerste = true;
    return function () {
      var r = sec.getBoundingClientRect();
      /* Een sticky kind scrubt over sectiehoogte min stickyhoogte,
         niet over de sectiehoogte. Per frame gemeten, nooit uit een
         gecachte offsetTop, want svh verandert met de adresbalk. */
      var stop = parseFloat(getComputedStyle(box).top) || 0;
      var reis = sec.offsetHeight - box.offsetHeight;
      if (reis <= 0) return;
      var f = (stop - r.top) / reis;
      f = f < 0 ? 0 : f > 1 ? 1 : f;

      box.style.setProperty('--open', Math.min(1, f / .26).toFixed(3));

      /* Hysterese van .03 zodat een trilling geen flikkering geeft. */
      var wil = stand;
      if (stand !== 'c' && f >= .62) wil = 'c';
      else if (stand === 'c' && f < .59) wil = 'b';
      if (wil !== 'c') {
        if (wil !== 'b' && f >= .30) wil = 'b';
        else if (wil === 'b' && f < .27) wil = '';
      }
      if (wil !== stand) {
        /* Bij een flick één frame zonder transitie, anders lopen er
           drie transities over elkaar heen. */
        if (!eerste && Math.abs(f - vorigeF) > .22) {
          box.classList.add('snel');
          setTimeout(function () { box.classList.remove('snel'); }, 40);
        }
        box.classList.remove('b', 'c');
        if (wil) box.classList.add(wil);
        stand = wil;
        if (wil === 'c') meet('dossier-uit');
      }
      vorigeF = f; eerste = false;
    };
  }

  /* ── 4. DE LADE: kleeft aan de onderrand ────────────────── */
  /* Ander mechanisme dan de pin, dus geen herhaling van hetzelfde
     trucje: hier bepaalt welk tekstblok in de middenband staat wat de
     lade laat zien. Getrapt, geen scrub, geen timer. */
  function lade() {
    var la = $('.lade'); if (!la) return;
    var stappen = $$('.doen .stap');
    if (rust) { la.dataset.stap = '3'; la.classList.add('in'); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var i = stappen.indexOf(e.target) + 1;
        if (i > Number(la.dataset.stap || 0)) la.dataset.stap = String(i);
        if (i === 3) meet('voorstel-uit');
      });
    }, { threshold: 0, rootMargin: '-45% 0px -45% 0px' });
    stappen.forEach(function (s) { io.observe(s); });

    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io2.unobserve(e.target); la.classList.add('in');
      });
    }, { threshold: 0, rootMargin: '0px 0px -10% 0px' });
    io2.observe(la);

    /* Wie er in één veeg voorbij gaat, landt alsnog op stap 3. */
    addEventListener('scroll', function vangnet() {
      if (la.getBoundingClientRect().bottom < 0) {
        la.dataset.stap = '3'; la.classList.add('in');
        removeEventListener('scroll', vangnet);
      }
    }, { passive: true });
  }

  /* ── 5. DE ENE REVEAL ───────────────────────────────────── */
  /* Eén recept, op sectieniveau, maximaal drie gestaggerde kinderen,
     daarna unobserve. Geen stagger per alinea: v4 had dertien
     varianten van dezelfde fade-up en dat is precies wat als
     sjabloon leest. */
  function onthullen() {
    var blokken = $$('.op');
    blokken.forEach(function (b) {
      [].slice.call(b.children).forEach(function (k, i) {
        k.style.setProperty('--dl', (Math.min(i, 2) * 90) + 'ms');
      });
    });
    if (rust) { blokken.forEach(function (b) { b.classList.add('in'); }); warm(); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        e.target.classList.add('in');
        /* De agenda begint met laden zodra het kantelpunt in beeld
           komt, ruim voordat hij op een knop kan drukken. */
        if (e.target.closest('.kantel')) warm();
      });
    }, { threshold: 0, rootMargin: '0px 0px -12% 0px' });
    blokken.forEach(function (b) { io.observe(b); });
  }
  function warm() { if (window.pqWarmCal) window.pqWarmCal(); }

  /* ── 6. DE NAV ──────────────────────────────────────────── */
  /* Het enige vaste ding op de pagina. De knop verschijnt pas na het
     kantelpunt, anders is hij de enige CTA boven de vouw en
     concurreert hij met de kaart. */
  function navigatie(pinTik) {
    var nav = $('nav'), kantel = $('.kantel');
    var wacht = false;
    function meten() {
      wacht = false;
      var y = pageYOffset || document.documentElement.scrollTop;
      if (nav) {
        nav.classList.toggle('vast', y > innerHeight * .74);
        if (kantel) nav.classList.toggle('toon', kantel.getBoundingClientRect().bottom < innerHeight * .5);
      }
      if (pinTik) pinTik();
    }
    function tik() { if (wacht) return; wacht = true; requestAnimationFrame(meten); }
    addEventListener('scroll', tik, { passive: true });
    addEventListener('resize', tik);
    meten();
    /* Na een herlaad halverwege de pagina vuurt er geen scroll-event,
       dus de nav zou wit op wit blijven staan. */
    setTimeout(meten, 400); setTimeout(meten, 1200);
  }

  /* ── 7. DE SHEET ────────────────────────────────────────── */
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

  /* ── 8. OPSTARTEN ───────────────────────────────────────── */
  function opstarten() {
    sheet();
    onthullen();
    lade();
    navigatie(pin());
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
