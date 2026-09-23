# BCS Batch 4 - Fase 4, Research

Datum: 17 augustus 2026
Klant: Backbone Customer Service (Jeffrey)
Bereik: 84 prospects, waarvan 83 verzendklaar. De 63 die na Fase B doorgingen, plus 22 aanvullingen, min Dstrezzed en met Veloretti geparkeerd.

## Eerst een correctie

In de eindstand van Fase B stond dat er 73 prospects doorgaan. Na natellen zijn het er 63. Er vallen 29 namen hard af en 8 staan geparkeerd tot één vraag beantwoord is. De eindstand is aangepast.

## Wat deze fase moest opleveren

De researchstandaard vraagt om een handeling of uitspraak van een mens, met een letterlijk citaat, een werkende bron, een datum en een controledatum. Ik heb die route eerst gelopen en daarna de verplichte controle gedraaid.

### De uitkomst van die controle

Ik legde negen kandidaat-triggers voor aan `triggercheck.py`. Uitslag: één goed, nul handcheck, acht afkeur.

| Prospect | Uitslag | Reden |
|---|---|---|
| Sapph | goed | bron van 10 juni 2026 |
| Summum Woman | afkeur | bron is 784 dagen oud |
| Studio Ins & Outs | afkeur | geen handeling van een mens, bron 495 dagen oud |
| LaDress | afkeur | bron is 1.211 dagen oud |
| Somnox | afkeur | bron is 1.263 dagen oud |
| Colourful Rebel | afkeur | bron is 2.105 dagen oud |
| Aaiko | afkeur | bron is 2.223 dagen oud |
| Podobrace | afkeur | bron is 2.512 dagen oud |
| Seepje | afkeur | citaat staat in de kop, spreker niet toe te wijzen, artikel achter betaalmuur |

Daarnaast heb ik de vindplaatsen-route gedraaid met `vindplaatsharvest.py` over acht vakmedia. Resultaat: 31 nieuwe regels in het register, nul matches op de pool.

Dat is een hard maar bruikbaar antwoord. **Deze doelgroep praat niet publiek.** Nederlandse D2C-merken van 3 tot 20 miljoen hebben zelden een oprichter die met datum en al iets op de plaat zet. Het handjevol citaten dat bestaat, is jaren oud. Een verlopen citaat is volgens de standaard de gevaarlijkste observatie die er is, dus die gaan er allemaal uit.

## De route die hier wel werkt

Op 16 augustus is aan het deepdive-document een uitzondering toegevoegd: gaat de propositie van de klant precies over wat je meet, dan mag de bevinding zelf de opening zijn. Dat is bij ConverSEO zo met vindbaarheid, en het is bij BCS zo met klantcontact.

Ik meet bereikbaarheid en afhandeling van klantcontact. Dat is exact wat BCS verkoopt. De uitzondering geldt hier dus onverkort, met de twee voorwaarden die hard blijven:

1. **Het is een mechanisme en nooit een verwijt.** Wij schrijven niet dat hun klantenservice slecht is. Wij beschrijven hoe het werkt: een desk die om half vijf sluit vangt de avond niet op, want dan bestellen consumenten.
2. **Het feit staat, de gok is een vraag.** Nooit een diagnose van hun bedrijf.

En de tweede helft van het gesprek is de rekensom, en niet het gebrek. Wat het nu kost dat een vraag die telefonisch twee minuten duurt, per mail drie dagen kost.

## Wat ik heb gemeten

Alle 63 zijn machinaal langs de klantenservice-, contact-, retour- en FAQ-pagina's van hun eigen site gehaald, plus de signaalscan voor teampagina's, vacatures en LinkedIn.

| Bevinding | Aantal van de 63 |
|---|---|
| Geen telefoonnummer op de klantenservicepagina | 42 |
| Toegezegde reactietijd in uren of enkele werkdagen | 16 |
| Zes of meer taal- en marktvarianten | 14 |
| Smalle openingstijden, vierdaags of eindigend voor 17:00 | 9 |
| Teampagina gevonden | 26 |
| Vacaturepagina gevonden | 16 |
| Kandidaat-namen uit de teampagina | 6 |

