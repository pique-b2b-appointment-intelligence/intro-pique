#!/usr/bin/env python3
"""Copyblokken voor de BCS-landingspagina's.

Alles wat per pagina hetzelfde zou zijn, staat hier in varianten. De generator
kiest per prospect een variant op basis van een vaste hash van de bedrijfsnaam,
zodat dezelfde prospect altijd dezelfde pagina krijgt en de batch als geheel
onder de grens voor gedeelde woordmassa blijft (25 procent, zie tellscan.py).

Regels uit Context/writing-standards.md gelden ook hier: ik-vorm, spreektaal,
korte zinnen. Zinnen die met Niet, Geen, Juist of Precies beginnen mogen niet,
en verbrande zinnen evenmin.
"""

# ── deel 1: waarom jij ────────────────────────────────────────────
S1_KOP = {
    "De bereikbaarheid is smaller dan wat de klant verwacht": [
        "Je klanten winkelen 's avonds. Je servicedesk niet.",
        "De vraag komt binnen op een moment dat er niemand zit.",
        "Bereikbaarheid is bij jullie een keuze geworden.",
        "Er zit een gat tussen wanneer je klant vraagt en wanneer jij antwoordt.",
    ],
    "Het volume groeit sneller dan de bezetting": [
        "Het aantal vragen groeit harder dan het aantal mensen.",
        "Jullie zijn gegroeid. De mailbox groeide mee.",
        "Elke order erbij is ook een gesprek erbij.",
        "De omzet schaalt. Het klantcontact doet dat lastiger.",
    ],
    "Er komt een merk, land of kanaal bij": [
        "Er is iets bij gekomen, en het klantcontact moet mee.",
        "Meer markten betekent meer soorten vragen door dezelfde deur.",
        "Elk kanaal dat je opent, opent ook een verwachting.",
        "Uitbreiden kost aan de voorkant weinig en aan de achterkant veel.",
    ],
    "Er wisselt iets in eigendom of leiding en alles wordt opnieuw ingericht": [
        "Er is net iets veranderd bij jullie aan de top.",
        "Wie opnieuw begint, richt ook het klantcontact opnieuw in.",
        "Een wissel aan de leiding is het moment dat alles op tafel gaat.",
        "Nieuwe leiding, en dus een nieuwe blik op wat er staat.",
    ],
    "Het team is klein en klantcontact wordt erbij gedaan": [
        "Klein team, veel klanten, en klantcontact komt erbij.",
        "Iemand bij jullie doet de service ernaast.",
        "Het team is bewust klein gehouden. Dat heeft een prijs aan de servicekant.",
        "Bij een klein team is klantcontact altijd het werk van iemand die ook iets anders doet.",
    ],
}

S1_TEKST = [
    "Ik kijk voor mijn werk naar hoe webshops hun klantcontact hebben staan. "
    "Bij jullie viel me iets op dat ik vaker zie bij merken die hard groeien.",
    "Ik kwam bij jullie terecht omdat ik in deze hoek van de markt kijk naar hoe "
    "shops hun klantvragen opvangen. Wat ik zag, wilde ik even voorleggen.",
    "Voor mijn werk loop ik webshops langs op één ding: wat er gebeurt als een "
    "klant een vraag heeft. Bij jullie bleef ik langer hangen dan gepland.",
    "Ik heb naar jullie contactpagina's gekeken zoals een klant dat zou doen. "
    "Dus met een vraag in mijn hoofd en de wens om snel antwoord te krijgen.",
    "Ik doe dit werk lang genoeg om te weten waar het meestal knelt. Bij jullie "
    "wees het naar dezelfde plek, dus ik ben even doorgelopen.",
]

# ── deel 3: het kantelpunt, aanloop naar het mechanisme ───────────
PIVOT_IN = [
    "Zet die dingen naast elkaar en er ontstaat een patroon.",
    "Los van elkaar valt het mee. Bij elkaar wordt het een mechanisme.",
    "Op zichzelf is elk punt klein. Samen vormen ze de bottleneck.",
    "Wat me opvalt is hoe die punten in elkaar grijpen.",
]

