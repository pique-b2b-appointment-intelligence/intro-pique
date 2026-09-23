# BCS Batch 3 - Persoonlijke landingspagina's

287 persoonlijke LP's gegenereerd, een per mailbaar prospect uit de batch-3 deep-research lijst. Zelfde design als bcs2 (journey/verhaallijn-model, video bovenaan, merk-favicon bij de naam).

## Aantallen

| | |
|---|---|
| Landingspagina's | 287 |
| Met ingesloten merk-favicon | 287 (100%) |
| Met WebwinkelKeur-partnerblok | 28 |
| Video bovenaan + Cal.com-embed | 287 (100%) |
| Em-dashes in copy | 0 |
| 'Geen'-zinstarts in copy | 0 |

## Design (1:1 met bcs2)

- Navy intro met de video van Jeffrey bovenaan, merk-favicon in de brand-tile naast de bedrijfsnaam, meta `plaats · 2026`.
- Persoonlijke aanhef uit de voornaam van de beslisser (`He [naam], dit is waarom je m'n brief hebt ontvangen.`), of neutraal waar geen naam bekend is.
- Journey-lijn (geanimeerd amber SVG-pad langs de hoofdstukken) met het vier-akten-model: herkenning -> spanning+gevolg -> brug -> bewijs.
- Findings per bedrijf uit de deep-research hook, met bron per observatie.
- Statische Backbone-brug + bewijs (Jeffrey & Dylan) + Cal.com-boekingsembed onderaan.

## WebwinkelKeur-USP (28 merken)

Bij merken die zelf WebwinkelKeur gebruiken staat een extra hoofdstuk 'Jullie WebwinkelKeur blijft staan': Backbone is officieel WebwinkelKeur-partner en handelt vragen en geschillen af volgens het WebwinkelKeur-beleid, dus de service telt gewoon mee voor het keurmerk. Bron: webwinkelkeur.nl/partner/backbonecustomerservice.

Merken met het blok: Blokzeep, DMQ, De Olijfolie Shop, De Theebaron, DesignSpiegels.nl, Doezelf, Dogs en Co, Dutch Balance, Happy Earth, House of Posters, Jenelry, Kidz In Color, Kunst in Kaart, MUZE Skincare, Mr.MATCHA, Natural Women Care, Olijfolie Concurrent, Perfect Age, Planjeweek, Plantpowders, Pretty Polish, Prohemp, Snoepdog, Spiegelshop, Twensies, Vital Nutrition, Webkarpet, Zebrapaardje.

## Bestanden

- `bcs3/[slug].html` - de 287 pagina's (klaar voor deploy op intro-pique.agency/bcs3/[slug]).
- `bcs3-base.json` - de 287 mailbare bedrijven (bedrijf, web, slug, plaats, beslisser, founder_fallback, hook).
- `bcs3-content.json` - de geschreven copy per bedrijf (lead, findings, pivot, betekenis, pull, imagine, wwk).
- `bcs3-style.css` - stijl (bcs2-basis + WWK-blok).
- `genereer-bcs3-lp.mjs` - generator. Draai opnieuw met `node genereer-bcs3-lp.mjs`.
- `bcs3-favicons/[slug].png` - opgehaalde merk-favicons.
- `webwinkel-keur-logo.svg` - WWK-logo (inline in het WWK-blok).

## Volgende stap

Deploy naar intro-pique.agency/bcs3/[slug] (`cd Klanten/BCS && vercel --prod --yes`) wanneer akkoord. Handgeschreven brieven voor dezelfde set via de brieven-csv-agent.
