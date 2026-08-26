/**
 * Pique gedrag-tracking.  Twee routes in één functie:
 *   GET  /api/t?p=<slug>&c=<kanaal>   klik in de mail -> logt het event, stuurt door naar de LP
 *   POST /api/t                       leesprofiel van de pagina zelf (sendBeacon uit lp-v2.js)
 * ---------------------------------------------------------------------------------------------
 * Waarom hier en niet via een mailtool: de link staat op hetzelfde domein als de landingspagina,
 * dus de mail bevat geen extra redirect-domein (dat leest als linkverkorter en kost deliverability).
 * En we meten geen opens met een pixel: die zijn sinds Apple Mail Privacy Protection grotendeels ruis
 * en maken een 1-op-1 mail juist verdacht. Een klik is een echt signaal.
 *
 * Het leesprofiel komt als één POST per bezoek, niet als een event per stap. De pagina telt zelf
 * op en flusht bij 20s, 90s en bij het weggaan; alle flushes van hetzelfde bezoek dragen dezelfde
 * sessie-id, zodat Belcockpit ze over elkaar heen legt in plaats van drie bezoeken te tellen.
 *
 * Geen npm-dependencies met opzet: dit project is een statische site zonder package.json, en dat
 * moet zo blijven. Het event gaat daarom door naar de Belcockpit-backend, die de Redis-sleutels al heeft.
 *
 * Env var (alleen deze): PIQUE_EVENT_SECRET, gelijk aan die op het pique-site project.
 */

const SITE = 'https://www.intro-pique.agency';
const SINK = 'https://www.pique.agency/api/belcockpit';

// Alleen eigen paden. Zonder deze check is /api/t een open redirect en dus bruikbaar voor
// phishing onder ons eigen domein.
function veiligeSlug(raw) {
  const slug = String(raw || '').trim().toLowerCase().replace(/^\/+|\/+$/g, '');
  const ok = /^[a-z0-9][a-z0-9/-]{0,120}$/.test(slug) && slug.indexOf('//') < 0 && slug.indexOf('..') < 0;
  return ok ? slug : '';
}

// Doorsturen naar Belcockpit. Hard afgekapt: de prospect mag nooit op onze logging wachten.
// Mislukt het, dan verliezen we één event en gaat de pagina gewoon door.
async function naarSink(bulk) {
  try {
    await fetch(SINK + '?action=event&s=' + encodeURIComponent(process.env.PIQUE_EVENT_SECRET || ''), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bulk: bulk }),
      signal: AbortSignal.timeout(1500),
    });
  } catch (e) { /* bewust stil */ }
}

// sendBeacon stuurt text/plain; Vercel parst dat niet naar een object, dus we vangen
// alle drie de vormen op waarin de body kan binnenkomen.
async function leesBody(req) {
  if (req.body && typeof req.body === 'object' && !Buffer.isBuffer(req.body)) return req.body;
  let ruw = '';
  if (typeof req.body === 'string') ruw = req.body;
  else if (Buffer.isBuffer(req.body)) ruw = req.body.toString('utf8');
  else {
    ruw = await new Promise(function (res) {
      let d = '';
      req.on('data', function (c) { d += c; if (d.length > 20000) { d = d.slice(0, 20000); req.destroy(); } });
      req.on('end', function () { res(d); });
      req.on('error', function () { res(''); });
    });
  }
  try { return JSON.parse(ruw); } catch (e) { return null; }
}

// Van rauw profiel naar één regel die een beller in één blik leest.
// "82s, tot het voorstel, kantelpunt 31s, video 40s"
const NAAM = { 'bevinding-1': 'de eerste bevinding', kantelpunt: 'het kantelpunt',
               belaanbod: 'het belaanbod', voorstel: 'het voorstel', cta: 'het eind' };
function samenvatting(p, diepste) {
  const stukken = [];
  stukken.push(Math.round(p.sec) + 's');
  if (diepste) stukken.push('tot ' + (NAAM[diepste] || diepste));
  const secties = p.secties && typeof p.secties === 'object' ? p.secties : {};
  const langste = Object.keys(secties)
    .filter(function (k) { return secties[k] >= 5; })
    .sort(function (a, b) { return secties[b] - secties[a]; })[0];
  if (langste && langste !== diepste) stukken.push(langste + ' ' + Math.round(secties[langste]) + 's');
  if (p.video > 0) stukken.push('video ' + Math.round(p.video) + 's');
  return stukken.join(', ').slice(0, 180);
}

// De volgorde van de pagina. Het diepste blok dat echt in beeld stond bepaalt hoe ver iemand kwam.
const VOLGORDE = ['bevinding-1', 'kantelpunt', 'belaanbod', 'voorstel', 'cta'];

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store, max-age=0');
  res.setHeader('Referrer-Policy', 'no-referrer');

  if (req.method === 'POST') {
    const p = await leesBody(req);
    const slug = p ? veiligeSlug(p.slug) : '';
    // Alleen geloofwaardige waarden. Een bezoek van drie uur is een vergeten tabblad of
    // iemand die met de klok speelt, en dat hoort niet bovenaan het belbord te komen.
    const sec = Math.max(0, Math.min(3600, Number(p && p.sec) || 0));
    if (!slug || !p) { res.statusCode = 204; return res.end(); }

    const secties = {};
    Object.keys(p.secties || {}).slice(0, 12).forEach(function (k) {
      const naam = String(k).replace(/[^a-z0-9_-]/gi, '').slice(0, 24);
      const n = Math.max(0, Math.min(3600, Number(p.secties[k]) || 0));
      if (naam && n > 0) secties[naam] = n;
    });
    let diepste = '';
    VOLGORDE.forEach(function (naam) { if (secties[naam] >= 2) diepste = naam; });

    const lees = {
      sessie: String(p.sessie || '').replace(/[^a-z0-9]/gi, '').slice(0, 24),
      sec: sec,
      diep: Math.max(0, Math.min(100, Number(p.diep) || 0)),
      diepste: diepste,
      secties: secties,
      video: Math.max(0, Math.min(3600, Number(p.video) || 0)),
      stappen: (Array.isArray(p.stappen) ? p.stappen : []).slice(0, 20)
        .map(function (x) { return String(x).replace(/[^a-z0-9:_-]/gi, '').slice(0, 32); }),
      reden: String(p.reden || '').slice(0, 12),
    };

    await naarSink([{
      type: 'paginabezoek',
      slug: slug,
      kanaal: 'pagina',
      ts: Date.now(),
      sessie: lees.sessie,
      meta: samenvatting(lees, diepste),
      lees: lees,
    }]);

    res.statusCode = 204;
    return res.end();
  }

  const q = req.query || {};
  const slug = veiligeSlug(q.p);
  const kanaal = String(q.c || 'mail').replace(/[^a-z0-9_-]/gi, '').slice(0, 24) || 'mail';
  const doel = slug ? SITE + '/' + slug : SITE + '/';

  if (slug) await naarSink([{ type: 'mail_klik', slug: slug, kanaal: kanaal, ts: Date.now() }]);

  res.statusCode = 302;
  res.setHeader('Location', doel);
  res.end();
};