# ── deel 5: wat dit kost ──────────────────────────────────────────
REKENSOM_KOP = [
    "Wat dat in de praktijk kost.",
    "Reken het eens door.",
    "De rekening die niemand opschrijft.",
    "Wat er ondertussen weglekt.",
]
REKENSOM = [
    "Een vraag die aan de telefoon in twee minuten klaar is, kost per mail al snel "
    "drie berichten over twee dagen. <strong>Dezelfde klant, tien keer zoveel werk, "
    "en een slechter gevoel aan het eind.</strong>",
    "Een klant die wacht, koopt in die dagen niets. En als hij afhaakt, schrijft hij "
    "er soms iets over op. <strong>Die ene review blijft daarna staan voor iedereen "
    "die jullie opzoekt.</strong>",
    "Elke wachtende klant kost twee keer. Eén keer de order die blijft hangen, en "
    "één keer de tijd die er alsnog in gaat zodra iemand kwaad terugbelt. "
    "<strong>Het tweede stuk is altijd duurder.</strong>",
    "Het gaat zelden mis bij de eerste vraag. Het gaat mis bij de derde herinnering. "
    "<strong>Tegen die tijd is het gesprek al over iets anders gaan.</strong>",
]
REKENSOM_PULL = [
    "'Meer mensen inhuren lost de piek op. Het lost het dal daarna niet op.'",
    "'Een klant meet je service op de dag dat er iets misgaat, niet op de andere dagen.'",
    "'De duurste ticket is die van de klant die twee keer moest vragen.'",
    "'Bereikbaarheid is geen kostenpost tot het moment dat je hem misloopt.'",
]

# ── deel 6: hoe het anders kan ────────────────────────────────────
ANDERS = [
    "Stel dat elke vraag binnen een paar minuten antwoord krijgt, ook op zondagavond "
    "en ook in december. Zonder dat je daar iemand voor hoeft aan te nemen.",
    "Stel dat de mailbox aan het eind van de dag leeg is, en dat jij alleen nog de "
    "gevallen ziet waar echt een besluit voor nodig is.",
    "Stel dat je klanten hetzelfde antwoord krijgen op dinsdagochtend en op "
    "zaterdagavond, in de taal waarin ze schrijven.",
    "Stel dat de drukke weken eruitzien als de rustige. Zelfde reactietijd, zelfde "
    "toon, zonder dat er iemand extra ingewerkt moet worden.",
]

VOORSTEL_SUB = [
    "Ik neem het klantcontact van {bedrijf} over. De mail, de chat, WhatsApp en de telefoon.",
    "Wij zetten de servicedesk van {bedrijf} op en draaien hem daarna zelf.",
    "Ik richt het klantcontact van {bedrijf} in en jij houdt de regie op de uitzonderingen.",
    "Wij nemen de vragen van jullie klanten over, in jullie toon en onder jullie naam.",
]

# ── founder ───────────────────────────────────────────────────────
FOUNDER = [
    ["Ik ben Jeffrey. Ik begon Backbone omdat klantcontact bij bijna elke webshop het "
     "onderdeel is dat als laatste aandacht krijgt en als eerste piept.",
     "Wij nemen het over. Wij richten het in, wij draaien het, en jij hoeft er zelf "
     "niets voor te doen. Er staat altijd een mens achter, dus als het ingewikkeld "
     "wordt, pakt iemand het op."],
    ["Ik ben Jeffrey. In de shops waar ik binnenkom zie ik steeds hetzelfde: de site is "
     "getest, de advertenties zijn gemeten, en de mailbox groeide stilletjes mee.",
     "Daar zijn wij voor. Wij zetten het klantcontact op, draaien het, en houden de "
     "toon van jullie merk aan. Bij een lastig geval neemt een mens het over."],
    ["Ik ben Jeffrey. Ik zag te vaak dat een goed merk struikelde over iets kleins: een "
     "klant die drie dagen op antwoord wachtte en het daarna opschreef.",
     "Wij lossen dat op door het over te nemen. Inrichten, draaien en meten doen wij. "
     "Jij ziet alleen nog de gevallen die een besluit van jou vragen."],
]

# ── cta ───────────────────────────────────────────────────────────
CTA_H = ["Even bijpraten?", "Zullen we bellen?", "Twintig minuten?", "Even sparren?"]
CTA_SUB = [
    "Gewoon kijken of dit bij {bedrijf} past. Twintig minuten, en je verbindt je nergens aan.",
    "Ik loop je door de cijfers heen die ik heb gezien. Daarna weet je of het de moeite is.",
    "Een gesprek van twintig minuten waarin ik laat zien wat ik zou doen bij {bedrijf}.",
    "Ik vertel wat ik zou aanpakken en wat het kost. Daarna beslis jij.",
]

