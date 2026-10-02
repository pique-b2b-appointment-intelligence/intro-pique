/**
 * Slot op de Domek-pagina's.
 * ---------------------------------------------------------------------------
 * De codepoort op de pagina zelf is geen slot. Die draait in de browser, dus
 * de hele HTML staat in de broncode en daarmee ook de code en de gegevens van
 * de ontvanger. noindex vraagt Google alleen om hem niet te tonen.
 *
 * Dit draait aan de rand van het netwerk, voordat er iets wordt uitgeleverd.
 * Zonder sleutel krijg je een nette gesloten-pagina met een verwijzing naar
 * Lightr, en niet de inhoud.
 *
 * LET OP, hier ging het de eerste keer mis. Hetzelfde bestand is via meerdere
 * routes bereikbaar en de matcher kijkt naar het pad vóór de rewrite:
 *
 *   evenkennismaken.nl/domek          -> pad /domek
 *   lightr.intro-pique.agency/domek   -> pad /domek
 *   evenkennismaken.nl/lightr/domek   -> pad /lightr/domek
 *   intro-pique.agency/lightr/domek   -> pad /lightr/domek
 *   intro-pique.vercel.app/lightr/..  -> pad /lightr/domek
 *
 * Alleen /domek afschermen liet dus vier open deuren staan. Elke pagina moet
 * daarom twee keer in de matcher: kaal en met /lightr ervoor. De matcher moet
 * een letterlijke lijst zijn, die wordt bij het bouwen uitgelezen en kan dus
 * niet berekend worden.
 *
 * Een pagina erbij: zet hem in PAGINAS én twee keer in config.matcher. Vergeet
 * je de matcher, dan draait dit bestand er niet voor en staat de pagina open.
 */

export const config = {
  matcher: [
    '/domek',
    '/domek-motor',
    '/domek-alle-paginas',
    '/domek-pagina',
    '/churnless-voor-domek',
    '/churnless/domek',
    '/lightr/domek',
    '/lightr/domek-motor',
    '/lightr/domek-alle-paginas',
    '/lightr/domek-pagina',
    '/lightr/churnless-voor-domek',
    '/lightr/churnless/domek',
  ],
};

const PAGINAS = new Set([
  'domek',
  'domek-motor',
  'domek-alle-paginas',
  'domek-pagina',
  'churnless-voor-domek',
  'churnless/domek',
]);

/* Eén sleutel voor de hele set. Wie er één opent, kan ze daarna allemaal bij
   op dat apparaat. Zes losse links rondsturen werkt in de praktijk niet. */
const SLEUTEL = 'dk-BALVltrpOXboF0xq';
const KOEKJE = 'dk';
const DERTIG_DAGEN = 60 * 60 * 24 * 30;

export default function middleware(request) {
  const url = new URL(request.url);

  /* het pad zoals het hier binnenkomt kan /lightr ervoor hebben */
  const naam = url.pathname.replace(/^\/lightr\//, '').replace(/^\//, '');
  if (!PAGINAS.has(naam)) return doorlaten();

  if (heeftKoekje(request)) return doorlaten();

  /* sleutel in de link: koekje zetten en de sleutel uit de URL halen, zodat
     hij niet in een schermafdruk of in de geschiedenis blijft staan */
  if (url.searchParams.get('k') === SLEUTEL) {
    url.searchParams.delete('k');
    const vraag = url.searchParams.toString();
    return new Response(null, {
      status: 302,
      headers: {
        location: url.pathname + (vraag ? '?' + vraag : ''),
        'set-cookie': `${KOEKJE}=${SLEUTEL}; Path=/; Max-Age=${DERTIG_DAGEN}; Secure; HttpOnly; SameSite=Lax`,
        'cache-control': 'no-store',
      },
    });
  }

  return new Response(GESLOTEN, {
    status: 403,
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': 'no-store',
      'x-robots-tag': 'noindex, nofollow',
    },
  });
}

function heeftKoekje(request) {
  const rauw = request.headers.get('cookie') || '';
  return rauw.split(';').some((deel) => deel.trim() === `${KOEKJE}=${SLEUTEL}`);
}

/* Een verzoek doorlaten zonder framework erbij. Dit project heeft bewust geen
   package.json, dus @vercel/edge valt af. */
function doorlaten() {
  return new Response(null, { headers: { 'x-middleware-next': '1' } });
}

const GESLOTEN = `<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Deze pagina is gesloten</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230E1526'/%3E%3Cpath d='M11 14v-2.5a5 5 0 0 1 10 0V14' fill='none' stroke='white' stroke-width='2.2'/%3E%3Crect x='9' y='14' width='14' height='10' rx='2.5' fill='white'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  min-height:100svh;display:grid;place-items:center;padding:1.5rem;
  font-family:'Plus Jakarta Sans',system-ui,-apple-system,sans-serif;
  background:radial-gradient(900px 540px at 50% -10%,#16233b 0%,#0E1526 62%);
  color:#fff;-webkit-font-smoothing:antialiased;line-height:1.6
}
.kaart{max-width:420px;width:100%;text-align:center}
.slot{
  width:58px;height:58px;margin:0 auto 1.9rem;border-radius:16px;
  background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);
  display:grid;place-items:center
}
.slot svg{width:26px;height:26px;color:rgba(255,255,255,.72)}
h1{font-size:1.5rem;font-weight:800;letter-spacing:-.025em;margin-bottom:.7rem}
p{color:rgba(255,255,255,.58);font-size:.95rem}
a.knop{
  display:inline-block;margin-top:1.9rem;text-decoration:none;
  font-weight:600;font-size:.92rem;color:#0E1526;background:#fff;
  padding:.72rem 1.5rem;border-radius:99px;transition:transform .18s
}
a.knop:hover{transform:translateY(-1px)}
.voet{
  margin-top:2.4rem;padding-top:1.4rem;border-top:1px solid rgba(255,255,255,.1);
  font-size:.78rem;color:rgba(255,255,255,.34)
}
</style>
</head>
<body>
  <div class="kaart">
    <div class="slot">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <rect x="4" y="10.5" width="16" height="11" rx="2.5"/>
        <path d="M8 10.5V7a4 4 0 0 1 8 0v3.5"/>
      </svg>
    </div>
    <h1>Deze pagina is gesloten</h1>
    <p>Hier staat werk dat alleen voor de betrokkenen bedoeld is. Heb je de link gekregen maar werkt hij niet meer, neem dan contact op met Lightr.</p>
    <a class="knop" href="https://lightr.nl">Naar lightr.nl</a>
    <p class="voet">Lightr B.V.</p>
  </div>
</body>
</html>`;
