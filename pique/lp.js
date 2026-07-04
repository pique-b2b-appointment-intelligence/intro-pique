// Pique LP — reveal on scroll + Cal.com embed (gedeeld over alle pagina's)

// Reveal
(function () {
  var els = document.querySelectorAll('.r');
  if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('v'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('v'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -32px 0px', threshold: 0.04 });
  els.forEach(function (el) { io.observe(el); });
})();

// Cal.com inline embed — Pique belafspraak
(function (C, A, L) { let p = function (a, ar) { a.q.push(ar) }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true } if (ar[0] === L) { const api = function () { p(api, arguments) }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]) } else p(cal, ar); return } p(cal, ar) } })(window, "https://app.cal.com/embed/embed.js", "init");
if (document.getElementById('cal-inline')) {
  Cal("init", "belafspraak-pique", { origin: "https://app.cal.com" });
  Cal.ns["belafspraak-pique"]("inline", {
    elementOrSelector: "#cal-inline",
    config: { "layout": "month_view", "useSlotsViewOnSmallScreen": "true" },
    calLink: "simon-kempers/belafspraak-pique"
  });
  Cal.ns["belafspraak-pique"]("ui", { "hideEventTypeDetails": false, "layout": "month_view" });
}
