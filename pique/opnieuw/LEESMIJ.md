# Heractivatie: mensen met wie al gesproken is

Batch oktober 2026. De selectie komt uit
`Leads/Heractivatie-Gesproken/Gesproken-Bedrijven-okt2026.csv`.

**Live staan er twee, op de v12-standaard** (12 oktober 2026):

- https://intro-pique.agency/pique/jr-finance (Jason Ramkisoen)
- https://intro-pique.agency/pique/studio-rendement (Tjerk Moraal)

Finovion is er op 12 oktober uitgehaald. De pagina's staan rechtstreeks in `pique/`,
zonder tussenmap in de URL. Deze map houdt alleen nog de bouwbestanden.

De tien andere prospects staan nog in `PROSPECTEN` en zijn met de keten hieronder terug
te maken. Let op: hun slug mag niet botsen met een bestaande pagina in `pique/`.
`finovion.html` bestaat daar al, van de franchisebatch.

## De verzendlijst

`Kaarten-JRFinance-StudioRendement.csv` is de enige lijst die klopt. Twee regels, met de
kaarttekst, het geverifieerde adres en de goede QR-link.

De kaarttekst belooft geen prijs meer, want die staat niet meer op de pagina. Een kaart
die iets belooft wat de pagina niet geeft, is erger dan een kaart zonder belofte.

`Kaarten-VERZENDKLAAR-VEROUDERD.csv` is de oude lijst van twaalf. **Druk daar niets uit.**
De links daarin wijzen naar `/pique/opnieuw/` en die adressen geven 404, en de
kaartteksten beloven de staffel.

## De bouwketen, drie stappen

    python3 bouw.py jrfinance studiorendement
    cd ../..                                      # naar Klanten/BCS
    python3 ../../Context/tools/lp-v12-omzetter.py pique/jr-finance.html --schrijf
    python3 ../../Context/tools/lp-v12-omzetter.py pique/studio-rendement.html --schrijf
    cd pique/opnieuw && python3 na-omzetten.py

**Stap twee moet vanuit `Klanten/BCS` draaien met een pad dat `pique/` bevat.** De
omzetter leidt zijn prefix af uit dat pad: `pique/x.html` geeft prefix leeg, een relatief
pad als `../x.html` geeft ten onrechte `../` en dan slaat hij de pagina over.

**Stap drie is niet optioneel.** De omzetter hangt een vast paneel in met de regel
'we hebben je nooit eerder gesproken', en dat is bij deze batch onwaar. `na-omzetten.py`
vervangt die zin per pagina door wanneer er wél gesproken is.

## Geen cases

Simon, 12 oktober 2026: er mogen geen cases in. Het kapittel met een klantverhaal en de
link naar `pique.agency/cases` is eruit, en de `CASES`-tabel in `bouw.py` ook. Wat ervoor
in de plaats staat is wat de aanpak meetbaar doet, zonder een andere klant te noemen: 98
procent op het bureau, 64,5 scans per honderd kaarten, 9,5 procent van de scanners plant
een gesprek, over ruim tienduizend benaderingen, met cold email onder de 1 procent als
ijkpunt, peildatum 19 september 2026. De voetnoot over aanbod, lijst en opvolging hoort
daarbij en staat erin. Het geheugen houdt die cijfers bij onder reference-pique-huiscijfers.

**Let op de logorij in de donkere band.** Die komt uit het vaste v12-blok en noemt Taco
Mundo, Van Dorp, TSNed, Drukwerkdeal, OTTO Work Force, Fortune Coffee en Wonder Group
onder de kop 'Vertrouwd door o.a.'. Een deel daarvan is prospect en geen klant, en
Drukwerkdeal en OTTO staan zelfs op deze heractivatielijst. Die rij staat er nog. Wil
Simon echt niets wat naar andere partijen verwijst, dan moet die er ook uit.

## Wat deze pagina's anders doen dan een koude v12

1. **De aanloop is een bekentenis.** Wat er verstuurd is, wat zij deden, en wat er daarna
   van onze kant uitbleef.
2. **De maquettekaart is naamloos.** odido-v12 zet de naam van de ontvanger op die kaart
   terwijl de bijschriften eronder over 'zijn bureau' gaan. tellscan vangt dat terecht als
   derde persoon. Hier staat 'Hoi Jan' op de kaart, ondertekend door het bedrijf van de
   ontvanger.

De vaste hero-kop, de vaste kop van het eerste hoofdstuk en het vaste founderblok zijn
overgenomen zoals de v12-standaard ze voorschrijft. De uitzondering van 6 oktober, waarbij
het voorstelblok wegviel bij mensen die Simon persoonlijk kent, is daarmee vervallen.

tellscan geeft per pagina één treffer, op die vaste hero-kop. Dat is de bekende en
toegestane treffer uit CLAUDE.md.

## Geen prijs meer op de pagina

Simon, 12 oktober 2026: de sectie 'Wat het kost' mag eraf. De staffel is uit `bouw.py`
gehaald, net als de railverwijzing, de tabelstijl en alle copy die ernaar wees. De prijs
is weer een gespreksonderwerp. Op beide pagina's staat nu dat het aantal benaderingen het
bedrag bepaalt en dat Simon het in het gesprek voorrekent.

