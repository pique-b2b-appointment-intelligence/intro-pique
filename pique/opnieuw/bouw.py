#!/usr/bin/env python3
"""
Bouwt de pagina's voor de heractivatiebatch: mensen met wie Simon al gesproken heeft.

De vorm komt uit Componenten/lp-v2/_voorbeeld.html en wordt hier niet aangeraakt.
De statische brokken (nav met logo, QR-svg, footer, boeksheet) worden daar letterlijk
uitgeknipt, zodat een wijziging aan het component hier automatisch meekomt.

Twee dingen wijken bewust af van het voorbeeld:
  1. De videoknop in de hero is eruit. De VSL staat onderaan, vlak voor de CTA.
     Twee video's op een pagina laat de lezer kiezen welke hij overslaat.
  2. De tariefstaffel is er per 12 oktober 2026 uit. De prijs is weer een onderwerp
     voor het gesprek, niet voor de pagina.

De inhoud staat per prospect in PROSPECTEN. Elke feitelijke bevinding heeft een bron
met datum, meestal de kaart die de ontvanger zelf nog heeft liggen.

    python3 bouw.py            # alles
    python3 bouw.py audion     # alleen die
"""
import sys
from pathlib import Path

HIER = Path(__file__).parent
UIT = HIER.parent          # pagina's staan in pique/, zodat er geen map in de URL zit
VOORBEELD = HIER.parent.parent.parent.parent / "Componenten" / "lp-v2" / "_voorbeeld.html"
MODEL_V12 = UIT / "odido-v12.html"   # de drie maquettes komen hier letterlijk uit

# Laatste staffel die in een echt verstuurd voorstel heeft gestaan: Leads/STILL,
# eind september 2026, met telefonische opvolging door Pique. pique.agency/tarieven
# bestaat niet meer en zet door naar /contact, dus die kan geen bron meer zijn.

# De cases staan live op pique.agency/cases. Cijfers hier letterlijk daarvandaan.
CASES = {
    "zon": ("pique.agency/cases/zon-en-laadinfra", "de campagne waar jij in zat"),
    "wegmetexcel": ("pique.agency/cases/wegmetexcel", "WegMetExcel"),
    "potentiel": ("pique.agency/cases/potentiel", "Potentiel"),
    "ogg": ("pique.agency/cases/online-goed-gevonden", "Online Goed Gevonden"),
    "azora": ("pique.agency/cases/azora-studio", "Azora Studio"),
    "geduld": ("pique.agency/cases/online-geduld", "Online Geduld"),
    "backbone": ("pique.agency/cases/backbone", "Backbone"),
}


