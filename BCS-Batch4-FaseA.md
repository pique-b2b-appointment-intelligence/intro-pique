# BCS Batch 4 - Fase A

Datum: 17 augustus 2026
Klant: Backbone Customer Service (Jeffrey)
Fase: A, discovery. Fase B (beslissers, adressen, harde verificatie) volgt hierna.

## Waarom deze batch anders is opgebouwd

Batch 3 leverde 301 Tier 1-prospects. In de fte-kolom van dat bestand staat het probleem zwart op wit: de grootste groep zit op 2 tot 8 medewerkers, en 21 bedrijven op 5 tot 15. Dat waren merken die aan alle ICP-criteria voldeden en toch nooit een gesprek konden opleveren, omdat er domweg te weinig tickets binnenkomen om uit te besteden.

De oorzaak zit in het oude ICP zelf. Dat schreef 500K tot 5M omzet voor en zocht naar bedrijven zonder systeem. Die twee criteria versterken elkaar de verkeerde kant op. Een merk zonder CS-systeem heeft meestal geen systeem omdat het te klein is om er een nodig te hebben.

Daarom draait het selectieprincipe om. Batch 4 zoekt naar merken waarvan aantoonbaar vaststaat dat er ticketvolume is. Een merk dat Gorgias of Zendesk betaalt, heeft tickets. Een merk dat in twaalf landen levert, heeft tickets in meerdere talen. Dat is harder bewijs dan een omzetschatting.

## De herijkte ICP

| Criterium | Batch 3 | Batch 4 |
|---|---|---|
| Omzetband | 500K tot 5M | 3M tot 20M |
| CS-team aanwezig | uitsluiting | toegestaan, wordt zelfs een pluspunt |
| Platform | Shopify hard | Shopify voorop, andere platforms mogen bij sterke fit |
| Merktype | eigen merk D2C | ongewijzigd, eigen merk D2C |
| Selectiebewijs | afwezigheid van een systeem | aanwezigheid van volume |

Bij 3M tot 20M heeft vrijwel elk merk al een of twee mensen op klantcontact. Dat is de opening voor Jeffrey. Het gesprek gaat over pieken, avonden en weekenden, verloop en kosten per ticket. Het gaat over werk dat al gebeurt en dat beter en goedkoper geregeld kan worden.

## Wat ik machinaal heb vastgesteld

Ik heb 351 Nederlandse en Belgische merken gescand op hun eigen website. Per merk staat vast:

- of de site leeft en op welk platform hij draait (Shopify herkend via de header en via de publieke productfeed)
- hoeveel producten in de feed staan, als maat voor assortiment en dus voor vragen
- welke CS-tooling draait (Gorgias, Zendesk, Freshdesk, Trengo, Intercom, Crisp, WhatsApp, AI-chat)
- hoeveel taal- en marktvarianten de site voert
- welke contactkanalen openstaan en welke ontbreken
- welk reviewplatform draait en hoeveel reviews zichtbaar zijn
- of er naast D2C ook een wholesale- of B2B-ingang is
- of er een carrierepagina met een CS-vacature staat
- KVK-nummer, BTW-nummer, postcode en telefoonnummer waar die in de site staan

De ruwe scandata staan in `BCS-Batch4-Scan-Ruwe-Data.csv`. Alles in dat bestand is waargenomen op 17 augustus 2026, dus geen schatting.

## Overlap met eerdere batches

Ik heb op drie manieren gecontroleerd wie BCS al gehad heeft:

1. Alle bedrijfsnamen uit elke BCS-CSV in de map, genormaliseerd op kleine letters zonder leestekens. Dat levert 1.413 namen.
2. Alle websites uit diezelfde bestanden, 892 domeinen.
3. Alle mapnamen van de landingspagina's in `bcs`, `bcs2` en `bcs3`, 460 slugs. Wie een pagina kreeg, is echt benaderd.

