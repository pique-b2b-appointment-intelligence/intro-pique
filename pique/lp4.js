/* ============================================================
   PIQUE LP v4 — "De kaart schrijft verder"
   Eén voorwerp draagt de pagina. Dit bestand verplaatst dat voorwerp
   en laat het schrijven; verder zet het alleen dingen aan.

   Zonder JavaScript staat de hele pagina er gewoon: elke klasse hier
   voegt iets toe, niets verbergt tekst die er anders wel zou staan.

   Pagina-instellingen (in een <script> hierboven):
     window.PQ4 = { slug, bedrijf, klant, campagne, cal, video, video540,
                    poster, meetUrl, terugbelUrl, kaart:{regels,ja,sub,lees} }
   ============================================================ */
(function () {
  'use strict';
  var C = window.PQ4 || {};
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches ||
             location.search.indexOf('statisch') > -1;
  var EASE = 'cubic-bezier(.16,1,.3,1)';

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

  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return [].slice.call(document.querySelectorAll(s)); };

  /* Alle tekens vooraf onzichtbaar in de DOM, woorden in een nowrap-wikkel.
     Zo heeft het papier vanaf het begin zijn eindhoogte en breekt de browser
     niet midden in een woord af. Per regel opnieuw beginnen, anders plakt het
     eerste woord van de volgende regel aan het laatste van de vorige. */
  function zetTekens(doel, regels) {
    var alle = [];
    regels.forEach(function (r) {
      var rg = document.createElement('span');
      rg.className = 'rg';
      r.split('|').forEach(function (deel, di) {
        if (di > 0) rg.appendChild(document.createElement('br'));
        var woord = null;
        var lijst = [];
        deel.split('*').forEach(function (seg, si) {
          for (var i = 0; i < seg.length; i++) lijst.push({ c: seg[i], hl: si % 2 === 1 });
        });
        lijst.forEach(function (t) {
          var s = document.createElement('span');
          s.className = 'pc' + (t.hl ? ' hl' : '');
          s.textContent = t.c;
          if (t.c === ' ') { woord = null; rg.appendChild(s); }
          else {
            if (!woord) { woord = document.createElement('span'); woord.className = 'pw'; rg.appendChild(woord); }
            woord.appendChild(s);
          }
          alle.push(s);
        });
      });
      doel.appendChild(rg);
    });
    return alle;
  }

  /* Tijdgestuurd schrijven, nooit aan de scrollpositie: handschrift dat aan de
     duim hangt loopt achteruit als je terugscrolt en leest als een kapotte pagina. */
  function schrijf(tekens, tempo, klaar) {
    var i = 0, per = Math.max(1, Math.round(16 / tempo));
    (function stap() {
      var eind = Math.min(tekens.length, i + per);
      for (; i < eind; i++) tekens[i].classList.add('aan');
      if (i < tekens.length) setTimeout(stap, tempo);
      else if (klaar) klaar();
    })();
  }
  function alles(tekens) { tekens.forEach(function (t) { t.classList.add('aan'); }); }

  /* FLIP: meet waar iets staat, zet het terug naar waar het vandaan kwam, en
     laat het naar zijn eigen plek lopen. Draait iemand zijn telefoon tijdens de
     vlucht, dan klopt de landing niet meer, dus dan zetten we hem hard neer. */
  function flip(el, van, ms, klaar) {
    var naar = el.getBoundingClientRect();
    if (!naar.width || !van.width) { if (klaar) klaar(); return; }
    var sc = van.width / naar.width;
    var dx = (van.left + van.width / 2) - (naar.left + naar.width / 2);
    var dy = (van.top + van.height / 2) - (naar.top + naar.height / 2);
    el.style.transition = 'none';
    el.style.transform = 'translate(' + dx.toFixed(1) + 'px,' + dy.toFixed(1) + 'px) scale(' + sc.toFixed(3) + ')';
    el.getBoundingClientRect();
    var afgebroken = false;
    function stop() { afgebroken = true; el.style.transition = ''; el.style.transform = ''; if (klaar) klaar(); }
    addEventListener('resize', stop, { once: true });
    requestAnimationFrame(function () {
      if (afgebroken) return;
      el.style.transition = 'transform ' + ms + 'ms ' + EASE;
      el.style.transform = '';
      setTimeout(function () {
        if (afgebroken) return;
        removeEventListener('resize', stop);
        el.style.transition = '';
        if (klaar) klaar();
      }, ms);
    });
  }

  /* ── 1. DE KAARTLAAG ────────────────────────────────────── */
  function kaartlaag(klaar) {
    if (!C.kaart || location.search.indexOf('nokaart') > -1) {
      var sc = $('#slotcard'); if (sc) sc.classList.add('show');
      var hero = $('.hero'); if (hero) hero.classList.add('geland');
      return klaar(false);
    }
    document.documentElement.className += ' kaart-aan';

    var el = document.createElement('div');
    el.id = 'kl';
    el.innerHTML =
      '<div class="waas"><img src="' + (C.poster || '') + '" alt=""></div>' +
      '<div class="kl-podium">' +
        '<div class="pap" id="dekaart"><div class="kl-merk">' + (C.logo || '') +
          '<span>Persoonlijk</span></div><div class="inkt" id="deinkt"></div></div>' +
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
      var tekens = zetTekens(el.querySelector('#deinkt'), C.kaart.regels);

      function sluit(metVideo, vEl) {
        if (af) return; af = true;
        meet(metVideo ? 'kaart-video' : 'kaart-lezen');
        el.classList.add('weg');
        el.style.pointerEvents = 'none';

        var slot = $('#slotcard'), plek = $('#slot');
        if (plek && !rust) {
          var a = kaart.getBoundingClientRect(), b = plek.getBoundingClientRect();
          kaart.classList.add('vlieg');
          kaart.style.transform = 'translate(' + ((b.left + b.width / 2) - (a.left + a.width / 2)).toFixed(1) + 'px,' +
            ((b.top + b.height / 2) - (a.top + a.height / 2)).toFixed(1) + 'px) scale(' +
            (b.width / a.width).toFixed(3) + ') rotate(-2.6deg)';
          kaart.style.opacity = '0';
        } else {
          el.style.opacity = '0'; el.style.transition = 'opacity .3s ease';
        }
        setTimeout(function () { if (slot) slot.classList.add('show'); }, rust ? 0 : 620);
        setTimeout(function () {
          if (el.parentNode) el.parentNode.removeChild(el);
          if (metVideo && vEl) videolaag(vEl, klaar);
          else { ontgrendel(); klaar(false); }
        }, rust ? 300 : 960);
      }

      /* Het geluid hangt aan de ontgrendeling binnen de klik: play() gevolgd door
         pause() in het gebaar zelf, want daarna mag het niet meer van iOS. */
      el.querySelector('#kja').addEventListener('click', function () {
        var v = null;
        if (C.video) {
          v = maakVideo();
          try { var p = v.play(); if (p && p.then) p.then(function () { v.pause(); }, function () {}); } catch (e) {}
        }
        sluit(!!v, v);
      });
      lees.addEventListener('click', function () { sluit(false); });

      if (rust) { alles(tekens); kaart.classList.add('er'); keuze.classList.add('er'); lees.classList.add('er'); return; }
      var gestart = false;
      function start() {
        if (gestart) return; gestart = true;
        setTimeout(function () { kaart.classList.add('er'); }, 60);
        setTimeout(function () { lees.classList.add('er'); }, 900);
        /* Met de hand geschreven loopt een spatie sneller dan een letter, dus
           hier geen vast tempo maar per teken een eigen pauze. */
        setTimeout(function () {
          var i = 0;
          (function stap() {
            if (i >= tekens.length) { keuze.classList.add('er'); meet('kaart-af'); return; }
            var t = tekens[i++];
            t.classList.add('aan');
            setTimeout(stap, t.textContent === ' ' ? 14 : 30);
          })();
        }, 600);
      }
      if (document.fonts && document.fonts.load) document.fonts.load('600 2rem Caveat').then(start, start);
      setTimeout(start, 1200);
    }
  }

  function ontgrendel() {
    document.documentElement.className = document.documentElement.className.replace(' kaart-aan', '');
  }

  function maakVideo() {
    var v = document.createElement('video');
    v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'auto';
    if (C.poster) v.poster = C.poster;
    /* 540p op een telefoon, het origineel op een groot scherm. */
    var klein = C.video540 && matchMedia('(max-width:759px)').matches;
    v.src = klein ? C.video540 : C.video;
    return v;
  }

  /* ── 2. DE VIDEOLAAG ────────────────────────────────────── */
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

    function mmss(s) { var m = Math.floor(s / 60); var r = Math.floor(s % 60); return m + ':' + (r < 10 ? '0' : '') + r; }
    v.addEventListener('timeupdate', function () {
      if (!v.duration) return;
      balk.style.width = (v.currentTime / v.duration * 100) + '%';
      tel.textContent = mmss(v.duration - v.currentTime);
      /* Na een minuut is 'Overslaan' geen afhaken meer maar doorgaan. */
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
      naarPortret(el, v, function () { ontgrendel(); klaar(true); });
    }
  }

  /* De man uit de video wordt de foto naast de kaart. Wie hem overslaat ziet
     hetzelfde, dus de overgang is altijd dezelfde beweging. */
  function naarPortret(laag, v, klaar) {
    var doel = $('#portret'), foto = doel && doel.querySelector('img');
    if (!doel || rust) {
      laag.classList.remove('er');
      if (foto) foto.classList.add('er');
      setTimeout(function () { if (laag.parentNode) laag.parentNode.removeChild(laag); klaar(); }, 420);
      return;
    }
    var van = v.getBoundingClientRect(), naar = doel.getBoundingClientRect();
    laag.querySelector('.doek').style.transition = 'opacity .5s ease';
    laag.querySelector('.doek').style.opacity = '0';
    laag.querySelector('.v-bed').style.opacity = '0';
    laag.style.background = 'transparent';
    v.style.position = 'fixed';
    v.style.left = van.left + 'px'; v.style.top = van.top + 'px';
    v.style.width = van.width + 'px'; v.style.height = van.height + 'px';
    v.style.margin = '0'; v.style.borderRadius = '3px'; v.style.zIndex = '895';
    v.style.transformOrigin = 'top left';
    v.getBoundingClientRect();
    v.style.transition = 'transform .9s ' + EASE;
    v.style.transform = 'translate(' + (naar.left - van.left).toFixed(1) + 'px,' + (naar.top - van.top).toFixed(1) +
      'px) scale(' + (naar.width / van.width).toFixed(3) + ',' + (naar.height / van.height).toFixed(3) + ')';
    setTimeout(function () { if (foto) foto.classList.add('er'); }, 700);
    setTimeout(function () { if (laag.parentNode) laag.parentNode.removeChild(laag); klaar(); }, 1120);
  }

  /* ── 3. DE HERO: krabbel, pijl, en de krimp naar de hoek ── */
  function hero(naVideo) {
    var h = $('.hero'); if (!h) return;
    setTimeout(function () { h.classList.add('geland'); }, naVideo ? 120 : 700);

    var kr = $('.krabbel .tekst'), arw = $('.arw');
    if (kr && C.krabbel) {
      var t = zetTekens(kr, [C.krabbel]);
      if (rust) alles(t);
      else setTimeout(function () {
        schrijf(t, 26, function () { if (arw) arw.classList.add('er'); });
      }, naVideo ? 900 : 1600);
    } else if (arw) arw.classList.add('er');
    if (arw) {
      var p = arw.querySelector('path');
      if (p) { var l = Math.ceil(p.getTotalLength()); p.style.setProperty('--len', l); }
    }
    var foto = $('#portret img');
    if (foto && !naVideo) setTimeout(function () { foto.classList.add('er'); }, rust ? 0 : 1100);

    /* De kaart krimpt op de scrollfractie naar het kaartje linksboven.
       Dit is naast de journeylijn en de voortgangsbalk de enige gescrubde beweging. */
    var slot = $('#slotcard'), hoek = $('#hoek'), nav = $('nav');
    if (!slot || !hoek || rust) { if (hoek && !rust) hoek.classList.add('er'); return; }
    var aan = false, doel = 0, breed = 0;
    function ijk() {
      breed = innerWidth;
      doel = slot.offsetWidth ? (hoek.offsetWidth || 76) / slot.offsetWidth : .34;
    }
    ijk();
    function krimp() {
      if (innerWidth !== breed) ijk();
      var r = h.getBoundingClientRect();
      var uit = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height * 0.62)));
      if (uit <= 0) { slot.style.transform = 'rotate(-2.6deg)'; slot.style.opacity = ''; }
      else if (uit < .92) {
        var sc = 1 + (doel - 1) * uit;
        slot.style.transform = 'rotate(' + (-2.6 + (-5 + 2.6) * uit).toFixed(2) + 'deg) scale(' + sc.toFixed(3) + ')';
        slot.style.opacity = '';
      } else { slot.style.opacity = '0'; }
      var wil = uit >= .92;
      if (wil !== aan) {
        aan = wil;
        hoek.classList.toggle('er', wil);
        if (nav) nav.classList.toggle('hoekje', wil);
      }
    }
    krimp();
    return krimp;
  }

  /* ── 4. DE JOURNEYLIJN (uit v2, hergebruikt) ────────────── */
  function lijn(wrapSel) {
    var wrap = typeof wrapSel === 'string' ? $(wrapSel) : wrapSel; if (!wrap) return null;
    var svg = wrap.querySelector('.padlijn');
    var basis = svg && svg.querySelector('.basis'), voort = svg && svg.querySelector('.voort');
    if (!svg || !basis || !voort) return null;
    var dots = [].slice.call(wrap.querySelectorAll('.dot'));
    var totaal = 0;
    function bouw() {
      var pad = wrap.querySelector('.pad'); if (!pad || dots.length < 2) return;
      var pr = pad.getBoundingClientRect();
      svg.setAttribute('viewBox', '0 0 56 ' + pr.height);
      svg.style.height = pr.height + 'px';
      var pts = dots.map(function (d) {
        var r = d.getBoundingClientRect();
        return { x: 28, y: r.top + r.height / 2 - pr.top };
      });
      var d = 'M 28 ' + pts[0].y.toFixed(1);
      for (var i = 1; i < pts.length; i++) {
        var a = pts[i - 1], c = pts[i], my = ((a.y + c.y) / 2).toFixed(1);
        /* De krul: tussen halte 2 en 3 loopt de lijn zichtbaar terug, want daar
           ging Simon terug naar 2023. Dat is de enige plek waar hij dat doet. */
        if (wrap.dataset.krul && i === Number(wrap.dataset.krul)) {
          /* De lus loopt zichtbaar naar rechts en weer terug, want dat is de
             omweg die hij werkelijk liep. Hij blijft links van de tekst. */
          var hoog = Math.max(70, c.y - a.y);
          var u = (a.y + hoog * .32).toFixed(1), t = (a.y + hoog * .68).toFixed(1);
          d += ' C 46 ' + u + ', 88 ' + u + ', 88 ' + ((a.y + c.y) / 2).toFixed(1);
          d += ' C 88 ' + t + ', 46 ' + t + ', 28 ' + c.y.toFixed(1);
        } else {
          d += ' C 28 ' + my + ', 28 ' + my + ', 28 ' + c.y.toFixed(1);
        }
      }
      basis.setAttribute('d', d); voort.setAttribute('d', d);
      totaal = voort.getTotalLength();
      voort.style.strokeDasharray = totaal;
      bij();
    }
    function bij() {
      if (!totaal) return;
      var pad = wrap.querySelector('.pad'); if (!pad) return;
      var pr = pad.getBoundingClientRect(), trig = innerHeight * .52;
      var frac = Math.max(0, Math.min(1, (trig - pr.top) / Math.max(1, pr.height)));
      voort.style.strokeDashoffset = totaal * (1 - frac);
      dots.forEach(function (d) {
        var r = d.getBoundingClientRect();
        var h = d.closest('.halte'); if (h) h.classList.toggle('bereikt', r.top + r.height / 2 < trig);
      });
    }
    bouw();
    addEventListener('load', bouw);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(bouw);
    if (window.ResizeObserver) new ResizeObserver(bouw).observe(wrap);
    return { bouw: bouw, bij: bij };
  }

  /* ── 5. HET KANTELPUNT: de kaart komt terug en schrijft ─── */
  function kantelpunt() {
    var blok = $('.kantel'), brief = $('#brief'); if (!blok || !brief) return;
    var doel = brief.querySelector('.verder');
    var tekens = doel && C.kantel ? zetTekens(doel, C.kantel) : [];
    var hoek = $('#hoek'), bezig = false;

    function afmaken() {
      blok.classList.add('klaar');
      meet('kantelpunt-gelezen');
      if (hoek) setTimeout(function () { hoek.classList.add('er'); }, 400);
      /* Vanaf hier duurt het nog minstens twee blokken voordat hij op een
         knop drukt. Dat is het moment om de agenda stil te laten laden. */
      if (window.pqWarmCal) window.pqWarmCal();
    }
    if (rust) { alles(tekens); blok.classList.add('klaar'); return; }

    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting || bezig) return;
        bezig = true; io.disconnect();
        var van = hoek ? hoek.getBoundingClientRect() : null;
        if (van && van.width && hoek.classList.contains('er')) {
          hoek.classList.remove('er');
          flip(brief, van, 900, function () { setTimeout(function () { schrijf(tekens, 13, afmaken); }, 250); });
        } else {
          setTimeout(function () { schrijf(tekens, 13, afmaken); }, 200);
        }
      });
    }, { threshold: 0, rootMargin: '-30% 0px -30% 0px' });
    io.observe(brief);

    /* Wie er in één ruk voorbijscrolt krijgt de zin alsnog in één keer. */
    addEventListener('scroll', function vangnet() {
      if (bezig) { removeEventListener('scroll', vangnet); return; }
      if (brief.getBoundingClientRect().bottom < 0) {
        bezig = true; io.disconnect(); removeEventListener('scroll', vangnet);
        alles(tekens); afmaken();
      }
    }, { passive: true });
  }

  /* ── 6. ALLES WAT IN BEELD MAG KOMEN ────────────────────── */
  function onthullen() {
    var stukken = $$('.halte, .krul, .kost, .ask, .gezicht, .wijzer, .namen, .trechter');
    if (rust) { stukken.forEach(function (s) { s.classList.add('in'); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        e.target.classList.add('in');
        /* De pijl bij het voorstel wijst naar het kaartje linksboven. Dat
           kaartje wiebelt één keer terug, zodat het een voorwerp blijft en
           geen plaatje. */
        if (e.target.classList.contains('wijzer')) {
          var hk = $('#hoek');
          if (hk && hk.classList.contains('er')) setTimeout(function () {
            hk.classList.add('wiebel');
            setTimeout(function () { hk.classList.remove('wiebel'); }, 640);
          }, 750);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px -12% 0px' });
    stukken.forEach(function (s) { io.observe(s); });
    /* De regels in de ask en de namen komen na elkaar op, niet tegelijk. */
    $$('.ask li').forEach(function (li, i) { li.style.setProperty('--dl', (i * 120) + 'ms'); });
    $$('.kost .zweef').forEach(function (z, i) { z.style.setProperty('--dl', (i * 150) + 'ms'); });
    $$('.namen span').forEach(function (s, i) { s.style.setProperty('--dl', (i * 80) + 'ms'); });
    $$('.tl-i').forEach(function (t, i) { t.style.setProperty('--dl', (i * 250) + 'ms'); });
  }

  /* ── 7. DE SHEET (uit v2) ───────────────────────────────── */
  function sheet() {
    var sh = $('#sheet'); if (!sh) return function () {};
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
    /* De agenda begint met laden zodra het kantelpunt voorbij is, ruim voordat
       hij op een knop kan drukken. De sheet staat dan buiten beeld maar heeft
       wel afmetingen, dus cal kan gewoon renderen. */
    window.pqWarmCal = function () {
      if (calGeladen || !C.cal) return;
      if (window.requestIdleCallback) requestIdleCallback(laadCal, { timeout: 1500 });
      else setTimeout(laadCal, 400);
    };

    function tab(naam) {
      sh.querySelectorAll('.sheet-tabs button').forEach(function (b) { b.classList.toggle('on', b.dataset.tab === naam); });
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
      b.addEventListener('click', function (e) { e.preventDefault(); meet('klik', b.dataset.doel || ''); open(b.dataset.tab); });
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
      var naam = ($('#bn') || {}).value || '', tel = ($('#bt') || {}).value || '';
      naam = naam.trim(); tel = tel.trim();
      if (!tel) return;
      meet('terugbelverzoek', tel);
      var lading = JSON.stringify({ naam: naam, tel: tel, wanneer: gekozen,
        bedrijf: C.bedrijf || '', slug: C.slug || '', klant: C.klant || 'pique', campagne: C.campagne || '' });
      /* Bewust text/plain: daarmee is het een simpele request en vraagt de
         browser geen preflight, die een Apps Script-webapp niet beantwoordt. */
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
    return dicht;
  }

  /* ── 8. DE VASTE LAGEN ──────────────────────────────────── */
  /* Eén scrollafhandeling voor de hele pagina. Alles wat aan de scrollpositie
     hangt wordt hier uitgelezen en pas in de volgende frame geschreven, zodat
     de browser niet per element opnieuw hoeft te meten. */
  function lagen(geefKrimp, lijnen) {
    var bar = $('.mbar'), nav = $('nav'), hoek = $('#hoek'), dok = $('.dok');
    var ask = $('#ask'), slot = $('#sluit');
    var dokWeg = false, dokEr = false, wacht = false;

    if (hoek) hoek.addEventListener('click', function () {
      meet('hoekkaart-terug');
      hoek.classList.add('wiebel');
      setTimeout(function () { hoek.classList.remove('wiebel'); }, 640);
      scrollTo({ top: 0, behavior: rust ? 'auto' : 'smooth' });
    });
    var wegknop = dok && dok.querySelector('.weg');
    if (wegknop) wegknop.addEventListener('click', function () {
      dokWeg = true; dok.classList.remove('er'); meet('dok-weggeklikt');
    });

    function meten() {
      wacht = false;
      var y = pageYOffset || document.documentElement.scrollTop;

      if (bar) {
        var hoog = document.documentElement.scrollHeight - innerHeight;
        bar.style.width = (hoog > 0 ? Math.min(100, (y / hoog) * 100) : 0) + '%';
      }
      if (nav) {
        nav.classList.toggle('vast', y > innerHeight * .6);
        nav.classList.toggle('toon', y > innerHeight * 1.2);
      }
      /* De dock komt pas op als hij het aanbod voorbij is: eerder is het een
         banner, daarna is het een antwoord op wat hij net gelezen heeft. */
      if (dok && !dokWeg && ask) {
        var wil = ask.getBoundingClientRect().bottom < innerHeight * .4;
        if (slot && slot.getBoundingClientRect().top < innerHeight * .85) wil = false;
        if (wil !== dokEr) {
          dokEr = wil; dok.classList.toggle('er', wil);
          /* --dock reserveert de ruimte onder het slot en de footer, zodat de
             dock nergens over tekst valt. */
          document.documentElement.style.setProperty('--dock', wil ? '4.6rem' : '0px');
          if (wil) meet('dok-getoond');
        }
      }
      var k = geefKrimp && geefKrimp(); if (k) k();
      lijnen.forEach(function (l) { l.bij(); });
    }
    function tik() { if (wacht) return; wacht = true; requestAnimationFrame(meten); }
    addEventListener('scroll', tik, { passive: true });
    addEventListener('resize', function () { lijnen.forEach(function (l) { l.bouw(); }); tik(); });
    meten();
    setTimeout(meten, 400); setTimeout(meten, 1200);
  }

  /* ── 9. OPSTARTEN ───────────────────────────────────────── */
  function opstarten() {
    sheet();
    $$('.arw path, .wijzer svg path').forEach(function (pd) {
      try { pd.style.setProperty('--len', Math.ceil(pd.getTotalLength())); } catch (e) {}
    });
    onthullen();
    var lijnen = $$('[data-pad]').map(lijn).filter(Boolean);
    kantelpunt();

    var krimp = null;
    lagen(function () { return krimp; }, lijnen);

    /* De kaartlaag gaat als eerste open en geeft pas terug of er een video
       tussen zat; de hero weet daardoor of hij nog moet landen of al mag staan. */
    kaartlaag(function (naVideo) {
      krimp = hero(naVideo);
      lijnen.forEach(function (l) { l.bouw(); });
      meet('pagina-open', naVideo ? 'na-video' : 'direct');
    });

    /* Ankers lopen zacht, behalve voor wie dat heeft uitgezet. */
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
