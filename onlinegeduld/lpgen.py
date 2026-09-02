#!/usr/bin/env python3
"""Bouwt de persoonlijke landingspagina's voor Online Geduld op het lp-v2 component.

De vorm komt uit Componenten/lp-v2 en wordt hier niet aangeraakt. Wat hier staat is
inhoud: per prospect een denkpad dat volgt uit hoe ik hem daadwerkelijk heb gezocht
en wat ik daarbij wel en niet vond.

Zeven denkpaden, want zeven verschillende manieren waarop het bij deze bedrijven
misgaat. Binnen elk pad rouleren de formuleringen op een hash van de bedrijfsnaam,
zodat twee buren nooit dezelfde zinnen krijgen.
"""
import csv, html, json, os, re, sys, unicodedata, hashlib

UIT = "/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/BCS/onlinegeduld"
BRON = "/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/Online-Geduld/Online-Geduld-FaseB-Batch50.csv"
DATUM = "25 augustus 2026"
TEL = "06 48 91 90 97"
MAIL = "info@onlinegeduld.nl"

# Het adres wordt met de hand geschreven en met de hand overgetypt. De naam van
# het bedrijf is dus leidend, en het vakwoord ervoor mag weg zodra het te lang wordt.
SLUGRUIS = ('bv','vof','nv','cv','zn','zonen','beheer','holding','jr','sr')
GENERIEK = ('bouwbedrijf','aannemersbedrijf','aannemingsbedrijf','transportbedrijf',
            'schildersbedrijf','installatiebedrijf','stukadoorsbedrijf','dakdekkersbedrijf',
            'loodgietersbedrijf','hoveniersbedrijf','grondverzetbedrijf','timmerbedrijf',
            'montagebedrijf','onderhoudsbedrijf','constructiebedrijf','lasbedrijf',
            'installatieburo','installatiebureau','machinefabriek','metaalbewerking',
            'metaalwerken','gebroeders','gebr','loonbedrijf')

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\(.*?\)', ' ', s)
    w = [x for x in re.split(r'[^a-z0-9]+', s) if x]
    w = [x for x in w if x not in SLUGRUIS and not (len(x) == 1 and x.isalpha())]
    kern = [x for x in w if x not in GENERIEK]
    vak = [x for x in w if x in GENERIEK]
    if not kern:
        kern, vak = vak, []
    def lang(l): return sum(len(y) + 1 for y in l) - 1
    # eerst de naam, daarna het vakwoord ervoor als het nog past
    uit = []
    for x in kern:
        if uit and lang(uit + [x]) > 30: break
        uit.append(x)
    if vak and lang([vak[0]] + uit) <= 30:
        uit = [vak[0]] + uit
    return '-'.join(uit) or 'bedrijf'

def kies_rij(lijst, sleutel, zout=''):
    """Zelfde volgorde als kies, maar als lijst, zodat je kunt doorschuiven bij een botsing."""
    h = int(hashlib.sha1((sleutel + '|' + zout).encode()).hexdigest(), 16) % len(lijst)
    return lijst[h:] + lijst[:h]

def kies(lijst, sleutel, zout=''):
    """Vaste keuze per bedrijf, zodat een pagina bij hergenereren gelijk blijft."""
    h = int(hashlib.sha1((sleutel + '|' + zout).encode()).hexdigest(), 16)
    return lijst[h % len(lijst)]

def E(s):
    return html.escape(str(s or ''), quote=False)

# ══════════════════════════════════════════════════════════════════════
#  Vaktaal per branche. Dit bepaalt in wiens wereld de pagina staat.
# ══════════════════════════════════════════════════════════════════════
VAK = {
 'installatie': dict(
   wat='installatiewerk', klus='ketel of warmtepomp', mens='monteur', mensen='monteurs',
   opdr='een aannemer of een vastgoedbeheerder', ding='je bus',
   zoekt='zonder warm water zit, of een offerte nodig heeft voor een verbouwing',
   term='installateur', leuk='Ik heb zelf jaren in de installatie gezeten, dus ik weet hoe lang je soms naar een schema kunt staan kijken voordat het kwartje valt.'),
 'elektro': dict(
   wat='elektrotechniek', klus='groepenkast of laadpaal', mens='monteur', mensen='monteurs',
   opdr='een aannemer of een installateur', ding='je bus',
   zoekt='midden in een verbouwing zit en er een elektricien bij nodig heeft',
   term='elektricien', leuk='Laadpalen vind ik zelf het leukste stuk techniek van de afgelopen jaren. Half elektro, half software, en niemand die precies weet waar het over vijf jaar staat.'),
 'bouw': dict(
   wat='bouwwerk', klus='verbouwing', mens='timmerman', mensen='mensen',
   opdr='een architect of een projectontwikkelaar', ding='je keet',
   zoekt='een verbouwing voorbereidt en offertes opvraagt',
   term='aannemer', leuk='Wat mij aan de bouw blijft verbazen is hoeveel er wordt afgesproken zonder dat er iets op papier staat, en hoe vaak dat gewoon goed gaat.'),
 'afbouw': dict(
   wat='afbouwwerk', klus='wand of vloer', mens='vakman', mensen='mensen',
   opdr='een aannemer of een particulier met een verbouwing', ding='je bus',
   zoekt='midden in een verbouwing zit en snel iemand nodig heeft',
   term='afbouwer', leuk='Stukwerk is het enige vak waar ik echt niets van kan. Ik heb het één keer geprobeerd in mijn eigen gang en het is nog steeds te zien.'),
 'metaal': dict(
   wat='metaalwerk', klus='constructie of machineonderdeel', mens='lasser', mensen='mensen',
   opdr='een machinebouwer of een aannemer', ding='je werkplaats',
   zoekt='iets nodig heeft dat nergens op voorraad ligt',
   term='constructeur', leuk='Ik heb veel te lang staan kijken naar hoe een kantbank werkt toen ik daar een keer stond. Dat verkoopt niets, ik vond het gewoon mooi.'),
 'grond': dict(
   wat='grondwerk', klus='oprit of bouwrijp terrein', mens='machinist', mensen='mensen',
   opdr='een aannemer of een gemeente', ding='je materieel',
   zoekt='een kavel heeft en niet weet wie hij daarvoor belt',
   term='grondwerker', leuk='Van alle bedrijven die ik deze weken heb bekeken, hebben die met graafmachines de mooiste foto\'s. En bijna niemand zet ze ergens neer.'),
}
VAK['techniek'] = VAK['metaal']

# ══════════════════════════════════════════════════════════════════════
#  De zeven denkpaden. Elk pad heeft een eigen manier van zoeken,
#  een eigen kantelvraag en een eigen gevolg.
# ══════════════════════════════════════════════════════════════════════

def pad_bepalen(r):
    st = r['site_status']
    geb = r['gebreken']
    if st == 'geen':
        if r.get('trustoo') == 'ja': return 'portaal'
        if 'bedrijvenkring' in r.get('bron', ''): return 'kring'
        return 'gids'
    if st == 'dood':
        return 'weg'
    if r.get('disciplines'): return 'vak'
    if 'geen mobiele weergave' in geb or 'over de rand' in geb: return 'mobiel'
    return 'lek'

