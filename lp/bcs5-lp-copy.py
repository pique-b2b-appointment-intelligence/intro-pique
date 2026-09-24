#!/usr/bin/env python3
"""Roterende copy voor de BCS batch 5-landingspagina's.

Waarom dit bestand los staat van batch 4. De pagina's van batch 4 openden met een
bevinding over de inrichting van de klantenservice: de desk sluit om vijf uur, er staat
geen telefoonnummer, de belofte is 24 uur. Dat leverde over vier batches 90 gesprekken en
nul afspraken op, want die inrichting is een keuze die de prospect bewust heeft gemaakt.
Het antwoord was altijd "we doen hier al iets mee", en dat is waar.

Batch 5 draait de pagina om. We bekritiseren niets. We laten zien wat er aan volume
zichtbaar is, en stellen daarna de drie vragen waarop ze het antwoord niet hebben: hoe
lang duurt het gemiddeld voor een klant antwoord heeft, wat vinden klanten van de service,
en hoeveel procent is in een bericht opgelost. Zie Klanten/BCS/BCS-Belscript-Batch5-Cijfers.md.

De regel die daaruit volgt en die in elke zin hieronder zit: **de pagina zegt nooit dat
er iets mis is.** Hij zegt wat er staat, en vraagt naar een getal.

Alles wat op elke pagina hetzelfde zou zijn roteert over varianten, gekozen op een vaste
hash van de bedrijfsnaam. Zonder die rotatie loopt de gedeelde woordmassa over de 25
procent die tellscan.py toestaat.
"""

# ── deel 1: waarom jij ────────────────────────────────────────────
S1_KOP = [
    "Waarom ik juist jullie schrijf.",
    "Waarom deze kaart bij jullie ligt.",
    "Waarom ik bij {bedrijf} uitkwam.",
    "Waarom jullie op mijn lijst staan.",
]
S1_STAART = [
    "Ik heb niets doorgerekend en ik ga ook niets aanwijzen. Ik heb alleen gekeken naar "
    "wat er aan volume zichtbaar is.",
    "Dit is geen analyse van jullie service. Ik heb gekeken hoeveel er binnenkomt, meer niet.",
    "Ik zeg niets over hoe jullie het doen. Ik kijk naar hoeveel er langskomt.",
    "Er zit geen oordeel over jullie klantenservice in. Wel een paar dingen die iets "
    "zeggen over volume.",
]

# ── deel 2: de kantelzin onder de waarnemingen ────────────────────
PIVOT = [
    "Al die dingen zeggen iets over hoeveel er binnenkomt. Ze zeggen niets over hoe snel "
    "het eruit gaat. Dat is precies het stuk dat bijna niemand meet.",
    "Dit is allemaal volume. Wat ik nergens kan zien is de doorlooptijd, en dat is nu net "
    "het getal waar een klant zijn oordeel op baseert.",
    "Wat hier staat gaat over instroom. Over uitstroom staat nergens iets, en daar zit de "
    "hele ervaring van de klant in.",
    "Hoeveel er binnenkomt is van buiten te zien. Hoe lang het daarna duurt niet, en juist "
    "dat cijfer bepaalt wat een klant van jullie vindt.",
]

# ── deel 3: de drie vragen, het hart van de pagina ────────────────
DRIE_KOP = [
    "Drie getallen.",
    "De drie cijfers.",
    "Drie vragen.",
    "Drie dingen die ik zou willen weten.",
]
DRIE_IN = [
    "Als ik {bedrijf} zou bellen, zou ik deze drie vragen stellen. Ze zeggen samen meer "
    "dan een uur presenteren.",
    "Dit zijn de drie dingen die ik aan elke webshop vraag. Meer heb ik er niet nodig.",
    "Als jullie deze drie getallen paraat hebben, is dit gesprek zo klaar en hoeven we "
    "verder niets.",
    "Drie vragen die ik bij {bedrijf} zou stellen. Ze zijn kort en ze zijn onaangenaam "
    "precies.",
]
DRIE_UIT = [
    "De meeste webshops hebben deze drie niet liggen. Dat komt doordat het gewoon gebeurt "
    "en er zelden een klacht over komt.",
    "Bijna niemand heeft ze paraat. Dat is ook logisch: het loopt, er piept niets, dus "
    "niemand telt.",
    "Negen van de tien keer komt er een schatting in plaats van een cijfer. Dat is geen "
    "slordigheid, dat is hoe het groeit.",
    "Ik hoor hier zelden een hard getal. Meestal een gevoel, en een gevoel schuift langzaam "
    "mee zonder dat iemand het merkt.",
]