# ── het aanbod halverwege ─────────────────────────────────────────
ASK_SUB = [
    "Hieronder staat wat ik zou doen. Wil je dat liever horen dan lezen, dan pak ik de "
    "telefoon. Twintig minuten, en je zit nergens aan vast.",
    "Wat ik voorstel staat hieronder. Als je het liever even bespreekt, bel ik je. "
    "Twintig minuten is genoeg.",
    "Verderop staat mijn voorstel. Liever in het echt horen? Dan bel ik je even, "
    "en daarna weet je of het past.",
    "Hieronder leg ik uit hoe ik het zou aanpakken. Bellen mag ook, dan hoor je het "
    "in twintig minuten.",
]

# ── hero ──────────────────────────────────────────────────────────
HERO_H1 = [
    'Daarom kreeg je <span class="u">mijn kaart</span>.',
    'Dit zag ik <span class="u">bij jullie</span>.',
    'Waarom ik jou <span class="u">schreef</span>.',
    'Even over <span class="u">jullie klantcontact</span>.',
    'Dit viel me op, <span class="u">en het bleef hangen</span>.',
]
SLOT_TAG = ["De kaart op je bureau", "De kaart die je vasthield",
            "De kaart die je net scande", "De kaart uit je hand"]
CHIP_LEES = ["2 minuten lezen", "Twee minuten leeswerk", "Ongeveer 2 minuten",
             "Kort, twee minuten"]

# ── de drie mockups ───────────────────────────────────────────────
TOON = [
    {"k1": "De kaart die je vasthield",
     "p1": "Met de hand geschreven, aan jou gericht, met dit webadres eronder. Zo kwam je hier.",
     "k2": "Deze pagina",
     "p2": "Wat ik zag bij {bedrijf}, uitgeschreven met het bewijs erbij. Je leest hem nu.",
     "k3": "Een gesprek van twintig minuten",
     "p3": "Je plant het zelf in, of je laat je nummer achter. Daarna weet je wat ik zou doen.",
     "v1k": "Wij richten het in",
     "v1p": "De koppeling met je webshop, de antwoorden en de toon. Jij levert alleen de kennis die wij nog missen.",
     "v2k": "Een vaste prijs per ticket",
     "v2p": "Je weet vooraf wat een maand kost, ook in december. Op de factuur staan tickets en verder niets.",
     "v3k": "Er staat altijd een mens achter",
     "v3p": "Wordt het ingewikkeld, dan neemt een collega het gesprek over. Dat zit in de afspraak."},
    {"k1": "Een kaart, met de hand",
     "p1": "Geschreven aan jou, met dit adres eronder. Daarom lees je dit nu.",
     "k2": "Deze uitwerking",
     "p2": "Mijn bevindingen over {bedrijf}, met de zinnen erbij waar ik ze vond.",
     "k3": "Twintig minuten in je agenda",
     "p3": "Zelf inplannen of je nummer achterlaten. Daarna weet je wat het zou kosten.",
     "v1k": "De inrichting doen wij",
     "v1p": "Koppelen, antwoorden schrijven, toon afstemmen. Van jou hebben we alleen je productkennis nodig.",
     "v2k": "Per ticket een vast bedrag",
     "v2p": "Geen verrassing op de factuur in het hoogseizoen. Je rekent met één getal.",
     "v3k": "Een collega als achtervang",
     "v3p": "Bij een lastig of emotioneel gesprek stapt er iemand in. Standaard, zonder meerprijs."},
    {"k1": "Het kaartje in je hand",
     "p1": "Handgeschreven, met één adres eronder. Dat adres bracht je hier.",
     "k2": "Wat je nu leest",
     "p2": "Drie dingen over {bedrijf}, met de bron erbij zodat je het zelf kunt nakijken.",
     "k3": "Een kwartier of twintig minuten",
     "p3": "Kies een moment of laat je nummer achter. Dan hoor je wat ik zou aanpakken.",
     "v1k": "Opzetten doen wij",
     "v1p": "Wij bouwen de desk, schrijven de antwoorden en leggen de koppeling. Jij kijkt mee.",
     "v2k": "Vaste ticketprijs",
     "v2p": "Wat een maand kost weet je vooraf. Ook als november en december uitlopen.",
     "v3k": "Altijd een mens erachter",
     "v3p": "Loopt een gesprek vast, dan pakt een collega het op. Dat hoort erbij."},
    {"k1": "De handgeschreven kaart",
     "p1": "Aan jou geschreven, met dit webadres onderaan. Daar begon dit.",
     "k2": "Deze pagina over {bedrijf}",
     "p2": "Mijn observaties, met het citaat en de datum erbij. Alles is na te lopen.",
     "k3": "Een kort gesprek",
     "p3": "Twintig minuten, ingepland door jou. Daarna weet je of dit past.",
     "v1k": "Het opzetten is aan ons",
     "v1p": "Wij regelen de techniek, de teksten en de toon. Jouw inbreng blijft klein.",
     "v2k": "Eén prijs per ticket",
     "v2p": "Vooraf duidelijk, ook in de drukste maand van het jaar. Verder staat er niets op.",
     "v3k": "Menselijke achtervang",
     "v3p": "Als een gesprek erom vraagt, neemt een collega over. Dat is inbegrepen."},
]