Die derde controle was nodig. Naif Care stond in de oude lijst onder een andere schrijfwijze, waardoor de naamcheck hem doorliet terwijl er in batch 1 al een landingspagina voor klaarstond. Hij is er alsnog uit gehaald. Na alle drie de controles staan er nul botsingen tussen deze lijst en wat eerder de deur uit ging.

## Van 351 naar 100

| Stap | Aantal |
|---|---|
| Gescande kandidaten | 351 |
| Site leeft | 290 |
| Al benaderd in batch 1, 2 of 3 | 48 af |
| Te groot voor de band of concern met eigen CS-apparaat | 57 af |
| Verkoopt via dealers of groothandel, webshop is etalage | 71 af |
| Te weinig consumentenvolume | 11 af |
| **Blijft over** | **116** |
| Waarvan top 100 | 100 |
| Reserve | 16 |

De 139 afvallers staan met reden in `BCS-Batch4-FaseA-Uitgesloten.csv`, zodat je kunt zien of ik ergens te streng ben geweest.

## De top 100

Van de honderd draait 51 op Shopify, 23 heeft een volwassen CS-tool draaien en 45 is D2C-kern, waarbij de webshop het hoofdkanaal is. Van 49 heb ik het KVK-nummer al, van 64 de postcode en van 36 het telefoonnummer, wat Fase B goedkoper maakt.

Model in de tabel: D2C-kern betekent dat de webshop het hoofdkanaal is. Hybride betekent eigen merk met zowel wholesale als een eigen webshop, waarbij het consumentenvolume echt is en de wholesale-verhouding in Fase B nog vastgesteld moet worden.