Van de 63 hebben er 58 minstens één bevinding die machinaal door de poorten komt. Voor de overige vijf plus drie uit de aanvulling heb ik de bevinding met de hand geschreven op basis van reviews en nieuws, omdat de automaat daar iets miste dat er wel is. Denk aan Printenbind, dat tot 21:30 open is en dus buiten mijn regel voor smalle openingstijden viel terwijl de lange avond juist het punt is.

## De aanvulling naar 85

Je vroeg om minimaal 75 brieven. Na Fase B stonden er 63, dus ik heb er 22 bij gezocht.

Ik heb daarbij de les uit Fase B meteen als eerste filter gebruikt: eigen reviewaanwezigheid. Van 107 nieuw gescande domeinen bleven er 22 over die eigen merk of eigen dienst zijn, een reviewplatform of CS-tool draaien, en niet eerder benaderd zijn.

De opbrengst zat vooral in twee niches die in de eerdere rondes onderbelicht bleven: personalisatie en maatwerk. Bij allebei ontstaat het meeste klantcontact ná de bestelling, want dan pas blijkt of de gravure klopt of de maat past.

De sterkste aanvullingen:

| Prospect | Waarom |
|---|---|
| Namens Mij | Belooft 24 uur, en is bereikbaar op maandag, dinsdag en donderdag van 09:00 tot 14:30 |
| Tuinmaximaal | 300.000 orders geleverd, desk tot 21:00, en klanten melden dat ze na aankoop moeilijk te bereiken zijn |
| MaakjeCadeau | Servicedesk van 09:00 tot 21:00 met een belofte van één werkdag |
| Or Coffee | Belgische branderij die na 23 jaar is overgedragen, Wouter Helsen is de nieuwe man, Gorgias draait al |
| Metis Supplements | Belgisch, 368 reviews, en klanten melden dat de servicedesk achterloopt met opvolging |
| Foto op Hout | Zendesk, WhatsApp en een belofte van 24 uur, zonder telefoonnummer |
| PersonalSurprise | Helpscout, vijf markten, belofte van 24 uur |
| Tafels op maat | Maatwerkmeubels, bereikbaar tot half vijf, contact via WhatsApp zonder telefoonnummer |
| Little Thingz | Belgisch, 3.000 artikelen in de feed, geen telefoonnummer |
| Confirm Clothing | Shopify met Judge.me, desk van 09:00 tot 17:00 zonder telefoonlijn |

Eerlijk over de onderkant van die 22: een deel is kleiner dan de kern van de lijst. Ze komen door de poorten en ze passen op het ICP, maar ze zijn geen vervanging voor namen als Flinndal of PLNTS. Zet ze in de tweede helft van de verzending.

**Eén ding dat ik onderweg heb weggegooid.** Mijn eerste generator las "binnen 14 dagen" op servicepagina's als toegezegde reactietijd. Dat is bijna altijd de retourtermijn. Zo'n zin zou de prospect terecht betwisten, dus die claims zijn eruit gehaald. Dat kostte Summum Woman en vijf anderen hun sterkste zin, en dat is de goede uitkomst.


## Verwerkt na jouw doorloop, 17 augustus 2026

**Dstrezzed is eruit.** Zij hebben hun klantcontact vorig jaar uitbesteed aan een partij binnen Aquila Imperium waar jij contact mee hebt. Staat met die reden in `BCS-Batch4-FaseA-Uitgesloten.csv`, zodat hij ook bij een volgende batch niet terugkomt.

**Matt Sleeps is herschreven, en dit is nu het sterkste dossier van de lijst.** Jouw signaal klopte en het is harder dan alles wat ik zelf had gevonden. Ze draaien Recruitee, dus de actuele stand is op te vragen:

- Senior Customer Support Agent, geplaatst 23 juli 2026, staat vandaag nog open
- Customer Service Medewerker, geplaatst 6 juli 2026, staat vandaag nog open

Uit hun eigen vacaturetekst, letterlijk: "Matt Sleeps zoekt een senior customer support agent die onze customer support afdeling in de volgende groeifase ondersteunt." En: "Het Matt team bestaat uit 15 enthousiaste en ondernemende droom-najagers."

Wat er in die seniorrol moet gebeuren zegt de rest: inbox management en werkverdeling bewaken, reviews op Trustpilot, Google en de eigen site binnen korte doorlooptijden afhandelen, en structurele problemen signaleren. Dat is de functieomschrijving van een desk die vol zit.

