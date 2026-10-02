/**
 * Slot op de demopagina's die niet voor iedereen zijn.
 * ---------------------------------------------------------------------------
 * De codepoort op /domek zelf is geen slot. Die draait in de browser, dus de
 * hele HTML staat in de broncode en daarmee ook de code en de gegevens van de
 * ontvanger. noindex vraagt Google alleen om hem niet te tonen.
 *
 * Dit draait ervoor, aan de rand van het netwerk, voordat er iets wordt
 * uitgeleverd. Zonder sleutel komt er een 404 terug en geen 401, want een 401
 * verraadt dat er iets te halen valt.
 *
 * Werking: je deelt de link één keer mét ?k=<sleutel>. Die zet een koekje voor
 * dertig dagen en haalt de sleutel meteen uit de URL, zodat hij niet in een
 * schermafdruk of in de geschiedenis van een gedeelde computer blijft staan.
 * Daarna werkt de kale link op dat apparaat gewoon.
 *
 * De matcher staat hieronder en is exact. /domek-motor en /pilot vallen er
 * bewust buiten: die zijn wel openbaar.
 *
 * Een nieuwe pagina erbij: zet hem in SLOTEN én in config.matcher. Vergeet je
 * de matcher, dan draait dit bestand er niet voor en staat de pagina open.
 */

export const config = {
  matcher: ['/domek'],
};

/* sleutel per pad, zodat een gedeelde link niet meteen alles opent */
const SLOTEN = {
  '/domek': 'dk-BALVltrpOXboF0xq',
};

const DERTIG_DAGEN = 60 * 60 * 24 * 30;

export default function middleware(request) {
  const url = new URL(request.url);
  const sleutel = SLOTEN[url.pathname];

  /* pad valt niet onder een slot: niets doen */
  if (!sleutel) return doorlaten();

  const koek = `dk${url.pathname.replace(/\W/g, '')}`;

  /* al eerder binnengelaten op dit apparaat */
  if (heeftKoekje(request, koek, sleutel)) return doorlaten();

  /* sleutel in de link: koekje zetten en de sleutel uit de URL halen */
  if (url.searchParams.get('k') === sleutel) {
    url.searchParams.delete('k');
    const naar = url.pathname + (url.searchParams.toString() ? '?' + url.searchParams : '');
    return new Response(null, {
      status: 302,
      headers: {
        location: naar,
        'set-cookie': `${koek}=${sleutel}; Path=${url.pathname}; Max-Age=${DERTIG_DAGEN}; Secure; HttpOnly; SameSite=Lax`,
        'cache-control': 'no-store',
      },
    });
  }

  return new Response('Not Found', {
    status: 404,
    headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store' },
  });
}

function heeftKoekje(request, naam, waarde) {
  const rauw = request.headers.get('cookie') || '';
  return rauw.split(';').some((deel) => deel.trim() === `${naam}=${waarde}`);
}

/* De manier om een verzoek door te laten zonder een framework erbij. Dit
   project heeft bewust geen package.json, dus @vercel/edge valt af. */
function doorlaten() {
  return new Response(null, { headers: { 'x-middleware-next': '1' } });
}