# ── deel 4: wat dit kost ──────────────────────────────────────────
KOST_KOP = [
    "Waarom dat derde getal het duurste is.",
    "Wat een dag wachten doet.",
    "Waar het geld weglekt.",
    "De rekening die niemand opschrijft.",
]
KOST = [
    "Een vraag die in een bericht klaar is, kost een paar minuten. Dezelfde vraag over drie "
    "berichten en twee dagen kost een veelvoud, en de klant is aan het eind minder tevreden "
    "dan bij het begin. <strong>Dat verschil zie je nergens terug in een factuur.</strong>",
    "Een klant die op antwoord wacht, bestelt in die dagen niets. Haakt hij af, dan schrijft "
    "hij het soms op. <strong>Die ene regel blijft daarna staan voor iedereen die jullie "
    "opzoekt.</strong>",
    "Het gaat zelden mis bij de eerste vraag. Het gaat mis bij de tweede herinnering, want "
    "dan is het gesprek niet meer over de bestelling. <strong>Het gaat dan over hoe jullie "
    "met mensen omgaan.</strong>",
    "Elke wachtende klant kost twee keer: de order die blijft hangen, en de tijd die er "
    "alsnog in gaat zodra iemand geirriteerd terugbelt. <strong>Dat tweede stuk is altijd "
    "duurder dan het eerste.</strong>",
]
KOST_PULL = [
    "'Een klant beoordeelt je service op de dag dat er iets misgaat, niet op de andere dagen.'",
    "'De duurste vraag is die van de klant die hem twee keer moest stellen.'",
    "'Meer mensen inhuren lost de piek op. Het dal erna lost het niet op.'",
    "'Wat je niet meet, schuift. En het schuift altijd dezelfde kant op.'",
]

# ── deel 5: hoe het anders kan ────────────────────────────────────
ANDERS = [
    "Bij onze klanten weten we precies hoeveel er binnenkomt, hoe lang het duurt en wat "
    "ervan in een keer klaar is. Sturen kan pas op iets dat je ziet.",
    "Wij meten die drie getallen vanaf dag een. Aan een oplopende reactietijd zie je twee "
    "weken vooruit dat het gaat piepen, en dat is voordat de eerste klant klaagt.",
    "Wat wij overnemen gaan we ook tellen. Dat is het saaie deel van dit werk en tegelijk "
    "het enige deel waaraan je ziet of het beter wordt.",
    "Bij ons staan die drie cijfers op een scherm. Dat maakt het gesprek over klantcontact "
    "voor het eerst een gesprek over getallen in plaats van over gevoel.",
]

VOORSTEL_SUB = [
    "Een kwartier, drie getallen, en je weet waar {bedrijf} staat ten opzichte van de rest.",
    "Een kwartier bellen. Ik reken jullie drie getallen uit en zet ze naast de rest van de markt.",
    "Vijftien minuten. Aan het eind heb je drie cijfers over {bedrijf} die je nu niet hebt.",
    "Een kwartier aan de telefoon en je weet hoe {bedrijf} het doet vergeleken met "
    "vergelijkbare shops.",
]

# ── founder ───────────────────────────────────────────────────────
FOUNDER = [
    ["Ik ben Jeffrey. Ik draai het klantcontact voor een groep Nederlandse webshops, en "
     "daardoor weet ik wat een normale reactietijd is in vrijwel elke categorie.",
     "Dat is wat ik hier aanbied en verder niets. Ik reken jullie drie getallen uit en zeg "
     "waar ze staan. Wat je daarna doet is aan jou."],
    ["Ik ben Jeffrey. Ik begon Backbone omdat klantcontact bij bijna elke webshop het "
     "onderdeel is dat als laatste aandacht krijgt en als eerste piept.",
     "Inmiddels draai ik het voor genoeg shops om te weten wat normaal is. Die maatstaf "
     "deel ik graag, ook als je er verder niets mee doet."],
    ["Ik ben Jeffrey. In de shops waar ik binnenkom zie ik steeds hetzelfde: de site is "
     "getest, de advertenties zijn gemeten, en de mailbox groeide stilletjes mee.",
     "Daarom vraag ik naar die drie cijfers. Ze zijn bij vrijwel elke shop het stuk dat "
     "nooit gemeten is, en dat maakt ze interessant."],
]