PROSPECTEN = {
    # ────────────────────────────── kaart, afspraak, daarna stil ──────────────
    "audion": {
        "slug": "audion-packaging-machines",
        "bedrijf": "Audion Packaging Machines",
        "voornaam": "Michel",
        "kaart": "Hoi Michel.<br>In augustus bleef dit liggen.",
        "h1": 'Dit is de <span class="u">tweede kaart</span>.',
        "sub": "In augustus scande je de eerste drie keer en daarna stond er een afspraak. "
               "Toen werd het stil, en dat kwam van mijn kant.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Nu met de staffel erbij"],
        "aanloop_kop": "De eerste kaart ging over Interpack.",
        "aanloop": "Die lag op 17 augustus bij je op het bureau en ging over de Speedpack Dual, "
                   "de machine die bij jullie in D&uuml;sseldorf stond en zowel papier als "
                   "plastic aankan. Je hebt die kaart drie keer gescand, de laatste keer op "
                   "26 augustus om 8:25 's ochtends. Daarna hebben we elkaar gesproken en stond "
                   "er een afspraak in de agenda.",
        "aanloop2": "<strong>En toen werd het stil. Dat kwam van mijn kant, en ik ga het niet "
                    "mooier maken dan het is.</strong>",
        "note": "ditmaal met de prijs erbij",
        "finds": [
            {"tag": "Wat ik niet goed deed", "kop": "De prijs stond er nergens",
             "text": "Op die pagina stond wel wat ik voorstelde en nergens wat het kost. Dat "
                     "moest je dus aan mij vragen voordat je het intern kon neerleggen. Daar "
                     "haakt iemand af, en terecht.",
             "quote": "'Wat ik voorstel. Ik lever gesprekken met beslissers die je normaal niet "
                      "aan de lijn krijgt.'",
             "dom": "intro-pique.agency/pique/food-agri/audion-packaging-machines",
             "datum": "augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "Het tarief hangt aan het aantal",
             "text": "Je bepaalt zelf hoeveel bedrijven er per maand worden aangeschreven, en "
                     "daar hangt de prijs aan. Bij vijftig per maand betaal je per benadering "
                     "meer dan bij tweehonderd, omdat de voorbereiding niet meekrimpt met de "
                     "order. De lijst, het onderzoek per bedrijf en het belscript kosten "
                     "hetzelfde bij vijftig als bij tweehonderd."},
        ],
        "pivot": "Je hoeft niet te beginnen bij het aantal waar we het in augustus over hadden. "
                 "Honderd per maand is genoeg om te zien of jullie markt hierop reageert, en "
                 "daarna beslis je of het groter mag.",
        "tijdlijn": [("17 aug", "kaart op je bureau"), ("26 aug", "derde scan, 8:25"),
                     ("aug", "afspraak, daarna stil"), ("nu", "met de prijs erbij")],
        "tl_hand": "Die stilte ertussen is mijn werk geweest.",
        "case": "zon",
        "case_kop": "384 kaarten, 98,4 procent gescand.",
        "case_text": "Jij zat in die batch. Zes niches tegelijk, waaronder machinebouw voor food "
                     "en agri, en vierhonderd namen die er op papier goed uitzagen. "
                     "<strong>Eenendertig vlogen er v&oacute;&oacute;r de drukker uit</strong>, "
                     "op verlopen aanleidingen, beslissers die inmiddels ergens anders werkten "
                     "en adressen waar het bedrijf niet meer zat.",
        "voorstel_sub": "Honderd machinebouwers en verpakkingsinkopers per maand, twee maanden, "
                        "en we bellen de scans na.",
        "cta_sub": "Twintig minuten om te kijken of dit bij Audion past. Nu met de staffel erbij, "
                   "zodat je het intern kunt neerleggen zonder mij erbij.",
        "dock": "Even bellen over de staffel?",
    },

    "twinfloor": {
        "slug": "twinfloor",
        "bedrijf": "Twinfloor",
        "voornaam": "Albert",
        "kaart": "Hoi Albert.<br>Ik had je op 14 september<br>terug moeten bellen.",
        "h1": 'Er stond een <span class="u">datum</span> in mijn systeem.',
        "sub": "14 september, om je terug te bellen na ons gesprek in augustus. Die dag is "
               "voorbijgegaan zonder dat ik iets deed.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Nu met de staffel erbij"],
        "aanloop_kop": "De kaart ging over twee vacatures.",
        "aanloop": "Je wierf in Breda tegelijk een Accountmanager en een Project Engineer, en "
                   "daar ging de kaart over die je op 12 augustus om kwart voor drie scande. "
                   "Een week later hadden we elkaar aan de lijn en zette ik 14 september in "
                   "mijn eigen systeem als de dag om je terug te bellen.",
        "aanloop2": "<strong>Dat belletje is er nooit gekomen. Jij hebt intussen twee functies "
                    "in te vullen en een orderboek te vullen, dus jij ging door.</strong>",
        "note": "en nu wel met het bedrag",
        "finds": [
            {"tag": "Wat ik toen schreef", "kop": "De aanleiding klopte, de opvolging niet",
             "text": "De kaart ging over iets concreets dat jij zelf had gepubliceerd. Daar was "
                     "niets mis mee. Wat eraan ontbrak was wat het kost, en een tweede belletje "
                     "op de dag die ik zelf had geprikt.",
             "quote": "'Twinfloor werft in Breda tegelijk een Accountmanager en een Project "
                      "Engineer.'",
             "dom": "de kaart die je kreeg", "datum": "12 augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "Honderd per maand kan ook",
             "text": "In augustus praatten we over een omvang die bij een bedrijf van jullie "
                     "soort hoort. Dat hoeft niet. Je kiest het aantal bedrijven per maand en "
                     "dat aantal bepaalt het tarief per benadering."},
        ],
        "pivot": "Een vloerenbouwer die twee mensen zoekt heeft genoeg aan een handvol goede "
                 "gesprekken. Honderd namen per maand levert die, en je ziet binnen zes weken "
                 "of het werkt.",
        "tijdlijn": [("12 aug", "kaart gescand, 14:52"), ("19 aug", "afspraak"),
                     ("14 sep", "mijn terugbeldag, gemist"), ("nu", "met de prijs erbij")],
        "tl_hand": "De gemiste dag staat er bewust bij.",
        "case": "wegmetexcel",
        "case_kop": "Honderdnegenenveertig namen, twee afspraken.",
        "case_text": "WegMetExcel haalt bedrijven van hun losse spreadsheets af. Het profiel werd "
                     "bewust smal gehouden: twee bewezen profielen, acht criteria en negen "
                     "uitsluitingen. <strong>Veertig van de honderdnegenenveertig openden hun "
                     "eigen pagina</strong>, negenentwintig zijn nagebeld en er kwamen twee "
                     "afspraken uit.",
        "voorstel_sub": "Honderd aannemers, projectinrichters en vastgoedbeheerders per maand, "
                        "twee maanden, en we bellen de scans na.",
        "cta_sub": "Twintig minuten om te kijken of dit bij Twinfloor past. De staffel staat "
                   "hierboven, dus je weet al wat je vraagt.",
        "dock": "Alsnog dat belletje?",
    },

    "sweere": {
        "slug": "sweere",
        "bedrijf": "Sweere",
        "voornaam": "Theo",
        "kaart": "Hoi Theo.<br>We spraken elkaar<br>op 14 augustus.",
        "h1": 'Eén gesprek, en toen <span class="u">niets</span>.',
        "sub": "Je scande de kaart op 13 augustus en de dag erna zaten we aan de telefoon. "
               "Daarna heb je niets meer van me gehoord.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Nu met de staffel erbij"],
        "aanloop_kop": "De kaart ging over de bonenmachine.",
        "aanloop": "Jullie kondigden in juni een nieuwe machine aan voor de verwerking van "
                   "groene bonen, en daar ging de kaart over. Je scande hem op 13 augustus om "
                   "tien voor tien en keek er diezelfde ochtend nog een tweede keer naar. De "
                   "dag erna spraken we elkaar.",
        "aanloop2": "<strong>Daarna is er van mijn kant niets meer gekomen. Bij een bedrijf dat "
                    "de eigenaar zelf runt is dat extra vervelend, want jij hebt die tijd "
                    "vrijgemaakt.</strong>",
        "note": "kort stukje, met een bedrag",
        "finds": [
            {"tag": "Wat ik toen schreef", "kop": "De aanleiding was van jullie zelf",
             "text": "Ik had niets bedacht. Jullie hadden die machine zelf aangekondigd en ik "
                     "las erover. Zo begint elke kaart die ik schrijf, en zo zou de volgende "
                     "ook beginnen.",
             "quote": "'Jullie kondigden in juni een nieuwe machine voor de verwerking van "
                      "groene bonen aan.'",
             "dom": "de kaart die je kreeg", "datum": "13 augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "Je kunt het klein houden",
             "text": "De vraag die bij jou blijft hangen is wat zoiets kost als je het één keer "
                     "wil proberen. Die staat hieronder. Het aantal bedrijven per maand bepaalt "
                     "het tarief, en honderd is het kleinste getal waar iets uit te leren valt."},
        ],
        "pivot": "Bij een machinebouwer die op naam verkoopt gaat het om een handvol juiste "
                 "mensen. Daar hoort een lijst bij die je zelf nog kunt overzien.",
        "tijdlijn": [("juni", "machine aangekondigd"), ("13 aug", "kaart gescand, 9:52"),
                     ("14 aug", "we spraken elkaar"), ("nu", "met de prijs erbij")],
        "tl_hand": "Tussen die laatste twee zat alles wat ik had moeten doen.",
        "case": "potentiel",
        "case_kop": "Vijftig kaarten, drie klanten.",
        "case_text": "Een health club wilde weten of je klein kunt beginnen. Vijftig namen, elk "
                     "met een eigen aanleiding, en verder niets. <strong>Negen mensen "
                     "reageerden en drie daarvan werden klant.</strong> Op vijftig kaarten is "
                     "dat een kleine steekproef en dat zeg ik er ook bij, maar het is wel het "
                     "antwoord op de vraag of klein beginnen kan.",
        "voorstel_sub": "Honderd verwerkers en loonbedrijven per maand, twee maanden, en ik bel "
                        "de scans zelf na.",
        "cta_sub": "Twintig minuten, en je hoeft niets voor te bereiden. Past het niet bij wat "
                   "een klant jullie oplevert, dan hoor je dat in datzelfde gesprek.",
        "dock": "Even bijpraten?",
    },

    "ash": {
        "slug": "ash-carrosserie",
        "bedrijf": "ASH Carrosserie",
        "voornaam": "Roel",
        "kaart": "Hoi Roel.<br>Ik zou je op 2 september<br>terugbellen.",
        "h1": 'De tweede afspraak <span class="u">kwam er niet</span>.',
        "sub": "Je scande de kaart op 20 augustus, we spraken elkaar, en 2 september stond "
               "genoteerd als de dag dat ik terug zou bellen.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Nu met de staffel erbij"],
        "aanloop_kop": "De kaart ging over de Veiligheidsregio.",
        "aanloop": "Jullie bouwden aan het ge&euml;lektrificeerde wagenpark van de "
                   "Veiligheidsregio Rotterdam-Rijnmond, ruim honderd voertuigen, en daar ging "
                   "de kaart over. Je scande hem op 20 augustus aan het eind van de middag en "
                   "keek er die dag nog een tweede keer naar.",
        "aanloop2": "<strong>Daarna liep het dood op mij. Dat is zuur bij een opdracht van die "
                    "omvang, want juist dan is de vraag waar de volgende vandaan komt.</strong>",
        "note": "nu met het bedrag erbij",
        "finds": [
            {"tag": "Wat ik toen schreef", "kop": "Honderd voertuigen is een referentie",
             "text": "Een wagenpark van die omvang voor een veiligheidsregio is iets waar andere "
                     "opdrachtgevers naar kijken. Dat was mijn aanleiding om te schrijven, en "
                     "het is nog steeds de sterkste zin die je in een gesprek kunt gebruiken.",
             "quote": "'Jullie bouwen momenteel aan het ge&euml;lektrificeerde wagenpark van de "
                      "Veiligheidsregio Rotterdam-Rijnmond, ruim honderd voertuigen.'",
             "dom": "de kaart die je kreeg", "datum": "20 augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "Het aantal bepaalt de prijs",
             "text": "Wat er in augustus ontbrak was een bedrag waar je intern iets mee kon. Je "
                     "kiest hoeveel bedrijven er per maand worden aangeschreven en dat aantal "
                     "zet het tarief per benadering vast. Verder komt er niets overheen."},
        ],
        "pivot": "Gemeenten, veiligheidsregio's en vervoerders die nu elektrificeren zijn te "
                 "tellen. Bij zo'n groep telt één kaart die hun situatie kent zwaarder dan "
                 "duizend die dat niet doen.",
        "tijdlijn": [("20 aug", "kaart gescand, 16:48"), ("20 aug", "afspraak"),
                     ("2 sep", "mijn terugbeldag, gemist"), ("nu", "met de prijs erbij")],
        "tl_hand": "Twee weken ertussen, en toen niets.",
        "case": "zon",
        "case_kop": "384 kaarten, 98,4 procent gescand.",
        "case_text": "Jij zat in die batch, in de niche bedrijfswagens. Zes niches tegelijk en "
                     "vierhonderd namen die er op papier goed uitzagen. <strong>Eenendertig "
                     "vlogen er v&oacute;&oacute;r de drukker uit</strong>, op verlopen "
                     "aanleidingen, beslissers die inmiddels ergens anders werkten en adressen "
                     "waar het bedrijf niet meer zat.",
        "voorstel_sub": "Honderd vervoerders, gemeenten en opbouwers per maand, twee maanden, en "
                        "we bellen de scans na.",
        "cta_sub": "Twintig minuten om te kijken of dit bij ASH past. De staffel staat hierboven, "
                   "dus de prijsvraag is al beantwoord.",
        "dock": "Alsnog dat belletje?",
    },

    "unica": {
        "slug": "unica",
        "bedrijf": "Unica",
        "voornaam": "Susan",
        "kaart": "Hoi Susan.<br>Je feedback heeft<br>onze regels veranderd.",
        "h1": 'Je had <span class="u">gelijk</span>.',
        "sub": "Vijf van de negenentwintig aanleidingen die ik je liet zien waren verlopen. Dat "
               "zei je hardop, en daar is sindsdien een harde regel van gemaakt.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Wat er met je feedback gebeurd is"],
        "aanloop_kop": "Je bent de reden dat er nu een poort voor staat.",
        "aanloop": "In augustus liet ik je negenentwintig bedrijven zien met per bedrijf een "
                   "aanleiding. Je prikte er doorheen: vijf ervan waren verlopen. Dat was "
                   "ongemakkelijk en het was terecht.",
        "aanloop2": "<strong>Sindsdien gaat elke aanleiding door een controle die de bron "
                    "ophaalt en kijkt of het citaat er letterlijk staat en of de datum klopt. "
                    "Valt er &eacute;&eacute;n af, dan gaat dat bedrijf de batch niet in.</strong>",
        "note": "en ja, dat had eerder gemoeten",
        "finds": [
            {"tag": "Wat je toen zag", "kop": "De aanleiding was te oud",
             "text": "De kaart die je kreeg ging over de nieuwe Commercieel Directeur op "
                     "groepsniveau. Dat klopte. Een deel van de lijst die ik je daarna liet "
                     "zien klopte niet meer, en dat verschil is precies waar het op aankomt.",
             "quote": "'Jullie vulden net een Commercieel Directeur op groepsniveau in. Hoe "
                      "gericht de nieuwe klant per divisie binnenkomt, bleef me bezighouden.'",
             "dom": "de kaart die je kreeg", "datum": "augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "Je keek op 7 september nog een keer",
             "text": "Je hebt de pagina drie keer geopend, de laatste keer op 7 september, drie "
                     "weken na ons gesprek. Dat is de reden dat ik je nog een keer schrijf in "
                     "plaats van het erbij te laten zitten. Wat er toen ontbrak was wat het "
                     "kost per divisie, en dat staat hieronder."},
        ],
        "pivot": "Bij een groep met divisies is de vraag nooit of outbound werkt, maar wie er "
                 "precies wordt aangeschreven en namens welke divisie. Dat is een lijstvraag, "
                 "en die is per divisie te beantwoorden.",
        "tijdlijn": [("10 aug", "eerste scan"), ("17 aug", "ons gesprek"),
                     ("7 sep", "je keek nog een keer"), ("nu", "met de prijs erbij")],
        "tl_hand": "Die derde scan heeft deze kaart veroorzaakt.",
        "case": "ogg",
        "case_kop": "Zevenendertig niches, apart gehouden.",
        "case_text": "Online Goed Gevonden bedient het hele MKB, wat in de praktijk betekent dat "
                     "niemand hun klant is. We schreven bijna tweeduizend bedrijven aan over "
                     "zevenendertig niches, elk apart onderzocht. <strong>Bij garages bleek dat "
                     "van 3.069 bedrijven er zeventien online boeken aanbieden</strong>, en dat "
                     "ene cijfer stuurde de hele campagne.",
        "voorstel_sub": "Honderd beslissers per maand binnen &eacute;&eacute;n divisie, twee "
                        "maanden, en we bellen de scans na.",
        "cta_sub": "Twintig minuten. Als je wil begin ik met de divisie waar de meeste ruimte "
                   "zit, dan hoeft de rest van de groep er nog niet aan te geloven.",
        "dock": "Even over één divisie?",
    },

    "bonotech": {
        "slug": "bonotech-bedrijfswagens",
        "bedrijf": "BonoTech Bedrijfswagens",
        "voornaam": "Arjan",
        "kaart": "Hoi Arjan.<br>Van ons gesprek heb ik<br>niets vastgelegd.",
        "h1": 'Ik heb het <span class="u">laten lopen</span>.',
        "sub": "We spraken elkaar op 22 september. Mijn opname bevatte geen bruikbaar geluid en "
               "ik heb er daarna niets van opgeschreven.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Nu met de staffel erbij"],
        "aanloop_kop": "De kaart ging over Car Service Partner.",
        "aanloop": "Je sloot je op 1 juli aan bij dat netwerk om marketing- en "
                   "managementondersteuning te krijgen zonder je eigen naam op te geven. Daar "
                   "ging de kaart over die je op 31 augustus rond lunchtijd scande, en een paar "
                   "weken later hadden we elkaar aan de lijn.",
        "aanloop2": "<strong>Wat je toen gezegd hebt weet ik niet meer. Dat is mijn fout en geen "
                    "reden om net te doen alsof ik het wel weet.</strong>",
        "note": "dus dit keer op papier",
        "finds": [
            {"tag": "Wat ik toen schreef", "kop": "Je koos zelf voor ondersteuning",
             "text": "Dat je je bij een netwerk aansloot om aan marketing te komen, en wel met "
                     "behoud van je eigen identiteit, was de reden dat ik je schreef. Iemand die "
                     "die keuze maakt heeft al besloten dat er iets moet gebeuren.",
             "quote": "'BonoTech sloot zich op 1 juli 2026 aan bij het Car Service "
                      "Partner-netwerk om marketing-, kennis- en managementondersteuning te "
                      "krijgen met behoud van eigen identiteit.'",
             "dom": "de kaart die je kreeg", "datum": "31 augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "Alles wat ik zei staat nu op papier",
             "text": "Hieronder staat wat het kost bij welk aantal per maand. Dat hoef je niet "
                     "uit je hoofd terug te halen uit een telefoongesprek, en ik ook niet."},
        ],
        "pivot": "Een bedrijfswagenspecialist verkoopt aan wagenparkbeheerders en aan "
                 "ondernemers met een handvol bussen. Dat zijn twee heel verschillende "
                 "gesprekken, en allebei beginnen ze bij de juiste naam op de envelop.",
        "tijdlijn": [("1 jul", "aansluiting Car Service Partner"),
                     ("31 aug", "kaart gescand, 12:57"), ("22 sep", "we spraken elkaar"),
                     ("nu", "op papier")],
        "tl_hand": "De derde stap is het stuk dat ik kwijt ben.",
        "case": "zon",
        "case_kop": "384 kaarten, 98,4 procent gescand.",
        "case_text": "Jij zat in die batch, in de niche bedrijfswagens. <strong>Eenendertig "
                     "namen vlogen er v&oacute;&oacute;r de drukker uit</strong>, op verlopen "
                     "aanleidingen, beslissers die inmiddels ergens anders werkten en adressen "
                     "waar het bedrijf niet meer zat. Wat overbleef scande bijna voltallig.",
        "voorstel_sub": "Honderd wagenparkbeheerders en ondernemers met bussen per maand, twee "
                        "maanden, en we bellen de scans na.",
        "cta_sub": "Twintig minuten, en deze keer leg ik het wel vast. Past het niet, dan hoor "
                   "je dat in hetzelfde gesprek.",
        "dock": "Opnieuw, en nu goed?",
    },

    "vervaet": {
        "slug": "vervaet",
        "bedrijf": "Vervaet",
        "voornaam": "Jonathan",
        "kaart": "Hoi Jonathan.<br>Van 4 september heb ik<br>niets vastgelegd.",
        "h1": 'Een gesprek dat <span class="u">nergens staat</span>.',
        "sub": "We spraken elkaar op 4 september. De opname duurde drie minuten en bevatte geen "
               "bruikbaar geluid, dus wat je zei staat nergens.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Nu met de staffel erbij"],
        "aanloop_kop": "De kaart ging over de Hydro Trike 3.0.",
        "aanloop": "Jullie bouwden de eerste serie en die was al uitverkocht voordat de Europese "
                   "demotour in juli begon. Daar ging de kaart over die je op 18 augustus om "
                   "negen uur 's ochtends scande, en je keek er die ochtend nog een tweede keer "
                   "naar.",
        "aanloop2": "<strong>In september hebben we elkaar gesproken en daar heb ik niets van "
                    "overgehouden. Jij hebt die tijd wel gegeven.</strong>",
        "note": "dus nu zwart op wit",
        "finds": [
            {"tag": "Wat ik toen schreef", "kop": "Uitverkocht voor de demotour",
             "text": "Een serie die vol zit voordat hij te zien is geweest, zegt genoeg over de "
                     "planning die daarachter hangt. Dat was de reden dat ik je schreef, en "
                     "voor een CCO is dat ook het interessantste stuk.",
             "quote": "'Vervaet bouwt momenteel de eerste serie van de nieuwe Hydro Trike 3.0, "
                      "die al volledig is uitverkocht voordat de Europese demotour in juli "
                      "begon.'",
             "dom": "de kaart die je kreeg", "datum": "18 augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "De prijs staat er nu gewoon bij",
             "text": "In plaats van je te vragen het gesprek van september te herhalen, zet ik "
                     "op deze pagina wat het kost. Het aantal bedrijven per maand bepaalt het "
                     "tarief per benadering en daar komt niets overheen."},
        ],
        "pivot": "Loonwerkers en mestdistributeurs die over zo'n machine beslissen zijn met "
                 "weinig, zitten verspreid over Europa en kopen op naam. Dat is precies het "
                 "soort markt waar post nog aankomt.",
        "tijdlijn": [("juli", "demotour, serie vol"), ("18 aug", "kaart gescand, 8:59"),
                     ("4 sep", "gesprek, niets vastgelegd"), ("nu", "zwart op wit")],
        "tl_hand": "Stap drie is het stuk dat ik kwijt ben.",
        "case": "zon",
        "case_kop": "384 kaarten, 98,4 procent gescand.",
        "case_text": "Jij zat in die batch, in de niche food en agri. Zes niches tegelijk en "
                     "vierhonderd namen die er op papier goed uitzagen. <strong>Eenendertig "
                     "vlogen er v&oacute;&oacute;r de drukker uit</strong>, op verlopen "
                     "aanleidingen en op adressen waar het bedrijf niet meer zat.",
        "voorstel_sub": "Honderd loonwerkers en mestdistributeurs per maand, twee maanden, en ik "
                        "bel de scans zelf na.",
        "cta_sub": "Twintig minuten. Deze keer leg ik vast wat er besproken is en krijg je het "
                   "op papier terug.",
        "dock": "Opnieuw, en nu vastgelegd?",
    },

    # ───────────────── prijs, timing of een andere partij ────────────────────
    "nederburgh": {
        "slug": "nederburgh",
        "bedrijf": "Nederburgh",
        "voornaam": "Daniel",
        "kent_hem": True,
        "kaart": "Hoi Daniel.<br>Ik begon bij duizend brieven.<br>Dat was te groot.",
        "h1": 'Ik begon bij <span class="u">duizend</span>.',
        "sub": "De offerte van 11 augustus ging over duizend brieven. Je vond het te duur, en "
               "achteraf begon ik gewoon aan de verkeerde kant.",
        "chips": ["Tweede voorstel", "2 minuten lezen", "Nu met de staffel erbij"],
        "aanloop_kop": "Duizend brieven was mijn getal, niet het jouwe.",
        "aanloop": "In augustus legde ik drie versies naast elkaar, allemaal op duizend brieven "
                   "naar vastgoedbeleggers. Je gaf aan dat het te duur was en daar had je "
                   "gelijk in, want ik had je laten kiezen tussen drie bedragen die allemaal "
                   "boven de acht mille lagen.",
        "aanloop2": "<strong>De vraag was nooit welke versie. De vraag was of je er klein mee "
                    "kon beginnen, en dat antwoord gaf ik er niet bij.</strong>",
        "note": "nu wel",
        "finds": [
            {"tag": "Wat ik toen voorlegde", "kop": "Drie versies, allemaal duizend",
             "text": "Meten, Regio en Signaal. Het verschil zat in hoe diep we per ontvanger "
                     "gingen, en het aantal lag in alle drie vast op duizend. De enige knop die "
                     "je kon draaien was dus de duurste.",
             "quote": "'Postcampagne beleggers. 1.000 brieven. &euro; 8.500, &euro; 10.500 of "
                      "&euro; 13.500.'",
             "dom": "Offerte Nederburgh &times; Pique, PIQUE-NB-2026-11",
             "datum": "11 augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "Het aantal is nu de knop",
             "text": "Je kiest het aantal per maand en dat zet het tarief per benadering vast. "
                     "Vijftig per maand is de onderkant en kost minder dan tweeduizend per "
                     "maand als je zelf nabelt. Dat is een twintigste van wat er in augustus "
                     "op tafel lag."},
        ],
        "pivot": "Honderd beleggers per maand is genoeg om te zien of jullie verhaal aankomt bij "
                 "iemand die net verkocht heeft of net heeft bijgekocht. Werkt dat, dan is "
                 "opschalen een rekensom in plaats van een gok.",
        "tijdlijn": [("10 aug", "ons gesprek"), ("11 aug", "offerte, duizend brieven"),
                     ("aug", "te duur"), ("nu", "vanaf honderd")],
        "tl_hand": "De fout zat in stap twee.",
        "case": "potentiel",
        "case_kop": "Vijftig kaarten, drie klanten.",
        "case_text": "Een health club wilde weten of vijftig kaarten genoeg zijn om iets te "
                     "bewijzen, of dat je meteen groot moet beginnen. Vijftig namen, elk met "
                     "een eigen aanleiding. <strong>Negen mensen reageerden en drie daarvan "
                     "werden klant.</strong> Dat is een kleine steekproef en dat zeg ik erbij, "
                     "maar het beantwoordt wel de vraag.",
        "voorstel_sub": "Honderd beleggers per maand, twee maanden, en we bellen de scans na.",
        "cta_sub": "Twintig minuten om te kijken waar je wil beginnen. Je zit nergens aan vast "
                   "en de staffel staat hierboven.",
        "dock": "Kleiner beginnen?",
    },

    "acendae": {
        "slug": "acendae",
        "bedrijf": "Acendae",
        "voornaam": "Pramuka",
        "kaart": "Hoi Pramuka.<br>Je bent met iemand<br>anders begonnen.",
        "h1": 'Je koos iemand <span class="u">anders</span>.',
        "sub": "Dat hoorde ik later. Daar ga ik niets van vinden, en het is ook geen reden om "
               "je nooit meer iets te laten horen.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Voor als je gaat vergelijken"],
        "aanloop_kop": "Je zocht voorspelbaarheid.",
        "aanloop": "We spraken elkaar op 6 augustus over de white label development unit. Die "
                   "groeit organisch met ongeveer een klant per kwartaal en dat moest "
                   "voorspelbaar worden. Veertien eigen developers, en de ruimte om snel op te "
                   "schalen zodra er meer binnenkomt.",
        "aanloop2": "<strong>Inmiddels ben je met een andere partij gestart. Wat ik je toen "
                    "nooit gaf is een prijs, en zonder prijs kun je over een paar maanden niets "
                    "vergelijken.</strong>",
        "note": "daarom alsnog",
        "finds": [
            {"tag": "Wat je toen vertelde", "kop": "De winst zit na de build",
             "text": "Het geld zit in de change requests die volgen op een project, bij zestig "
                     "euro per uur. Daarom zijn stabiele scale-up bureaus je ICP en startups "
                     "niet: je wil partijen die minstens een jaar en twaalf projecten "
                     "vooruitkijken. Dat is een smalle groep.",
             "quote": "'ICP zijn stabiele scale-up bureaus, geen startups, die minstens een jaar "
                      "en twaalf projecten willen.'",
             "dom": "gespreksnotitie Acendae &times; Pique", "datum": "6 augustus 2026"},
            {"tag": "Waarom deze kaart", "kop": "Over een paar maanden weet je het",
             "text": "Dan weet je of de partij die je koos levert wat je nodig hebt. Op dat "
                     "moment is het handig als je weet wat het hier kost, zodat je kunt "
                     "vergelijken zonder er eerst een gesprek voor in te plannen. Daarvoor "
                     "staat de staffel hieronder."},
        ],
        "pivot": "Bij een groep die zo smal is bepaalt de lijst het resultaat en de boodschap "
                 "nauwelijks. Honderd bureaus per maand is dan eerder te veel dan te weinig.",
        "tijdlijn": [("6 aug", "kennismaking"), ("aug", "mijn voorstel, zonder staffel"),
                     ("sinds", "je werkt met een ander"), ("nu", "de prijs, voor later")],
        "tl_hand": "Geen haast, wel compleet.",
        "case": "azora",
        "case_kop": "Vier directeuren die nooit terugbelden.",
        "case_text": "Azora maakt videocontent voor marketingbureaus en SaaS-bedrijven, een markt "
                     "waarin iedereen al door iedereen benaderd wordt. De vraag ging over vier "
                     "specifieke directeuren die nooit hadden gereageerd. <strong>Alle vier "
                     "zaten binnen zes weken aan tafel.</strong> Bij drie bedrijven schoven we "
                     "de ontvanger om, van de oprichter naar de marketinglead.",
        "voorstel_sub": "Honderd scale-up bureaus per maand, twee maanden, en we bellen de "
                        "scans na.",
        "cta_sub": "Loopt het goed met de partij die je koos, dan hoor ik dat graag en laat ik "
                   "je verder met rust. Loopt het anders, dan weet je nu wat het hier kost.",
        "dock": "Voor als je gaat vergelijken.",
    },
    "jrfinance": {
        "slug": "jr-finance",
        "bedrijf": "JR Finance",
        "voornaam": "Jason",
        "kent_hem": True,
        "kaart": "Hoi Jason.<br>Je was er in juli<br>nog niet aan toe.",
        "h1": 'Je was er nog <span class="u">niet aan toe</span>.',
        "sub": "In juli was acquisitie nog niet aan de orde. Ik legde toch een maandbedrag neer, "
               "en dat was de verkeerde vraag op het verkeerde moment.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Met het oog op januari"],
        "aanloop_kop": "Je gaat per januari fulltime.",
        "aanloop": "Dat vertelde je me op 1 juli, met de ambitie om dan rond vijftien mille per "
                   "maand te draaien, ongeveer drie klanten van vijf. We hadden het over je "
                   "messaging, over leiden met een bedrag, en over je RA-achtergrond bij "
                   "Deloitte die veel te ver naar achteren stond.",
        "aanloop2": "<strong>Daarna begon ik over een maandbedrag van 3.500. Jij was op dat "
                    "moment met iets anders bezig en ik luisterde slecht.</strong>",
        "note": "januari is dichtbij",
        "finds": [
            {"tag": "Wat we toen bespraken", "kop": "Je verkoopt een bedrag, geen dienst",
             "text": "Vijftig tot tweehonderdduizend aan fiscale lekkage voorkomen is iets dat "
                     "een DGA begrijpt zonder dat je uitlegt wat je doet. Daar begint het "
                     "gesprek, en pas daarna komt wie je bent.",
             "quote": "'Leiden met een bedrag, 50k tot 200k fiscale lekkage voorkomen, en de "
                      "RA-achtergrond veel prominenter.'",
             "dom": "gespreksnotitie JR Finance &times; Pique", "datum": "1 juli 2026"},
            {"tag": "Waarom deze kaart", "kop": "Je betaalt per benadering",
             "text": "Je kiest zelf hoeveel DGA's er per maand worden aangeschreven, en daar "
                     "hangt het bedrag aan. Dat is iets anders dan een maandbedrag dat doorloopt "
                     "of je nu klanten binnenhaalt of niet, en het past beter bij iemand die in "
                     "januari begint. Wat het bij jouw aantal wordt, reken ik in dat gesprek "
                     "voor je uit."},
        ],
        "pivot": "Drie klanten van vijf mille is een jaar werk als je op gevoel zoekt, en een "
                 "kwestie van honderd goede namen als je weet welke DGA net verkocht heeft of "
                 "net een holding heeft opgezet.",
        "tijdlijn": [("1 jul", "ons gesprek"), ("jul", "nog niet aan de orde"),
                     ("jan", "je gaat fulltime"), ("nu", "deze kaart")],
        "tl_hand": "Vandaar deze kaart, en niet die in januari.",
        "case": "potentiel",
        "case_kop": "Vijftig kaarten, drie klanten.",
        "case_text": "Een health club met een aanbod dat je moeilijk in een advertentie uitlegt "
                     "wilde weten of vijftig kaarten genoeg zijn om iets te bewijzen. Vijftig "
                     "namen, elk met een eigen aanleiding. <strong>Negen mensen reageerden en "
                     "drie daarvan werden klant.</strong> "
                     "</p><p class='ch-text'>Over al onze campagnes samen, ruim tienduizend "
                     "benaderingen: <strong>98 procent komt op het bureau</strong>, er volgen "
                     "64,5 scans per honderd kaarten, en 9,5 procent van de scanners plant een "
                     "gesprek. Honderd kaarten worden zo ongeveer zes gesprekken. Cold email "
                     "blijft onder de 1 procent. Wat het bij jou wordt hangt af van je aanbod, "
                     "je lijst en de opvolging.",
        "voorstel_sub": "Honderd DGA's per maand, twee maanden, en we bellen de scans na.",
        "cta_sub": "Twintig minuten, wanneer het jou uitkomt. Dan reken ik ook voor wat het bij "
                   "jouw aantal kost. Blijkt januari nog te vroeg, dan is dat een prima uitkomst.",
        "dock": "Even over januari?",
    },
    "finovion": {
        "slug": "finovion",
        "bedrijf": "Finovion",
        "voornaam": "Wichard",
        "kaart": "Hoi Wichard.<br>Je zei december.<br>Dit is alvast de prijs.",
        "h1": 'Je zei <span class="u">december</span>.',
        "sub": "In juli lagen je prioriteiten ergens anders en vroeg je om er later op terug te "
               "komen. December komt eraan.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Met het oog op december"],
        "aanloop_kop": "Je wil van zestig kantoren naar driehonderd.",
        "aanloop": "In tien jaar, met ongeveer twintig nieuwe kantoren per jaar, langs twee "
                   "sporen: franchisenemers werven en kantoren overnemen. Daar stelde ik op "
                   "23 juli een pilot voor van twee maanden, honderd benaderingen per maand.",
        "aanloop2": "<strong>Je gaf aan dat er eerst andere dingen voorgingen en dat december "
                    "een beter moment was. Ik ben het daarna blijven behandelen als een "
                    "voorstel dat nog open stond, en dat was niet wat je zei.</strong>",
        "note": "dus nu, voor december",
        "finds": [
            {"tag": "Wat je toen zei", "kop": "Je rekende hem wel na",
             "text": "Je deelde mijn maandbedrag door het aantal afspraken dat ik vastlegde en "
                     "kwam op duizend euro per online afspraak, met daarbovenop nog een tweede "
                     "conversie naar een fysieke afspraak. Iemand die dat uitrekent heeft het "
                     "serieus bekeken.",
             "quote": "'Op ongeveer 5 afspraken per maand komt dat neer op 1.000 euro per "
                      "online afspraak, en daar moet nog een tweede conversie naar een fysieke "
                      "afspraak overheen.'",
             "dom": "gespreksnotitie Finovion &times; Pique", "datum": "23 juli 2026"},
            {"tag": "Waarom deze kaart", "kop": "Reken nu met het aantal",
             "text": "Hieronder staat de prijs per benadering in plaats van per maand. Daarmee "
                     "maak je in december je eigen som, op het aantal afspraken dat jij "
                     "verwacht."},
        ],
        "pivot": "Een accountantskantoor dat overweegt zich aan te sluiten doet dat een keer in "
                 "zijn bestaan. Dat is een gesprek over opvolging, over schaal en over de "
                 "eigenaar die wil blijven, en dat begint zelden bij een advertentie.",
        "tijdlijn": [("23 jul", "ons gesprek"), ("jul", "jouw rekensom"),
                     ("jul", "andere prioriteiten"), ("dec", "jouw eigen moment")],
        "tl_hand": "Zodat december geen gesprek over geld wordt.",
        "case": "geduld",
        "case_kop": "Vijftig namen in \u00e9\u00e9n regio.",
        "case_text": "Online Geduld bouwt websites voor bouw en techniek. De verleiding is om "
                     "heel Nederland aan te schrijven. We deden het omgekeerde: <strong>vijftig "
                     "bedrijven in dertien plaatsen rond Apeldoorn</strong>, met een enkel "
                     "signaal als enig criterium. De ontvanger is altijd de eigenaar, nooit een "
                     "algemeen adres.",
        "voorstel_sub": "Honderd kantoren per maand in een afgebakende regio, twee maanden, "
                        "en we bellen de scans na.",
        "cta_sub": "Geen haast. Wil je het in december oppakken, dan staat de prijs er nu alvast "
                   "zodat je het intern kunt voorbereiden.",
        "dock": "Alvast voor december?",
    },
    # ────────────────────────────── voorstel lag stil ─────────────────────────
    "studiorendement": {
        "slug": "studio-rendement",
        "bedrijf": "Studio Rendement",
        "voornaam": "Tjerk",
        "kent_hem": True,
        "kaart": "Hoi Tjerk.<br>Je zat vol.<br>Daar hoort een kleine<br>lijst bij.",
        "h1": 'Je zat <span class="u">vol</span>.',
        "sub": "Je zat vol in augustus, en dat is een ander probleem dan te weinig klanten "
               "hebben. Het vraagt om een ander soort lijst, en dat onderscheid maakte "
               "ik toen niet.",
        "chips": ["Tweede kaart", "2 minuten lezen", "Wat de aanpak doet"],
        "aanloop_kop": "Via Aquila kwamen we bij één segment uit.",
        "aanloop": "In augustus spraken we elkaar via Luke en Alvinho. Je zat vol, dus de vraag "
                   "ging over welk soort klant er dan nog bij moest. Daar kwam de ondernemer "
                   "uit die net verkocht heeft en opeens een vermogen moet onderbrengen.",
        "aanloop2": "<strong>Daarna legde ik twee bedragen neer en liet ik het daarbij. Bij "
                    "iemand die vol zit is dat precies de verkeerde volgorde.</strong>",
        "note": "eerst het aantal, dan het bedrag",
        "finds": [
            {"tag": "Wat we toen bespraken", "kop": "Twee smaken, geen aantal",
             "text": "Een strategiedag of een begeleidingstraject. Twee goede producten, en bij "
                     "geen van beide stond het aantal: hoeveel van die ondernemers wil je per "
                     "maand spreken.",
             "quote": "'Twee smaken: Strategiedag &euro; 4.750 of Begeleiding &euro; 7.250.'",
             "dom": "gespreksnotitie Studio Rendement &times; Pique",
             "datum": "11 augustus 2026"},
            {"tag": "Wat er veranderd is", "kop": "Jij zet de kraan open",
             "text": "Het aantal benaderingen per maand bepaalt wat het kost, en dat aantal kun "
                     "je elke maand bijstellen. Loopt je agenda vol, dan zet je het stil. Dat is "
                     "het hele verschil met een campagne die doorloopt. Wat het bij jouw aantal "
                     "wordt, reken ik in dat gesprek voor je uit."},
        ],
        "pivot": "Een ondernemer die net verkocht heeft, beslist binnen een paar maanden waar "
                 "dat geld heen gaat. Die momenten zijn te zien in het handelsregister, en dat "
                 "maakt de lijst klein en de timing scherp.",
        "tijdlijn": [("11 aug", "kennismaking via Aquila"), ("aug", "twee bedragen"),
                     ("aug", "je zat vol"), ("nu", "jij bepaalt het aantal")],
        "tl_hand": "Volgorde omgedraaid.",
        "case": "azora",
        "case_kop": "Vier directeuren die nooit terugbelden.",
        "case_text": "Azora maakt videocontent voor marketingbureaus en SaaS-bedrijven, een "
                     "markt waarin iedereen al door iedereen benaderd wordt. De vraag ging over "
                     "vier directeuren die nooit hadden gereageerd op bellen, mailen of "
                     "LinkedIn. <strong>Alle vier zaten binnen zes weken aan tafel.</strong> "
                     "</p><p class='ch-text'>Over al onze campagnes samen, ruim tienduizend "
                     "benaderingen: <strong>98 procent komt op het bureau</strong>, er volgen "
                     "64,5 scans per honderd kaarten, en 9,5 procent van de scanners plant een "
                     "gesprek. Honderd kaarten worden zo ongeveer zes gesprekken. Cold email "
                     "blijft onder de 1 procent. Wat het bij jou wordt hangt af van je aanbod, "
                     "je lijst en de opvolging.",
        "voorstel_sub": "Honderd ondernemers per maand die net verkocht hebben, twee maanden, en "
                        "we bellen de scans na.",
        "cta_sub": "Twintig minuten. Zit je nog steeds vol, dan is dit het gesprek om te bepalen "
                   "wie je er dan wél bij wil, en wat dat kost.",
        "dock": "Even over het aantal?",
    },
}