Over jouw punt van de AI-tooling: in dezelfde vacature staat "Je bent bekend met AI tooling op klantenservice systemen en kunt ondersteunen om deze te verbeteren." Dat bevestigt dat ze er al mee werken. De naam van het pakket staat er niet bij en ik vond hem ook niet in hun broncode, dus die neem ik over als jouw waarneming en laat ik verifiëren voordat hij in tekst komt.

Deze drie triggers zijn door `triggercheck.py` gehaald en staan alle drie op goed. Daarmee is Matt Sleeps na Sapph de tweede prospect met een trigger die de volledige researchstandaard haalt, in plaats van alleen een bevinding.

**Dezelfde sweep over de hele lijst.** Jouw tip bleek een route, dus ik heb alle 84 langs de vacature-API's gehaald. Dat leverde nog twee treffers op:

- Veloretti, Customer Care Agent 32 tot 40 uur, geplaatst 6 juli 2026
- Printenbind, Print Support en Klantenservicemedewerker, al open sinds 28 maart 2024

Die van Printenbind staat er dus al bijna tweeënhalf jaar. Dat is een structureel gat in plaats van een momentopname, en het past bij een desk die tot half tien open is.

**Veloretti gaat wel op geparkeerd.** In zijn eigen vacaturetekst staat: "Sinds 2022 horen we bij Pon.Bike." Dat is dezelfde situatie als Homey onder LG, dus de vraag is of het merk zijn leveranciers nog zelf kiest. Dat moet eerst helder zijn.

De sweep raakte maar drie ATS-systemen met een gokje op de bedrijfsnaam, dus hij is verre van volledig. Voor batch 5 zou ik dit als vaste stap opnemen, want een openstaande klantcontactvacature is voor BCS het scherpste signaal dat er bestaat en het is machinaal en gedateerd op te halen.

**Let op bij het schrijven.** Een vacature alleen is volgens jullie eigen standaard verboden als opening, want elke SDR kijkt daar als eerste. De opening blijft dus het mechanisme en hun eigen zin. De vacature is het bewijs eronder en de reden dat het nú moet.

Stand: 84 dossiers, 82 op bevinding, 1 op volledige trigger, 1 geparkeerd. Dat is 83 verzendklaar.

## De werkset koopmomenten

De standaard vraagt om koppeling aan een koopmoment van de klant. Voor BCS liggen die niet vastgelegd, dus ik heb ze afgeleid uit het ICP-document. **Deze vijf moeten met Jeffrey bevestigd worden voordat er tekst op gebaseerd wordt.**

1. Het volume groeit sneller dan de bezetting
2. De bereikbaarheid is smaller dan wat de klant verwacht
3. Er komt een merk, land of kanaal bij
4. Er wisselt iets in eigendom of leiding en alles wordt opnieuw ingericht
5. Het team is klein en klantcontact wordt erbij gedaan

Verdeling over de 85: bereikbaarheid 49, uitbreiding 18, volume 18.

## De twaalf sterkste dossiers

Hieronder de dossiers waar bevinding, mechanisme en aanleiding elkaar versterken. De volledige 63 staan in `BCS-Batch4-Research-Dossiers.csv`.

### Sapph

**Trigger, door de controle:** Erik van der Maat is sinds mei 2026 CEO, onder eigenaar Shawn Harris die het merk in maart 2026 overnam. Textilia schreef er op 10 juni 2026 over. Het managementteam staat er met naam bij: Lara Guerrini op business, Charlotte Bienen op merchandise, Tristan Knights op online kanalen en Danielle van Dijk-Boersma op merkbeleid.
**Bevinding:** klanten die in juli 2024 bestelden, wachtten volgens Radar eind juni 2025 nog op levering en terugbetaling.
**Mechanisme:** een nieuw team erft de mailbox van het oude, inclusief alles wat daar nog open in staat.
**Vraag:** ik was benieuwd hoeveel van die oude gevallen nog bij het nieuwe team op tafel liggen.
**Koopmoment:** eigendom en leiding gewisseld.
**Bron:** textilia.nl, 10 juni 2026, gecontroleerd 17 augustus 2026.

### Catwalk Junkie