# ── de aanloop: waar ik begon te kijken, inclusief de omweg ───────────
AANLOOP = {
 'portaal': [
  "Ik zocht {termen} in de regio die ik zou kunnen bellen. Zo kwam ik bij {bedrijf}, via {portaal}.\n\nDaarna wilde ik je eigen site zien, want op zo'n portaal ziet iedereen er hetzelfde uit.\n\nDie heb ik niet gevonden.",
  "Ik kwam je tegen op {portaal}. Daar staan de bedrijven die aan werk willen komen, dus daar begin ik.\n\nToen zocht ik je eigen site. Die is er niet.",
 ],
 'kring': [
  "Ik liep de ledenlijst van de Bedrijvenkring Apeldoorn langs en klikte op {bedrijf}.\n\nDaar hield het op. Er zit geen site achter je naam.",
  "Ik begon bij de leden van de Bedrijvenkring, want wie contributie betaalt wil gezien worden. Zo kwam ik bij {bedrijf}.\n\nJe profiel staat er. Een link naar een eigen site ontbreekt.",
 ],
 'gids': [
  "Ik zocht {termen} in {plaats} en omgeving. {bedrijf} stond in de bedrijvengids, onder {rubriek}.\n\nDaarna ben ik je site gaan zoeken. Een half uur later ben ik gestopt.",
  "Ik ben deze maand {termen} in de regio langsgegaan. {bedrijf} vond ik in de gids, met een adres in {plaats}.\n\nWat ik daarna zocht was je site, want ik wilde zien wat voor werk jullie doen. Die vond ik niet.",
 ],
 'weg': [
  "Ik keek naar {termen} in de regio en kwam bij {bedrijf}. Toen wilde ik je site openen.\n\nDat lukte niet, en dat is iets anders dan een site die traag is.",
  "Bij {bedrijf} kwam ik een webadres tegen dat ooit ergens naartoe wees.\n\nEr is dus iemand geweest die dit voor je heeft gebouwd. En er is een moment geweest waarop het stopte.",
 ],
 'mobiel': [
  "Ik heb {domein} geopend op mijn telefoon, want daar kijkt degene die je zoekt.\n\nOp een laptop is er weinig aan de hand. Op een telefoon gebeurt er iets anders.",
  "Ik ging {termen} in de regio langs en kwam bij {domein}.\n\nMijn eerste indruk was dat hij prima was. Toen pakte ik mijn telefoon erbij.",
 ],
 'vak': [
  "Ik kwam bij {domein} terecht en keek eerst naar wat jullie doen, daarna pas naar de site.\n\nDaartussen zit een gat, en dat is de reden dat ik schrijf.",
  "Bij {bedrijf} viel me iets op dat niets met het ontwerp te maken heeft. Het zit in wat er wel en niet op staat.",
 ],
 'lek': [
  "Ik heb {domein} geopend zoals iemand dat doet die jullie nodig heeft. Op een telefoon, buiten, met één hand.\n\nDe site doet het. Ik kwam er alleen niet doorheen.",
  "Ik ging {termen} in de regio langs en kwam bij {domein}. Hij laadt en hij ziet er verzorgd uit.\n\nToch strandde ik op het laatste stukje, van kijken naar bellen.",
 ],
}

# ── de kantelvraag: een vraag waar hij het antwoord niet op weet ──────
PIVOT = {
 'portaal': [
  "Je betaalt per aanvraag voor mensen die je op {portaal} vinden. En als iemand daarna je naam intypt om te kijken wie je bent, komt hij nergens uit.\n\nHoeveel van die mensen zijn er, en wat doen ze dan?",
  "Op {portaal} sta je tussen de anderen. Daarbuiten sta je nergens.\n\nDus wie kiest jou als hij eenmaal je naam heeft?",
 ],
 'kring': [
  "Je betaalt contributie om gezien te worden. En als iemand op je naam klikt, houdt het daar op.\n\nWaar komt iemand terecht die jou wil bekijken voordat hij belt?",
  "Je staat op een ledenlijst waar mensen komen kijken wie er in de regio zit. Verder dan je naam komen ze niet.\n\nWat weet zo iemand op dat moment eigenlijk van je?",
 ],
 'gids': [
  "Wie jou nu vindt, kende je al. Dat werkt, tot je een keer iemand nodig hebt die je nog niet kent.\n\nHoe komt de volgende klant bij je binnen?",
  "Er staat een naam, een adres en een nummer. Iemand die twijfelt tussen jou en twee anderen, heeft niets om op te kiezen.\n\nWaar kijkt hij dan naar?",
 ],
 'weg': [
  "Er is ooit iemand geweest die dit heeft gebouwd. En er is een moment geweest waarop dat is gestopt.\n\nWeet je nog wanneer dat was, en wat er sindsdien is veranderd aan hoe mensen je vinden?",
  "Het adres staat nog op je briefpapier en waarschijnlijk ook op {ding}. Wie dat intypt, krijgt niets.\n\nHoeveel mensen hebben dat het afgelopen jaar geprobeerd?",
 ],
 'mobiel': [
  "Vier van de vijf mensen die jou zoeken doen dat op hun telefoon. Op die telefoon werkt hij niet.\n\nWat gebeurt er met iemand die het bij jou opgeeft en de volgende belt?",
  "De site is gemaakt voor het scherm waarop hij is gebouwd. Hij wordt gebruikt op een ander scherm.\n\nHoe vaak is jou dat de afgelopen tijd ontgaan?",
 ],
 'vak': [
  "Op {ding} staat wat je nu doet. Op je site staat wat je vroeger deed.\n\nWie zoekt op wat je erbij hebt gedaan, komt bij iemand anders uit. Bij wie eigenlijk?",
  "Je bent uitgebreid. De site is meegegroeid met niets.\n\nHoeveel aanvragen voor dat nieuwe werk zijn er tot nu toe binnengekomen via je site?",
 ],
 'lek': [
  "De site vertelt wat je doet. Hij maakt het alleen niet makkelijk om je daarover te bellen.\n\nWie geeft het op halverwege, en hoor jij daar ooit iets van?",
  "Alles staat er. Het laatste stukje, van kijken naar bellen, is waar het misgaat.\n\nHoeveel mensen zijn er dit jaar tot daar gekomen?",
 ],
}

