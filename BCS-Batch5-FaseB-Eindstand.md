# BCS batch 5, Fase B eindstand

Datum: 23 september 2026. Werklijst: `Klanten/BCS/lp/sweep/BCS-Batch5-FaseB-Werklijst.csv`.

## Wat Fase B deze keer moest opleveren

Vier batches lang was het haakje een bevinding over de inrichting van de klantenservice:
de desk sluit om vijf uur, er staat geen telefoonnummer, de belofte is 24 uur. Dat leverde
90 gesprekken en nul afspraken op, want die inrichting is een keuze die ze bewust hebben
gemaakt en het antwoord is dus altijd "we doen hier al iets mee".

Fase B zocht daarom naar iets anders: bewijs dat er volume binnenkomt. Drie dingen tonen
dat aan, en ze staan alle drie op de eigen site van de prospect.

| | signaal | wat het bewijst |
|---|---|---|
| 1 | er staat een klantcontactvacature open | er komt meer binnen dan het team aankan |
| 2 | ticketsysteem plus meerdere taalmarkten | er is volume en er wordt al voor betaald |
| 3 | zakelijke verkoop naast de webshop | twee soorten vragen in dezelfde mailbox |

## De uitkomst

139 prospects, 135 sites bereikbaar.

| soort | aantal | wat ermee kan |
|---|---|---|
| trigger, bron openbaar | 7 | kaart plus landingspagina, triggerpoort geeft goed |
| trigger, mens moet kijken | 10 | kaart mag, maar iemand opent eerst de vacaturepagina |
| onderbouwing | 53 | belhaakje in de belsheet, geen kaartopening |
| geen signaal | 64 | site open, geen bewijs van volume |
| uitgesloten | 5 | afgevallen bij de beslisserronde |

Triggerpoort over de 17 triggers: **7 goed, 8 handcheck, 2 afkeur**. De twee afkeuren zijn
Superyoga en Mason Garments: allebei een echte klantenservicevacature op de eigen site,
allebei zonder plaatsingsdatum. Die datum moet met de hand van de pagina komen.

## Het onderscheid dat de batch draagt

**Een trigger is een handeling van een mens met een datum.** Een toestand is dat niet. Er
draait een ticketsysteem, er zijn elf markten, er is een pagina `/zakelijk`: dat is alle
drie waar en alle drie na te kijken, maar het is ring 1 uit `context/signaal-diepte.md` en
daarmee onderbouwing. Dit soort waarneming stond de vorige vier batches op de
kaart, en dat is de reden dat dit document het scheidt.

De 53 onderbouwingsregels gaan dus **wel** de belsheet in met een haakje, en **niet** de
kaart op als opening.

## Wat er stukging en hoe het nu staat

**De kolom `vacature` in de A-lijst is niet wat hij lijkt.** Die bevat de triggervacature
uit de sweep, en die viel terug op elke willekeurige vacature als er geen klantcontact-
vacature was. Door die kolom rechtstreeks te gebruiken kwamen er 59 "klantcontactsignalen"
uit die in werkelijkheid Media Buyers, magazijnmedewerkers en stagiairs social media waren.
Na de toets op werkveld plus rol bleven er 18 over. Dat is de echte opbrengst.

**Het eigen nieuwsoverzicht is geen bron.** `eigennieuws.py` vond over 139 shops zes
gedateerde berichten en alle zes waren contentmarketing: een handleiding voor een
JURA-melkkoeler, een biografie van een tennisser, productcopy over bouwsets. Het blog van
een D2C-webshop is een verkoopkanaal en geen nieuwsrubriek. Het spoor is uit
`faseb-bouw.py` geschrapt. De oogst staat nog in `A-nieuws.csv`.

**Een datum in de structured data kan jaren oud zijn.** Inktweb gaf `datePosted` 2021 terug
op een vacature die in augustus 2026 op LinkedIn stond, omdat het vacaturesjabloon nooit is
bijgewerkt. Een JSON-LD-datum ouder dan een jaar vervalt nu en valt terug op de
plaatsingsdatum van LinkedIn.

**Te snel scannen kost je de helft van je lijst.** De eerste ronde met tien workers gaf 65
van de 139 sites als onbereikbaar. Na een pauze en een herstelronde met twee workers waren
er daarvan 61 gewoon open. Het waren 429's van mijn eigen tempo, geen dode sites. Scan een
lijst als deze met hoogstens vier gelijktijdige verzoeken.

**Een winkelbanner in een citaat veroudert binnen een week.** Het citaat van Onlineverf
bevatte "Nazomer deals: 10% extra korting" en viel daardoor bij de tweede controle al af.
`faseb-bouw.py` knipt de banner er nu af en valt anders terug op de functietitel.

## Bestanden

| bestand | inhoud |
|---|---|
| `lp/sweep/BCS-Batch5-FaseB-Werklijst.csv` | alle 139, met soort, signaal, trigger, onderbouwing, belhaakje, beslisser en adres |
| `lp/sweep/BCS-Batch5-FaseB-Triggercheck.csv` | de 17 kaartwaardige regels in het formaat van de poort |
| `lp/sweep/BCS-Batch5-FaseB-Triggeruitslag.csv` | de uitslag van `triggercheck.py` per regel |
| `lp/sweep/A-signalen.csv` | het ruwe bewijs per shop van de eigen site |
| `lp/sweep/A-nieuws.csv` | de nieuwsoogst, niet gebruikt |

Nieuwe klantonafhankelijke tools: `Context/tools/ticketsignaal.py` en
`Context/tools/eigennieuws.py`.

## Wat hierna moet

1. **De twee datumloze vacatures met de hand nakijken** (Superyoga, Mason Garments).
2. **De 8 handcheck-regels openen** voordat de kaart de deur uit gaat: staat de vacature er
   nog.
3. **Adressen.** Van de 70 bruikbare prospects hebben er 30 een postcode. De rest moet er
   nog een krijgen voordat er iets gedrukt wordt.
4. **De 64 zonder signaal.** Die horen achteraan in plaats van eruit. Bij
   een aantal, zoals Swiss Sense en BERG Toys, komt het lage cijfer doordat ze hun markten
   met een landenkiezer regelen in plaats van met hreflang. Dat is met de hand te
   corrigeren als de batch aangevuld moet worden.