**Bevinding:** op de klantenservicepagina staat geen telefoonnummer, het contact loopt via een formulier. Op diezelfde pagina staat een toegezegde reactietijd van 24 uur. De site voert 40 taal- en marktvarianten en de feed telt 613 artikelen.
**Mechanisme:** een belofte van 24 uur wordt per binnenkomend bericht gemeten, en zonder telefoonlijn komt elke twijfel als bericht binnen.
**Vraag:** ik was benieuwd hoe vaak die 24 uur in de weken na een drop nog gehaald wordt.
**Koopmoment:** bereikbaarheid smaller dan de verwachting.
**Bron:** klantenservicepagina catwalkjunkie.com, gecontroleerd 17 augustus 2026.

### Wolplein

**Bevinding:** de klantenservice is volgens klanten alleen 's ochtends bereikbaar, bij een organisatie van 55 medewerkers en meer dan 3.000 artikelen in de feed.
**Mechanisme:** haken en breien is een hobby met veel vragen, en die vragen ontstaan aan de keukentafel in de middag en de avond.
**Vraag:** ik was benieuwd waar de middagvragen nu landen.
**Koopmoment:** bereikbaarheid smaller dan de verwachting.
**Aanleiding:** zoon Koen heeft de dagelijkse leiding overgenomen van zijn moeder Petra Glimmerveen.

### Flinndal

**Bevinding:** bereikbaar op werkdagen van 09:00 tot 17:00 en op zaterdag van 10:00 tot 16:00, via een gratis 0800-nummer, met een retourtermijn van 100 dagen plus 14 dagen om terug te sturen. Meer dan 22.000 Trustpilot-reviews.
**Mechanisme:** zaterdagbereikbaarheid en een gratis servicenummer zijn allebei kostenposten die iemand bewust heeft goedgekeurd, dus het volume rechtvaardigt ze al.
**Vraag:** ik was benieuwd wat een ticket jullie op dit moment kost.
**Koopmoment:** volume groeit sneller dan de bezetting.

### PLNTS

**Bevinding:** 22.463 Trustpilot-reviews. Contact loopt via chat, formulier, WhatsApp en social media. Klanten melden beschadigde planten in te kleine dozen en lange reactietijden.
**Mechanisme:** levende planten per post beschadigen onderweg, en elke beschadiging is een bericht plus een vervanging in plaats van alleen een bericht.
**Vraag:** ik was benieuwd hoeveel van de berichten over schade gaan.
**Koopmoment:** volume groeit sneller dan de bezetting.

### Printenbind

**Bevinding:** bereikbaar maandag tot en met donderdag van 08:00 tot 21:30, met duizenden orders per dag en meer dan 9.500 Trustpilot-reviews op vijf sterren.
**Mechanisme:** ze houden de desk al tot half tien open, dus het volume loopt aantoonbaar buiten kantooruren door.
**Vraag:** ik was benieuwd wie die avonden nu draait.
**Koopmoment:** volume groeit sneller dan de bezetting.
**Aanleiding:** oprichter Bart van Diepen investeerde met Ricoh in een nieuw pand en een nieuw machinepark.

### Matt Sleeps

**Bevinding:** 120 dagen gratis thuis proefslapen, bereikbaar maandag tot en met vrijdag van 10:00 tot 17:00, met ruim 5.300 Trustpilot-reviews.
**Mechanisme:** een proefperiode van vier maanden houdt elke klant vier maanden lang in het contactkanaal, want de twijfel komt pas in week zes.
**Vraag:** ik was benieuwd hoeveel gesprekken er per proefslaper bij komen kijken.
**Koopmoment:** volume groeit sneller dan de bezetting.

### Veloretti

**Bevinding:** geen telefoonnummer op de site, Trustpilot loopt door tot 174 pagina's, met klachten over lange wachttijden op reparatie en over montage-instructies die te summier zijn.
**Mechanisme:** een fiets die beschadigd of onvolledig aankomt kan de klant niet zelf oplossen, dus elke melding wordt een reeks berichten in plaats van één.
**Vraag:** ik was benieuwd hoeveel berichten er gemiddeld over één beschadigde levering gaan.
**Koopmoment:** bereikbaarheid smaller dan de verwachting.

### Cosmeau

