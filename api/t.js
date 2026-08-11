/**
 * Pique klik-tracking.  /api/t?p=<slug>&c=<kanaal>  ->  logt het event, stuurt door naar de LP.
 * ---------------------------------------------------------------------------------------------
 * Waarom hier en niet via een mailtool: de link staat op hetzelfde domein als de landingspagina,
 * dus de mail bevat geen extra redirect-domein (dat leest als linkverkorter en kost deliverability).
 * En we meten geen opens met een pixel: die zijn sinds Apple Mail Privacy Protection grotendeels ruis
 * en maken een 1-op-1 mail juist verdacht. Een klik is een echt signaal.
 *
 * Geen npm-dependencies met opzet: dit project is een statische site zonder package.json, en dat
 * moet zo blijven. Het event gaat daarom door naar de Belcockpit-backend, die de Redis-sleutels al heeft.
 *
 * Env var (alleen deze): PIQUE_EVENT_SECRET, gelijk aan die op het pique-site project.
 */

const SITE = 'https://www.intro-pique.agency';
const SINK = 'https://www.pique.agency/api/belcockpit';

module.exports = async function handler(req, res) {
  const q = req.query || {};
  const slug = String(q.p || '').trim().toLowerCase().replace(/^\/+|\/+$/g, '');
  const kanaal = String(q.c || 'mail').replace(/[^a-z0-9_-]/gi, '').slice(0, 24) || 'mail';

  // Alleen eigen paden doorlaten. Zonder deze check is /api/t een open redirect en dus
  // bruikbaar voor phishing onder ons eigen domein.
  const veilig = /^[a-z0-9][a-z0-9/-]{0,120}$/.test(slug) &&
                 slug.indexOf('//') < 0 &&
                 slug.indexOf('..') < 0;
  const doel = veilig ? SITE + '/' + slug : SITE + '/';

  if (veilig) {
    try {
      const url = SINK + '?action=event' +
        '&type=mail_klik' +
        '&slug=' + encodeURIComponent(slug) +
        '&kanaal=' + encodeURIComponent(kanaal) +
        '&s=' + encodeURIComponent(process.env.PIQUE_EVENT_SECRET || '');
      // Hard afgekapt: de prospect mag nooit op onze logging wachten. Mislukt het, dan
      // verliezen we één event en gaat de doorverwijzing gewoon door.
      await fetch(url, { signal: AbortSignal.timeout(1200) });
    } catch (e) { /* bewust stil */ }
  }

  res.setHeader('Cache-Control', 'no-store, max-age=0');
  res.setHeader('Referrer-Policy', 'no-referrer');
  res.statusCode = 302;
  res.setHeader('Location', doel);
  res.end();
};