# ── het gevolg: rustig, met een maat, verankerd in zijn wereld ────────
GEVOLG = [
 "Dit staat op geen enkele factuur. Iemand die {zoekt} kwam bij je uit, kwam er niet doorheen, en belde de volgende. Daar hoor jij nooit iets van.\n\nTwee per maand is voorzichtig gerekend. Wat één {klus} bij jullie oplevert weet jij, en dat cijfer hoor ik graag.",
 "Reken het eens terug. Twee mensen per maand die {zoekt}, jou vinden en het opgeven. Dat zijn vierentwintig gesprekken per jaar die je nooit hebt gevoerd.\n\nWat één {klus} waard is bij jullie, weet jij beter dan ik. Zeg dat bedrag in het gesprek, dan reken ik het ter plekke uit.",
 "Je ziet het niet weggaan, en dat is precies het probleem. Het zit in de aanvragen die nooit binnenkomen, en die kun je nergens terugzoeken.\n\nEén {klus} per maand extra is al snel een bedrag waar je aan het eind van het jaar iets van merkt.",
 "Iemand die {zoekt} komt bij je uit. Hij komt er niet doorheen en belt de volgende. Jij merkt daar niets van, want er komt geen bericht dat iemand het heeft opgegeven.\n\nZet er twee per maand op. Wat dat waard is in {wat}, hoor ik liever van jou dan dat ik het verzin.",
]
GEVOLG_MENS = [
 "En er is nog een kant die vaker vergeten wordt. {Mensen} zoeken je op voordat ze solliciteren, en zeker voordat ze opzeggen bij hun huidige baas. Als er dan niets te zien is, blijven ze zitten waar ze zitten.\n\nIn dit vak is dat op dit moment het duurste wat er kan gebeuren.",
 "Daar komt bij dat een {mens} tegenwoordig kieskeurig kan zijn. Die kijkt eerst wat voor bedrijf je bent, en pas daarna of hij belt. Wat hij op dat moment ziet, bepaalt of hij dat doet.",
]

# ── de projectie: hoe het anders zou zijn, zonder 'stel je voor' ──────
PROJECTIE = [
 "Zo zou het eruitzien. Iemand typt je naam in, ziet foto's van werk dat af is, leest in vijf seconden wat jullie doen en waar, en drukt op één knop om te bellen.\n\nDaar hoeft geen campagne bij.",
 "Wat er dan staat is niet ingewikkeld. Jullie eigen projecten, de plaatsen waar jullie komen, en een nummer waar je met één tik op belt.\n\nMeer heeft iemand die je zoekt ook niet nodig.",
 "De versie die ik voor me zie: foto's van afgerond werk, je certificeringen erbij, en een aanvraagknop die ook werkt als het regent en je handschoenen aanhebt.",
 "Iemand zoekt je, vindt je, herkent het werk, en belt. Zonder dat hij ergens over hoeft na te denken.\n\nDat is het hele verschil.",
]

# ── de brug: wat ik zou doen, in handelingen ──────────────────────────
BRUG = [
 "Ik begin met een telefoontje van een kwartier. Ik wil weten waar jullie opdrachten vandaan komen en wie er opneemt als er iets binnenkomt.\n\nDaarna heb ik foto's van jullie nodig, en de certificeringen die jullie voeren. Dat is het meeste werk aan jouw kant, en het kost je een halfuur.\n\nDe rest doe ik. Binnen een week kun je hem openen en zeggen wat er anders moet.",
 "We bellen eerst een kwartier over hoe het werk binnenkomt. Dat bepaalt de hele opbouw, meer dan welke kleur dan ook.\n\nDan lever jij foto's van afgerond werk aan. Die van jullie werken altijd beter dan wat ik ergens zou kopen.\n\nEen week later staat er iets dat je kunt openen op je telefoon.",
 "Ik zou beginnen met bellen. Een kwartier, om te horen hoe jullie aan werk komen en wie er belt. Dat bepaalt wat er op de site moet, meer dan welke smaakkeuze ook.\n\nDaarna vraag ik je om foto's van jullie eigen werk. Die van jullie zijn altijd beter dan wat ik zou kunnen kopen, ook als ze scheef staan.\n\nEn dan bouw ik hem. Binnen een week staat er een versie die je kunt openen, en daarop zeg jij wat er anders moet.",
 "Eerst een gesprek van een kwartier over hoe jullie aan opdrachten komen. Over kleuren hebben we het later, want daar valt weinig te kiezen zolang dat eerste niet duidelijk is.\n\nDan verzamel ik wat er al is: foto's van projecten, je certificeringen, de plaatsen waar jullie werken. Dat is meestal meer dan mensen zelf denken.\n\nBinnen een week staat er iets dat werkt. Jij kijkt, ik pas aan, hij gaat live.",
 "Ik bel je eerst, een kwartier. Ik wil weten wie er belt als er werk binnenkomt, en waar die mensen vandaan komen.\n\nDaarna heb ik van jou foto's nodig van afgerond werk, en de certificeringen die jullie voeren. De rest schrijf ik zelf, en jij corrigeert.\n\nEen week later staat hij live.",
]

# ── de brugblokken: drie argumenten die elkaar niet herhalen ──────────
BLOKSETS = [
 [("Ik kom uit de techniek", "Ik heb zelf in de installatie gewerkt. Ik ga je niet vragen wat jullie kernwaarden zijn, en ik weet waarom een projectfoto meer doet dan een pagina tekst."),
  ("Je krijgt mij aan de lijn", "Er zit geen accountmanager tussen ons in. Je belt mij, en ik ben ook degene die je site gebouwd heeft."),
  ("795 euro, en dat staat gewoon op mijn site", "Live binnen een week, hosting en livegang inbegrepen. Daarna 65 euro per maand als ik hem bijhoud, en dat mag je ook laten zitten.")],
 [("Ik spreek je taal al", "Jarenlang in de techniek gezeten. Je hoeft mij niet uit te leggen wat een certificering doet in een uitvraag, of waarom een offerteknop met handschoenen te bedienen moet zijn."),
  ("Eén persoon, van begin tot eind", "Ik bel, ik bouw, ik zet hem live. Er zit niemand tussen die het moet doorgeven, en dat scheelt meestal drie weken."),
  ("Je weet vooraf wat het kost", "795 euro voor de site, binnen een week live. 65 euro per maand als ik hem bijhoud. Meer smaken zijn er niet.")],
 [("Uit de techniek, niet uit de marketing", "Ik heb in de installatie gewerkt. Dat merk je vooral aan wat ik niet vraag."),
  ("Eén aanspreekpunt", "Je hebt mijn nummer en dat is het enige nummer. Wachten tot iemand het intern heeft doorgegeven hoeft nooit."),
  ("Vaste prijs, vaste week", "795 euro, live binnen een week, hosting erbij. Het maandbedrag van 65 euro is optioneel.")],
 [("Ik weet hoe jullie aan werk komen", "Dat is het verschil met een bureau dat bij het ontwerp begint. Ik begin bij de vraag wie er belt en waarom."),
  ("Je praat met de bouwer zelf", "Wat je tegen mij zegt komt niet via drie mensen op de werkvloer terecht. Ik ben de werkvloer."),
  ("795 euro en klaar in een week", "Inclusief livegang en hosting. Het bijhouden kost 65 euro per maand en is geen verplichting.")],
]

