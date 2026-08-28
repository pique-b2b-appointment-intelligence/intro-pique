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
 * Drie vragen boven aan de pagina, en een voorstel onderaan dat erop antwoordt.
 *
 * Wat de lezer invult blijft in zijn eigen browser. Er gaat pas iets weg op het
 * moment dat hij zelf zijn nummer achterlaat, en dan gaan de antwoorden mee in
 * hetzelfde bericht. Dat is de enige eerlijke volgorde.
 *
 * Het bedrag is het enige getal dat wij niet kunnen meten en hij wel weet. Daarom
 * rekenen we er niets omheen: twintig procent eraf, afgerond op vijftig euro, en
 * dat is het voorstel.
 */
(function () {
  'use strict';
  var vak = document.getElementById('intake');
  if (!vak) return;
  var staat = {positie: '', partij: '', bedrag: ''};

  try {
    var bewaard = localStorage.getItem('pq-intake-' + (window.PQ_SLUG || 'x'));
    if (bewaard) staat = JSON.parse(bewaard);
  } catch (e) { /* privémodus of geblokkeerde opslag: dan begint hij gewoon leeg */ }

  function bewaar() {
    try {
      localStorage.setItem('pq-intake-' + (window.PQ_SLUG || 'x'), JSON.stringify(staat));
    } catch (e) { /* niets aan de hand, de pagina werkt ook zonder */ }
  }

  var ANTWOORD = {
    positie: {
      ja: 'Je staat op pagina één. Op je eigen naam waarschijnlijk ook. De vraag is of je er ' +
          'staat op de termen waarop iemand koopt die jou nog niet kent, en dat is precies ' +
          'waar wij een positie en een datum in het contract zetten.',
      nee: 'Je staat niet op pagina één. Dat is geen mening en geen inspanningsverplichting: ' +
           'wij zetten de termen, de positie en de datum in de overeenkomst.',
      weet: 'Je weet niet waar je staat. Dat is het eerlijkste antwoord dat er is, en het is ' +
            'meteen het probleem. Wij beginnen met een nulmeting, en die lijst is van jou, ' +
            'ook als je verder niets met ons doet.'
    },
    partij: {
      goed: 'Je bent tevreden over je huidige partij. Dat zegt iets over de samenwerking en ' +
            'niets over de uitkomst. Hierboven staan vijf bevindingen, en er is er geen ' +
            'één van bij je gemeld.',
      wisselend: 'Het gaat wisselend. Dan kost dit gesprek je een kwartier en levert het je ' +
                 'een tweede mening op over dezelfde rekening.',
      matig: 'Het loopt niet lekker. Dan is de enige vraag nog wanneer je overstapt, en niet of.'
    }
  };

  function euro(n) {
    return '€ ' + Math.round(n).toLocaleString('nl-NL');
  }

  function teken() {
    var doel = document.getElementById('intake-antwoord');
    if (!doel) return;
    var rijen = '';
    if (staat.positie && ANTWOORD.positie[staat.positie]) {
      rijen += '<div class="aw-r"><b>Je positie</b><span>' +
               ANTWOORD.positie[staat.positie] + '</span></div>';
    }
    if (staat.partij && ANTWOORD.partij[staat.partij]) {
      rijen += '<div class="aw-r"><b>Je huidige partij</b><span>' +
               ANTWOORD.partij[staat.partij] + '</span></div>';
    }
    doel.innerHTML = rijen;

    var prijsvak = document.getElementById('intake-prijs');
    if (!prijsvak) return;
    var bedrag = parseInt(String(staat.bedrag).replace(/[^0-9]/g, ''), 10);
    if (!bedrag || bedrag < 100) {
      prijsvak.hidden = true;
      return;
    }
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
  }

  vak.addEventListener('click', function (e) {
    var k = e.target.closest('.ivr-k');
    if (!k) return;
    var veld = k.parentNode.dataset.veld;
    staat[veld] = k.dataset.waarde;
    Array.prototype.forEach.call(k.parentNode.querySelectorAll('.ivr-k'), function (b) {
      b.setAttribute('aria-pressed', b === k ? 'true' : 'false');
    });
    bewaar();
    teken();
    if (window.pqTrack) window.pqTrack('intake-' + veld, staat[veld]);
  });

  var geld = document.getElementById('ivr-bedrag');
  if (geld) {
    geld.addEventListener('input', function () {
      staat.bedrag = geld.value;
      bewaar();
      teken();
    });
    geld.addEventListener('change', function () {
      if (window.pqTrack && staat.bedrag) window.pqTrack('intake-bedrag', staat.bedrag);
    });
  }

  /* terugzetten wat hij eerder invulde */
  Object.keys(staat).forEach(function (veld) {
    var groep = vak.querySelector('[data-veld="' + veld + '"]');
    if (groep && staat[veld]) {
      var k = groep.querySelector('[data-waarde="' + staat[veld] + '"]');
      if (k) k.setAttribute('aria-pressed', 'true');
    }
  });
  if (geld && staat.bedrag) geld.value = staat.bedrag;
  teken();

  /* De antwoorden gaan mee zodra hij zelf zijn nummer achterlaat. Niet eerder. */
  var form = document.getElementById('belform');
  if (form) {
    form.addEventListener('submit', function () {
      window.PQ_EXTRA = {positie: staat.positie, partij: staat.partij, bedrag: staat.bedrag};
    }, true);
  }
})();