# ── kleine teksten ────────────────────────────────────────────────
CTA_H = ["Zullen we bellen?", "Een kwartier?", "Even bellen?", "Vijftien minuten?"]
CTA_SUB = [
    "Een kwartier, en je hebt drie getallen over {bedrijf} die je nu niet hebt.",
    "Vijftien minuten aan de telefoon. Je verbindt je nergens aan.",
    "Een kwartier. Ik reken de cijfers uit, jij bepaalt wat je ermee doet.",
    "Kort gesprek, drie getallen, en daarna weet je waar {bedrijf} staat.",
]
ASK_SUB = [
    "Een kwartier is genoeg. Ik heb alleen jullie kant van het verhaal nodig.",
    "Vijftien minuten, en ik hoef niets voor te bereiden.",
    "Kort gesprek. Ik stel drie vragen en reken het daarna voor je uit.",
    "Een kwartier, zonder presentatie en zonder scherm. Gewoon drie cijfers.",
]
ASK_LEES = ["Ik lees eerst verder", "Eerst het voorstel lezen", "Ik lees het eerst uit",
            "Eerst even doorlezen"]
CTA_ALT = ["Of laat je nummer achter", "Of geef je nummer door", "Liever teruggebeld?",
           "Of laat een nummer achter"]
NAV_CTA = ["Plan een kwartier", "Even bellen", "Plan een gesprek", "Een kwartier plannen"]
SLOT_TAG = ["De kaart op je bureau", "De kaart die je vasthield", "De handgeschreven kaart",
            "De kaart die je kreeg"]
CHIP_LEES = ["2 minuten lezen", "Twee minuten leeswerk", "Ongeveer 2 minuten",
             "Kort, 2 minuten"]
HERO_SUB = [
    "Dit is geen analyse van jullie klantenservice. Het zijn drie getallen die ik zou "
    "willen weten, en waarom juist die drie.",
    "Ik zeg niets over hoe jullie het doen. Ik laat zien wat er aan volume zichtbaar is, en "
    "stel daarna drie vragen.",
    "Dit gaat niet over wat er beter kan. Het gaat over drie cijfers die bijna geen enkele "
    "webshop paraat heeft.",
    "Er staat hier geen lijst met verbeterpunten. Wel wat ik van buiten zie, en de drie "
    "vragen die daarop volgen.",
]
SHEET_NOTE = [
    "Een kwartier is genoeg. Loopt het door, dan is er ruimte.",
    "Ik zet een kwartier in de agenda. Er staat dertig minuten voor het geval het uitloopt.",
    "Vijftien minuten gepland, dertig gereserveerd.",
    "Een kwartier. De rest van het blok is er voor als het interessant wordt.",
]
DOCK = ["Een kwartier plannen", "Even bellen", "Plan een gesprek", "Kort bellen"]

# ── de handgeschreven kaart ───────────────────────────────────────
# Het middenstuk van de kaart, tussen de twee feiten en de ondertekening.
#
# Waarom dit roteert en in batch 4 niet. Daar stond op alle vijfenzeventig kaarten
# letterlijk dezelfde slotalinea. Op een kaart van veertig woorden is dat tweeëntwintig
# woorden gedeelde tekst, en tellscan rekende de batch daarop af op 38,5 procent terwijl
# het plafond 25 is. Een handgeschreven kaart wordt zelden naast een andere gelegd, maar
# de regel is de regel en het kost niets om hem te halen.
#
# Elke variant moet: naar de pagina hiernaast wijzen, de QR-code noemen zonder webadres
# (regel van 31 augustus 2026), en eindigen zonder belofte over wat er dan gebeurt.
KAART_MIDDEN = [
    "Ik ben daarna nog wat dieper in {bedrijf} gedoken. Wat me is opgevallen staat "
    "hiernaast. Scan de QR-code en ik neem je erin mee.",

    "Daarna ben ik verder gaan kijken bij {bedrijf}. De rest staat op het kaartje "
    "hiernaast. Scan de code, dan loop ik het met je langs.",

    "Ik heb er vervolgens wat langer naar gekeken. Wat me opviel heb ik hiernaast voor "
    "{bedrijf} gezet. De QR-code brengt je erheen.",

    "Vanaf daar ben ik verder gegaan. Hiernaast staat wat ik bij {bedrijf} nog meer zag. "
    "Scan de code, dan laat ik het je zien.",

    "Daarna ben ik nog even doorgegaan. Wat dat opleverde staat op de pagina hiernaast. "
    "Scan de QR-code en ik praat je bij.",

    "Ik ben er daarna nog wat verder ingedoken. De rest heb ik voor {bedrijf} hiernaast "
    "gezet. Via de code kom je er.",
]