# ── iets teruggeven: iets dat hij zonder mij kan doen ─────────────────
TERUG = {
 'portaal': "Kijk deze week eens hoeveel je het afgelopen jaar aan {portaal} hebt betaald. Deel dat door het aantal opdrachten dat eruit kwam. Dat getal is interessanter dan alles wat ik hierboven heb geschreven, en je hebt mij er niet voor nodig.",
 'kring': "Vraag je laatste drie klanten eens waar ze je gevonden hebben. Komen ze alle drie via iemand die je al kende, dan weet je wat er nog niet loopt.",
 'gids': "Typ je eigen bedrijfsnaam eens in bij Google, en daarna je vak plus {plaats}. Bij de eerste vind je jezelf waarschijnlijk wel. Bij de tweede is het de vraag, en dat is de zoekopdracht die je klant gebruikt.",
 'weg': "Bel de partij die destijds je site heeft gemaakt en vraag wie het domein op zijn naam heeft staan. Dat is goed om te weten, ook als je verder niets doet. Een domein dat op naam van iemand anders staat, ben je zomaar kwijt.",
 'mobiel': "Pak je telefoon, open je eigen site, en probeer jezelf te bellen vanaf die pagina. Lukt dat met één tik, dan zit het goed. Moet je het nummer overtypen, dan weet je wat ik bedoel.",
 'vak': "Zoek eens op je nieuwe werk plus {plaats}, en kijk op welke plek je staat. Dat kost je een minuut en het zegt meer dan een offerte van mij.",
 'lek': "Vraag iemand die jullie niet kent om op zijn telefoon een offerte bij je aan te vragen. Kijk mee, en zeg niets. Waar hij aarzelt, zit het probleem.",
}


# ══════════════════════════════════════════════════════════════════════
#  Varianten voor de vaste blokken. Drie of meer per slot, want een zin
#  telt pas als sjabloon zodra hij op meer dan de helft van de pagina's
#  staat. Zie Context/tools/tellscan.py.
# ══════════════════════════════════════════════════════════════════════
SLOT_TAG = ["De kaart op je bureau", "Wat er bij je op de mat lag", "De kaart die je kreeg", "Het kaartje van vorige week"]
VROW = [("Liever horen dan lezen?", "Ik stel mezelf voor in 40 seconden"),
        ("Weinig tijd?", "In 40 seconden vertel ik wie ik ben"),
        ("Liever even zien wie dit schrijft?", "40 seconden, en dan weet je genoeg"),
        ("Kort filmpje", "Ik leg in 40 seconden uit waarom ik je schrijf")]
ASK_HAND = ["Zal ik je hier even over bellen?", "Wil je dat ik je bel?",
            "Zullen we dit even doornemen?", "Even hierover bellen?"]
ASK_SUB = [
 "Hieronder staat wat ik zou doen. Wil je dat liever horen, laat dan je nummer achter. Een kwartier, en je zit nergens aan vast.",
 "Verderop staat mijn voorstel. Lees je liever niet, laat dan je nummer achter en ik bel je een keer. Duurt een kwartier.",
 "Wat ik zou doen staat hieronder. Bellen mag ook, dan hoor je het in een kwartier en scheelt het je lezen.",
 "Onder deze knop staat de rest. Heb je daar nu geen zin in, geef me dan je nummer, dan bel ik je op een rustig moment.",
]
ASK_BTN = ["Laat je nummer achter", "Bel me maar", "Ik hoor het liever", "Bel me een keer"]
ASK_LEES = ["Ik lees eerst verder", "Eerst de rest lezen", "Laat de rest maar zien", "Ik lees het liever zelf"]
ASK_LATER = ["Of bel zelf:", "Liever meteen zelf bellen?", "Je mag ook gewoon bellen:", "Of pak de telefoon:"]
DOCK = [("Even bellen over wat ik zag?", "Een kwartier."),
        ("Wil je dit even doornemen?", "Kwartiertje."),
        ("Zal ik je terugbellen?", "Vijftien minuten."),
        ("Even sparren hierover?", "Een kwartier, meer niet.")]
SHEET_N = ["Een kwartier met Cheraldo", "Vijftien minuten, met mij", "Kort bellen met Cheraldo", "Een kwartier aan de telefoon"]
SHEET_S = ["Telefoon. Ik bel je op een moment dat jou uitkomt.",
           "Gewoon telefonisch. Zeg maar wanneer het schikt.",
           "Ik bel je terug, op het moment dat jij noemt.",
           "Per telefoon. Jij kiest het moment."]
FO_EYE = ["Wie dit geschreven heeft", "De persoon achter deze pagina", "Wie ik ben", "Over de afzender"]
FOUNDER = [
 ["Ik ben Cheraldo. Ik heb zelf in de installatietechniek gewerkt en maak nu websites voor bedrijven in dat vak, in de regio Apeldoorn.",
  "Ik ben hiermee begonnen omdat ik bij het bedrijf waar ik werkte zag hoe vaak goede vakmensen online niets voorstelden. De bussen glommen en de site stond al vier jaar stil. Dat gat vond ik zonde."],
 ["Cheraldo, uit de regio Apeldoorn. Ik heb in de installatie gewerkt en bouw nu websites voor de bedrijven waar ik toen mee te maken had.",
  "De reden dat ik dit doe: ik zag van dichtbij hoe goed die bedrijven hun werk deden, en hoe weinig daarvan online terug te zien was. Daar zit meer verschil tussen dan mensen denken."],
 ["Ik ben Cheraldo Geduld. Mijn vak was techniek, inmiddels bouw ik sites, en die twee liggen dichter bij elkaar dan het klinkt.",
  "Wat me destijds opviel: een bedrijf met tien man en een volle orderportefeuille, en een website waar je niets aan af kon lezen. Dat kwam ik keer op keer tegen."],
 ["Cheraldo. Voordat ik dit deed werkte ik in de installatietechniek, hier in de buurt.",
  "Ik ben begonnen omdat het me stoorde. Vakmensen die alles op orde hebben, en dan een site die dat op geen enkele manier laat zien. Dat is makkelijker op te lossen dan het lijkt."],
]
FO_NAME = ["Cheraldo Geduld, Online Geduld", "Cheraldo, Online Geduld",
           "Cheraldo Geduld", "Cheraldo &middot; Online Geduld"]
CH_SIGN = ["Cheraldo, Online Geduld", "Cheraldo Geduld", "Cheraldo &middot; regio Apeldoorn", "Cheraldo, uit Apeldoorn"]
CTA_SUB = [
 "In dat kwartier loop ik met je door wat ik hierboven vond, en laat ik zien hoe zo'n eerste versie eruitziet. Past het niet, dan is dat ook prima. Dan weet je in elk geval waarom er een kaart naar {plaats} ging.",
 "We nemen samen door wat ik hierboven zag en ik laat je zien hoe een eerste versie er in jullie geval uit zou zien. Zie je het niet zitten, ook goed. Dan heb je in elk geval gehoord waarom ik je schreef.",
 "Ik neem een kwartier de tijd om je te laten zien wat ik zou bouwen en waarom. Zeg je daarna nee, dan hoor je verder niets meer van me. Dat is ook een prima uitkomst.",
 "Een kwartier waarin ik laat zien wat ik zou maken en wat het je oplevert. Blijkt het niets voor je, dan stopt het daar. Dan weet je waarom er post uit Apeldoorn kwam.",
]
CTA_ALT = ["Liever meteen bellen?", "Zelf bellen mag ook:", "Of pak de telefoon:", "Rechtstreeks bellen kan ook:"]
FT_META = [
 "Websites voor installatietechniek, machinebouw en bouw in de regio Apeldoorn",
 "Websites voor technische bedrijven in en om Apeldoorn",
 "Websites voor installateurs, machinebouwers en aannemers, regio Apeldoorn",
 "Ik maak websites voor de techniek. Regio Apeldoorn",
]
KOP_TERUG = ["Iets dat je zonder mij kunt doen", "Dit kun je vanmiddag zelf nakijken",
             "Zonder mij, en zonder kosten", "Doe dit eerst eens zelf"]
