# BCS Batch 4 - de landingspagina's

Datum: 24 augustus 2026
Klant: Backbone Customer Service (Jeffrey)
Map: `Klanten/BCS/bcs4/` - 78 pagina's
URL-patroon: `intro-pique.agency/bcs4/[slug]`

## Wat er is gebouwd

De vorm komt onaangeraakt uit `Componenten/lp-v2`. Alleen het thema en de inhoud zijn nieuw, precies zoals `LEESMIJ.md` voorschrijft. Dat betekent dat de kaartlaag, de journeylijn, de voortgangsrail, het dock en de boeksheet meelopen zonder dat er iets aan de vorm is gesleuteld.

| Onderdeel | Waar |
|---|---|
| Thema | `Componenten/lp-v2/thema-bcs.css`, ook gekopieerd naar `bcs4/` |
| Generator | `Klanten/BCS/lp/bcs-lp-generator.py` |
| Copyblokken | `Klanten/BCS/lp/bcs-lp-copy.py` |
| Servicescan | `Klanten/BCS/lp/bcs-servicescan.py` en `.csv` |
| Video | `bcs4/jeffrey-staand.mp4`, 11 MB, met poster |
| Overzicht | `BCS-Batch4-LP-URLs.csv` en `.txt` |

## Het merk

De oude BCS-pagina's draaiden nog op het Pique-palet: amber, Playfair Display en Inter. Dat is nu weg. De kleuren komen van backbonecustomerservice.com zelf.

| Token | Waarde | Waar het vandaan komt |
|---|---|---|
| `--accent` | `#233DFF` | het elektrische blauw van hun site |
| `--ink` | `#211A12` | hun warme bijna-zwart |
| `--donker` | `#1A140D` | hero, kantelpunt en CTA |
| `--tape-rgb` | `232,226,212` | hun crème `#E8E2D4`, als plakband op het papier |
| `--serif` en `--sans` | Schibsted Grotesk | hun merkfont, dus geen serif |

Warm donker met elektrisch blauw laat dat blauw zingen. Playfair met Inter is volgens de standaard de tell van een gegenereerde pagina, en die combinatie zat in de oude BCS-pagina's.

## Logo en favicon

Het merk zelf staat nu in de nav en de footer, gehaald uit `assets/bcs-logo.png` op hun eigen site. Dat is het blauwe papieren vliegtuigje in exact `#233DFF`, wat het merkblauw uit het thema bevestigt.

Er staan twee versies in de map, want de nav is doorzichtig boven de donkere hero en daar heeft het merkblauw te weinig contrast:

| Bestand | Waar |
|---|---|
| `bcs-logo.png` | merkblauw, voor de witte nav en de footer |
| `bcs-logo-licht.png` | lichtblauw `#5B72FF`, voor de doorzichtige nav boven de hero |

Het component wisselt die twee zelf om via `.op-donker` en `.op-licht`, dus daar hoefde niets aan.

De favicon staat inline als base64 in de head, net als in batch 2 en 3, en komt uit datzelfde logo. Zo passen het tabblad en de nav bij elkaar.

## Het bewijs onder elke bevinding

De standaard vraagt als bewijs een letterlijk citaat met domein en datum, geen bronregel. Elke zin in een citaatblok is overgetypt van hun eigen contact- of servicepagina, met de controledatum eronder. Waar ik die zin niet letterlijk heb, toont de bevinding geen citaatblok. Een parafrase in een citaatblok zetten is de duurste fout die er is, want de prospect kijkt het in dertig seconden na.

Catwalk Junkie laat zien waarom dat werkt. Drie citaten van hun eigen site, onder elkaar:

- `'maandag t/m vrijdag tussen 9:00 en 18:00'`
- `'binnen 24 uur'`
- `'catwalkjunkie@uspfashion.com'`

Ze beloven 24 uur, ze zijn vijf dagen bereikbaar en het enige kanaal is een mailadres. Die drie zinnen naast elkaar zijn het hele argument.

| | Aantal van de 78 |
|---|---|
| Minstens één letterlijk citaat | 54 |
| Drie bevindingen | 26 |
| Voornaam op de kaart, hard geverifieerd | 19 |

De voornaam gaat alleen mee als de beslisser in Fase B op GEVERIFIEERD stond. Bij de rest opent de kaart met "Ik keek een tijd naar [bedrijf]", zonder aanhef. Een kaart die de verkeerde naam uitschrijft, is meteen ontmaskerd.

## Wat er per pagina verschilt

Vijf prospects kregen geen pagina, omdat hun site niets opleverde dat als bevinding standhoudt: Bijzonder Mooi, Naamkado, OR Coffee, Rebottled en Vitalitas. Veloretti staat op geparkeerd wegens Pon.Bike en heeft dus ook geen pagina.

