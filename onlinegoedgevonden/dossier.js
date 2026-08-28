/* Het venster achter de twee vervaagde bevindingen.
 *
 * De waas alleen is een plaatje: de lezer ziet dat er iets is en kan er niets mee.
 * Er moet iets gebeuren als hij klikt, anders leest het als een truc. Wat er
 * opengaat vertelt niet wat de bevinding is, want dan is het slot weg. Het vertelt
 * waar hij over gaat, wanneer we hem vonden en waarom hij niet op papier staat,
 * en zet daar de twee knoppen onder.
 */
(function () {
  'use strict';
  var venster = document.getElementById('dsvenster');
  if (!venster) return;
  var kaart = venster.querySelector('.ds-vkaart');
  var laatste = null;

  function vul(knop) {
    var d = knop.dataset;
    venster.querySelector('.ds-vnum').textContent = d.num || '';
    venster.querySelector('.ds-vtitel').textContent = d.titel || '';
    venster.querySelector('.ds-vuitleg').textContent = d.uitleg || '';
    var strook = venster.querySelector('.ds-vstrook');
    strook.innerHTML = '';
    [['Onderdeel', d.vak], ['Gevonden op', d.datum], ['Bron', d.bron]].forEach(function (r) {
      if (!r[1]) return;
      var el = document.createElement('div');
      el.className = 'ds-vs';
      var b = document.createElement('b');
      b.textContent = r[0];
      var s = document.createElement('span');
      s.textContent = r[1];
      el.appendChild(b);
      el.appendChild(s);
      strook.appendChild(el);
    });
  }

  function open(knop) {
    laatste = knop;
    vul(knop);
    venster.classList.add('aan');
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(function () { venster.classList.add('in'); });
    setTimeout(function () { venster.querySelector('.ds-vsluit').focus(); }, 60);
  }

  function sluit() {
    venster.classList.remove('in');
    document.body.style.overflow = '';
    setTimeout(function () { venster.classList.remove('aan'); }, 320);
    if (laatste) laatste.focus();
  }

  Array.prototype.forEach.call(document.querySelectorAll('.ds-sk'), function (k) {
    k.addEventListener('click', function () { open(k); });
  });
  venster.querySelector('.ds-vsluit').addEventListener('click', sluit);
  venster.querySelector('.ds-vbg').addEventListener('click', sluit);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && venster.classList.contains('aan')) sluit();
  });
  /* de knoppen in het venster openen het bestaande plan/bel-scherm, dus eerst dit
     venster dicht zodat er geen twee lagen over elkaar liggen */
  Array.prototype.forEach.call(kaart.querySelectorAll('[data-open="sheet"]'), function (b) {
    b.addEventListener('click', function () { sluit(); });
  });
})();

/* ══ De intake ══════════════════════════════════════════════════════════════════
 * Een echt formulier. Drie vragen, een naam en een mailadres, en dan het voorstel.
 *
 * Wat er gebeurt bij verzenden: het gaat naar hetzelfde eindpunt als een
 * terugbelverzoek, met soort 'intake' erbij zodat Murphy ze uit elkaar houdt. De
 * lezer krijgt zijn voorstel meteen op de pagina te zien, want een formulier dat
 * belooft te sturen en verder niets laat zien voelt als een val.
 *
 * Lukt het versturen niet, dan zien we dat wel maar hij niet: hij heeft zijn
 * voorstel al. Het bericht gaat dan alsnog met een beacon de deur uit.
 */