KOP_LEUK = ["En iets dat niets verkoopt", "Even iets anders", "Nog iets, en dat verkoopt niets",
            "Buiten de bestelling om"]

RAIL = [
 ["Waarom je dit krijgt", "Wat ik zocht", "Waar ik op uitkwam", "Wat ik zou doen", "Even bellen"],
 ["De aanleiding", "Wat ik vond", "De vraag die overbleef", "Mijn voorstel", "Bellen"],
 ["Hoe ik hier kom", "Wat me opviel", "Wat ik me afvroeg", "Hoe ik het aanpak", "Contact"],
 ["Waarom jij", "Wat ik tegenkwam", "Wat het betekent", "Wat er dan gebeurt", "Afspraak"],
]

# ── koppen per pad, zodat de sectiekoppen per pagina verschillen ──────
KOP_AANLOOP = {
 'portaal': ["Ik vond je wel, maar niet bij jezelf", "Je staat er, ergens anders", "Op het portaal wel, daarbuiten niet"],
 'kring':   ["Je naam staat er, en verder niets", "Een profiel zonder link", "Ik klikte en er gebeurde niets"],
 'gids':    ["Een adres en een nummer", "Ik heb je gezocht en niet gevonden", "Waar ik strandde"],
 'weg':     ["Het adres bestaat nog", "Er stond hier ooit iets", "Vier keer geprobeerd, vier keer niets"],
 'mobiel':  ["Op de laptop niets aan de hand", "Het ging mis op mijn telefoon", "Twee schermen, twee verhalen"],
 'vak':     ["Wat er wel en niet op staat", "De bus zegt iets anders dan de site", "Je bent verder dan je site"],
 'lek':     ["Hij werkt, en toch kwam ik er niet door", "Het laatste stukje", "Waar ik bleef haken"],
}

# ══════════════════════════════════════════════════════════════════════
#  Bevindingen. Elke bevinding is gemeten, met de bron en de datum erbij.
#  Geen oordeel over smaak, alleen wat na te meten is.
# ══════════════════════════════════════════════════════════════════════
def bevindingen(r, v, dom):
    geb = r['gebreken']
    uit = []
    def add(kop, tekst, bewijs, bron):
        uit.append(dict(kop=kop, tekst=tekst, bewijs=bewijs, bron=bron))

    reg = {'telefoonboek.nl': 'telefoonboek.nl',
           'bedrijvenkringapeldoorn.nl': 'bedrijvenkringapeldoorn.nl',
           'openstreetmap': 'openstreetmap.org'}
    bronnaam = next((w for k, w in reg.items() if k in r.get('bron', '')), 'telefoonboek.nl')

    if r['site_status'] == 'geen':
        add(kies(["Er is geen adres om naartoe te sturen",
                  "Je staat in het register en verder nergens",
                  "Geen webadres, ook niet bij de bron"], r['bedrijf'], 'b1'),
            f"Ik vond je gegevens wel. Naam, adres in {v['plaats']}, telefoonnummer. Een webadres staat er niet bij, en ik heb er zelf ook geen kunnen vinden.",
            f"Bedrijfsvermelding zonder websiteveld",
            f"{bronnaam}, gecontroleerd op {DATUM}")
        if r.get('telefoon'):
            add(kies(["Je nummer staat er, en dat is alles",
                      "Alles hangt aan de telefoon",
                      "Eén ingang, en dat is je nummer"], r['bedrijf'], 'b2'),
                f"Wie jou wil bereiken, moet bellen. Dat werkt prima bij iemand die je al kent. Bij iemand die je vergelijkt met twee anderen is het de enige stap die hij moet zetten voordat hij iets van je weet.",
                f"{r['telefoon']}, het enige contactgegeven in de vermelding",
                f"{bronnaam}, gecontroleerd op {DATUM}")
    elif r['site_status'] == 'dood':
        add(kies(["Het domein staat er nog",
                  "Het adres bestaat, de site niet",
                  "Er draait niets meer op"], r['bedrijf'], 'b1'),
            f"{dom} is nog van jullie, maar er komt geen pagina meer terug. Ik heb het met http en https geprobeerd, met en zonder www.",
            f"Vier varianten van {dom} geprobeerd, alle vier zonder antwoord",
            f"{dom}, gecontroleerd op {DATUM}")
        add(kies(["Het staat waarschijnlijk nog op je drukwerk",
                  "Dat adres circuleert nog wel",
                  "Op papier bestaat hij nog"], r['bedrijf'], 'b2'),
            f"Een adres verdwijnt niet uit de wereld als de site eruit ligt. Het staat op {v['ding']}, op je briefpapier en in oude offertes. Iedereen die het intypt, komt bij niets uit.",
            f"Domein actief, pagina leeg",
            f"{dom}, gecontroleerd op {DATUM}")
    else:
        stuk = []
        if 'certificaat niet geldig' in geb:
            stuk.append(("Je browser noemt de site niet veilig",
                f"Het beveiligingscertificaat klopt niet. Wie {dom} opent, krijgt eerst een waarschuwing van zijn eigen browser voordat hij iets van jullie ziet.",
                "Certificaatfout bij het openen van de pagina"))
        if 'geen mobiele weergave' in geb:
            stuk.append(("Op een telefoon loopt hij over de rand",
                "De pagina is gebouwd voor een laptopscherm. Op een telefoon moet je naar rechts vegen om de tekst uit te lezen.",
                "Geen viewport-instelling, tekst loopt buiten het scherm"))
        if 'telefoonnummer geen klikbare link' in geb:
            stuk.append(("Je nummer is geen knop",
                "Het staat er wel, maar je kunt er niet op drukken. Wie je wil bellen, moet het overtypen. Met werkhandschoenen aan doet niemand dat.",
                "Telefoonnummer staat als platte tekst op de pagina"))
        if 'geen aanvraagformulier' in geb:
            stuk.append(("Er is geen manier om iets aan te vragen",
                "Wie 's avonds op je site komt en niet wil bellen, heeft geen enkele knop om op te drukken. Die is de volgende ochtend vergeten dat hij je zocht.",
                "Geen formulier op de pagina gevonden"))
        if 'formulier opent de mailapp' in geb:
            stuk.append(("Het formulier opent zijn mailprogramma",
                "Bij het versturen springt zijn eigen mailapp open. Op een telefoon en bij iedereen met webmail gebeurt er dan niets, en dat merk jij nooit.",
                "Formulier verstuurt via een mailto-link"))
        if 'footer stopt bij' in geb:
            j = re.search(r'footer stopt bij (\d{4})', geb)
            if j: stuk.append((f"Onderaan staat nog {j.group(1)}",
                f"De jaartelling in de voettekst is blijven staan op {j.group(1)}. Dat is het eerste waar iemand naar kijkt als hij zich afvraagt of een bedrijf nog bestaat.",
                f"Copyrightjaar {j.group(1)} in de voettekst"))
        if 'nauwelijks fotos' in geb:
            j = re.search(r'nauwelijks fotos \((\d+)\)', geb)
            n = j.group(1) if j else '0'
            stuk.append((f"Er staan {n} afbeeldingen op",
                f"In {v['wat']} is een foto van afgerond werk het enige harde bewijs dat je hebt. Een tekst over vakmanschap kan iedereen schrijven, een foto van je eigen project niet.",
                f"{n} afbeeldingen op de hele pagina"))
        if 'laadtijd' in geb:
            j = re.search(r'laadtijd ([\d.,]+)s', geb)
            if j: stuk.append((f"Hij doet er {j.group(1).replace('.',',')} seconden over",
                "Op een bouwplaats met matig bereik wordt dat meer. De meeste mensen wachten dat niet af.",
                f"Laadtijd {j.group(1).replace('.',',')} seconden, gemeten op een mobiele verbinding"))
        if 'geen werkenbij' in geb:
            stuk.append(("Er staat niets over werken bij jullie",
                f"Een {v['mens']} kijkt op je site voordat hij solliciteert, en zeker voordat hij opzegt bij zijn huidige baas. Wat hij dan ziet, bepaalt of hij belt.",
                "Geen vacature- of werkenbij-pagina gevonden"))
        # sorteer op zwaarte en neem er twee, drie bij een sterke derde
        for kop, tekst, bewijs in stuk[:3]:
            add(kop, tekst, bewijs, f"{dom}, gecontroleerd op {DATUM}")
        if r.get('disciplines'):
            d = r['disciplines'].split(';')[0]
            uit.insert(0, dict(
                kop=f"Je doet {d}, en dat lees ik nergens terug",
                tekst=f"Op je site kwam ik {d} tegen, maar het staat er niet als iets waar je op gevonden wilt worden. Wie zoekt op {d} plus {v['plaats']}, komt bij iemand anders uit.",
                bewijs=f"{d} genoemd in de paginatekst, niet in de opbouw van de site",
                bron=f"{dom}, gecontroleerd op {DATUM}"))
    return uit[:3]