Bij drie van die vijf kwam dat pas na de tweede servicescan boven. Die vond bij hen alsnog een telefoonnummer, waardoor de bevinding "alles loopt via het toetsenbord" onwaar werd. De generator ruimt zulke pagina's nu zelf op, want een oude pagina met een claim die inmiddels niet klopt is erger dan geen pagina.

Alles wat op elke pagina hetzelfde zou zijn, roteert over varianten die op een vaste hash van de bedrijfsnaam worden gekozen. Dezelfde prospect krijgt dus altijd dezelfde pagina, en de batch als geheel blijft onder de norm.

Gemeten met `tellscan.py`: **19,7 procent gedeelde woordmassa**, plafond 25, nul pagina's erboven. Zonder die rotatie stond de eerste versie op 48,1 procent en was de batch afgekeurd. Nu 19,7 procent.

## Controles

| Controle | Uitkomst |
|---|---|
| Vaste kleuren in `lp.css` | leeg, dus geen merklekkage naar andere klanten |
| `tellscan.py` op tells en verbrande zinnen | geen treffers |
| Gedeelde woordmassa | 14,1 procent van maximaal 25 |
| Echte 390px-viewport via iframe | gehaald |
| Horizontale overloop | nul elementen |
| Kantelpunt houdt zijn donkere vlak op mobiel | `rgb(26, 20, 13)`, klopt |
| Elke sheet-knop heeft een passende `data-tab` | zes van de zes |

## Drie correcties na het nakijken van de voorbeeldpagina

**De boekingsknop was stuk.** De pagina's wezen naar `cal.com/backbone-cs/30min`, overgenomen uit batch 3. Die geeft 404. Het echte adres staat op hun eigen site: `cal.com/jeffrey-backbone-cs/30min`. **De pagina's van batch 3 hebben dezelfde kapotte link, dus daar is nu ook niets te boeken.**

**Het kantelpunt was een muur.** Dat blok staat in displaytype van 2,5rem en had gemiddeld 40 woorden, met een uitschieter van 79. Het plakte namelijk alle mechanismen uit het dossier achter elkaar. Nu is het één zin van hooguit 17 woorden, gekozen op wat de zwaarste bevinding is.

**De drie mockups hoorden hier niet.** Het component toont bij Pique de kaart, de pagina en de afspraak, en dat is zelfverwijzend omdat Pique dat verkoopt. Een prospect van BCS koopt geen kaarten en geen landingspagina's. Er staan nu drie kaarten in dezelfde stijl met wat BCS wel levert: doorlopende bereikbaarheid, een vaste prijs per ticket en een mens als achtervang. De drie vinkjes eronder gaan over de overgang zelf.

Daarnaast hebben de bevindingen context gekregen uit het Fase B-dossier: hoe groot de shop is, in hoeveel markten hij levert, en wat klanten er in reviews over schrijven. Die reviewzinnen staan altijd in de lopende tekst met bronvermelding erbij, nooit in een citaatblok, want het zijn parafrases.

## Wat er live staat

Eén pagina staat live om te bekijken: **https://www.intro-pique.agency/bcs4/catwalk-junkie**

Twee dingen kwamen daarbij boven die anders stil waren misgegaan:

- `.vercelignore` sluit alle mp4-bestanden uit met een uitzondering per map, en voor `bcs4` bestond die nog niet. Zonder de toegevoegde regel `!bcs4/*.mp4` was de video van Jeffrey een 404 geweest.
- `lp-intro.js` valt zonder `ctaSub` terug op de standaardtekst "Video van Simon · 1 min 20". Die stond dus onder de knop van de kaartlaag, op een klantpagina waar Pique nergens hoort te staan. Elke volgende klantpagina op dit component moet `ctaSub` meegeven.

De overige 77 pagina's staan klaar in de map en zijn nog niet gecommit.

## Twee dingen die jij moet beslissen

**Het webadres op de kaart.** Er staat nu `intro-pique.agency/bcs4/[slug]`, zoals bij batch 3. De standaard zegt dat Pique op een klantpagina nergens hoort te staan, en dit is de laatste plek waar dat nog gebeurt. Jeffrey ondertekent de kaart, dus een prospect die het adres natrekt komt bij Pique uit. Zet Jeffrey een subdomein aan, dan is het één regel:

```bash
BCS_LP_BASIS=intro.backbonecustomerservice.com python3 bcs-lp-generator.py
```

**Het mailadres in de footer.** Ik heb `jeffrey@backbonecustomerservice.com` aangehouden. Klopt dat, of moet het een ander adres zijn?

## Iets kleins in het component

`_voorbeeld.html` verwees eerst naar `lp.js` terwijl het bestand `lp-v2.js` heet. Dat is inmiddels rechtgezet in de map, maar `LEESMIJ.md` noemt nog steeds `lp.js` in het stukje over wat er onderaan de body hoort.