De staffel zelf staat in het geheugen onder `reference-staffel-okt2026`.

## Twee video's, elk op zijn plek

`PQ_VIDEO` en `PQ_POSTER` moeten in de paginaconfig staan. Zonder die twee zet
`lp-intro.js` `heeftVideo` op false, en dan doet de knop 'Ja, laat maar zien' in de
introlaag niets: hij sluit de laag en toont geen video. Dat was op 12 oktober de klacht,
en het kwam doordat ik die regels op 6 oktober had weggehaald toen de videoknop uit de
hero ging.

- **introlaag**: `simon-staand.mp4` met `simon-staand-poster.jpg`, staand, opent in een
  overlay. Zo doet odido-v12 het ook.
- **donkere band**: de VSL van 1:01, liggend. `lp12.js` laadt `vsl-720-zacht.mp4` met een
  pad zonder prefix, dus die pagina moet naast dat bestand staan. Dat is nog een reden
  waarom de pagina's rechtstreeks in `pique/` horen.

## Bouwen

    python3 bouw.py                 # alle twaalf
    python3 bouw.py audion unica    # alleen die

De vorm komt uit `Componenten/lp-v2/_voorbeeld.html` en wordt daar letterlijk uitgeknipt
(nav, footer, boeksheet), dus een wijziging aan het component komt hier vanzelf mee. De
inhoud staat per prospect in `PROSPECTEN`, de cases in `CASES`.

## De gedeelde woordmassa, en waarom hij boven het plafond staat

`tellscan` meet 44,8 procent gedeelde tekst over deze twaalf, tegen een plafond van 25.
Ter vergelijking: de live batches `pique/food-agri` en `pique/bedrijfswagens` zitten op
76,7 en 76,4 procent.

Wat er na het snijden overblijft is meubilair en commerciële voorwaarden: de boekmodal,
Simons bio, de prijstabel, de drie voorwaarden en de sectiekoppen. Die horen identiek te
zijn. De hero, de aanloop, beide bevindingen, het kantelpunt, de tijdlijn en de case zijn
wel per prospect geschreven.

De regel is gemaakt voor koude batches waar ontvangers elkaar kennen, zoals
franchisenemers of bedrijven in hetzelfde pand. Deze twaalf zitten in twaalf
verschillende sectoren en kennen elkaar niet. Dat is de afweging. **Dit is een besluit
van Simon en geen vrijbrief voor volgende batches.**

## Voor verzending

1. `python3 Context/tools/tellscan.py Klanten/BCS/pique/opnieuw/` moet schoon zijn op de
   pagina's.
2. `python3 Context/tools/ailint.py <pagina>` nalopen. Treffers zijn vragen.
3. Committen en pushen, daarna `vercel --prod --yes --archive=tgz` vanuit `Klanten/BCS/`.
   De regel `!pique/opnieuw/*.mp4` staat al in `.vercelignore`, anders geeft de video 404
   terwijl de rest gewoon laadt.
4. `./verify-live.sh pique` draaien, en daarna `vsl.mp4` en `vsl-poster.jpg` apart
   controleren.
5. Adressen opnieuw verifiëren. Die in de CSV komen uit augustus 2026.

## Drie ontvangers kent Simon persoonlijk

Daniel Medina Diaz (Nederburgh), Tjerk Moraal (Studio Rendement) en Jason Ramkisoen
(JR Finance). Bij die drie staat `kent_hem: True` in `PROSPECTEN` en **vervalt het blok
waarin Simon zichzelf voorstelt**. Jezelf voorstellen aan iemand die je kent leest als een
standaardpagina, en daarvoor is deze batch nu juist gemaakt. De handtekening blijft
staan, want die hoort bij de kaart.

Zet die vlag ook bij elke volgende prospect die Simon al kent.

## Open punten

Alle twaalf adressen staan in de verzendlijst en zijn bevestigd in de BAG
(`Context/tools/bagcheck.py`, 6 okt 2026). Twee dingen verdienen nog aandacht:

- **Acendae staat op een registeradres.** `acendae.com` publiceert nergens een adres en de
  site zegt dat ze op afstand werken. Papegaaistraat 14, 4461 AD Goes komt uit northdata
  (KvK 99801620). Dat kan het adres van hun accountant zijn, en dat is de val uit
  [[feedback-adres-bag-is-niet-genoeg]]. Bevestigen bij Pramuka.
- **Nederburgh loopt ook via Mustafa**, vanuit Online Goed Gevonden. Stem af voor er een
  kaart heen gaat.

De zeven uit groep D staan op adressen die in augustus geverifieerd zijn en nu opnieuw door
de BAG kwamen. De BAG zegt alleen dat het adres bestaat, dus toets voor de drukopdracht nog
of het bedrijf er zit (`Context/tools/adrescontrole.py`).

Hard uit primaire bron: Finovion (eigen servicekantoorpagina), JR Finance (eigen algemene
voorwaarden, Ramki Consulting B.V., KvK 97892114), Studio Rendement (eigen
privacyverklaring) en Nederburgh (bezoekadres op hun site, bevestigd door Simon).