(function () {
  'use strict';
  var form = document.getElementById('intakeform');
  if (!form) return;
  var dank = document.getElementById('ivr-dank');
  var fout = document.getElementById('ivr-fout');

  /* Twee keer tevredenheid, apart gevraagd. De interessantste uitkomst is tevreden
     over de samenwerking en niet over het resultaat: dan is er geen ruzie en wel een
     probleem, en dat is precies de reden dat het al zo lang zo blijft. */
  var ANTWOORD = {
    resultaat: {
      ja: 'Je bent tevreden over het resultaat. Dan is de vraag alleen nog of het ook ' +
          'goedkoper kan. Hierboven staan vijf dingen die daar het antwoord op geven.',
      wisselend: 'Het resultaat is wisselend. Dat komt zelden door te weinig inzet en meestal ' +
                 'door wat er nooit is nagekeken. Hierboven staan vijf dingen die niemand je ' +
                 'heeft gemeld.',
      nee: 'Je bent niet tevreden over het resultaat. Dan is de enige vraag nog wanneer je ' +
           'overstapt, en niet of.'
    },
    samenwerking: {
      ja: 'Over de samenwerking ben je wel tevreden. Dat maakt het lastig, en het is precies ' +
          'de reden dat dit soort dingen blijft liggen. Aardig zijn en gevonden worden zijn ' +
          'twee verschillende opdrachten.',
      wisselend: 'De samenwerking loopt wisselend. Dan kost dit gesprek je een kwartier en ' +
                 'levert het je een tweede mening op over dezelfde rekening.',
      nee: 'De samenwerking loopt niet lekker. Dan hoef je van ons alleen te weten dat je er ' +
           'na drie maanden zonder opzegtermijn weer uit kunt.'
    }
  };

  function euro(n) { return '€ ' + Math.round(n).toLocaleString('nl-NL'); }
  function veld(naam) {
    var el = form.elements[naam];
    if (!el) return '';
    if (el.length && el[0] && el[0].type === 'radio') {
      for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value;
      return '';
    }
    return String(el.value || '').trim();
  }

  /* het voorstel onderaan, dat op zijn antwoorden slaat */
  function vulVoorstel(a) {
    var doel = document.getElementById('intake-antwoord');
    if (doel) {
      var rijen = '';
      if (ANTWOORD.resultaat[a.resultaat]) {
        rijen += '<div class="aw-r"><b>Het resultaat</b><span>' +
                 ANTWOORD.resultaat[a.resultaat] + '</span></div>';
      }
      if (ANTWOORD.samenwerking[a.samenwerking]) {
        rijen += '<div class="aw-r"><b>De samenwerking</b><span>' +
                 ANTWOORD.samenwerking[a.samenwerking] + '</span></div>';
      }
      doel.innerHTML = rijen;
    }
    var prijsvak = document.getElementById('intake-prijs');
    if (!prijsvak) return 0;
    var bedrag = parseInt(String(a.bedrag).replace(/[^0-9]/g, ''), 10);
    if (!bedrag || bedrag < 100) { prijsvak.hidden = true; return 0; }
    var wij = Math.round(bedrag * 0.8 / 50) * 50;
    prijsvak.hidden = false;
    prijsvak.innerHTML =
      '<div class="prijs-rij">' +
      '<span class="prijs-label">Nu</span><span class="prijs-nu">' + euro(bedrag) + ' p/m</span>' +
      '<span class="prijs-label">Bij ons</span><span class="prijs-wij">' + euro(wij) + ' p/m</span>' +
      '</div>' +
      '<p>Twintig procent onder wat je vandaag kwijt bent, voor het geheel: je vindbaarheid, ' +
      'je advertenties en de artikelen die over je verschijnen. Dat bedrag komt in de ' +
      'overeenkomst te staan, samen met de posities en de datums hierboven.</p>';
    return wij;
  }

  function verstuur(a) {
    var lading = JSON.stringify({
      soort: 'intake', naam: a.naam, email: a.email,
      resultaat: a.resultaat, samenwerking: a.samenwerking, bedrag: a.bedrag,
      bedrijf: window.PQ_BEDRIJF, slug: window.PQ_SLUG,
      klant: window.PQ_KLANT, campagne: window.PQ_CAMPAGNE
    });
    var url = window.PQ_TERUGBEL_URL;
    if (!url) {
      if (window.console) console.debug('[pique] intake (nog geen endpoint ingesteld)', lading);
      return;
    }
    /* text/plain houdt het een simpele request, zodat een Apps Script-webapp geen
       preflight hoeft te beantwoorden die hij toch niet kan geven. */
    fetch(url, {method: 'POST', body: lading, keepalive: true,
                headers: {'Content-Type': 'text/plain;charset=utf-8'}})
      .catch(function () {
        if (navigator.sendBeacon) {
          navigator.sendBeacon(url, new Blob([lading], {type: 'text/plain'}));
        }
      });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var a = {resultaat: veld('resultaat'), samenwerking: veld('samenwerking'),
             bedrag: veld('bedrag'), naam: veld('naam'), email: veld('email')};

    var mist = [];
    if (!a.resultaat) mist.push('of je tevreden bent over het resultaat');
    if (!a.samenwerking) mist.push('of je tevreden bent over de samenwerking');
    if (!parseInt(String(a.bedrag).replace(/[^0-9]/g, ''), 10)) mist.push('je maandbedrag');
    if (!a.naam) mist.push('je naam');
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(a.email)) mist.push('een geldig mailadres');
    if (mist.length) {
      fout.hidden = false;
      fout.textContent = 'We missen nog ' + (mist.length > 1
        ? mist.slice(0, -1).join(', ') + ' en ' + mist[mist.length - 1] : mist[0]) + '.';
      return;
    }
    fout.hidden = true;

    var wij = vulVoorstel(a);
    verstuur(a);
    if (window.pqTrack) window.pqTrack('intake-verstuurd', a.bedrag);

    form.hidden = true;
    dank.hidden = false;
    dank.innerHTML =
      '<h3>Dank je, ' + a.naam.split(' ')[0].replace(/[<>&]/g, '') + '. Je voorstel staat klaar.</h3>' +
      '<p>Onderaan deze pagina staat wat we vastleggen en wat het kost' +
      (wij ? ': <strong>' + euro(wij) + ' per maand</strong>' : '') +
      '. Je krijgt het ook in je mail, zodat je het rustig kunt nalezen.</p>' +
      '<div class="knoppen">' +
      '<button class="btn-a" type="button" data-open="sheet" data-tab="plan">' +
      'Loop het met ons door</button>' +
      '<a class="btn-b" href="#belofte">Naar mijn voorstel</a></div>';
    /* de knop in dit blok bestond nog niet toen lp-v2.js zijn luisteraars zette */
    var plan = dank.querySelector('[data-open="sheet"]');
    if (plan && window.pqOpenSheet) {
      plan.addEventListener('click', function () { window.pqOpenSheet('plan'); });
    }
  });
})();