def knip(bron: str, start: str, eind: str) -> str:
    """Knipt een letterlijk blok uit het voorbeeldbestand, inclusief de grenzen."""
    i = bron.index(start)
    j = bron.index(eind, i) + len(eind)
    return bron[i:j]




STIJL = """
<style>
  /* lp.css styleert geen links in de lopende tekst, want de research-pagina's
     hebben er geen. Deze batch verwijst wel naar de cases, dus hier wel. */
  .ch-text a{color:var(--accent-h);text-decoration:none;
    border-bottom:1px solid rgba(var(--accent-rgb),.42);
    padding-bottom:1px;transition:border-color .18s ease,color .18s ease}
  .ch-text a:hover{color:var(--accent);border-bottom-color:var(--accent)}
</style>"""


def founderblok(data: dict) -> str:
    """Het vaste founderblok van v12, letterlijk uit odido-v12.html.

    De bedrijfsnaam is de enige variabele. Op 6 oktober liet ik dit blok weg bij
    ontvangers die Simon persoonlijk kent; de v12-standaard van 9 oktober zet het
    vast voor iedereen, dus die uitzondering is eruit.
    """
    return """
<section class="founder" id="founder">
  <img class="fo-photo fr" src="simon.png" alt="Simon Kempers, oprichter Pique" loading="lazy" decoding="async">
  <div class="fr">
    <div class="fo-eyebrow">De persoon achter dit voorstel</div>
    <div class="fo-text"><p>Ik ben Simon. Ik begon Pique omdat de inbox van elke beslisser inmiddels vol zit met dezelfde geautomatiseerde berichten. Daar val je niet meer tussen op.</p>
      <p>Dus doen we het omgekeerd. Een klein aantal bedrijven, per stuk het onderzoek dat je hierboven zag, en een kaart plus pagina die echt alleen over hen gaan. Zoals deze over %s.</p>
      <p>We schrijven er per maand een stuk of twintig aan, en bij elke doen we dit werk opnieuw.</p></div>
    <img class="fo-sig" src="handtekening.png" alt="Handtekening van Simon Kempers" width="560" height="208">
    <p class="fo-name">Simon Kempers, oprichter Pique</p>
  </div>
</section>""" % data["bedrijf"]