**Bevinding:** bereikbaar maandag tot en met vrijdag van 10:00 tot 17:00, zonder telefoonnummer, met 1.843 zichtbare reviews en meer dan 200.000 huishoudens.
**Mechanisme:** in hun eigen verhaal bij Rabobank staat dat ze het interne team klein houden om scherp in prijs te blijven tegenover huismerken van supermarkten. Klantcontact is het onderdeel dat als eerste knelt zodra je die twee tegelijk wilt.
**Vraag:** ik was benieuwd hoe jullie dat team klein houden nu er een eigen winkel en eigen productie bij zijn gekomen.
**Koopmoment:** team is klein en klantcontact wordt erbij gedaan.

### Grutto

**Bevinding:** klanten melden dat mails onbeantwoord blijven en dat het bedrijf telefonisch niet bereikbaar is wanneer een pakket niet geleverd wordt. Actief in vier landen.
**Mechanisme:** vers vlees met een leverafspraak kent geen uitstel, dus een gemiste levering is dezelfde dag urgent en niet volgende week.
**Vraag:** ik was benieuwd wat er nu gebeurt met een melding die na vijf uur binnenkomt.
**Koopmoment:** bereikbaarheid smaller dan de verwachting.

### Purewhite

**Bevinding:** geen telefoonnummer op de site, en klanten melden dat mails en telefoontjes onbeantwoord blijven. Het merk wordt binnenkort hernoemd naar PUREPATH.
**Mechanisme:** een naamswijziging levert per definitie een golf vragen op, want elke klant wil weten wat er met zijn bestelling, garantie en account gebeurt.
**Vraag:** ik was benieuwd of jullie al hebben ingeschat hoeveel extra vragen de naamswijziging oplevert.
**Koopmoment:** er komt een merk, land of kanaal bij.

### Podobrace

**Bevinding:** reactiebelofte van 24 uur, met telefoon en WhatsApp open, 1.051 Trustpilot-reviews en een gewonnen prijs voor beste service.
**Mechanisme:** de omzet is vertienvoudigd via platforms naast de eigen webshop, en er kwam met de overname van DUTCC een tweede consumentenwebshop bij. Elk extra kanaal heeft zijn eigen berichtenstroom met eigen regels.
**Vraag:** ik was benieuwd hoeveel kanalen er nu langs dezelfde mensen lopen.
**Koopmoment:** er komt een merk, land of kanaal bij.

## Wat dit betekent voor de volgende stap

De bevindingen zijn hard, geverifieerd op datum, en ze gaan precies over wat BCS verkoopt. Dat is genoeg om mee te bouwen.

Wat ontbreekt is de laag eronder: de zin die de ondernemer zelf heeft gezegd. Die is voor deze doelgroep alleen te halen met een ingelogde LinkedIn-ronde, en dat is volgens het signaaldiepte-document handwerk dat je gericht inzet op twintig namen, niet in de breedte. Mijn advies is die ronde te doen op de kopgroep en de rest op de bevinding te laten draaien.

## Wat er nog moet gebeuren

1. De vijf koopmomenten met Jeffrey bevestigen of bijstellen.
2. Ingelogde LinkedIn-ronde op de kopgroep van veertien, voor de persoonlijke laag.
3. Beslissers dichtzetten voor de 41 die nog open staan. De signaalscan leverde zes kandidaat-namen die eerst geverifieerd moeten worden: onder andere Julian Jagtenberg bij Somnox, Thomas Krol bij Xsensible en Hans Peters bij Quotrell. Let op: bij LaDress kwam Esther van Bezooijen als CEO naar boven terwijl Simone van Trojen als oprichter bekend staat, dus daar klopt iets nog niet.
4. Adres per prospect via twee bronnen bevestigen.
5. Daarna Fase 5, humanization.

## Bestanden

| Bestand | Inhoud |
|---|---|
| `BCS-Batch4-Research-Dossiers.csv` | 85 dossiers met bevinding, mechanisme, vraag, koopmoment en bronregel |
| `BCS-Batch4-Research-Triggercheck.csv` | uitslag van de verplichte controle op de negen kandidaat-triggers |
| `BCS-Batch4-Signaalscan.csv` | teampagina's, vacatures, LinkedIn, kandidaat-namen en platform per prospect |
| `BCS-Batch4-Researchpool.csv` | de 85 prospects die de deur uit kunnen |