# ── kleine vaste stukken ──────────────────────────────────────────
SHEET_NOTE = [
    "Ik bel zelf. Je nummer gaat nergens anders heen en komt op geen enkele lijst.",
    "Ik bel je persoonlijk. Je nummer blijft bij mij en gaat op geen lijst.",
    "Je spreekt mij, niet een callcenter. Je nummer wordt verder nergens voor gebruikt.",
    "Ik pak zelf de telefoon. Je nummer bewaar ik nergens anders voor.",
]
DOCK = [
    "<b>Even bellen over wat ik zag?</b> 20 minuten.",
    "<b>Zal ik je hierover bellen?</b> Twintig minuten.",
    "<b>Liever even sparren?</b> 20 minuten.",
    "<b>Kort bellen over deze pagina?</b> 20 minuten.",
]
CTA_ALT = [
    "Liever eerst even schriftelijk?",
    "Liever eerst een mailtje?",
    "Wil je het liever op papier?",
    "Eerst even schriftelijk iets vragen?",
]
ASK_LEES = ["Ik lees eerst het voorstel", "Eerst even verder lezen",
            "Ik lees het liever eerst", "Laat het voorstel maar zien"]
NAV_CTA = ["Plan een gesprek", "Even bellen", "Plan twintig minuten", "Een gesprek plannen"]

# ── varianten binnen de bevindingen ───────────────────────────────
BEV_AVOND = [
    "De meeste consumentbestellingen worden 's avonds geplaatst. De vragen die daarbij "
    "horen, komen dus binnen als het licht uit is.",
    "Klanten bestellen vooral tussen acht en elf 's avonds. Hun vragen ontstaan op "
    "datzelfde moment en blijven dan liggen.",
    "Wie na sluitingstijd twijfelt over een maat, legt zijn winkelmandje weg. De volgende "
    "ochtend is die order er vaak niet meer.",
    "De piek in bestellingen ligt in de avond. De bezetting op klantcontact ligt overdag.",
]
BEV_VIERDAAGS = [
    "De servicedesk staat open tot en met donderdag. Wie vrijdagavond bestelt en zaterdag "
    "een vraag heeft, wacht tot maandag.",
    "Van vrijdag tot en met zondag komt er niemand bij de berichten. Dat is drie dagen "
    "waarin de vragen zich opstapelen.",
    "De week eindigt bij jullie op donderdag. Het weekend, waarin veel wordt besteld, "
    "loopt door in dezelfde mailbox.",
    "Wie op vrijdag een vraag stelt, krijgt maandag antwoord. In die tussentijd staat de "
    "bestelling stil.",
]
BEV_KANAAL = [
    "Een twijfel die aan de telefoon in twee minuten klaar is, wordt zo een wachtrij.",
    "Een vraag die je in een gesprek meteen wegneemt, kost per bericht al snel twee dagen.",
    "Alles gaat via tekst, dus elk misverstand kost een extra ronde heen en weer.",
    "Zonder lijn wordt elke twijfel een bericht, en elk bericht een plek in de rij.",
]
BEV_BELOFTE = [
    "Deze zin staat op jullie eigen servicepagina. Hij wordt gemeten per binnenkomend "
    "bericht, dus hij weegt zwaarder naarmate het drukker wordt.",
    "Dat is jullie eigen belofte. Elke klant leest hem, en elke klant rekent erop, ook "
    "in de week voor kerst.",
    "Deze toezegging staat er zwart op wit. Klanten houden je eraan, zeker als er iets "
    "misgaat met hun bestelling.",
    "Dit is wat je belooft. De vraag is alleen of dat ook lukt in de weken dat het volume "
    "verdubbelt.",
]