| # | Bedrijf | Domein | Vertical | Model | Volumebewijs |
|---|---|---|---|---|---|
| 1 | Jane Lushka | janelushka.com | fashion-dames | hybride | volwassen CS-tool: gorgias, 48 taal-/marktvarianten, 919 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 2 | Aaiko | aaiko.com | fashion-dames | D2C-kern | volwassen CS-tool: gorgias, 27 taal-/marktvarianten, 357 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 3 | 10DAYS | 10days.nl | fashion-dames | D2C-kern | volwassen CS-tool: gorgias, 14 taal-/marktvarianten, 358 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 4 | Summum Woman | summumwoman.com | fashion-dames | hybride | volwassen CS-tool: gorgias, 4 taal-/marktvarianten, 654 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 5 | LaDress | ladress.com | fashion-dames | D2C-kern | volwassen CS-tool: trengo, 6 taal-/marktvarianten, 491 producten in de feed, Shopify |
| 6 | Lekker Bikes | lekkerbikes.com | mobiliteit | D2C-kern | volwassen CS-tool: freshdesk, 13 taal-/marktvarianten, 46 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 7 | Catwalk Junkie | catwalkjunkie.com | fashion-dames | hybride | 40 taal-/marktvarianten, 613 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 8 | Poools | poools.nl | fashion-dames | hybride | 144 taal-/marktvarianten, 324 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 9 | Violet Hamden | violethamden.com | sieraden | D2C-kern | 5 taal-/marktvarianten, 3000 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 10 | Colourful Rebel | colourfulrebel.com | fashion-dames | D2C-kern | 33 taal-/marktvarianten, 799 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 11 | Poederbaas | poederbaas.com | sport-wintersport | hybride | 54 taal-/marktvarianten, 510 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 12 | Cosmeau | cosmeau.com | huishoud | D2C-kern | lichte CS-tool: crisp, 4 taal-/marktvarianten, 126 producten in de feed, 1843 reviews zichtbaar, B2B/wholesale naast D2C, Shopify |
| 13 | Zenggi | zenggi.com | fashion-dames | hybride | 5 taal-/marktvarianten, 487 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 14 | Ballin Amsterdam | ballinamsterdam.com | fashion-streetwear | D2C-kern | volwassen CS-tool: gorgias, 2 taalvarianten, 171 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 15 | Isabel Bernard | isabelbernard.com | sieraden | D2C-kern | 10 taal-/marktvarianten, 264 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 16 | RainPharma | rainpharma.com | beauty-be | hybride | 32 taal-/marktvarianten, 250 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 17 | Moodstreet | moodstreet.nl | kinderkleding | hybride | 6 taal-/marktvarianten, 228 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 18 | ANNA plus NINA | anna-nina.nl | sieraden | hybride | 2 taalvarianten, 819 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 19 | Ivy Beau | ivybeau.com | fashion-dames | hybride | 3 taal-/marktvarianten, 601 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 20 | Butcher of Blue | butcherofblue.com | fashion-heren | hybride | 3 taal-/marktvarianten, 360 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 21 | Rosefield | rosefieldwatches.com | horloges | hybride | 14 taal-/marktvarianten, 545 producten in de feed, Shopify |
| 22 | Studio Ins en Outs | studioinsenouts.nl | lifestyle | D2C-kern | 5 taal-/marktvarianten, 960 producten in de feed, Shopify |
| 23 | Raizzed | raizzed.com | kinderkleding | hybride | 3 taal-/marktvarianten, 408 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 24 | Wolplein | wolplein.nl | hobby | hybride | 25 taal-/marktvarianten, 3000 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 25 | Sapph | sapph.com | lingerie | hybride | volwassen CS-tool: gorgias, 230 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 26 | Nialaya | nialaya.com | sieraden | D2C-kern | volwassen CS-tool: gorgias, 661 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 27 | Trixie Baby | trixie-baby.com | baby-be | hybride | lichte CS-tool: crisp, 5 taal-/marktvarianten, 785 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 28 | Marcels Green Soap | marcelsgreensoap.com | huishoud | hybride | 5 taal-/marktvarianten, 137 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 29 | Malelions | malelions.com | fashion-streetwear | hybride | 2 taalvarianten, 2568 producten in de feed, Shopify |
| 30 | Quotrell | quotrell.com | fashion-streetwear | D2C-kern | 11 taal-/marktvarianten, 355 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 31 | Loavies | loavies.com | fashion-dames | D2C-kern | volwassen CS-tool: zendesk, 4 taal-/marktvarianten, B2B/wholesale naast D2C, headless/custom of onbekend platform |
| 32 | Carnibest | carnibest.nl | huisdier | D2C-kern | volwassen CS-tool: zendesk, 123 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 33 | Muchachomalo | muchachomalo.com | ondergoed | hybride | 4 taal-/marktvarianten, 1725 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 34 | Xtorm | xtorm.eu | elektronica | hybride | 11 taal-/marktvarianten, 161 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 35 | Shoesme | shoesme.nl | kinderschoenen | hybride | volwassen CS-tool: zendesk, 3 taal-/marktvarianten, B2B/wholesale naast D2C, magento |
| 36 | Walra | walra.nl | home-textiel | hybride | 360 producten in de feed, 16418 reviews zichtbaar, B2B/wholesale naast D2C, Shopify |
| 37 | Seepje | seepje.com | huishoud | hybride | 3 taal-/marktvarianten, 64 producten in de feed, 1202 reviews zichtbaar, Shopify |
| 38 | Pieter Pot | pieter-pot.nl | food-abonnement | D2C-kern | 528 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 39 | Eyelove Brillen | eyelovebrillen.nl | brillen | D2C-kern | 2 taalvarianten, B2B/wholesale naast D2C, woocommerce, volumeoordeel op productmodel: brillen op sterkte plus eigen winkels |
| 40 | Moscow Fashion | moscowfashion.nl | fashion-dames | hybride | volwassen CS-tool: trengo, 3 taal-/marktvarianten, B2B/wholesale naast D2C, shopware |
| 41 | Fromanteel | fromanteel.nl | horloges | hybride | 16 taal-/marktvarianten, Shopify |
| 42 | Veloretti | veloretti.com | mobiliteit | D2C-kern | volwassen CS-tool: gorgias, Shopify |
| 43 | Bunnies JR | bunniesjr.nl | kinderschoenen | hybride | 590 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 44 | Yogisha | yogisha.nl | sport | D2C-kern | volwassen CS-tool: zendesk, 1557 reviews zichtbaar, B2B/wholesale naast D2C, lightspeed |
| 45 | Dstrezzed | dstrezzed.com | fashion-heren | hybride | 4 taal-/marktvarianten, 281 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 46 | Blond Amsterdam | blond-amsterdam.com | lifestyle | D2C-kern | volwassen CS-tool: gorgias, CS-vacature op de site, shopware |
| 47 | Retour Jeans | retourjeans.com | kinderkleding | hybride | 6 taal-/marktvarianten, B2B/wholesale naast D2C, woocommerce |
| 48 | Floer | floer.nl | vloeren | D2C-kern | B2B/wholesale naast D2C, woocommerce, volumeoordeel op productmodel: vloeren: samples, m2-berekening, leggen en kleurafwijking |
| 49 | Veneta | veneta.com | maatwerk-raamdecoratie | D2C-kern | headless/custom of onbekend platform, site achter bot-beveiliging (scan beperkt), volumeoordeel op productmodel: raamdecoratie op  |
| 50 | Rehab Footwear | rehabfootwear.com | schoenen | hybride | 2 taalvarianten, 373 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 51 | Wakuli | wakuli.com | food-abonnement | D2C-kern | 5 taal-/marktvarianten, 57 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 52 | Printenbind | printenbind.nl | personalisatie-print | D2C-kern | volwassen CS-tool: intercom, B2B/wholesale naast D2C, headless/custom of onbekend platform |
| 53 | Fred de la Bretoniere | freddelabretoniere.com | schoenen | hybride | 3 taal-/marktvarianten, B2B/wholesale naast D2C, shopware |
| 54 | Homey | homey.app | smart-home | D2C-kern | 82 taal-/marktvarianten, headless/custom of onbekend platform |
| 55 | Flinndal | flinndal.nl | supplementen | D2C-kern | headless/custom of onbekend platform, site achter bot-beveiliging (scan beperkt), volumeoordeel op productmodel: vitamine-abonneme |
| 56 | Tramontana | tramontana.nl | fashion-dames | hybride | volwassen CS-tool: zendesk, B2B/wholesale naast D2C, shopware |
| 57 | PLNTS | plnts.com | planten | D2C-kern | B2B/wholesale naast D2C, headless/custom of onbekend platform, volumeoordeel op productmodel: levende planten per post: schade en  |
| 58 | Sencebeauty | sencebeauty.nl | beauty | hybride | 4 taal-/marktvarianten, B2B/wholesale naast D2C, headless/custom of onbekend platform |
| 59 | Charlie Temple | charlietemple.com | brillen | D2C-kern | headless/custom of onbekend platform, volumeoordeel op productmodel: brillen op sterkte online: sterktecontrole, pasvorm, retour |
| 60 | Nukus | nukus.nl | fashion-dames | hybride | 217 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 61 | Purewhite | purewhite.nl | fashion-streetwear | D2C-kern | 264 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 62 | Vinrose | vinrose.nl | kinderkleding | hybride | 6 taal-/marktvarianten, headless/custom of onbekend platform |
| 63 | Podobrace | podobrace.nl | gezondheid | D2C-kern | volwassen CS-tool: trengo, 2 taalvarianten, headless/custom of onbekend platform |
| 64 | Werk aan de Muur | werkaandemuur.nl | lifestyle | D2C-kern | headless/custom of onbekend platform, site achter bot-beveiliging (scan beperkt), volumeoordeel op productmodel: print on demand:  |
| 65 | Grutto | grutto.com | food-abonnement | D2C-kern | headless/custom of onbekend platform, volumeoordeel op productmodel: vleespakket-abonnement met leverafspraken en versbederf |
| 66 | Power Supplements | powersupplements.nl | supplementen | D2C-kern | 4 taal-/marktvarianten, B2B/wholesale naast D2C, headless/custom of onbekend platform |
| 67 | Somnox | somnox.com | health-tech | D2C-kern | volwassen CS-tool: intercom, 2 taalvarianten, woocommerce |
| 68 | Fotofabriek | fotofabriek.nl | personalisatie-print | D2C-kern | headless/custom of onbekend platform, volumeoordeel op productmodel: fotoproducten: bestandsproblemen, drukfouten, deadlines |
| 69 | Estseven | estseven.com | fashion-dames | hybride | 186 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 70 | CanvasCompany | canvascompany.nl | personalisatie-print | D2C-kern | volwassen CS-tool: zendesk, magento |
| 71 | Matt Sleeps | mattsleeps.com | slapen | D2C-kern | volwassen CS-tool: intercom, B2B/wholesale naast D2C, headless/custom of onbekend platform |
| 72 | Just Franky | justfranky.com | personalisatie-sieraden | D2C-kern | headless/custom of onbekend platform, volumeoordeel op productmodel: gegraveerde sieraden: spelfouten en levertijd rond feestdagen |
| 73 | Names4ever | names4ever.nl | personalisatie-sieraden | D2C-kern | 2 taalvarianten, headless/custom of onbekend platform, volumeoordeel op productmodel: gepersonaliseerde sieraden |
| 74 | BoJungle | bojungle.eu | baby-be | hybride | 10 taal-/marktvarianten, B2B/wholesale naast D2C, woocommerce |
| 75 | Indian Blue Jeans | indianbluejeans.com | kinderkleding | hybride | 80 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 76 | Sticky Lemon | stickylemon.nl | tassen | hybride | 465 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 77 | Blue Rebel | bluerebel.nl | kinderkleding | hybride | 4 taal-/marktvarianten, B2B/wholesale naast D2C, headless/custom of onbekend platform |
| 78 | Yehwang | yehwang.com | sieraden | hybride | 7 taal-/marktvarianten, B2B/wholesale naast D2C, headless/custom of onbekend platform |
| 79 | LouLou Essentiels | loulouessentiels.nl | tassen | hybride | 184 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 80 | Casimoda | casimoda.nl | elektronica-accessoires | D2C-kern | lightspeed, volumeoordeel op productmodel: hoog ordervolume telefoonaccessoires |
| 81 | Shabbies Amsterdam | shabbiesamsterdam.com | schoenen | hybride | 3 taal-/marktvarianten, B2B/wholesale naast D2C, shopware |
| 82 | Dogs Companion | dogscompanion.nl | huisdier | D2C-kern | volwassen CS-tool: zendesk, lightspeed |
| 83 | Fitchef | fitchef.nl | food-abonnement | D2C-kern | headless/custom of onbekend platform, volumeoordeel op productmodel: maaltijdabonnement met wekelijkse leveringen |
| 84 | Greve Shoes | greve.nl | schoenen | hybride | 282 producten in de feed, B2B/wholesale naast D2C, Shopify |
| 85 | Natural Heroes | naturalheroes.nl | supplementen | hybride | B2B/wholesale naast D2C, Shopify |
| 86 | Wolky | wolky.com | schoenen | hybride | 5 taal-/marktvarianten, B2B/wholesale naast D2C, woocommerce |
| 87 | Esqualo | esqualo.com | fashion-dames | hybride | lichte CS-tool: tawk, B2B/wholesale naast D2C, magento |
| 88 | Matchu Sports | matchusports.com | maatwerk-sport | D2C-kern | woocommerce, volumeoordeel op productmodel: maatwerk teamkleding, deels via clubs |
| 89 | MYOMY do goods | myomydogoods.com | tassen | D2C-kern | headless/custom of onbekend platform, volumeoordeel op productmodel: leren tassen, garantie- en reparatievragen |
| 90 | Circle of Trust | circleoftrust.nl | fashion-dames | hybride | B2B/wholesale naast D2C, magento |
| 91 | Trouwringen Circles | circles.nl | sieraden | D2C-kern | headless/custom of onbekend platform, volumeoordeel op productmodel: maatwerk trouwringen, lage aantallen |
| 92 | Costes Fashion | costesfashion.com | fashion-dames | hybride | 2 taalvarianten, B2B/wholesale naast D2C, salesforce-cc |
| 93 | Blackstone Shoes | blackstoneshoes.com | schoenen | hybride | headless/custom of onbekend platform, site achter bot-beveiliging (scan beperkt), volumeoordeel op productmodel: site bot-beveilig |
| 94 | Xsensible | xsensible.com | schoenen | hybride | B2B/wholesale naast D2C, magento |
| 95 | Red-Rag | red-rag.nl | kinderschoenen | hybride | B2B/wholesale naast D2C, shopware |
| 96 | Maxim Sports Nutrition | maximsport.com | sportvoeding | D2C-kern | headless/custom of onbekend platform, volumeoordeel op productmodel: sportvoeding, deels via dealers |
| 97 | Beaumont Amsterdam | beaumont.nl | fashion-dames | hybride | Shopify |
| 98 | Frankie and Liberty | frankieandliberty.com | kinderkleding | hybride | B2B/wholesale naast D2C, woocommerce |
| 99 | Fifth House | fifthhouse.nl | fashion-dames | hybride | 2 taalvarianten, shopware |
| 100 | Off The Pitch | offthepitch.com | fashion-streetwear | hybride | shopware |

