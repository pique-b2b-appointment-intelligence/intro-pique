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