# ── kantelzin: één zin, want dit blok staat in displaytype ────────
KANTEL_UREN = [
    "Je klanten kopen op het moment dat je servicedesk dicht is.",
    "De drukste uren van je webshop vallen buiten de uren van je klantenservice.",
    "Het gat tussen sluitingstijd en de volgende ochtend is waar je orders blijven hangen.",
    "Je bent bereikbaar wanneer het rustig is, en dicht wanneer het druk wordt.",
]
KANTEL_KANAAL = [
    "Elke twijfel wordt bij jullie een bericht, en elk bericht een plek in de rij.",
    "Zonder telefoonlijn duurt een vraag van twee minuten al gauw twee dagen.",
    "Alles loopt via tekst, dus elk misverstand kost een extra ronde heen en weer.",
    "De klant die even wil bellen, moet bij jullie gaan typen en wachten.",
]
KANTEL_BELOFTE = [
    "Je belooft snel antwoord op het enige kanaal dat traag is.",
    "De belofte staat op je site, de bezetting om hem waar te maken staat er niet naast.",
    "Je hebt jezelf een reactietijd opgelegd zonder de lijn om hem te halen.",
    "Wat je belooft en wat je kunt bemensen, lopen bij jullie uit elkaar.",
]
KANTEL_VOLUME = [
    "Je bent gegroeid in alles, behalve in de mensen die de vragen beantwoorden.",
    "Meer markten en meer artikelen komen bij jullie door dezelfde ene deur.",
    "De omzet schaalt mee met de groei. Het klantcontact doet dat niet vanzelf.",
    "Elke order erbij is ook een gesprek erbij, en dat gesprek moet iemand voeren.",
]

# ── extra bevindingsvarianten ─────────────────────────────────────
BEV_UREN = [
    "Buiten deze uren blijft een bericht liggen tot de volgende ochtend.",
    "Wie daarbuiten schrijft, hoort de volgende werkdag pas iets.",
    "Alles wat na dit tijdslot binnenkomt, schuift door naar morgen.",
    "Deze uren bepalen hoe snel een klant geholpen wordt, ongeacht wanneer hij koopt.",
]
BEV_REVIEWSTAART = [
    "Zo'n review blijft daarna staan voor iedereen die jullie opzoekt.",
    "Dat leest de volgende klant ook, precies op het moment dat hij twijfelt.",
    "Eén zo'n ervaring weegt bij een nieuwe koper zwaarder dan tien goede.",
    "Die zin staat er nog steeds, en hij werkt door bij elke volgende bezoeker.",
]
BEV_SCHAAL_KOP = [
    "De omvang van wat er binnenkomt",
    "Waar het volume vandaan komt",
    "Hoe groot dit eigenlijk is",
    "Wat er dagelijks langskomt",
]
BEV_SCHAAL = [
    "Elke variant brengt zijn eigen vragen mee over maat, levertijd en retour.",
    "Dat vertaalt zich rechtstreeks naar het aantal berichten per dag.",
    "Hoe breder het aanbod, hoe vaker iemand iets wil weten voordat hij koopt.",
    "Dat is het volume waar je klantcontact elke dag doorheen moet.",
]

