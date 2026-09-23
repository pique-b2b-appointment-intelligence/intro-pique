# BCS Batch 3 - Deep research: beslisser + hook + adres

Vervolg op de Fase A/B prospectlijst. Doel: per prospect 100% de beslisser, 100% een sterke hook en 100% het bedrijfsadres. Aanpak: de 217 harde prospects kregen elk een deep-research hook (55 batches) met her-bevestiging van naam en adres; de 84 zachte prospects kregen een recovery-ronde (14 batches) om naam en adres alsnog hard te maken plus een hook.

## Uitkomst

| Categorie | Aantal |
|---|---|
| TIER1-prospects (uniek, na dedup CIME) | 300 |
| **Met een sterke, gebronde hook** | **300 (100%)** |
| Met 100% geverifieerd bedrijfsadres + hook (kaart kan eropaf) | 287 |
| **Volledig: geverifieerde beslissernaam + geverifieerd adres + hook** | **247** |
| Adres hard, beslisser = geverifieerde doelrol (naam volgt) | 40 |
| Adres nog te bevestigen | 13 |

## Beslisser-laag: functionele vs founder

De beslisser-tabel schrijft voor: <25 fte -> founder/eigenaar; 25-150 -> Head/Manager van CS/Operations/E-commerce; >150 -> Director. Omdat de BCS-ICP bedrijven met een volwassen in-house CS-afdeling droppt, zit ~80% van de lijst onder de 25 fte, waar de founder de echte beslisser is (en vaak zelf de CS doet, wat de hook is). Voor die groep is de founder correct.

Voor de 32 echt-middelgrote prospects (~25+ fte) is een aparte ronde gedaan om de operationele/commerciele beslisser te vinden (Head of Customer Care/Success, Operations Manager, E-commerce Manager, Commercieel Directeur), omdat die makkelijker te benaderen is voor een CS-uitbesteding. Uitkomst:
- Functionele beslisser gevonden en toegepast als primair contact (founder = fallback, in kolom `founder_fallback`): **CIME** (Loes Christiaens, Operations Manager), **De Bonte Koe** (Tomas van Klaveren, Operationeel manager), **Stooker** (Yoshka Stooker, E-commerce Manager), **Joe Merino** (Yvo Batenburg, E-commerce Manager).
- CS/Ops-laag bestaat aantoonbaar maar de huidige naam is niet publiek (via telefoon achterhalen), gevlagd in notitie: **Gray Label**, **Supergreens**, (en Undiemeister/HappySoaps als aandachtspunt).
- Rest: geen verifieerbare functionele laag; echt founder-run, founder blijft contact. Nooit een naam of functie verzonnen.

De recovery-ronde tilde 44 beslissers van doelrol naar geverifieerd en maakte 71 adressen hard. Waar de beslissernaam niet met een harde bron te bevestigen was (vaak KVK-persoonsdata achter betaalmuur) blijft het een doelrol met 'naam volgt', nooit een verzonnen naam.

## Bestand

`Klanten/BCS/BCS-Batch3-Prospects-Beslisser-Hook-Adres.csv` — 300 rijen, gesorteerd op volledigheid (compleet eerst). Kolommen: bedrijf, website, voornaam, achternaam, functie, beslisser_status, founder_fallback, straatnaam, postcode, plaatsnaam, land, adres_zeker, hook, hook_bron, notitie. De kolom `founder_fallback` is gevuld bij de bedrijven waar een functionele beslisser het primaire contact is.

Onderliggende data: `batch3-hooks/wave1-4.json` (hooks), `batch3-hooks/recovery.json`, `batch3-hooks/FINAL-assembled.json`.

## Hook-standaard

Elke hook is één specifieke, moeilijk vindbare observatie die een gesprek over klantenservice opent, met bron-URL's. Doorstaat de homepage-test en de SDR-test. Typen: strategische verandering (overname, nieuwe markt, funding, leiderschapswissel), groeisignaal (vacature voor support-rol, schaalsprong), spanning/contradictie (kanaalbelofte als same-day of 24/7 die botst met teamgrootte), seizoenspiek, en CS-signalen uit reviews. Copyregels gecheckt: geen em-dashes, geen zin die met 'Geen' begint, geen 'niet X maar Y', enkele aanhalingstekens, geen emoji.

## Belangrijke correcties en vlaggen (in de notitie-kolom)

- Beslisser-correcties: Kopje Thee (Tina Vancampenhout i.p.v. Senne Keysers), Food2Smile (Menno Snijders bleek Sales Manager, founder Miriam Bouwens / MD Chantal Meertens is juiste laag), Friedhats (Lex Wenneker).
- Beslisser vervallen: Bee Nature (oprichter Marine Andre verkocht eind 2020; huidige leiding niet publiek, opnieuw verifieren).
- Adres-correcties: Gftd (Generaal Lemanstraat 24), Keecie (Zeeburgerdijk 379), Maed for mini (Bloemgracht 166), MarathonR (De Bloementuin 30), Stricters (Korte Stadionweg 103a), La Rhode (Schepenstraat 6 Geulle), Snoozebaby (Cruquiusweg 96-E Amsterdam; oude adres was fulfilment-magazijn), Velor Cycling (Brightlands Chemelot Campus), HOUTR (Trivium 76 Etten-Leur), Washgiant (Veldkaamp 4).
- MyFleury: opgegeven adres bleek van een ander bedrijf; adres nog te bevestigen.
- Stabiliteitsvlag: Another Label had faillissement (feb 2024) met doorstart; stabiliteit checken.

## Volgende stap

De 248 volledige regels zijn direct klaar voor de handgeschreven brieven via [[brieven-csv-agent]] en de landingspagina's. De 40 'naam volgt'-regels: beslissernaam via KVK-uittreksel of telefonisch bevestigen. De 13 zonder hard adres: adres aanvullen of laten vallen.