def bouw(data: dict, voorbeeld: str) -> Path:
    nav = knip(voorbeeld, '<nav id="nav">', "</nav>")
    qr = knip(voorbeeld, "<svg class='qr'", "</svg>")
    footer = knip(voorbeeld, "<footer>", "</footer>")
    sheet = knip(voorbeeld, "<!-- boeksheet -->", "</div>\n</div>\n\n<script")
    sheet = sheet[: sheet.rindex("<script")].rstrip()
    sheet = sheet.replace('value="Martijn"', f'value="{data["voornaam"]}"')
    # de sheet wordt letterlijk uit _voorbeeld geknipt en kent het ../-prefix niet
    sheet = sheet.replace('src="simon.png"', 'src="simon.png"')

    bedrijf = data["bedrijf"]
    voornaam = data["voornaam"]
    maquettes = knip(MODEL_V12.read_text(encoding="utf-8"),
                     '<section class="toon" id="toon">', "</section>")
    # odido-v12 zet de naam van de ontvanger zelf op deze maquettekaart, terwijl de
    # bijschriften eronder over 'zijn bureau' en 'zijn bedrijf' gaan. tellscan vangt dat
    # terecht als derde persoon. De maquette toont wat de ONTVANGER straks verstuurt, dus
    # staat er een naamloze prospect op en ondertekent de ontvanger zelf.
    maquettes = (maquettes.replace("Hoi Martijn.", "Hoi Jan.")
                          .replace("naar <em>Odido Zakelijk</em>", "naar <em>zijn bedrijf</em>")
                          .replace('<div class="mk-s">Simon</div>',
                                   f'<div class="mk-s">{bedrijf}</div>')
                          .replace('<div class="mk-adres">pique.agency</div>',
                                   '<div class="mk-adres">jullie-eigen-pagina</div>')
                          .replace("Odido Zakelijk", bedrijf))
    case_url, case_naam = CASES[data["case"]]

    chips = "".join(
        f'<span class="chip">{c}</span>' if i else f'<span class="chip"><i></i>{c}</span>'
        for i, c in enumerate(data["chips"])
    )

    finds = ""
    for i, f in enumerate(data["finds"]):
        kant = "right" if i % 2 == 0 else "left"
        idd = ' id="s2"' if i == 0 else ""
        bewijs = ""
        if f.get("quote"):
            bewijs = f"""
          <div class="f-bewijs">
            <p class="f-quote">{f['quote']}</p>
            <div class="f-meta"><span class="dom">{f['dom']}</span><span class="sep"></span><span>{f['datum']}</span></div>
          </div>"""
        finds += f"""
  <section class="chapter {kant} find"{idd}>
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="f-head"><div class="f-num">0{i + 1}<span class="of">/ 0{len(data['finds'])}</span></div><div class="f-tag">{f['tag']}</div></div>
        <h2 class="f-kop">{f['kop']}</h2>
        <p class="ch-text">{f['text']}</p>{bewijs}
      </div>
    </div>
  </section>"""

    tl = "".join(
        f'<div class="tl-i{" nu" if i == len(data["tijdlijn"]) - 1 else ""}" style="--dl:{.2 + i * .25:.2f}s">'
        f'<span class="d"></span><b>{wat}</b><span>{uitleg}</span></div>'
        for i, (wat, uitleg) in enumerate(data["tijdlijn"])
    )

    html = f"""<!DOCTYPE html>
<!--
  Heractivatiebatch oktober 2026. Vorm uit Componenten/lp-v2, inhoud uit bouw.py.
  Deze pagina gaat naar iemand met wie al gesproken is, dus hij bouwt door op de
  eerste kaart in plaats van opnieuw te beginnen. De VSL staat onderaan.
-->
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Pique voor {bedrijf}</title>
<meta name="description" content="Een tweede voorstel voor {bedrijf}.">
<meta name="robots" content="noindex">
<link rel="icon" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://app.cal.com"><link rel="preconnect" href="https://cal.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=Inter:wght@300;400;500;600;700&family=Caveat:wght@500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="thema-pique.css">
<link rel="stylesheet" href="lp.css">
{STIJL}

<script>
  window.PQ_BEDRIJF      = '{bedrijf}';
  window.PQ_KLANT        = 'pique';
  window.PQ_CAMPAGNE     = 'opnieuw-okt26';
  window.PQ_CAL          = 'simon-kempers/belafspraak-pique';
  window.PQ_VIDEO        = 'simon-staand.mp4';
  window.PQ_POSTER       = 'simon-staand-poster.jpg';
  window.PQ_TRACK_URL    = '/api/t';
  window.PQ_TERUGBEL_URL = 'https://script.google.com/macros/s/AKfycby37aGED41tyit5g9IemLY07prmG6J8CIERkkrYSxl92H3aBGCCui-G2stGXMDaUNsngQ/exec';
  window.PIQUE_INTRO     = {{ voornaam: '{voornaam}', bedrijf: '{bedrijf}' }};
</script>
<script src="lp-intro.js"></script>
</head>
<body>
<div class="mbar" id="mbar"></div>

{nav}

<div class="rail" id="rail">
  <a href="#s1"><span class="rd"></span><span class="rl">Waarom weer</span></a>
  <a href="#s2"><span class="rd"></span><span class="rl">Wat er anders is</span></a>
  <a href="#s4"><span class="rd"></span><span class="rl">Wat ik voorstel</span></a>
  <a href="#gesprek"><span class="rd"></span><span class="rl">Even bellen</span></a>
</div>

<header class="hero" id="top">
  <div class="hero-grid"></div>
  <div class="hero-inner">
    <div class="hero-left">
      <div class="slot" id="slot">
        <div class="slot-card" id="slotcard">
          <div class="h">{data['kaart']}</div>
          <div class="sig">Simon</div>
        </div>
        <span class="slot-tag">De kaart op je bureau</span>
      </div>
    </div>
    <div class="hero-right">
      <h1 class="hero-h1">H&eacute; <span class="u">{voornaam}</span>, dit is waarom ik je een kaart heb gestuurd.</h1>
      <p class="hero-sub">{data['sub']}</p>
      <div class="hero-meta">{chips}</div>
      <div class="scrollcue"><i></i><span>Scroll</span></div>
    </div>
  </div>
</header>

<main class="journey" id="journey">
  <svg class="jpath" id="jpath" preserveAspectRatio="none" aria-hidden="true">
    <path class="jp-base" id="jp-base"></path>
    <path class="jp-prog" id="jp-prog"></path>
  </svg>

  <section class="chapter left" id="s1">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">Waarom je dit weer krijgt</div>
        <h2 class="ch-kop">Waarom ik je een kaart stuurde.</h2>
        <p class="ch-text">{data['aanloop']}</p>
        <p class="ch-text">{data['aanloop2']}</p>
        <div class="ch-sign">Simon, oprichter Pique</div>
      </div>
      <div class="note">{data['note']}
        <svg class="arw" viewBox="0 0 52 26"><path d="M2 5c13 0 24 5 32 14M34 19l-6-1.4M34 19l1.2-6"/></svg>
      </div>
    </div>
  </section>
{finds}
  <section class="chapter center pivot" id="s3">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">Waar het op neerkomt</div>
        <p class="ch-pivot">{data['pivot']}</p>
        <div class="tl">
          <div class="tl-rail">{tl}</div>
          <p class="tl-hand">{data['tl_hand']}</p>
        </div>
      </div>
    </div>
  </section>
</main>

<section class="ask" id="ask">
  <div class="ask-in">
    <p class="ask-hand">Zal ik je er gewoon even over bellen?</p>
    <p class="ask-sub">Hieronder staat wat een vergelijkbare campagne opleverde en wat ik voor
    {bedrijf} zou doen. Hoor je dat liever, dan pak ik de telefoon. Twintig minuten.</p>
    <div class="ask-btns">
      <button class="btn-a" data-open="sheet" data-tab="plan">Ja, plan een gesprek</button>
      <button class="btn-b" id="askread">Ik lees het eerst</button>
    </div>
    <p class="ask-later">Of <button data-open="sheet" data-tab="bel">laat je nummer achter</button> en ik bel je terug.</p>
  </div>
</section>

<main class="journey" id="journey2">
  <svg class="jpath" id="jpath2" preserveAspectRatio="none" aria-hidden="true">
    <path class="jp-base" id="jp-base2"></path>
    <path class="jp-prog" id="jp-prog2"></path>
  </svg>

  <section class="chapter left">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">{case_naam.capitalize() if case_naam.startswith('de ') else case_naam}</div>
        <h2 class="ch-kop">{data['case_kop']}</h2>
        <p class="ch-text">{data['case_text']}</p>
        <p class="ch-text"><a href="https://{case_url}">De hele campagne staat op {case_url}</a></p>
      </div>
    </div>
  </section>

  <section class="chapter center phase" id="s4">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">Het voorstel</div>
        <h2 class="ch-kop ch-head">Wat we voorstellen.</h2>
        <p class="ch-sub">{data['voorstel_sub']}</p>
      </div>
    </div>
  </section>

</main>

{maquettes}
{founderblok(data)}
<section class="cta" id="gesprek">
  <div class="cta-inner">
    <div class="cta-eyebrow reveal">De volgende stap</div>
    <h2 class="cta-h reveal">Even bijpraten?</h2>
    <p class="cta-sub reveal">{data['cta_sub']}</p>
    <div class="cta-btns reveal">
      <button class="btn-a" data-open="sheet" data-tab="plan">Kies een moment</button>
      <button class="btn-b" style="color:rgba(255,255,255,.75);border-color:rgba(255,255,255,.2)" data-open="sheet" data-tab="bel">Laat me terugbellen</button>
    </div>
    <p class="cta-alt reveal">Liever eerst even schriftelijk? <a href="mailto:info@pique.agency?subject={bedrijf.replace(' ', '%20')}%20%C3%97%20Pique">Mail me een korte vraag.</a></p>
  </div>
</section>

{footer}

<div class="dock" id="dock">
  <span class="dock-t"><b>{data['dock']}</b> 20 minuten.</span>
  <button class="dock-b" data-open="sheet" data-tab="plan">Plannen</button>
  <button class="dock-x" id="dockx" aria-label="Sluiten">&times;</button>
</div>

{sheet}

<script src="lp-v2.js"></script>
</body>
</html>
"""
    uit = UIT / f"{data['slug']}.html"
    uit.write_text(html, encoding="utf-8")
    return uit


def main() -> None:
    voorbeeld = VOORBEELD.read_text(encoding="utf-8")
    keuze = sys.argv[1:] or list(PROSPECTEN)
    for sleutel in keuze:
        if sleutel not in PROSPECTEN:
            print(f"onbekend: {sleutel}")
            continue
        pad = bouw(PROSPECTEN[sleutel], voorbeeld)
        print(f"{pad.name:34} {pad.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()