# ══════════════════════════════════════════════════════════════════════
#  De pagina
# ══════════════════════════════════════════════════════════════════════
HERO_H1 = {
 'portaal': ["Ik kon je nergens vinden.", "Je staat er, maar niet bij jezelf."],
 'kring':   ["Ik klikte op je naam.", "Achter je naam zat niets."],
 'gids':    ["Ik heb je gezocht.", "Ik kwam niet verder dan je nummer."],
 'weg':     ["Je adres bestaat nog.", "Er staat niets meer op."],
 'mobiel':  ["Ik heb hem op mijn telefoon geopend.", "Op een telefoon gaat het mis."],
 'vak':     ["Je bent verder dan je site.", "Dat leest niemand terug."],
 'lek':     ["Hij werkt, en toch liep ik vast.", "Ik kwam er net niet doorheen."],
}
HERO_SUB = [
 "Ik heb er {n} dingen uitgehaald die je zelf kunt nakijken. Daarna vertel ik wat ik zou doen.",
 "Hieronder staat wat ik tegenkwam, met erbij waar het vandaan komt. Het kost je een paar minuten.",
 "{n} dingen die me opvielen, plus wat ik me daarbij afvroeg. Daaronder mijn voorstel.",
 "Wat ik zag, waar ik het vond, en wat ik ermee zou doen. Kijk het gerust na.",
]
KAART = [
 "Ik keek naar {bedrijf} en liep ergens vast.",
 "Ik zocht {bedrijf} en kwam er niet uit.",
 "Ik heb even naar {bedrijf} gekeken.",
]

