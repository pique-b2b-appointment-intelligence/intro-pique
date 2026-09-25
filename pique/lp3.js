/* ============================================================
   PIQUE LP v3 — gedrag
   Vier dingen, en alle vier hebben ze een reden:
     1. de nav krijgt een lijn zodra je scrollt (feedback: je bent los van de top)
     2. blokken komen in beeld (hiërarchie: je leest in de volgorde van het verhaal)
     3. het krabbeltje en de onderstreping tekenen zichzelf (verhaal: dit is met
        de hand gezet, niet gegenereerd)
     4. de kantlijnnotitie komt pas als de feiten er staan (volgorde: eerst wat
        er is, dan wat het betekent)
   Alles staat uit onder prefers-reduced-motion.
   ============================================================ */
(function () {
  'use strict';
  var rust = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. nav */
  var nav = document.querySelector('nav');
  if (nav) {
    var top = document.createElement('div');
    top.setAttribute('aria-hidden', 'true');
    top.style.cssText = 'position:absolute;top:0;height:1px;width:1px';
    document.body.prepend(top);
    new IntersectionObserver(function (e) {
      nav.classList.toggle('vast', !e[0].isIntersecting);
    }).observe(top);
  }

  /* 2, 3 en 4: alles wat pas mag verschijnen als het in beeld komt */
  var doelen = document.querySelectorAll('.in-view, .kantlijn, .krabbel, .hero-h1 .mark');
  if (rust) {
    doelen.forEach(function (el) { el.classList.add('zicht'); });
  } else {
    /* De getekende lijnen moeten hun eigen lengte kennen, anders klopt de
       dasharray niet en springt de animatie. */
    document.querySelectorAll('.krabbel path, .hero-h1 .mark path').forEach(function (p) {
      var l = Math.ceil(p.getTotalLength());
      p.style.setProperty('--len', l);
      p.style.strokeDasharray = l;
      p.style.strokeDashoffset = l;
    });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('zicht');
        io.unobserve(e.target);
      });
    }, { threshold: 0, rootMargin: '0px 0px -12% 0px' });
    doelen.forEach(function (el) { io.observe(el); });
  }

  /* De FAQ is een <details>, dus hij werkt ook zonder dit script. Dit zorgt er
     alleen voor dat er één tegelijk openstaat, zodat je niet scrollt door een
     muur van opengeklapte antwoorden. */
  var faq = document.querySelectorAll('.faq details');
  faq.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      faq.forEach(function (a) { if (a !== d) a.open = false; });
    });
  });
})();
