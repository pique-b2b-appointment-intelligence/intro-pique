/* ============================================================
   PIQUE LP v3 — de trechter
   Volgorde: kaart -> video -> één zin -> bewijs -> de rest.
   Elke stap is meetbaar, want dit is een trechter en zonder meting
   weet je niet waar iemand afhaakt.
   ============================================================ */
(function () {
  'use strict';
  var C = window.PQ3 || {};
  /* ?statisch zet alle beweging uit. Voor controlefoto's en voor het geval
     iemand de pagina wil printen of nalopen zonder animatie. */
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches ||
             location.search.indexOf('statisch') > -1;
  var gezien = {};

  function meet(stap, extra) {
    if (gezien[stap]) return; gezien[stap] = 1;
    var lading = JSON.stringify({ slug: C.slug || location.pathname, stap: stap, extra: extra || null, t: Date.now() });
    if (C.meetUrl && navigator.sendBeacon) navigator.sendBeacon(C.meetUrl, lading);
    else if (window.console && console.debug) console.debug('[pique]', stap, extra || '');
  }

  /* ── 0. de kaart ────────────────────────────────────────── */
  function kaart(klaar) {
    if (!C.kaart || location.search.indexOf('nokaart') > -1) return klaar();
    document.documentElement.className += ' kaart-aan';

    var el = document.createElement('div');
    el.id = 'kaartlaag';
    el.innerHTML =
      '<div class="gloed"></div><div class="kaart-podium">' +
        '<div id="dekaart"><div class="kaart-merk">' + (C.logo || '') + '<span>Persoonlijk</span></div>' +
        '<div class="inkt" id="deinkt"></div></div>' +
        '<div class="kaart-keuze" id="dekeuze"><button class="knop" id="kaartja" type="button">' +
        C.kaart.ja + '</button><span class="kaart-sub">' + C.kaart.sub + '</span></div>' +
        '<button class="kaart-lees" id="kaartlees" type="button">' + C.kaart.lees + '</button>' +
      '</div>';

    function inhangen() { document.body.appendChild(el); begin(); }
    if (document.body) inhangen(); else document.addEventListener('DOMContentLoaded', inhangen);

    function begin() {
      var inkt = el.querySelector('#deinkt'), kaartEl = el.querySelector('#dekaart');
      var keuze = el.querySelector('#dekeuze'), lees = el.querySelector('#kaartlees');
      var af = false;

      var perRegel = C.kaart.regels.map(function (r) {
        var rg = document.createElement('span'); rg.className = 'rg';
        var tekens = [];
        r.split('|').forEach(function (deel, di) {
          if (di > 0) rg.appendChild(document.createElement('br'));
          /* Per deel opnieuw beginnen. Zonder deze regel bleef het laatste
             woord van de vorige regel openstaan en plakte 'op' vast aan
             'toevallig', dwars door de regelafbreking heen. */
          var woord = null;
          var lijst = [];
          deel.split('*').forEach(function (seg, si) {
            for (var i = 0; i < seg.length; i++) lijst.push({ c: seg[i], hl: si % 2 === 1 });
          });
          lijst.forEach(function (t) {
            var s = document.createElement('span');
            s.className = 'tk' + (t.hl ? ' hl' : ''); s.textContent = t.c;
            if (t.c === ' ') { woord = null; rg.appendChild(s); }
            else {
              if (!woord) { woord = document.createElement('span'); woord.className = 'wd'; rg.appendChild(woord); }
              woord.appendChild(s);
            }
            tekens.push(s);
          });
        });
        inkt.appendChild(rg);
        return tekens;
      });

      function sluit(metVideo) {
        if (af) return; af = true;
        meet(metVideo ? 'kaart-video' : 'kaart-lezen');
        el.classList.add('weg');
        el.style.pointerEvents = 'none';
        kaartEl.classList.add('vlieg');
        kaartEl.style.transform = 'translateY(-18px) scale(.9)';
        kaartEl.style.opacity = '0';
        setTimeout(function () {
          document.documentElement.className = document.documentElement.className.replace(' kaart-aan', '');
          if (el.parentNode) el.parentNode.removeChild(el);
          if (metVideo && C.video) video(klaar); else klaar();
        }, 620);
      }

      el.querySelector('#kaartja').addEventListener('click', function () { sluit(!!C.video); });
      lees.addEventListener('click', function () { sluit(false); });

      if (rust) {
        perRegel.forEach(function (r) { r.forEach(function (s) { s.classList.add('aan'); }); });
        kaartEl.classList.add('er'); keuze.classList.add('er'); lees.classList.add('er');
        return;
      }
      var gestart = false;
      function schrijven() {
        if (gestart) return; gestart = true;
        setTimeout(function () { kaartEl.classList.add('er'); }, 60);
        setTimeout(function () { lees.classList.add('er'); }, 900);
        setTimeout(function () {
          var r = 0, i = 0;
          (function stap() {
            if (r >= perRegel.length) { keuze.classList.add('er'); meet('kaart-af'); return; }
            var rij = perRegel[r];
            if (i >= rij.length) { r++; i = 0; return setTimeout(stap, 320); }
            rij[i].classList.add('aan');
            var p = rij[i].textContent === ' ' ? 13 : 28;
            i++; setTimeout(stap, p);
          })();
        }, 600);
      }
      if (document.fonts && document.fonts.load) document.fonts.load('600 2rem Caveat').then(schrijven, schrijven);
      setTimeout(schrijven, 1200);
    }
  }

  /* ── 0b. de video, meteen na 'laat maar zien' ───────────── */
  function video(klaar) {
    meet('video-start');
    var el = document.createElement('div');
    el.id = 'videolaag';
    el.innerHTML =
      '<video playsinline preload="auto" src="' + C.video + '"' +
        (C.poster ? ' poster="' + C.poster + '"' : '') + '></video>' +
      '<div class="video-over"><button type="button" id="videoover">Overslaan</button></div>' +
      '<div class="video-balk" id="videobalk"></div>';
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('er'); });

    var v = el.querySelector('video'), balk = el.querySelector('#videobalk'), weg = false;
    function dicht(reden) {
      if (weg) return; weg = true;
      meet('video-' + reden, v.currentTime ? Math.round(v.currentTime) + 's' : null);
      el.classList.remove('er');
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); klaar(); }, 420);
    }
    v.addEventListener('timeupdate', function () {
      if (v.duration) balk.style.width = (v.currentTime / v.duration * 100) + '%';
    });
    v.addEventListener('ended', function () { dicht('uitgekeken'); });
    el.querySelector('#videoover').addEventListener('click', function () { dicht('overgeslagen'); });
    /* Met geluid, want daar is hij voor opgenomen. Weigert de browser dat,
       dan starten we hem gedempt in plaats van helemaal niet. */
    v.muted = false;
    var p = v.play();
    if (p && p.catch) p.catch(function () { v.muted = true; v.play().catch(function () { dicht('geblokkeerd'); }); });
  }

  /* ── 1. de zin die zichzelf schrijft ────────────────────── */
  function zin() {
    var el = document.querySelector('.eenzin .zin');
    if (!el) return;
    var tekst = el.textContent; el.textContent = '';
    var tekens = [];
    tekst.split(' ').forEach(function (w, i, arr) {
      var wd = document.createElement('span'); wd.style.whiteSpace = 'nowrap';
      for (var j = 0; j < w.length; j++) {
        var s = document.createElement('span'); s.className = 'tk'; s.textContent = w[j];
        wd.appendChild(s); tekens.push(s);
      }
      el.appendChild(wd);
      if (i < arr.length - 1) {
        var sp = document.createElement('span'); sp.className = 'tk'; sp.textContent = ' ';
        el.appendChild(sp); tekens.push(sp);
      }
    });
    if (rust) { tekens.forEach(function (t) { t.classList.add('aan'); }); return; }
    new IntersectionObserver(function (es, ob) {
      if (!es[0].isIntersecting) return;
      ob.disconnect(); meet('zin-gelezen');
      var i = 0;
      (function stap() {
        var eind = Math.min(tekens.length, i + 2);
        for (; i < eind; i++) tekens[i].classList.add('aan');
        if (i < tekens.length) setTimeout(stap, 15);
      })();
    }, { threshold: .3 }).observe(el);
  }

  /* ── 2. alles wat in beeld mag komen ────────────────────── */
  function komen() {
    var stukken = document.querySelectorAll('[data-wacht], .slotsom');
    if (rust) { stukken.forEach(function (s) { s.classList.add('er'); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        e.target.style.setProperty('--wacht', (e.target.dataset.wacht || 0) + 'ms');
        e.target.classList.add('er');
      });
    }, { threshold: 0, rootMargin: '0px 0px -12% 0px' });
    stukken.forEach(function (s) { io.observe(s); });
  }

  /* ── 3. de dok, de balk, de bezwaren, en de leesdiepte ──── */
  function rest() {
    var dok = document.querySelector('.dok'), balk = document.querySelector('.voortgang');
    var slot = document.querySelector('.slotsec'), zinsec = document.querySelector('.eenzin');
    var uit = false;
    var x = dok && dok.querySelector('.weg');
    if (x) x.addEventListener('click', function () { uit = true; dok.classList.remove('er'); meet('dok-weg'); });

    var merken = [['.bewijs', 'bewijs'], ['.kost', 'kosten'], ['.doen', 'voorstel'],
                  ['.vraag', 'vraag'], ['.slotsec', 'slot']];
    var tik = false;
    function bij() {
      var h = document.documentElement.scrollHeight - innerHeight;
      if (balk) balk.style.width = (h > 0 ? Math.min(100, scrollY / h * 100) : 0) + '%';
      if (dok && !uit && zinsec && slot) {
        var na = zinsec.getBoundingClientRect().bottom < innerHeight * .4;
        var bijSlot = slot.getBoundingClientRect().top < innerHeight * .9;
        dok.classList.toggle('er', na && !bijSlot);
        if (na && !bijSlot) meet('dok-getoond');
      }
      merken.forEach(function (m) {
        var el = document.querySelector(m[0]);
        if (el && el.getBoundingClientRect().top < innerHeight * .65) meet(m[1]);
      });
    }
    addEventListener('scroll', function () {
      if (tik) return; tik = true;
      requestAnimationFrame(function () { bij(); tik = false; });
    }, { passive: true });
    bij();

    var v = document.querySelectorAll('.bezwaren details');
    v.forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (!d.open) return;
        meet('bezwaar', d.querySelector('summary').textContent.trim().slice(0, 60));
        v.forEach(function (a) { if (a !== d) a.open = false; });
      });
    });
    document.querySelectorAll('[data-doel]').forEach(function (a) {
      a.addEventListener('click', function () { meet('klik', a.dataset.doel); });
    });
  }

  function start() { zin(); komen(); rest(); meet('pagina-open'); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { kaart(start); });
  else kaart(start);
})();