Rang 1 tot 40 is Tier 1, 41 tot 70 is Tier 2, 71 tot 100 is Tier 3.

## Waar het bewijs dun wordt

Dit hoort erbij, want het bepaalt hoe je de lijst gebruikt.

Tot ongeveer rang 70 staat het volumebewijs stevig. Daaronder zit een groep waar de fit logisch is en het bewijs mager, meestal omdat de site de scanner blokkeert of omdat het merk vooral via winkels verkoopt. Die staan bewust in de lijst, met de opmerking dat Fase B daar eerst het volume moet harden voordat er research op gaat.

Er is nog iets. De Nederlandse markt van eigen-merk D2C tussen 3M en 20M, minus de 911 bedrijven die BCS al benaderd heeft, is eindig. Om aan honderd namen van Tier 1-kwaliteit te komen zijn er drie knoppen:

1. De bovengrens naar 30M tillen. Daar zit een groep met echt volume en met een CS-afdeling die tegen zijn plafond loopt.
2. Duitsland en Vlaanderen erbij nemen. Dezelfde merken, groter marktbereik, en meertaligheid is precies waar BCS goed in is.
3. De cashcow-bak openen die je noemde: dropshippers en resellers met hoog ticketvolume. Buiten het ICP, dus alleen voor gesprekken die de agenda vullen.