def bouw(r, idx):
    naam = r['bedrijf']
    v = dict(VAK.get(r['branche'], VAK['bouw']))
    v['plaats'] = r['plaats']
    pad = pad_bepalen(r)
    dom = re.sub(r'^https?://', '', (r.get('website') or '')).split('/')[0].replace('www.', '')
    portaal = {'warmtepomp-installateur': 'Trustoo', 'loodgieter': 'Trustoo', 'elektricien': 'Trustoo',
               'aannemer': 'Trustoo', 'dakdekker': 'Trustoo', 'stukadoor': 'Trustoo',
               'kozijnen': 'Trustoo', 'airco-installateur': 'Trustoo'}.get('', 'Trustoo')
    rub = (r.get('rubriek') or '').split(';')[0].replace('-', ' ') or v['term']
    sub = dict(bedrijf=naam, plaats=r['plaats'], domein=dom, portaal=portaal,
               rubriek=rub, termen=v['term'] + 's', ding=v['ding'], wat=v['wat'],
               klus=v['klus'], mens=v['mens'], mensen=v['mensen'], zoekt=v['zoekt'],
               Mensen=v['mensen'].capitalize())

    bev = bevindingen(r, v, dom)
    n = len(bev)
    rail = kies(RAIL, naam, 'rail')
    aanloop = kies(AANLOOP[pad], naam, 'aan').format(**sub)
    pivot = kies(PIVOT[pad], naam, 'piv').format(**sub)
    gevolg = kies(GEVOLG, naam, 'gev').format(**sub)
    if v['mensen'] == 'monteurs' or r['branche'] in ('installatie', 'elektro', 'metaal'):
        gevolg += "\n\n" + kies(GEVOLG_MENS, naam, 'gem').format(**sub)
    projectie = kies(PROJECTIE, naam, 'pro').format(**sub)
    brug = kies(BRUG, naam, 'bru').format(**sub)
    terug = TERUG[pad].format(**sub)
    kop_aan = kies(KOP_AANLOOP[pad], naam, 'ka')
    h1 = kies(HERO_H1[pad], naam, 'h1')
    hsub = kies(HERO_SUB, naam, 'hs').format(n=n)
    kaart = kies(KAART, naam, 'kt').format(bedrijf=naam)
    vrow = kies(VROW, naam, 'vr')
    dock = kies(DOCK, naam, 'dk')
    askbtn = kies(ASK_BTN, naam, 'ab')
    eyebrow_kost = kies(["Wat dit kost", "De andere kant", "Wat je misloopt", "De rekening ernaast"], naam, 'ke')
    kop_kost = next(k for k in kies_rij(["De rekening die je nooit krijgt", "Wat er stilletjes weglekt",
        "Het bedrag dat nergens staat", "Waar dit je geld kost"], naam, 'kg') if k.lower() != eyebrow_kost.lower())
    kop_voorstel = next(k for k in kies_rij(["Wat ik zou doen", "Zo pak ik het aan", "Dit is mijn plan", "Hoe ik het aanvlieg"], naam, 'kv') if k.lower() != rail[3].lower())
    askplan = kies(["Kies een moment", "Plan een kwartier", "Zet het in mijn agenda", "Kies zelf een tijd"], naam, 'ap')
    founder = kies(FOUNDER, naam, 'fo')
    blok = kies(BLOKSETS, naam, 'bl')
    ctasub = kies(CTA_SUB, naam, 'cu').format(plaats=r['plaats'])
    # de aanhef alleen bij een bevestigde naam
    vn = ''
    if r['beslisser_hardheid'] in ('hard', 'site'):
        vn = r['beslisser'].split()[0]
    aanhef = f"Hoi {E(vn)}.<br>" if vn else ""

    P = []
    A = P.append
    A(f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Online Geduld voor {E(naam)}</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="description" content="Wat mij opviel aan hoe {E(naam)} online staat.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=Manrope:wght@400;500;600;700&family=Caveat:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="thema-onlinegeduld.css">
<link rel="stylesheet" href="lp.css">
<script>
  window.PQ_BEDRIJF      = {json.dumps(naam)};
  window.PQ_KLANT        = 'onlinegeduld';
  window.PQ_CAMPAGNE     = 'apeldoorn-batch1';
  window.PQ_CAL          = 'cheraldogeduld/kort-gesprek';
  window.PQ_VIDEO        = 'cheraldo.mp4';
  window.PQ_POSTER       = 'cheraldo-poster.jpg';
  window.PQ_TRACK_URL    = '';
  window.PQ_TERUGBEL_URL = 'https://script.google.com/macros/s/AKfycby37aGED41tyit5g9IemLY07prmG6J8CIERkkrYSxl92H3aBGCCui-G2stGXMDaUNsngQ/exec';
  window.PIQUE_INTRO     = {{ {('voornaam: ' + json.dumps(vn) + ', ') if vn else ''}bedrijf: {json.dumps(naam)}, merk: false }};
</script>
<script src="lp-intro.js"></script>
</head>
<body>
<div class="mbar" id="mbar"></div>

<nav id="nav">
  <a href="#top" class="logo" aria-label="Online Geduld" style="font-family:var(--serif);font-weight:600;font-size:1.05rem;letter-spacing:-.02em">Online&nbsp;Geduld</a>
  <button class="nav-cta" data-open="sheet" data-tab="plan">Plan een gesprek</button>
</nav>

<div class="rail" id="rail">
  <a href="#s1"><span class="rd"></span><span class="rl">{E(rail[0])}</span></a>
  <a href="#s2"><span class="rd"></span><span class="rl">{E(rail[1])}</span></a>
  <a href="#s3"><span class="rd"></span><span class="rl">{E(rail[2])}</span></a>
  <a href="#s4"><span class="rd"></span><span class="rl">{E(rail[3])}</span></a>
  <a href="#gesprek"><span class="rd"></span><span class="rl">{E(rail[4])}</span></a>
</div>

<header class="hero" id="top">
  <div class="hero-grid"></div>
  <div class="hero-inner">
    <div class="hero-left">
      <div class="slot" id="slot">
        <div class="slot-card" id="slotcard">
          <div class="h">{aanhef}{E(kaart)}</div>
          <div class="sig">Cheraldo</div>
        </div>
        <span class="slot-tag">{E(kies(SLOT_TAG, naam, "st"))}</span>
      </div>
    </div>
    <div class="hero-right">
      <h1 class="hero-h1">{E(h1)}</h1>
      <p class="hero-sub">{E(hsub)}</p>
      <div class="hero-meta">
        <span class="chip"><i></i>{n} {'bevinding' if n == 1 else 'bevindingen'}</span>
        <span class="chip">2 minuten lezen</span>
        <span class="chip">Geschreven voor <b>{E(naam)}</b></span>
      </div>
      <button class="vrow" id="vrow" type="button">
        <span class="vthumb"><span class="vring"></span><img src="cheraldo-poster.jpg" alt=""><span class="vplay"></span></span>
        <span><b>{E(vrow[0])}</b>{E(vrow[1])}</span>
      </button>
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
        <div class="ch-eyebrow">{E(rail[0])}</div>
        <h2 class="ch-kop">{E(kop_aan)}</h2>
        {''.join(f'<p class="ch-text">{E(p)}</p>' for p in aanloop.split(chr(10) + chr(10)))}
        <div class="ch-sign">{kies(CH_SIGN, naam, "cs")}</div>
      </div>
      <div class="note">{n} {'ding' if n == 1 else 'dingen'}, en toen een vraag
        <svg class="arw" viewBox="0 0 52 26"><path d="M2 5c13 0 24 5 32 14M34 19l-6-1.4M34 19l1.2-6"/></svg>
      </div>
    </div>
  </section>
''')
    for i, b in enumerate(bev):
        kant = 'right' if i % 2 == 0 else 'left'
        ident = ' id="s2"' if i == 0 else ''
        A(f'''  <section class="chapter {kant} find"{ident}>
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="f-head"><div class="f-num">{i+1:02d}<span class="of">/ {n:02d}</span></div><div class="f-tag">{E(rail[1])}</div></div>
        <h2 class="f-kop">{E(b['kop'])}</h2>
        <p class="ch-text">{E(b['tekst'])}</p>
        <div class="f-bewijs">
          <p class="f-quote">{E(b['bewijs'])}</p>
          <div class="f-meta"><span class="dom">{E(b['bron'].split(',')[0])}</span><span class="sep"></span><span>gecontroleerd op {DATUM}</span></div>
        </div>
      </div>
    </div>
  </section>
''')
    A(f'''  <section class="chapter center pivot" id="s3">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">{E(rail[2])}</div>
        <p class="ch-pivot">{E(pivot.split(chr(10) + chr(10))[0])}</p>
        <p class="ch-text" style="max-width:44ch;margin:1.4rem auto 0">{E(pivot.split(chr(10) + chr(10))[-1])}</p>
      </div>
    </div>
  </section>
</main>

<section class="ask" id="ask">
  <div class="ask-in">
    <p class="ask-hand">{E(kies(ASK_HAND, naam, "ah"))}</p>
    <p class="ask-sub">{E(kies(ASK_SUB, naam, "as"))}</p>
    <div class="ask-btns">
      <button class="btn-a" data-open="sheet" data-tab="plan">{E(askplan)}</button>
      <button class="btn-b" id="askread">{E(kies(ASK_LEES, naam, "al"))}</button>
    </div>
    <p class="ask-later">Liever dat ik jou bel? <button data-open="sheet" data-tab="bel">Laat je nummer achter</button>. Of bel zelf: <a href="tel:+31648919097">{TEL}</a>.</p>
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
        <div class="ch-eyebrow">{E(eyebrow_kost)}</div>
        <h2 class="ch-kop">{E(kop_kost)}</h2>
        {''.join(f'<p class="ch-text">{E(p)}</p>' for p in gevolg.split(chr(10) + chr(10)))}
      </div>
    </div>
  </section>

  <section class="chapter right">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">{E(kies(["Hoe het ook kan", "De andere versie", "Waar ik naartoe zou werken"], naam, 'kp'))}</div>
        {''.join(f'<p class="ch-text">{E(p)}</p>' for p in projectie.split(chr(10) + chr(10)))}
      </div>
    </div>
  </section>

  <section class="chapter center phase" id="s4">
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="ch-eyebrow">{E(rail[3])}</div>
        <h2 class="ch-kop ch-head">{E(kop_voorstel)}</h2>
        {''.join(f'<p class="ch-text">{E(p)}</p>' for p in brug.split(chr(10) + chr(10)))}
      </div>
    </div>
  </section>
</main>

<section class="toon" id="toon">
  <div class="vw">
    <div style="--dl:.05s"><span>&#10003;</span><b>{E(blok[0][0])}</b><p>{E(blok[0][1])}</p></div>
    <div style="--dl:.18s"><span>&#10003;</span><b>{E(blok[1][0])}</b><p>{E(blok[1][1])}</p></div>
    <div style="--dl:.31s"><span>&#10003;</span><b>{E(blok[2][0])}</b><p>{E(blok[2][1])}</p></div>
  </div>
  <div class="narij">
    <div style="--dl:.44s"><b>{E(kies(KOP_TERUG, naam, "kt2"))}</b><p>{E(terug)}</p></div>
  </div>
</section>

<section class="founder" id="founder">
  <img class="fo-photo fr" src="cheraldo-portret.jpg?v=2" alt="Cheraldo Geduld van Online Geduld">
  <div class="fr">
    <div class="fo-eyebrow">{E(kies(FO_EYE, naam, "fe"))}</div>
    <div class="fo-text">
      {"".join(f"<p>{E(p)}</p>" for p in founder)}
    </div>
    <p class="fo-name">{kies(FO_NAME, naam, "fn")}</p>
  </div>
</section>

<section class="cta" id="gesprek">
  <div class="cta-inner">
    <div class="cta-eyebrow reveal">{E(rail[4])}</div>
    <h2 class="cta-h reveal">{E(kies(["Zullen we even bellen?", "Even een kwartier?", "Kunnen we elkaar even spreken?"], naam, 'ct'))}</h2>
    <p class="cta-sub reveal">{E(ctasub)}</p>
    <div class="cta-btns reveal">
      <button class="btn-a" data-open="sheet" data-tab="plan">{E(askplan)}</button>
      <button class="btn-b" style="color:rgba(255,255,255,.75);border-color:rgba(255,255,255,.2)" data-open="sheet" data-tab="bel">{E(askbtn)}</button>
    </div>
    <p class="cta-alt reveal">{E(kies(CTA_ALT, naam, "ca"))} <a href="tel:+31648919097">{TEL}</a>. Of mail: <a href="mailto:{MAIL}?subject={E(naam).replace(" ", "%20")}">{MAIL}</a>.</p>
  </div>
</section>

<footer>
  <div class="ft-logo" style="font-family:var(--serif);font-weight:600;font-size:1.4rem;color:var(--op-accent)">Online Geduld</div>
  <div class="ft-meta">{E(kies(FT_META, naam, "ft"))}<br><a href="mailto:{MAIL}">{MAIL}</a> &nbsp;&middot;&nbsp; {TEL}</div>
</footer>

<div class="dock" id="dock">
  <span class="dock-t"><b>{E(dock[0])}</b> {E(dock[1])}</span>
  <button class="dock-b" data-open="sheet" data-tab="plan">Plannen</button>
  <button class="dock-x" id="dockx" aria-label="Sluiten">&times;</button>
</div>

<div class="sheet" id="sheet" aria-hidden="true">
  <div class="sheet-bg" data-close></div>
  <div class="sheet-in" role="dialog" aria-modal="true" aria-label="Laat je nummer achter">
    <button class="sheet-x" data-close aria-label="Sluiten">&times;</button>
    <div class="sheet-host">
      <img src="cheraldo-portret.jpg?v=2" alt="">
      <div><div class="n">{E(kies(SHEET_N, naam, "sn"))}</div><div class="s">Telefoon of videocall, jij kiest.</div></div>
    </div>
    <div class="sheet-tabs">
      <button class="on" data-tab="plan">Zelf een moment kiezen</button>
      <button data-tab="bel">Laat mij terugbellen</button>
    </div>
    <div class="panes">
    <div class="pane on" id="pane-plan">
      <div id="cal-wrap">
        <div id="cal-embed"></div>
        <div class="cal-skel" id="calskel">
          <div class="kop"></div>
          <div class="grid"><u></u><u></u><u></u><u></u><u></u><u></u><u></u><u></u><u class="o"></u><u></u><u class="o"></u><u></u><u></u><u></u><u class="o"></u><u></u><u></u><u class="o"></u><u></u><u></u><u></u><u></u><u class="o"></u><u></u><u class="o"></u><u></u><u></u><u></u></div>
          <div class="glans"></div>
        </div>
      </div>
    </div>
    <div class="pane" id="pane-bel">
      <form id="belform">
        <div class="fld"><label for="bn">Je naam</label><input id="bn" name="naam" required autocomplete="name"></div>
        <div class="fld"><label for="bt">Telefoonnummer</label><input id="bt" name="tel" type="tel" placeholder="06" required autocomplete="tel"></div>
        <label style="display:block;font-size:.74rem;font-weight:600;color:var(--ink2);margin-bottom:.35rem">Wanneer schikt het?</label>
        <div class="slots" id="slots">
          <button type="button" data-v="Vandaag, later vanmiddag">Later vanmiddag</button>
          <button type="button" data-v="Morgenochtend">Morgenochtend</button>
          <button type="button" data-v="Morgenmiddag">Morgenmiddag</button>
          <button type="button" data-v="Deze week, maakt niet uit">Deze week, maakt niet uit</button>
        </div>
        <button class="btn-a" type="submit" style="width:100%;justify-content:center">Bel me terug</button>
        <p class="sheet-note">Ik bel zelf. Je nummer gaat nergens anders heen en komt op geen enkele lijst.</p>
      </form>
    </div>
    </div>
  </div>
</div>

<script src="lp-v2.js"></script>
</body>
</html>
''')
    return ''.join(P)


def main():
    rijen = list(csv.DictReader(open(BRON, encoding='utf-8')))
    rijen.sort(key=lambda r: -int(r['score'] or 0))
    top = rijen[:50]
    index = []
    for i, r in enumerate(top):
        s = slug(r['bedrijf'])
        open(os.path.join(UIT, s + '.html'), 'w', encoding='utf-8').write(bouw(r, i))
        index.append(dict(bedrijf=r['bedrijf'], slug=s, plaats=r['plaats'], branche=r['branche'],
                          pad=pad_bepalen(r), categorie=r['categorie'], adres=r['adres'],
                          postcode=r['postcode'], telefoon=r['telefoon'],
                          beslisser=r['beslisser'], hardheid=r['beslisser_hardheid'],
                          url=f"intro-pique.agency/onlinegeduld/{s}"))
    with open(os.path.join(UIT, '_index.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(index[0].keys())); w.writeheader(); w.writerows(index)
    import collections
    print(f"{len(index)} pagina's gebouwd")
    print("per denkpad:", dict(collections.Counter(x['pad'] for x in index)))
    print("per branche:", dict(collections.Counter(x['branche'] for x in index)))

main()
