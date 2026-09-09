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


  /* ── 0. de intro. Draait elke keer dat de pagina opengaat. ── */
  (function () {
    var intro = $('#intro');
    if (!intro) return;
    var overslaan = rust || location.search.indexOf('nointro') > -1;

    function sluiten(reden) {
      if (intro.dataset.klaar) return;
      intro.dataset.klaar = '1';
      document.body.classList.remove('introbezig');
      tik(reden);
      intro.classList.add('weg');
      setTimeout(function () { intro.classList.add('uit'); }, 950);
    }

    if (overslaan) {
      intro.classList.add('uit');
      intro.dataset.klaar = '1';
      document.body.classList.remove('introbezig');
      return;
    }
    document.body.classList.add('introbezig');
    /* Geen tijdslot: de laag blijft staan tot iemand het zegel verbreekt. Een
       voorstel dat vanzelf opengaat is geen voorstel dat je hebt geopend. */
    function openen(reden) {
      if (intro.dataset.klaar) return;
      intro.classList.add('drukt');
      setTimeout(function () {
        intro.classList.remove('drukt');
        intro.classList.add('opent');
        setTimeout(function () { sluiten(reden); }, 620);
      }, 130);
    }
    var slot = $('.slot');
    if (slot) slot.addEventListener('click', function () { openen('slot-geopend'); });
    $('.intro-skip').addEventListener('click', function () { openen('intro-overgeslagen'); });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape') openen('intro-overgeslagen');
    });
  })();

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
    var balk = $('.bar-voortgang');
    if (balk) {
      var hoog = document.body.scrollHeight - innerHeight;
      balk.style.width = (hoog > 0 ? Math.min(100, (y / hoog) * 100) : 100) + '%';
    }
  }
  addEventListener('scroll', bijScroll, { passive: true });
  addEventListener('resize', bijScroll);

  /* ── 4. de volumeschuif ─────────────────────────────────── */
  var staffel = window.PQ_STAFFEL || {};
  var kiesKnoppen = $$('.kies button[data-v]');
  var wieKnoppen = $$('.kies button[data-w]');
  /* Wie er nabelt verandert de prijs en of er een garantie op zit. Een trede
     mag daarom velden hebben met _zelf erachter. Staan die er niet, dan
     gedraagt de schuif zich zoals hij altijd deed. */
  var wie = window.PQ_OPVOLGING || 'met';
  function zetVolume(sleutel) {
    var d = staffel[sleutel];
    if (!d) return;
    kiesKnoppen.forEach(function (b) { b.classList.toggle('aan', b.dataset.v === sleutel); });
    wieKnoppen.forEach(function (b) { b.classList.toggle('aan', b.dataset.w === wie); });
    var toon = {};
    Object.keys(d).forEach(function (k) {
      if (k.slice(-5) !== '_zelf') toon[k] = d[k];
    });
    if (wie === 'zelf') Object.keys(d).forEach(function (k) {
      if (k.slice(-5) === '_zelf') toon[k.slice(0, -5)] = d[k];
    });
    Object.keys(toon).forEach(function (k) {
      $$('[data-prijs="' + k + '"]').forEach(function (el) { el.textContent = toon[k]; });
    });
    window.PQ_VOLUME = sleutel;
    window.PQ_OPVOLGING = wie;
    tik('volume-' + sleutel + '-' + wie);
  }
  kiesKnoppen.forEach(function (b) {
    b.addEventListener('click', function () { zetVolume(b.dataset.v); });
  });
  wieKnoppen.forEach(function (b) {
    b.addEventListener('click', function () {
      wie = b.dataset.w;
      zetVolume(window.PQ_VOLUME || String(window.PQ_ADVIES || ''));
    });
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

  /* ── 6. de keuze, het ondertekenen en het verzenden ───── */
  var form = $('.akkoord');
  function jaKnop() {
    return (form && form.dataset.jaKnop) || 'Ondertekenen en verzenden';
  }
  var doek = $('.hb-vlak');
  var ctx = doek ? doek.getContext('2d') : null;
  var getekend = false;

  /* De canvas is groot opgezet en wordt door de css geschaald, anders is de lijn
     op een scherm met hoge dichtheid korrelig. */
  function penKlaar() {
    if (!ctx) return;
    ctx.lineWidth = 4.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = getComputedStyle(document.documentElement)
      .getPropertyValue('--hand-ink').trim() || '#1B2540';
  }
  function punt(e) {
    var r = doek.getBoundingClientRect();
    return { x: (e.clientX - r.left) * (doek.width / r.width),
             y: (e.clientY - r.top) * (doek.height / r.height) };
  }
  if (doek) {
    penKlaar();
    var tekent = false;
    doek.addEventListener('pointerdown', function (e) {
      tekent = true; getekend = true;
      doek.setPointerCapture(e.pointerId);
      doek.classList.remove('mis');
      var p = punt(e); ctx.beginPath(); ctx.moveTo(p.x, p.y);
      tik('handtekening');
    });
    doek.addEventListener('pointermove', function (e) {
      if (!tekent) return;
      var p = punt(e); ctx.lineTo(p.x, p.y); ctx.stroke();
    });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (n) {
      doek.addEventListener(n, function () { tekent = false; });
    });
    $('.hb-wis').addEventListener('click', function () {
      ctx.clearRect(0, 0, doek.width, doek.height); getekend = false; penKlaar();
    });
  }

  /* Handtekening en voorwaarden horen alleen bij een ja. Wie eerst dossiers wil
     of gebeld wil worden tekent niets. */
  function zetKeuze() {
    var g = $('input[name="keuze"]:checked');
    var soort = g ? g.value : 'ja';
    $$('[data-alleen]').forEach(function (el) {
      el.hidden = el.dataset.alleen !== soort;
    });
    var k = $('.verzend .knop');
    /* Staat er geen handtekening op de pagina, dan onderteken je ook niets.
       De knop heet dan zoals data-ja-knop op het formulier zegt. */
    k.textContent = soort === 'ja' ? jaKnop() : 'Verzenden';
    /* Wie gebeld wil worden zonder nummer achter te laten, wordt niet gebeld. */
    var tel = $('#ak-tel');
    tel.required = soort === 'bellen';
    $('[data-tel-l]').textContent = soort === 'bellen' ? 'Telefoonnummer' : 'Telefoonnummer, mag ook leeg';
    window.PQ_KEUZE = soort;
  }
  $$('input[name="keuze"]').forEach(function (r) {
    r.addEventListener('change', function () { zetKeuze(); tik('keuze-' + r.value); });
  });
  if (form) zetKeuze();

  function melden(tekst, veld) {
    var f = $('.fout');
    f.textContent = tekst; f.hidden = false;
    if (veld) { veld.classList.add('mis'); veld.focus({ preventScroll: true }); }
    f.scrollIntoView({ behavior: rust ? 'auto' : 'smooth', block: 'center' });
  }

  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    $('.fout').hidden = true;
    $$('.mis').forEach(function (el) { el.classList.remove('mis'); });

    var soort = window.PQ_KEUZE || 'ja';
    var naam = $('#ak-naam'), mail = $('#ak-mail');
    if (!naam.value.trim()) return melden('Vul je naam even in.', naam);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail.value.trim()))
      return melden('Dat mailadres klopt nog niet. Zonder adres kan ik je geen kopie sturen.', mail);
    var vink = $('.vink input');
    if (soort === 'ja') {
      if (doek && !getekend) { doek.classList.add('mis'); return melden('Zet even je handtekening in het vak.'); }
      if (vink && !vink.checked) return melden('Zet het vinkje bij de algemene voorwaarden.', vink);
    }
    var tel = $('#ak-tel');
    if (soort === 'bellen' && tel.value.replace(/\D/g, '').length < 8)
      return melden('Vul een telefoonnummer in, anders kunnen we je niet bellen.', tel);

    var knop = $('.verzend .knop');
    knop.disabled = true; knop.textContent = 'Bezig met verzenden';

    var lading = {
      soort: 'akkoord', keuze: soort,
      naam: naam.value.trim(), functie: $('#ak-functie').value.trim(),
      email: mail.value.trim(), tel: $('#ak-tel').value.trim(),
      opmerking: $('#ak-opm').value.trim(), wanneer: $('#ak-wanneer').value.trim(),
      voorwaarden: !!(soort === 'ja' && vink && vink.checked),
      handtekening: soort === 'ja' && doek && getekend ? doek.toDataURL('image/png') : '',
      volume: window.PQ_VOLUME || '', opvolging: window.PQ_OPVOLGING || '', bedrag: ($('[data-prijs="bedrag"]') || {}).textContent || '',
      looptijd: ($('[data-prijs="looptijd"]') || {}).textContent || '',
      garantie: ($('[data-prijs="garantie"]') || {}).textContent || '',
      bedrijf: window.PQ_BEDRIJF, slug: SLUG, klant: window.PQ_KLANT,
      campagne: window.PQ_CAMPAGNE || 'voorstel', url: location.href
    };

    tik('verzonden-' + soort);
    flush('akkoord');

    var doel = window.PQ_AKKOORD_URL || '';
    var klaar = function (gelukt, reden) {
      if (!gelukt) {
        knop.disabled = false;
        knop.textContent = soort === 'ja' ? jaKnop() : 'Verzenden';
        if (console && console.warn && reden) console.warn('[pique] akkoord geweigerd: ' + reden);
        return melden('Het versturen lukte niet. Mail het even naar ' + (window.PQ_MAIL || 'info@pique.agency') + ', dan pakken we het zo op.');
      }
      form.hidden = true;
      var dank = $('.dank');
      var eigen = window.PQ_DANK || {};
      var teksten = eigen[soort] || {
        ja: ['Getekend. We zetten hem klaar.',
             'Je krijgt binnen een uur de opdrachtbevestiging en drie momenten voor de startsessie. Een kopie van dit ondertekende voorstel staat al in je mail.'],
        dossiers: ['Komen eraan.',
             'Je krijgt binnen twee werkdagen vier volledige dossiers uit je eigen lijst. Dat kost je een kwartier lezen en verplicht je tot niets.'],
        bellen: ['We bellen je.',
             'Je wordt binnen een werkdag gebeld. Komt het eerder uit, bel dan gerust zelf.']
      }[soort];
      $('[data-dank-kop]', dank).textContent = teksten[0];
      $('[data-dank-tekst]', dank).textContent = teksten[1];
      dank.classList.add('toon');
      dank.scrollIntoView({ behavior: rust ? 'auto' : 'smooth', block: 'center' });
    };

    if (!doel) { if (console && console.debug) console.debug('[pique] akkoord', lading); return klaar(true); }
    /* Bewust text/plain, net als bij het terugbelverzoek in lp-v2: dan is het een
       simpele request en vraagt de browser geen preflight, wat een Apps
       Script-webapp toch niet beantwoordt. Lukt fetch niet, dan gaat het alsnog
       met een beacon de deur uit en is het verzoek niet weg. */
    var ruw = JSON.stringify(lading);
    fetch(doel, { method: 'POST', body: ruw, keepalive: true,
      headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
      .then(function (r) { return r.text(); })
      .then(function (tekst) {
        /* Apps Script antwoordt altijd met 200 en zet het echte oordeel in de body.
           Kunnen we die lezen en staat er ok:false in, dan is er niets vastgelegd en
           mogen we hier geen bevestiging tonen. Lukt lezen niet, dan blokkeert CORS
           het antwoord en niet de verzending, en gaan we uit van verzonden. */
        try {
          var a = JSON.parse(tekst);
          if (a && a.ok === false) return klaar(false, a.fout);
        } catch (e) { /* geen leesbaar antwoord, dan is het onderweg */ }
        klaar(true);
      })
      .catch(function () {
        var blob = new Blob([ruw], { type: 'text/plain;charset=UTF-8' });
        klaar(!!(navigator.sendBeacon && navigator.sendBeacon(doel, blob)));
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
