/* ============================================================
   PIQUE LP v3 — de choreografie
   Niets staat er al. Alles wordt neergelegd op het moment dat hij kijkt,
   en in de volgorde waarin iemand het ook echt zou doen: eerst het papier,
   dan het handschrift erbij.
   Alles uit onder prefers-reduced-motion. Zonder JS staat de hele pagina er
   gewoon, want de klassen zetten alleen iets aan, nooit iets uit.
   ============================================================ */
(function () {
  'use strict';
  var C = window.PQ3 || {};
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── 0. de kaart die zichzelf schrijft ──────────────────── */
  function kaartlaag(klaar) {
    if (!C.kaart || location.search.indexOf('nokaart') > -1) return klaar(false);
    var regels = C.kaart.regels;
    document.documentElement.className += ' kaart-aan';

    var el = document.createElement('div');
    el.id = 'kaartlaag';
    el.innerHTML =
      '<div class="gloed"></div><div class="kaart-podium">' +
        '<div class="papier" id="dekaart"><div class="kaart-merk">' + (C.logo || '') +
          '<span>Persoonlijk</span></div><div class="inkt" id="deinkt"></div></div>' +
        '<div class="kaart-keuze" id="dekeuze"><button class="knop" id="kaartja" type="button">' +
          C.kaart.ja + '</button><span class="kaart-sub">' + C.kaart.sub + '</span></div>' +
        '<button class="kaart-lees" id="kaartlees" type="button">' + C.kaart.lees + '</button>' +
      '</div>';

    function inhangen() { document.body.appendChild(el); begin(); }
    if (document.body) inhangen();
    else document.addEventListener('DOMContentLoaded', inhangen);

    function begin() {
      var inkt = el.querySelector('#deinkt');
      var kaart = el.querySelector('#dekaart');
      var keuze = el.querySelector('#dekeuze');
      var lees = el.querySelector('#kaartlees');
      var gedaan = false;

      /* Alle tekens staan er meteen in, alleen onzichtbaar. Daardoor heeft de
         kaart vanaf het begin zijn eindhoogte en verspringt er niets. */
      var perRegel = regels.map(function (r) {
        var rg = document.createElement('span');
        rg.className = 'rg';
        var tekens = [], woord = null;
        r.split('|').forEach(function (deel, di) {
          if (di > 0) rg.appendChild(document.createElement('br'));
          var lijst = [];
          deel.split('*').forEach(function (seg, si) {
            for (var i = 0; i < seg.length; i++) lijst.push({ c: seg[i], hl: si % 2 === 1 });
          });
          lijst.forEach(function (t) {
            var s = document.createElement('span');
            s.className = 'tk' + (t.hl ? ' hl' : '');
            s.textContent = t.c;
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
        if (gedaan) return; gedaan = true;
        el.classList.add('weg');
        var plek = document.getElementById('kaartplek');
        if (!plek) { el.style.opacity = 0; setTimeout(function () { af(metVideo); }, 600); return; }
        var a = kaart.getBoundingClientRect(), b = plek.getBoundingClientRect();
        var sc = b.width / a.width;
        kaart.classList.add('vlieg');
        kaart.style.transform = 'translate(' + ((b.left + b.width / 2) - (a.left + a.width / 2)).toFixed(1) + 'px,' +
          ((b.top + b.height / 2) - (a.top + a.height / 2)).toFixed(1) + 'px) scale(' + sc.toFixed(3) + ') rotate(-2.4deg)';
        kaart.style.opacity = '0';
        setTimeout(function () {
          var g = document.getElementById('gelandekaart');
          if (g) g.classList.add('er');
        }, 620);
        setTimeout(function () { af(metVideo); }, 980);
      }
      function af(metVideo) {
        document.documentElement.className = document.documentElement.className.replace(' kaart-aan', '');
        if (el.parentNode) el.parentNode.removeChild(el);
        klaar(true);
        if (metVideo && window.pq3Video) window.pq3Video();
      }

      el.querySelector('#kaartja').addEventListener('click', function () { sluit(!!C.video); });
      lees.addEventListener('click', function () { sluit(false); });

      if (rust) {
        perRegel.forEach(function (r) { r.forEach(function (s) { s.classList.add('aan'); }); });
        kaart.classList.add('er'); keuze.classList.add('er'); lees.classList.add('er');
        return;
      }
      var gestart = false;
      function schrijven() {
        if (gestart) return; gestart = true;
        setTimeout(function () { kaart.classList.add('er'); }, 60);
        setTimeout(function () { lees.classList.add('er'); }, 900);
        setTimeout(function () {
          var r = 0, i = 0;
          (function stap() {
            if (r >= perRegel.length) { keuze.classList.add('er'); return; }
            var rij = perRegel[r];
            if (i >= rij.length) { r++; i = 0; return setTimeout(stap, 330); }
            rij[i].classList.add('aan');
            var pauze = rij[i].textContent === ' ' ? 13 : 29;
            i++; setTimeout(stap, pauze);
          })();
        }, 600);
      }
      if (document.fonts && document.fonts.load) document.fonts.load('600 2rem Caveat').then(schrijven, schrijven);
      setTimeout(schrijven, 1200);
    }
  }

  /* ── 1. alles wat wordt neergelegd ──────────────────────── */
  function choreografie() {
    var stukken = document.querySelectorAll('[data-leg]');
    if (rust) { stukken.forEach(function (s) { s.classList.add('er'); }); return; }

    /* Een groep krijgt zijn vertraging van zijn plek in de groep, zodat het
       lijkt alsof iemand ze na elkaar neerlegt in plaats van tegelijk. */
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        io.unobserve(el);
        setTimeout(function () { el.classList.add('er'); }, Number(el.dataset.leg) || 0);
      });
    }, { threshold: 0, rootMargin: '0px 0px -14% 0px' });
    stukken.forEach(function (s) { io.observe(s); });
  }

  /* ── 2. de lijn die de vellen verbindt ──────────────────── */
  function verbinding() {
    var svg = document.querySelector('.verbinding');
    var stapel = document.querySelector('.stapel');
    if (!svg || !stapel) return;
    var pad = svg.querySelector('path');

    function teken() {
      var vellen = [].slice.call(stapel.querySelectorAll('.vel'));
      if (vellen.length < 2) return;
      var r = stapel.getBoundingClientRect();
      svg.setAttribute('viewBox', '0 0 ' + r.width + ' ' + r.height);
      var punten = vellen.map(function (v) {
        var b = v.getBoundingClientRect();
        return { x: b.left + b.width / 2 - r.left, y: b.top + b.height / 2 - r.top };
      });
      var d = 'M ' + punten[0].x.toFixed(1) + ' ' + punten[0].y.toFixed(1);
      for (var i = 1; i < punten.length; i++) {
        var a = punten[i - 1], c = punten[i], my = ((a.y + c.y) / 2).toFixed(1);
        d += ' C ' + a.x.toFixed(1) + ' ' + my + ', ' + c.x.toFixed(1) + ' ' + my + ', ' +
             c.x.toFixed(1) + ' ' + c.y.toFixed(1);
      }
      pad.setAttribute('d', d);
      var len = Math.ceil(pad.getTotalLength());
      pad.style.setProperty('--len', len);
    }
    teken();
    addEventListener('load', teken);
    if (window.ResizeObserver) new ResizeObserver(teken).observe(stapel);
    if (rust) { svg.classList.add('er'); return; }
    new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { teken(); svg.classList.add('er'); }
    }, { threshold: .55 }).observe(stapel);
  }

  /* ── 3. de kantelzin typt zichzelf ──────────────────────── */
  function typen() {
    var el = document.querySelector('.getypt');
    if (!el) return;
    var tekst = el.textContent;
    el.textContent = '';
    var tekens = [];
    tekst.split(' ').forEach(function (w, i, arr) {
      var wd = document.createElement('span');
      wd.style.whiteSpace = 'nowrap';
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
      ob.disconnect();
      var i = 0;
      (function stap() {
        var eind = Math.min(tekens.length, i + 2);
        for (; i < eind; i++) tekens[i].classList.add('aan');
        if (i < tekens.length) setTimeout(stap, 16);
      })();
    }, { threshold: 0, rootMargin: '-25% 0px -25% 0px' }).observe(el);
  }

  /* ── 4. de onderstreping in de kop ──────────────────────── */
  function streep() {
    var p = document.querySelector('.markeer path');
    if (!p) return;
    var l = Math.ceil(p.getTotalLength());
    p.style.strokeDasharray = l;
    p.style.strokeDashoffset = rust ? 0 : l;
    if (rust) return;
    setTimeout(function () {
      p.style.transition = 'stroke-dashoffset 1s cubic-bezier(.16,1,.3,1)';
      p.style.strokeDashoffset = 0;
    }, 260);
  }

  /* ── 5. voortgang, en de vragen één tegelijk ────────────── */
  function rest() {
    var balk = document.querySelector('.voortgang');
    if (balk) {
      var tik = false;
      addEventListener('scroll', function () {
        if (tik) return; tik = true;
        requestAnimationFrame(function () {
          var h = document.documentElement.scrollHeight - innerHeight;
          balk.style.width = (h > 0 ? Math.min(100, scrollY / h * 100) : 0) + '%';
          tik = false;
        });
      }, { passive: true });
    }
    var v = document.querySelectorAll('.vragen details');
    v.forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (d.open) v.forEach(function (a) { if (a !== d) a.open = false; });
      });
    });
  }

  function start(naKaart) {
    choreografie(); verbinding(); typen(); rest();
    if (naKaart) streep();
    else setTimeout(streep, 400);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { kaartlaag(start); });
  } else { kaartlaag(start); }
})();