# ── wat je krijgt: de propositie van BCS, geen kaart en pagina ────
# De drie mockups uit het component tonen bij Pique de kaart, de pagina en de
# afspraak. Dat is zelfverwijzend en klopt daar. Een prospect van BCS koopt geen
# kaarten en geen landingspagina's, dus hier staan drie kaarten met wat hij wel
# krijgt: bereikbaarheid, een vaste prijs en een mens als achtervang.
USP = [
    [
        {"num": "24", "lab": "uur", "titel": "Altijd antwoord",
         "sub": "mail, chat, WhatsApp", "rij": "Ook 's avonds en in het weekend",
         "hand": "ook als jij dicht bent", "kop": "Bereikbaar wanneer je klant koopt",
         "p": "Je klant stelt zijn vraag om kwart over negen 's avonds en krijgt binnen een paar minuten antwoord."},
        {"num": "1", "lab": "tarief", "titel": "Vaste prijs per ticket",
         "sub": "vooraf bekend, ook in december", "rij": "Op de factuur staan tickets",
         "hand": "één getal om mee te rekenen", "kop": "Een prijs die je vooraf kent",
         "p": "Je betaalt per afgehandelde vraag. Wat een drukke maand kost, weet je voordat hij begint."},
        {"num": "1", "lab": "mens", "titel": "Mens als achtervang",
         "sub": "bij twijfel of emotie", "rij": "Escaleert vanzelf naar een collega",
         "hand": "nooit een bot die je vastzet", "kop": "Er staat altijd iemand achter",
         "p": "Wordt een gesprek ingewikkeld of emotioneel, dan neemt een collega het over. Dat zit in de afspraak."},
    ],
    [
        {"num": "24", "lab": "uur", "titel": "Altijd iemand paraat",
         "sub": "op elk kanaal dat je open hebt", "rij": "Weekend en feestdagen ook",
         "hand": "geen wachtrij meer op maandag", "kop": "De deur staat altijd open",
         "p": "Wie zondagavond iets vraagt, hoeft niet tot maandag te wachten. Dat scheelt precies de orders die anders blijven hangen."},
        {"num": "1", "lab": "prijs", "titel": "Eén tarief per ticket",
         "sub": "geen staffels, geen uren", "rij": "Vooraf te begroten",
         "hand": "ook in het hoogseizoen", "kop": "Kosten die je kunt begroten",
         "p": "Geen uurtje-factuurtje en geen verrassing in november. Je rekent met één bedrag per vraag."},
        {"num": "1", "lab": "mens", "titel": "Mens als achtervang",
         "sub": "standaard ingebouwd", "rij": "Een collega neemt over",
         "hand": "bij het lastige geval", "kop": "Een mens waar het moet",
         "p": "De makkelijke vragen gaan vanzelf. De lastige komen bij iemand terecht die er tijd voor neemt."},
    ],
    [
        {"num": "24", "lab": "uur", "titel": "Doorlopend open",
         "sub": "mail, chat en telefoon", "rij": "Ook buiten kantooruren",
         "hand": "de avond telt mee", "kop": "Bereikbaarheid zonder openingstijden",
         "p": "Je klanten winkelen 's avonds en in het weekend. Vanaf dat moment krijgen ze daar ook antwoord."},
        {"num": "1", "lab": "tarief", "titel": "Vast bedrag per ticket",
         "sub": "transparant op de factuur", "rij": "Geen verrassingen achteraf",
         "hand": "je weet wat een piek kost", "kop": "Vooraf weten wat het kost",
         "p": "Eén tarief per afgehandelde vraag, het hele jaar door. Een drukke maand is dan een som, geen schrik."},
        {"num": "1", "lab": "mens", "titel": "Een mens erachter",
         "sub": "als het erom gaat", "rij": "Escalatie zit erin",
         "hand": "geen doodlopende chat", "kop": "Waar het misgaat staat een mens",
         "p": "Een klant met een echt probleem komt bij een collega uit, en niet in een lus van standaardantwoorden."},
    ],
]

# De drie vinkjes eronder gaan over de overgang zelf.
VW = [
    [("Wij richten het in", "De koppeling met je webshop, de antwoorden en de toon. Van jou hebben we alleen je productkennis nodig."),
     ("In jullie naam en toon", "Je klant merkt er niets van. Hij mailt met jullie, en jullie antwoorden."),
     ("Elke maand de cijfers", "Hoeveel vragen, waarover, en hoe snel opgelost. Op basis daarvan sturen we bij.")],
    [("Het opzetten is aan ons", "Wij bouwen de desk, schrijven de antwoorden en leggen de koppeling. Jij kijkt mee."),
     ("Onder jullie eigen naam", "Alles gaat de deur uit zoals jullie het zouden schrijven. Je klant ziet één merk."),
     ("Maandelijks op cijfers", "We kijken naar volume, doorlooptijd en onderwerpen. Daar sturen we op bij.")],
    [("De inrichting doen wij", "Koppelen, antwoorden schrijven, toon afstemmen. Jouw inbreng blijft klein."),
     ("Jullie stem blijft staan", "De klant merkt geen overdracht. Hij krijgt antwoord van jullie merk."),
     ("Cijfers in plaats van verhalen", "Elke maand een overzicht van wat er binnenkwam en hoe snel het weg was.")],
]