Ik heb die drie bewust nog dichtgehouden, omdat jij eerst wilde zien wat de zuivere ICP-lijst oplevert.

## Wat Fase B moet doen

Per prospect, in deze volgorde, stoppen bij de eerste poort die faalt:

1. Omzetband harden. Voor de hybride merken is dat de belangrijkste vraag: hoeveel van de omzet komt uit de eigen webshop.
2. Beslisser bepalen. Onder 25 fte de oprichter, tussen 25 en 150 de Head of Operations, E-commerce of Customer Care, daarboven de directeur. Nooit invullen wat je niet hard hebt.
3. CS-situatie verifieren. Hoeveel mensen doen het klantcontact, welk pakket draait er, en wat kost dat.
4. Adres controleren via twee bronnen, zodat de handgeschreven kaart aankomt.

Voor de eerste golf zou ik rang 1 tot 40 nemen en die volledig door Fase B halen. Dat is genoeg materiaal voor de beller om mee te beginnen, en het houdt de researchinvestering bij de namen waar hij het meeste kans maakt.

## Bestanden

| Bestand | Inhoud |
|---|---|
| `BCS-Batch4-FaseA-Shortlist.csv` | 116 kandidaten, gerangschikt, met alle scandata per merk |
| `BCS-Batch4-FaseA-Uitgesloten.csv` | 139 afvallers met de reden van uitsluiting |
| `BCS-Batch4-Scan-Ruwe-Data.csv` | ruwe scanuitkomst van alle 351 gescande domeinen |
