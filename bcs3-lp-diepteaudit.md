# Diepteaudit BCS3 landingspagina's

Basis: `Klanten/BCS/bcs3/*.html` (290 pagina's, één template). Referentiecase: `aardig-wijntje.html`. Gecontroleerd tegen `belle-flora.html`, `beesha.html`, `bamboozy.html` — structuur is 100% identiek, alleen de tekstinhoud van akt 1 en 2 verschilt.

Toetssteen: vier-akten-model, Pique-positionering (rustig, exclusief, intelligent, high-ticket).

---

## Executive Summary

Dit is een pagina met een uitstekend skelet en een verkeerd gewichtsverdeling. De journey-lijn, het kleurpalet en de rust zijn beter dan 90% van wat B2B-Nederland maakt. Maar de pagina voert zijn eigen model niet uit: het vier-akten-model schrijft voor dat akt 2 (de spanning) het hoofddeel is met ~40% van het gewicht. In de praktijk is akt 1 ongeveer de helft van de pagina en akt 2 twee blokken lang, waarvan één blok één zin.

Het gevolg: de pagina bouwt tien schermen lang zorgvuldig op naar een moment dat er niet is. En op het punt waar de bezoeker beslist — de brug — schakelt de pagina over op twee generieke blokken die op alle 290 pagina's woord voor woord identiek zijn.

Daarnaast zitten er drie fouten in die de premium-claim actief ondermijnen: een videoframe zonder posterframe (een zwart vlak met browser-controls als eerste indruk), een videolabel dat persoonlijke opname claimt terwijl alle 290 pagina's hetzelfde `video.mp4` delen, en een Cal.com-iframe dat aan het einde de hele visuele taal doorbreekt.

**Belangrijkste sterke punten**

1. De journey-lijn met scroll-gekoppelde amber-progressie. Dit is echte craft, geen effect. Het maakt van losse blokken één beweging en het is het enige element op de pagina dat Linear/Stripe-niveau haalt.
2. Het kleurpalet. Navy `#0E1526`, amber `#C6893C`, warm off-white `#FBFAF8`. Volwassen, niet-SaaS, niet-agency. Dit hoeft niet aangepast.
3. De bronvermeldingen onder elke bevinding. Dit is het hele bewijs dat er werk in zit. Het is het meest onderscheidende element van de pagina.
4. De toon van de copy. Rustig, niet-verkoperig, geen superlatieven. Consistent met de positionering.
5. `noindex,nofollow` plus "Vertrouwelijk" in de topbar. Exclusiviteitssignaal dat klopt.

**Grootste zwakke punten**

1. Akt 2 is ondergewicht. De emotionele piek van de pagina is één tekstwand in een kolom van 400px.
2. De bevindingen verklappen de pivot. Bevinding 03 is letterlijk de pivot, vetgedrukt, drie blokken voordat de pivot komt.
3. De brug is boilerplate. Twee blokken, identiek op alle 290 pagina's, precies op het beslismoment.
4. Nul kwantificering in akt 2. Geen bedrag, geen percentage, geen aantal. Verliesaversie zonder getal is sfeer.
5. Video zonder posterframe. De eerste indruk is een zwart rechthoek.
6. Eén CTA, helemaal onderaan, als een 560px iframe van een ander merk.
7. Geen risico-omkering. Geen garantie, geen exit, geen "eerste maand", geen enkele klantnaam.
8. De H1 staat ónder de video en valt daardoor bij de meeste bezoekers onder de vouw.

**Scores**

| Dimensie | Score | Toelichting |
|---|---|---|
| Conversie | 5/10 | Eén CTA, geen risico-omkering, geen micro-commitment, zwakke brug |
| Premium-uitstraling | 7/10 | Palet en rust zijn sterk; video-frame en Cal-embed trekken het omlaag |
| Storytelling | 6/10 | Goed model, verkeerd uitgevoerd; spanning wordt weggegeven vóór de pivot |
| Psychologie | 4/10 | Nieuwsgierigheid en commitment werken; authority, social proof, verliesaversie, schaarste ontbreken of zijn onbenut |
| Motion Design | 5/10 | Eén excellent idee (journey-lijn), verder één generieke fade herhaald op alles |

**Verwachte impact van verbeteringen**

De top-10 van dit document is realistisch goed voor een conversieverbetering in de orde van 40-70% op deze pagina's, met het zwaartepunt in drie ingrepen: het herbouwen van akt 2 tot echt hoofddeel, het personaliseren van de brug, en het vervangen van de Cal-embed door een tweetraps-CTA met risico-omkering. De rest is verfijning die de premium-perceptie verhoogt maar minder direct converteert.

---

## Analyse per sectie

### 1. Topbar

Sticky navy balk, links "Backbone Customer Service", rechts "Vertrouwelijk · Voorbereid voor [bedrijf]".

**Wat werkt uitstekend.** "Vertrouwelijk" is het sterkste psychologische woord op de hele pagina en het staat op de goede plek: permanent zichtbaar, nooit opdringerig. De sticky uitvoering met `backdrop-filter: blur(16px) saturate(1.4)` is technisch netjes.

**Wat werkt onvoldoende.** Het staat op `.68rem` in `rgba(255,255,255,.4)`. Het meest exclusieve signaal van de pagina is bijna onleesbaar. En de balk doet verder niets: geen voortgangsindicatie, geen ankerpunt, geen CTA die meeschuift.

**Waarom.** Exclusiviteit werkt alleen als hij geregistreerd wordt. Op .4 alpha op navy scant het oog er overheen. Daarnaast is een sticky element dat tien schermen lang alleen een label toont verspilde permanente aandacht.

**Prioriteit.** Midden.

**Concrete verbeteringen.**
- Zet "Vertrouwelijk" op `.72rem` met `rgba(255,255,255,.62)` en geef het een amber punt ervoor (`·`) zodat het als status leest, niet als disclaimer.
- Voeg een 1px amber voortgangsbalk toe onderaan de topbar, gekoppeld aan dezelfde scroll-fractie die de journey-lijn al berekent. Kost drie regels code, hergebruikt bestaande logica.
- Laat vanaf de pivot een subtiele tekst-CTA rechts in de topbar infaden ("Plan een gesprek"), amber, klein. Niet eerder — pas nadat de spanning is geland.

**Motion.** Voortgangsbalk `transform: scaleX()` met `transform-origin: left`, geen transitie (volgt scroll direct). De CTA faden met 300ms opacity + 6px translateY, één keer, bij het passeren van de pivot.

---

### 2. Intro / hero (na de video)

Volgorde nu: eyebrow → brand-tile → videoframe → videolabel → H1 → subline → scrollcue.

**Wat werkt uitstekend.** De brand-tile met het logo van de prospect is een sterk herkenningsanker: binnen één seconde zie je je eigen merk terug. De gestapelde animatievertragingen (.15s → .9s) creëren een rustige, gecontroleerde binnenkomst.

**Wat werkt onvoldoende.** Drie dingen, waarvan twee ernstig.

*Ten eerste: het videoframe heeft geen posterframe.* `<video src="video.mp4#t=0.1" controls preload="metadata">` levert een zwart vlak met de native browser-controlbar. Op een navy achtergrond, in een 820px kader met `box-shadow: 0 50px 130px rgba(0,0,0,.5)`, is de eerste indruk letterlijk een zwart gat. Alle typografische en chromatische zorgvuldigheid eromheen wordt teniet gedaan door het grootste element op het scherm. De native controlbar is bovendien de meest merkloze UI die bestaat.

*Ten tweede: het videolabel claimt personalisatie die er niet is.* "Jeffrey, mede-oprichter van Backbone, over wat we bij Aardig Wijntje zagen." Alle 290 pagina's verwijzen naar hetzelfde `video.mp4`. Als één prospect dit doorheeft — en de doelgroep is precies scherp genoeg om het te vermoeden — dan valt niet de video om, maar de hele pagina. Elke bronvermelding daarna wordt verdacht. Dit is het grootste enkelvoudige risico op de pagina en het staat als open risico in het huismodel.

*Ten derde: de H1 staat onder de video.* Boven de vouw op een 1440×900-laptop staat: topbar, eyebrow, brand-tile, videoframe. De enige regel die de scroll verdient — "Hé Jurre, dit is waarom je m'n brief hebt ontvangen" — valt eronder. De pagina opent met een object in plaats van met een zin.

Daarbij is de subline `"Neem even de tijd. We nemen je stap voor stap mee."` nul informatie op prime real estate. Het is een instructie aan de lezer, geen belofte.

**Prioriteit.** Kritiek.

**Concrete verbeteringen.**
- Genereer per pagina een posterframe: een still van Jeffrey, `object-fit: cover`, met een amber play-knop van 64px in het midden. Verwijder `controls` tot eerste interactie (`controls` toevoegen in de click-handler). Dit is één van de goedkoopste en zichtbaarste verbeteringen op de pagina.
- Herschrijf het videolabel naar wat waar is: "Kort woord vooraf van Jeffrey, mede-oprichter van Backbone." Geen claim over deze specifieke prospect. Het huismodel schrijft dit al voor; de bcs3-set volgt het niet.
- Draai de volgorde: eyebrow → brand-tile → H1 → subline → videoframe → videolabel → scrollcue. De zin verdient de scroll, de video bevestigt hem.
- Vervang de subline door de inzet: "Drie dingen die ons opvielen bij Aardig Wijntje, en wat ze samen betekenen." Dat is een open lus in plaats van een instructie.

**Alternatieve opbouw.** Overweeg de video helemaal collapsed te starten: alleen de brand-tile, H1 en een regel "Liever in 90 seconden? Bekijk het woord vooraf van Jeffrey" met een dunne amber lijn eronder die bij klik het frame uitvouwt. Dan opent de pagina met taal en is de video een keuze in plaats van een blokkade. Dit is de radicale variant en waarschijnlijk de sterkere.

**Motion.** Posterframe met een zeer trage `scale(1.04) → scale(1)` over 8 seconden bij binnenkomst (Ken Burns, nauwelijks waarneembaar) geeft het frame leven zonder aandacht te trekken. Play-knop met `scale(1) → scale(1.08)` op hover, 200ms.

---

### 3. Akt 1 — "Waarom je dit ziet" + de drie bevindingen

Vijf blokken: aanhef, fase-kop "Bij [bedrijf]", en drie genummerde bevindingen met bron, afwisselend links en rechts.

**Wat werkt uitstekend.** Dit is het beste deel van de pagina. De zigzag over de journey-lijn creëert ritme. De genummerde bevindingen met `01/02/03` in `tabular-nums` geven een dossiergevoel. De bronvermeldingen zijn het bewijs dat er echt werk in zit en ze zijn het meest onderscheidende element van het hele concept.

**Wat werkt onvoldoende.** Drie problemen.

*De bevindingen verklappen de pivot.* Het huismodel is expliciet: bevindingen zijn neutrale waarneming, de these blijft bewaard voor de pivot. In de praktijk eindigt elke bevinding met een vetgedrukte conclusiezin die de pivot voorwegneemt. Bij Aardig Wijntje: bevinding 01 zegt "De aandacht voor Aardig Wijntje verdeelt zich over meerdere bedrijven tegelijk", bevinding 03 zegt "Die mail wacht dan tot iemand tijd vrijmaakt tussen twee ventures door". De pivot zegt vervolgens "Zolang drie oprichters het klantcontact erbij doen, bepaalt hun agenda hoe snel jullie wijnklanten antwoord krijgen." Dat is dezelfde gedachte voor de derde keer. Het moment dat het hardst zou moeten landen, is op dat punt oud nieuws.

Dit is structureel: hetzelfde patroon zit in belle-flora, beesha en bamboozy.

*De bron staat in de lichtste kleur van de pagina.* `.ch-bron` is `.72rem` in `--ink3` (`rgba(20,28,51,.42)`). Dat is onder WCAG AA en het is precies het element dat het meeste vertrouwen draagt. De bewijsvoering is de minst zichtbare tekst op het scherm. Dat is omgekeerd aan de bedoeling.

*Akt 1 is te lang naar verhouding.* Vijf van de tien journey-blokken, plus de hele hero. Het model zegt ~30%; dit is ongeveer de helft. Het huismodel noemt akt 1 expliciet "aanloop, niet het hoofddeel".

**Prioriteit.** Hoog.

**Concrete verbeteringen.**
- Schrap de vetgedrukte conclusiezin uit elke bevinding. Laat de bevinding eindigen op de waarneming zelf. Gebruik `<strong>` alleen voor het feitelijke detail (een aantal, een naam, een plaats), nooit voor de gevolgtrekking. Dit is de goedkoopste ingreep met de grootste impact op de pivot.
- Zet `.ch-bron` op `rgba(20,28,51,.58)` en geef het een amber punt of een 1px amber streepje ervoor. Overweeg het label "Bron" te vervangen door een klein icoon plus de domeinnaam — compacter en meer als voetnoot dan als disclaimer.
- Comprimeer akt 1: schuif de fase-kop "Bij [bedrijf]" en de aanhef samen tot één blok. Dat scheelt een volledig scherm zonder informatieverlies.

**Alternatieve opbouw.** Toon de drie bevindingen niet als drie opeenvolgende volledige schermen, maar als één sticky sectie waarin de drie kaarten na elkaar in beeld schuiven terwijl de kop "Bij Aardig Wijntje" blijft staan. Dan leest het als één waarneming met drie facetten in plaats van drie losse stellingen — wat precies is wat het model wil ("ze horen bij elkaar").

**Motion.** Bij het bereiken van de derde bevinding: laat de drie dots op de journey-lijn kort samen oplichten (amber glow, 600ms, gestagger 80ms) voordat de pivot in beeld komt. Dat is een visuele convergentie die de zin "ze horen bij elkaar" waarmaakt zonder één woord copy. Dit is de belangrijkste motion-toevoeging van het hele document.

---

### 4. Akt 2a — De pivot

Eén gecentreerd blok, één zin in `--serif` op `clamp(1.35rem, 2.1vw, 1.75rem)`.

**Wat werkt uitstekend.** De keuze om de pivot te isoleren is goed. Extra padding (`clamp(8vh,12vh,15vh)`), een grotere dot (16px), gecentreerd, geen kop erboven. Compositorisch klopt dit.

**Wat werkt onvoldoende.** De pivot is typografisch kleiner dan de bevindingen erboven. `.ch-pivot` gaat tot maximaal 1.75rem; `.ch-kop` gaat tot 2.7rem. Het belangrijkste moment van de pagina is de kleinste tekst in de journey. Het oog leest hem als een tussenzin.

En op mobiel verdwijnt het kaartje: `.chapter.center .ch-body { padding: 0 }` in de 800px-breakpoint haalt de achtergrond en de omkadering weg. De emotionele piek verliest zijn container precies waar de aandacht het meest fragmenteert.

**Prioriteit.** Kritiek.

**Concrete verbeteringen.**
- Zet de pivot op `clamp(1.9rem, 3.2vw, 2.6rem)`, dus minimaal gelijk aan de grootste kop op de pagina. Line-height naar 1.3.
- Geef de pivot ademruimte in plaats van een kaart: verwijder de achtergrond, zet er een dunne amber lijn boven van 40px, en isoleer hem op een volledig leeg scherm. De rest van de pagina zigzagt; hier staat alles stil.
- Behoud de behandeling op mobiel. Overschrijf de `padding: 0` voor `.chapter.pivot` specifiek.
- Overweeg de pivot op navy te zetten in plaats van op de warme achtergrond. Eén donker scherm midden in de pagina, precies op het kantelpunt. Dat is het sterkste contrastmiddel dat je hebt en het wordt nu nergens ingezet tussen hero en CTA.

**Motion.** De journey-lijn zou hier moeten haperen. Concreet: laat de amber progressielijn bij het naderen van de pivot-dot heel even vertragen en dan met een korte puls doorlopen (`filter: drop-shadow` van 6px naar 14px en terug, 500ms). Betekenis: hier gebeurt iets. Verder: de pivot-zin woord voor woord laten verschijnen (`opacity` per span, 40ms stagger) in plaats van als blok. Alleen hier, nergens anders — dat maakt het een gebeurtenis.

---

### 5. Akt 2b — "De prijs van stilzitten"

Eén blok, links uitgelijnd, 400px breed: twee alinea's, een pull-quote, en nog een alinea.

**Wat werkt onvoldoende.** Dit is het grootste probleem van de pagina.

Dit blok is inhoudelijk het hoofddeel — het is de enige plek waar het gevoelde probleem en het gevolg staan. Het is de reden dat iemand een gesprek plant. En het is vormgegeven als de dichtste tekstwand op de pagina, in een kolom van 400px, in `--ink2` op `font-weight: 400`, na negen schermen scrollen. De laatste zin — "Stel dat elke abonnee en elke horeca-order binnen het uur antwoord krijgt" — is de enige toekomstprojectie op de hele pagina en staat onderaan een wand, met een inline `style="margin-top:1.4rem"` alsof hij er later bij is geplakt.

Bij simulatie van scangedrag: op dit punt is de bezoeker in scanmodus. Een blok van vier alinea's zonder kop-onderbreking, zonder cijfer, zonder visueel ankerpunt, wordt overgeslagen op de pull-quote na. De pull-quote is bovendien een herhaling ("Drie oprichters, drie bedrijven, en toch landt elke wijnvraag bij dezelfde inbox") van wat al drie keer is gezegd.

En er staat geen enkel getal in. Het huismodel schrijft voor: "het gevolg verankeren in hún cijfers" en "verankerd in hún cijfers". Er is geen bedrag, geen percentage, geen aantal abonnees, geen ticketvolume, geen responstijd. "Dat kost je juist de klanten die het meeste opleveren" is een bewering zonder maat. Verliesaversie werkt via een concreet verlies; zonder getal is het een gevoel dat de bezoeker zelf moet invullen, en dat doet hij niet.

**Waarom.** Dit is waar 40% van het paginagewicht hoort te zitten en waar nu ongeveer 10% zit, in de slechtst leesbare vorm die de pagina kent. Dit alleen verklaart een groot deel van de conversiekloof.

**Prioriteit.** Kritiek.

**Concrete verbeteringen.**
- Breek dit blok op in drie afzonderlijke journey-momenten met eigen dots: (a) het gevoelde probleem, (b) het gevolg met een getal, (c) de toekomstprojectie. Dat maakt akt 2 vijf blokken in plaats van twee, en brengt de verhouding in lijn met het model.
- Zet het gevolg om in één concreet, van hen afgeleid cijfer. Bijvoorbeeld: geschat aantal abonnees × maandbedrag × een conservatief churn-percentage bij trage respons, met een bronregel eronder net als bij de bevindingen. Eén getal, groot, in serif, met een kleine onderbouwing. Dit is het enige moment op de pagina waar een groot cijfer hoort.
- Vervang de pull-quote. Nu herhaalt hij de pivot. Laat hem in plaats daarvan het gevolg vasthouden, of schrap hem — de amber `border-left` haalt aandacht weg van waar het moet zijn.
- Geef de toekomstprojectie een eigen blok, gecentreerd, in serif, op de warme achtergrond met veel witruimte. Dat is het moment waarop de bezoeker zich iets voorstelt; dat verdient geen alinea onderaan een wand.
- Maximaal 3 zinnen per alinea in dit hele deel.

**Alternatieve opbouw.** Overweeg een klein interactief element: een schuifregelaar met "aantal klantvragen per week" die het jaarlijkse gevolg live meerekent, met een conservatieve default die uit de research komt. Dat is de enige plek op de pagina waar interactie inhoudelijk iets toevoegt: de bezoeker rekent zelf, en wat hij zelf berekent gelooft hij. Dat is commitment en consistency in één component. Wel: alleen doen als de aannames verdedigbaar zijn, anders ondermijnt het de bronnendiscipline van akt 1.

**Motion.** Het getal van tel-animatie voorzien (0 → waarde, 1200ms, easing out) bij binnenkomst. Dit is het enige nummer op de pagina, dus het effect is niet inflatoir. De toekomstprojectie in een lichtere, warmere behandeling laten binnenkomen dan de rest — bijvoorbeeld een zeer subtiele amber gloed die vanuit het midden opkomt over 1,2s. Emotioneel contrast met het blok ervoor.

---

### 6. Akt 3 — De brug ("En dit is precies wat wij doen")

Fase-kop plus twee blokken: "Jouw toon, altijd" en "Vaste EU-agents".

**Wat werkt onvoldoende.** Deze twee blokken zijn woord voor woord identiek op alle 290 pagina's, op de bedrijfsnaam na. Na negen schermen bewijzen dat er persoonlijk werk in zit, schakelt de pagina over op template-tekst — precies op het moment dat de bezoeker beslist of hij een gesprek plant.

Dat is niet alleen een gemiste kans, het is een actief signaal. Het toonverschil is voelbaar: akt 1 en 2 zijn specifiek en onderzocht, akt 3 is generiek en verkoperig ("Jouw toon. Jouw naam. Jouw tempo."). Een scherpe lezer registreert dat als: het persoonlijke deel was de verpakking, dit is het echte aanbod. Dat is de meest schadelijke conclusie die deze pagina kan uitlokken.

Bovendien beantwoorden de twee blokken niet de vragen die op dit punt leven. Na de spanning denkt de lezer: hoe lang duurt dit, wat kost het, wat moet ik ervoor doen, wat als het niet werkt, merken mijn klanten het. Geen van die vijf wordt geraakt.

Het huismodel voorziet dit precies: "zwakke pitch = zwakke spanning upstream". Hier is de spanning inderdaad zwak, maar de brug is bovendien onvoldoende op eigen kracht.

**Prioriteit.** Kritiek.

**Concrete verbeteringen.**
- Maak minimaal het eerste brugblok prospect-specifiek. Niet "Jouw toon, altijd", maar hoe dat er bij dit merk uitziet: welke kanalen, welke talen, welk seizoenspatroon, welke vraag die in akt 1 is genoemd. Eén alinea die aantoonbaar over hén gaat, herstelt de continuïteit met akt 1 en 2.
- Voeg een derde brugblok toe dat de bezwaren adresseert die de lezer op dit punt heeft. Concreet en kort: hoe de overdracht verloopt, in hoeveel weken, wat het van hen vraagt in tijd.
- Land de brug expliciet op de spanning. De laatste zin van akt 3 moet terugverwijzen naar de pivot, niet naar de dienst. Nu eindigt de journey op "Vaste EU-agents ... juist als het druk wordt" — een productkenmerk, geen ontknoping.
- Overweeg een prijsanker. Het huismodel noemt de pricing-sectie optioneel; hier zou hij frictie wegnemen. "Vaste prijs per ticket" staat nu weggestopt in de proof-facts. Eén concreet startbedrag verlaagt de drempel voor een gesprek meer dan het er verhoogt, omdat het de belangrijkste onbeantwoorde vraag beantwoordt.

**Motion.** De journey-lijn kan hier van karakter veranderen: waar hij tot de pivot dun en zoekend is, kan hij na de pivot iets dikker en constanter worden (2.4px → 3px). Onbewust signaal dat het verhaal van waarneming naar richting kantelt. Verder: geen extra motion in akt 3. De aandacht moet naar de tekst.

---

### 7. Akt 4a — Proof / team-card

Twee-koloms kaart: foto van Jeffrey en Dylan links, bio plus drie feiten rechts.

**Wat werkt uitstekend.** De foto is de juiste keuze. Gezichten na tien schermen tekst verlagen de drempel meetbaar. De `object-position: center 15%` en de gradient-overlay zijn netjes uitgevoerd. "Bewust klein gehouden" is een goed positioneringszin: het maakt van een beperking een keuze.

**Wat werkt onvoldoende.** Het bewijs is volledig zelf-verklaard. "1M+ tickets", "20+ agents", "Vaste prijs" zijn drie beweringen zonder verificatie, terwijl de pagina tien schermen lang heeft laten zien dat hij bronvermelding beheerst. Het contrast is scherp: over de prospect wordt alles gestaafd, over zichzelf niets.

Er is geen enkele klantnaam, geen logo, geen resultaat, geen citaat, geen cijfer van een derde. Het huismodel zegt bewust "geen reviewblok onderaan" om statuur te bewaren — dat is een verdedigbare keuze, maar het laat een gat dat door niets anders wordt gevuld. Authority en social proof zijn op deze pagina praktisch afwezig.

Daarnaast: het WebwinkelKeur-partnerblok bestaat als CSS-klasse (`.ch-wwk`) maar wordt op deze pagina niet gebruikt. Dat is precies het type derdepartij-signaal dat hier zou helpen.

**Prioriteit.** Hoog.

**Concrete verbeteringen.**
- Staaf minimaal één van de drie feiten. "1M+ tickets sinds 2021, over 40 D2C-merken" is oneindig veel sterker dan "1M+ tickets" omdat het falsifieerbaar is.
- Voeg één klantbewijs toe in de vorm die de pagina wél toestaat: geen reviewblok, maar één regel onder de team-card met de merken waarvoor Backbone werkt, in grijs, klein, zonder opsmuk. Terughoudend gepresenteerde namen verhogen statuur; een carrousel met sterren verlaagt hem.
- Zet het WebwinkelKeur-blok in als partner-signaal waar het van toepassing is. De styling ligt er al.
- Voeg risico-omkering toe. Dit ontbreekt volledig op de pagina. Eén regel: opzegtermijn, proefperiode, of "we starten met één kanaal". Wat het ook is — de bezoeker heeft nu geen enkel antwoord op "en als het niet werkt".

**Motion.** De drie feiten met een korte stagger laten binnenkomen (80ms tussen elk, 400ms elk) in plaats van als één `.reveal`. De amber `border-left` van elk feit van hoogte 0 naar 100% laten groeien, 300ms. Klein, maar het maakt van drie statische regels een opsomming die zich opbouwt.

---

### 8. Akt 4b — CTA

Navy sectie, kop "Even kennismaken?", subline, en een Cal.com inline-embed van minimaal 560px.

**Wat werkt uitstekend.** "Dit wordt geen verkoopgesprek" is de juiste framing voor deze doelgroep. De navy achtergrond sluit de pagina af zoals hij begon — compositorisch een goede haakje.

**Wat werkt onvoldoende.** Vier dingen.

*De embed breekt de visuele taal.* Cal.com brengt zijn eigen typografie, knopkleuren, spacing en interactiemodel mee, in een wit kaartje van 560px op navy. Na een pagina die consequent Playfair, Inter, navy en amber aanhoudt, is dit het enige element dat van een ander merk komt. Het leest als een geplakte tool. Bovendien laadt het via een extern script: er is een periode waarin de bezoeker naar een leeg wit blok van 560px kijkt.

*De ask is zwaarder dan hij lijkt.* Een month-view kalender vraagt drie beslissingen (datum, tijd, formulier) op het moment van maximale twijfel. Voor een doelgroep die druk is, is "kies nu een concreet moment in mijn agenda" een hoge drempel.

*Er is geen alternatief.* Eén exit, één vorm. Wie geïnteresseerd is maar nu niet wil boeken, heeft geen enkele actie behalve wegklikken. Geen mailadres in beeld (alleen in de footer), geen "stuur me eerst wat meer", geen terugbel-optie.

*Amber komt hier niet voor.* Het accent van de hele pagina — journey-lijn, dots, eyebrows, pull-quotes — heeft geen eindbestemming. De ene plek waar amber naartoe zou moeten wijzen is een wit vlak. Dat is accent-inflatie: de kleur betekent overal iets kleins en nergens iets groots.

**Prioriteit.** Kritiek.

**Concrete verbeteringen.**
- Vervang de directe embed door een tweetraps-CTA: een amber knop "Kies een moment" die de kalender in een overlay opent. De pagina eindigt dan op een strak, merkeigen element in plaats van op een vreemd iframe, en de kalender laadt pas bij intentie. Dit alleen verbetert de premium-perceptie van de afsluiting aanzienlijk.
- Voeg een secundaire, lichtere optie toe onder de knop: "Liever eerst schriftelijk? Mail Jeffrey direct." Tekstlink, geen knop. Vangt de groep die overtuigd is maar niet wil boeken.
- Laat amber eindelijk zijn werk doen: de primaire knop in `--amber` met navy tekst. Dat is het eerste en enige gevulde amber vlak op de pagina, en het staat precies waar de journey-lijn eindigt.
- Voeg één regel risico-omkering direct onder de knop toe, klein en grijs. Duur van het gesprek, wat er gebeurt, wat er niet gebeurt.
- Sluit de journey-lijn visueel af in de CTA. Nu stopt de amber lijn in de `main`, en de proof- en CTA-secties staan er los van. Laat de lijn doorlopen tot in de knop. Dan is de knop letterlijk de bestemming van het pad dat de bezoeker tien schermen heeft gevolgd. Dit is de sterkste beschikbare koppeling tussen vorm en conversie.

**Motion.** De journey-lijn de laatste 200px naar de knop laten tekenen op scroll, met een lichte puls bij aankomst. Knop: `box-shadow` van 0 naar `0 12px 40px rgba(198,137,60,.35)` op hover, 250ms, plus 1px translateY omhoog. De overlay met een `backdrop-filter: blur(20px)` en een 300ms scale-in van .96 naar 1.

---

### 9. Footer

Drie regels grijze tekst.

**Wat werkt uitstekend.** Terughoudend, geen linkbrij, herhaalt "Vertrouwelijk". Correct.

**Wat werkt onvoldoende.** Niets van betekenis. Prioriteit laag. Eventueel het mailadres iets zichtbaarder, aangezien het nu het enige alternatieve contactkanaal op de pagina is.

---

## Doorsnijdende analyses

### Eerste indruk (0-5 seconden)

Wat er feitelijk gebeurt: navy scherm, een klein logo van het eigen bedrijf in een pilletje, en daaronder een groot zwart rechthoek met een browser-controlbar. Het gevoel is niet luxe en niet vertrouwen — het is *afwachting*. De pagina vraagt om een handeling (speel de video af) voordat hij iets heeft gegeven.

Het emotionele effect van "Voorbereid voor [bedrijf]" plus het eigen logo is sterk en wordt binnen een seconde weggegooid door het zwarte vlak. Met een posterframe en de H1 boven de video zou dezelfde sectie binnen 5 seconden herkenning, nieuwsgierigheid en statuur oproepen. Nu roept hij vooral op: er wordt me een video voorgeschoteld.

### Scangedrag (gesimuleerd)

**Eerste 2 seconden.** Oog gaat naar het zwarte videovlak (grootste element, hoogste contrast), dan naar het logo in de brand-tile (herkenning van het eigen merk trekt altijd). De topbar wordt niet gelezen.

**Volgende 8 seconden, scannend scrollen.** Het oog springt van serif-kop naar serif-kop: "Waarom je dit ziet" → "Bij Aardig Wijntje" → "Drie ventures" → "Twee klantstromen" → "Alles bij drie" → "De prijs van stilzitten" → "En dit is precies wat wij doen". De vetgedrukte zinnen binnen de bevindingen worden meegepakt. De bronvermeldingen worden op deze snelheid volledig gemist — te licht, te klein.

De pivot wordt waarschijnlijk overgeslagen. Hij heeft geen kop, staat in kleinere letters dan de koppen eromheen, en het scannende oog zoekt naar koppen. Dat is een ernstig probleem: het scharnierpunt van het verhaal ligt in een blinde vlek van het scanpatroon.

Het blok "De prijs van stilzitten" wordt op de kop en de pull-quote na overgeslagen. Vier alinea's zonder onderbreking activeert geen leesmodus in scanfase.

**Bij daadwerkelijk lezen.** De lezer die terugkeert, leest akt 1 volledig (kort, concreet, met bronnen — dit deel is goed leesbaar), en haakt aan het begin van "De prijs van stilzitten" af of leest schuin door. De twee brugblokken worden gelezen, en dat is precies waar de generieke toon wordt geregistreerd.

**Wat gegarandeerd wordt overgeslagen.** De bronvermeldingen. De subline in de hero. Het derde en vierde alinea van akt 2b. De bio-tekst in de team-card. De footer.

### Emotionele spanningsboog

De curve nu, per fase:

- Hero: gemiddeld. Herkenning stijgt door het logo, zakt door het zwarte vlak.
- Bevinding 01: stijgt scherp. "Hoe weten zij dit?" is het sterkste moment van de pagina.
- Bevinding 02 en 03: vlak tot licht dalend. De vetgedrukte conclusies maken het voorspelbaar; na bevinding 01 weet de lezer waar dit heen gaat.
- Pivot: zou hier de piek moeten zijn. Vlakt af, omdat de inhoud al is gegeven en de vorm hem niet markeert.
- "De prijs van stilzitten": daalt. Tekstwand, geen cijfer, geen visueel ankerpunt.
- Brug: daalt verder. Generieke tekst, herkenbaar als sjabloon.
- Proof: licht herstel. Gezichten helpen altijd.
- CTA: vlak. Iframe, geen amber, geen risico-omkering.

De pagina piekt dus rond scherm 3 van de 12 en daalt daarna. Dat is de omgekeerde curve van wat je wilt. In het gewenste profiel stijgt de spanning tot de pivot (scherm 7-8), houdt aan door het gevolg, ontspant bij de brug en de gezichten, en eindigt op een lichte, heldere ask.

De belangrijkste ingreep om de curve om te draaien is niet meer copy maar herverdeling: minder gewicht op akt 1, veel meer op akt 2, en de pivot als visueel evenement in plaats van als tussenzin.

### Psychologie

**Wat werkt.** *Nieuwsgierigheid* is het sterkste mechanisme op de pagina en het werkt goed in akt 1. *Commitment en consistentie* zitten impliciet in de journey-lijn: de bezoeker volgt een pad en pad-metaforen verhogen de neiging om af te maken. *Reciprociteit* zit in het zichtbare werk — de bronnen laten zien dat er tijd is ingestoken voordat er iets is gevraagd. Dat is het beste psychologische fundament van het hele concept.

**Wat ontbreekt of onbenut blijft.**

*Authority.* Volledig zelf-verklaard. Geen enkele externe bevestiging, geen klantnaam, geen certificering, geen cijfer van een derde partij.

*Social proof.* Praktisch afwezig, en dat is deels een bewuste keuze. Maar de keuze om geen reviewblok te plaatsen betekent niet dat de behoefte verdwijnt; hij wordt alleen onbeantwoord gelaten. Terughoudend gepresenteerde merknamen zouden de statuur niet verlagen.

*Verliesaversie.* Aanwezig in intentie ("de prijs van stilzitten") maar zonder kwantificering. Verliesaversie is een van de sterkste effecten in de gedragseconomie, en het is precies het effect dat een getal nodig heeft om te werken. Dit is de grootste onbenutte hefboom op de pagina.

*Exclusiviteit en schaarste.* Alleen het woord "Vertrouwelijk" op .68rem in .4 alpha. Er is geen enkel signaal dat dit werk beperkt is, dat er selectie plaatsvindt, of dat dit niet aan iedereen wordt gestuurd. Voor een propositie die op maat-onderzoek draait is dat een gemiste kans van formaat.

*Contrast.* Onbenut. Er wordt nergens getoond hoe het nu is versus hoe het kan zijn, behalve in één zin onderaan een tekstwand. Voor-en-na is het meest directe overtuigingsmiddel dat er is.

*Framing en anchoring.* Geen prijsanker, geen tijdsanker, geen vergelijkingskader. De lezer heeft geen referentiepunt om het aanbod tegen af te zetten.

*Cognitieve belasting.* Over het algemeen goed beheerst — dat is een verdienste. Uitzonderingen: het akt 2b-blok en de Cal-embed.

### Visuele hiërarchie

Het grid klopt: 1180px journey, 400px kolommen, 900px proof, 720px CTA. Progressieve versmalling naar de CTA toe is goed gedaan en trechtert onbewust.

Waar het misgaat: de typografische schaal loopt niet parallel aan het inhoudelijke belang. De grootste tekst op de pagina (na de H1) zijn de fase-koppen "Bij [bedrijf]" en "En dit is precies wat wij doen" — beide organisatorisch, niet inhoudelijk. De pivot, inhoudelijk het belangrijkst, is kleiner dan een bevindingskop. De bron, cruciaal voor geloofwaardigheid, is het kleinst en lichtst.

Herstel de rangorde: pivot > gevolg-cijfer > bevindingskoppen > fase-koppen. Fase-koppen mogen eyebrow-formaat zijn; ze zijn wegwijzers, geen inhoud.

Witruimte is over het algemeen goed. De verticale ritmiek is echter monotoon: bijna elk blok krijgt `clamp(5.5vh,8vh,10vh)`. Alleen pivot en phase wijken af. Meer variatie in verticale spatiëring — krap waar het opsommend is, ruim rond de pivot — zou de spanningsboog ondersteunen die de copy niet alleen kan dragen.

### Typografie

Playfair Display op weight 500 voor koppen, Inter 300/400 voor tekst. De combinatie is verdedigbaar en past bij de positionering.

Problemen:

- `--ink2` is `rgba(20,28,51,.66)`, wat op `#FBFAF8` neerkomt op een contrastverhouding rond 4,4:1. Dat is net onder WCAG AA voor normale tekst. Voor een doelgroep die vaak 45+ is, op laptopschermen in kantoorlicht, is dat een concreet leesbaarheidsprobleem, geen theoretisch.
- `--ink3` op `.42` is ongeveer 2,6:1. Dat is ver onder elke norm, en het is de kleur van de bronvermeldingen en de feitlabels.
- Inter op weight 300 voor `.intro-sub`, `.ch-sub` en `.proof-sub` in combinatie met lage contrastwaarden versterkt het probleem. Weight 300 is een display-gewicht, geen tekstgewicht.
- Playfair Display is een didone met hoog streekcontrast. Op `clamp(1.9rem, 3vw, 2.7rem)` werkt hij goed. Maar `.ch-pivot` op 1.35rem is aan de kleine kant voor deze letter — dunne haarlijnen vallen weg op niet-retina schermen.

Aanbevelingen: `--ink2` naar `.74`, `--ink3` naar `.56`, alle `font-weight: 300` naar 400, en de pivot fors omhoog in grootte. Dat zijn vier waarden in `:root` plus een paar regels. De impact op leesbaarheid en daarmee op doorlezen is aanzienlijk voor de moeite.

### Kleurgebruik

Het palet blijft. Navy `#0E1526`, amber `#C6893C`, warm off-white `#FBFAF8` — dit is een volwassen, warme, niet-technologische combinatie die precies het gewenste verschil maakt met SaaS en agency. Geen wijziging nodig.

Wat wel moet veranderen is de *distributie*. Amber wordt nu gebruikt voor eyebrows, de journey-lijn, dots, pull-quote-randen, feit-randen, de scroll-cue en gloed-effecten — zeven verschillende functies — en niet voor de conversie-actie. Een accentkleur die overal zit, wijst nergens naartoe.

Concreet: reserveer gevuld amber (`background: var(--amber)`) uitsluitend voor de primaire CTA-knop, één plek op de hele pagina. Alle andere amber-toepassingen blijven lijn, rand of tekst. Dan wordt het één keer gevulde amber-vlak automatisch het zwaartepunt van het scherm.

Tweede punt: de pagina gebruikt navy alleen aan begin en eind. Eén navy-sectie in het midden — de pivot — zou het beschikbare contrastmiddel inzetten op het enige moment dat het verdient.

### Copy × design

Het design is over het algemeen dienstbaar, wat een compliment is. Maar op drie plekken werken copy en design langs elkaar heen:

1. De copy zegt "we nemen je stap voor stap mee"; het design geeft je een videospeler. Belofte en eerste ervaring komen niet overeen.
2. De copy zegt bij de fase-kop "Ze horen bij elkaar"; het design toont drie los van elkaar zwevende blokken links en rechts van een lijn. De convergentie wordt beweerd, niet getoond. De voorgestelde dot-convergentie-animatie lost dit op.
3. De copy van akt 2 gaat over gevolg en verlies; het design behandelt het als een gewoon tekstblok, in dezelfde kolombreedte en hetzelfde ritme als de bevindingen. De inhoud escaleert, de vorm niet.

### Vergelijking met wereldklasse

Ten opzichte van Linear, Stripe, Attio en Arc zit het verschil op vier punten, niet op esthetiek:

*Ritmevariatie.* Linear varieert voortdurend de dichtheid: strakke opsommingen, dan een leeg scherm met één zin, dan een dicht diagram. Deze pagina heeft één ritme, tien schermen lang. Monotonie leest als lengte, ook als de pagina objectief niet lang is.

*Betekenisvolle interactie.* Stripe laat je een diagram bedienen zodat je begrijpt wat het product doet. Deze pagina heeft één interactief element (de video) en dat verklaart niets over de propositie. De journey-lijn is passief. De voorgestelde rekentool in akt 2 is de enige plek waar interactie hier inhoudelijk werk zou doen.

*Vertrouwenslaag.* Alle genoemde bedrijven besteden aanzienlijke ruimte aan verifieerbaar bewijs — logo's, cijfers met bron, cases. Deze pagina heeft drie zelf-verklaarde getallen in een kaart. De pagina is uitzonderlijk goed in het staven van beweringen over de prospect en uitzonderlijk zwak in het staven van beweringen over zichzelf.

*De afsluiting.* Geen van die bedrijven eindigt op een ingesloten tool van een derde partij. De laatste indruk is bij hen het meest verzorgde deel van de pagina; hier is het het minst verzorgde.

Waar deze pagina wél wint: rust en afwezigheid van marketingtaal. Er staat geen enkel superlatief, geen "revolutionair", geen emoji, geen fake-urgentie. Dat is zeldzaam en waardevol.

### Frictie: de onbeantwoorde vragen

Op het moment van de CTA leven deze vragen, en geen ervan wordt beantwoord:

1. Wat kost dit? (Alleen "vaste prijs per ticket", zonder bedrag.)
2. Hoe lang duurt de overdracht en wat vraagt het van mij?
3. Wat als het niet werkt — kan ik eruit?
4. Merken mijn klanten dat het uitbesteed is? (Beweerd, niet bewezen.)
5. Voor wie doen jullie dit nog meer? (Geen enkele naam.)
6. Wie zit er straks daadwerkelijk aan mijn tickets?
7. Wat gebeurt er als ik dat gesprek plan — hoe lang, met wie, waar?

Vraag 1, 3 en 5 zijn de zwaarste. Alle drie zijn met één regel te beantwoorden.

Aanvullende frictie: de bezoeker die overtuigd is bij de pivot moet nog vijf schermen scrollen voordat er een actie mogelijk is. Er is geen enkel opvangpunt onderweg.

### Informatiearchitectuur

De volgorde is grotendeels goed en volgt het model. Wijzigingen die ik zou doorvoeren:

**Eerder.** De H1 vóór de video. Het gevolg-cijfer direct na de pivot, niet begraven in alinea drie.

**Later.** Niets hoeft naar achteren.

**Weg.** De hero-subline ("Neem even de tijd"). De pull-quote in akt 2b in zijn huidige vorm. Eventueel het tweede brugblok als het generiek blijft — één sterk specifiek blok is beter dan één specifiek plus één generiek.

**Ontbreekt volledig.** Risico-omkering. Prijsanker. Extern bewijs. Een antwoord op "hoe verloopt het". Een tweede, lichtere conversiemogelijkheid. Een opvangpunt voor de vroeg-overtuigde bezoeker.

---

## Top 25 verbeteringen, gerangschikt op verwachte conversie-impact

1. Herbouw akt 2 tot het hoofddeel: splits "De prijs van stilzitten" in drie journey-momenten (gevoeld probleem / gevolg met cijfer / toekomstprojectie).
2. Voeg één concreet, van de prospect afgeleid getal toe aan het gevolg, met bronregel. Zonder getal werkt verliesaversie niet.
3. Maak akt 3 prospect-specifiek. Minimaal het eerste brugblok mag geen template-tekst meer zijn.
4. Vervang de Cal-embed door een amber knop die de kalender in een overlay opent.
5. Schrap de vetgedrukte conclusiezinnen uit de drie bevindingen zodat de pivot niet vooraf wordt verklapt.
6. Voeg risico-omkering toe onder de CTA (opzegtermijn, proef, of gefaseerde start).
7. Maak de pivot typografisch de grootste tekst in de journey en isoleer hem op een leeg scherm.
8. Voeg een posterframe toe aan de video en verberg de native controls tot eerste klik.
9. Verplaats de H1 boven het videoframe en vervang de subline door de inzet.
10. Herschrijf het videolabel naar wat waar is; verwijder elke suggestie dat de video per prospect is opgenomen.
11. Voeg een tweede, lichtere conversieoptie toe naast het boeken ("Mail Jeffrey direct").
12. Voeg een prijsanker toe aan het einde van akt 3.
13. Verhoog de contrastwaarden: `--ink2` naar .74, `--ink3` naar .56, weight 300 naar 400.
14. Staaf minimaal één van de drie proof-cijfers met een verifieerbaar detail.
15. Voeg terughoudend gepresenteerde klantnamen toe onder de team-card.
16. Laat de journey-lijn doorlopen tot in de CTA-knop.
17. Reserveer gevuld amber uitsluitend voor de primaire CTA.
18. Voeg de dot-convergentie-animatie toe bij de derde bevinding.
19. Voeg een derde brugblok toe over verloop en tijdsinvestering.
20. Zet de pivot-sectie op navy als enige donkere onderbreking in het midden.
21. Voeg een voortgangsbalk toe aan de topbar en een CTA die na de pivot infadet.
22. Maak de bronvermeldingen zichtbaarder (contrast plus amber markering).
23. Verkort akt 1 door de aanhef en de fase-kop samen te voegen.
24. Repareer de pivot-behandeling op mobiel (`padding: 0` overschrijven).
25. Vervang of schrap de pull-quote in akt 2b; hij herhaalt nu de pivot.

---

## Quick Wins (binnen één dag uitvoerbaar, over alle 290 pagina's)

Deze zijn allemaal via zoek-vervang of een `:root`-wijziging door te voeren:

- Contrastwaarden in `:root` aanpassen (punt 13). Vier waarden.
- Videolabel herschrijven (punt 10). Eén zoek-vervang.
- Vetgedrukte conclusiezinnen uit de bevindingen halen (punt 5). Per pagina één handmatige controle, maar mechanisch.
- H1 boven de video plaatsen (punt 9). Eén blok verplaatsen in het template.
- Pivot-grootte verhogen en mobiele padding repareren (punt 7 deels, punt 24). Twee CSS-regels.
- Posterframe toevoegen (punt 8). Eén still, één `poster`-attribuut.
- Secundaire mail-CTA toevoegen (punt 11). Eén regel HTML.
- Pull-quote schrappen (punt 25).
- Topbar-contrast verhogen en voortgangsbalk toevoegen (punt 21 deels). Hergebruikt bestaande scroll-logica.
- Amber alleen nog gevuld op de CTA (punt 17).

Samen zijn dit ongeveer twee tot drie uur werk op het template plus een geautomatiseerde uitrol, en ze pakken de meest zichtbare premium-schade aan.

---

## High Impact Design Upgrades

Grotere ingrepen, gerangschikt op verwachte ROI:

**1. Akt 2 als hoofddeel (punten 1, 2, 7, 20).** De grootste enkelvoudige ingreep. Vraagt om nieuwe copy per pagina (het cijfer moet per prospect kloppen) en drie nieuwe blokken in het template. Dit is waar het model belooft dat de conversie zit en waar de pagina nu het minst levert.

**2. Gepersonaliseerde brug (punten 3, 19).** Vraagt research-output die er deels al is. Het verschil tussen "een mooie persoonlijke pagina" en "deze mensen begrijpen mijn situatie én weten wat ze eraan doen" zit volledig in dit deel.

**3. CTA-herontwerp (punten 4, 6, 11, 16, 17).** Overlay in plaats van embed, amber knop als eindpunt van de journey-lijn, risico-omkering, secundaire optie. Dit is een afgebakende bouwklus op één sectie met effect op elke bezoeker die zo ver komt.

**4. Bewijslaag (punten 14, 15).** Klein in uitvoering, groot in effect, omdat authority nu praktisch nul is en de rest van de pagina zo goed is in staving.

**5. Interactieve gevolg-berekening in akt 2.** De radicale optie. Alleen doen als de aannames verdedigbaar zijn en met bron onderbouwd. Als dat kan, is het het sterkste overtuigingselement dat aan deze pagina toegevoegd kan worden, omdat de bezoeker zijn eigen conclusie berekent.

---

## Motion & Interaction Roadmap

Gerangschikt op verhouding tussen betekenis en inspanning. Alles hieronder heeft een functie; niets is decoratie.

| # | Interactie | Wat gebeurt er | Waarom het helpt |
|---|---|---|---|
| 1 | **Dot-convergentie** | Bij de derde bevinding lichten de drie bevinding-dots kort na elkaar op (80ms stagger, amber glow, 600ms) | Maakt de zin "ze horen bij elkaar" visueel waar. Bereidt de pivot voor zonder copy. Hoogste betekeniswaarde van de lijst. |
| 2 | **Pivot-hapering** | De amber progressielijn vertraagt bij de pivot-dot en pulseert kort door (drop-shadow 6→14px, 500ms) | Markeert het scharnierpunt in de enige taal die de hele pagina al spreekt: de lijn. |
| 3 | **Pivot woord-voor-woord** | De pivot-zin verschijnt per woord (40ms stagger). Alleen hier | Dwingt leestempo af op de plek waar scannen fataal is. Uniek gebruik maakt er een gebeurtenis van. |
| 4 | **Getal-teller** | Het gevolg-cijfer telt op vanaf 0 (1200ms, ease-out) | Verlengt de aandacht op het enige getal van de pagina en versterkt verliesaversie. |
| 5 | **Journey naar CTA** | De lijn loopt door tot in de CTA-knop en tekent zich af op scroll | Verbindt tien schermen verhaal fysiek met de actie. Sterkste vorm-conversie-koppeling beschikbaar. |
| 6 | **Topbar-voortgang** | 1px amber balk onder de topbar, volgt de scroll-fractie | Voortgangsfeedback verlaagt afhaakkans op lange pagina's. Hergebruikt bestaande logica. |
| 7 | **Topbar-CTA na pivot** | Tekstlink faded in na het passeren van de pivot (300ms) | Vangt de vroeg-overtuigde bezoeker die nu geen actie heeft. |
| 8 | **Reveal versnellen** | 1000ms naar 500ms, blur van 5px naar 2px, threshold van .18 naar .12 | Huidige reveals arriveren te laat bij snel scrollen en de blur is een leestaks. Rustiger én sneller. |
| 9 | **Feit-randen groeien** | De amber `border-left` van elk proof-feit groeit van 0 naar 100% hoogte, gestaggerd | Maakt van drie statische regels een opbouwende opsomming. |
| 10 | **Poster Ken Burns** | Zeer trage scale 1.04 → 1 over 8s op het posterframe | Geeft de hero leven zonder aandacht te vragen. |
| 11 | **CTA-overlay** | Kalender opent in een overlay met backdrop-blur en 300ms scale-in van .96 | Houdt de pagina merkeigen tot het laatste moment; laadt de externe tool pas bij intentie. |
| 12 | **Lijn-karakterwissel** | De journey-lijn wordt na de pivot 2.4px → 3px | Onbewust signaal dat het verhaal van waarneming naar richting kantelt. |

**Verwijderen.** De `march`-animatie op de gestippelde basislijn (40s, `stroke-dashoffset` naar -92) is onwaarneembaar en draait permanent. Kost rendering, levert niets. Weg.

**Technische opmerking.** De `build()`-functie wordt nu aangeroepen via zes verschillende paden, waaronder `setTimeout(build, 400)` en `setTimeout(build, 1200)`. Dat zijn noodverbanden rond het laden van fonts, video en layout. De `ResizeObserver` en `document.fonts.ready` dekken die gevallen al af; de timeouts kunnen weg zodra dat is geverifieerd. Bij het toevoegen van bovenstaande interacties is het verstandig de scroll-handler te bundelen in één `requestAnimationFrame`-lus in plaats van meerdere losse listeners.

---

## Final Verdict

*Als deze pagina morgen meedoet aan de Webby Awards én tegelijkertijd 100 high-ticket prospects moet overtuigen, wat houdt hem dan nog tegen om een absolute wereldklasse landingspagina te zijn?*

Drie dingen.

**Ten eerste: de pagina voert zijn eigen model niet uit.** Het vier-akten-model is goed en het is Pique's IP. Maar deze uitvoering geeft de helft van het gewicht aan de aanloop en behandelt de spanning — het hoofddeel — als een tekstblok van 400px breed. De pagina bouwt tien schermen op naar een moment dat er niet is. Dat is geen ontwerpprobleem en geen copyprobleem; het is een verdelingsprobleem, en het is met dezelfde bouwstenen op te lossen.

**Ten tweede: de pagina bewijst alles over de prospect en niets over zichzelf.** Er is geen mooiere asymmetrie denkbaar voor een propositie die op onderzoek draait, en geen schadelijkere. Elke bewering over Aardig Wijntje heeft een bron. Elke bewering over Backbone heeft er geen. Een intelligente, sceptische lezer registreert dat verschil, ook als hij het niet benoemt. Eén geverifieerd cijfer, één klantnaam en één vorm van risico-omkering sluiten dat gat.

**Ten derde: de pagina houdt de belofte niet vol tot het einde.** Negen schermen persoonlijk werk, dan twee generieke blokken, dan een iframe van een ander merk. De laatste twintig procent van de ervaring — precies het deel dat de beslissing draagt — is het minst verzorgde deel. Bij Apple, Linear en Stripe is dat omgekeerd: de afsluiting is het meest verzorgde deel van de pagina, omdat dat is waar de kwaliteit van alles ervoor wordt bevestigd of ontkend.

En dan het risico dat boven alles hangt: het videolabel claimt dat Jeffrey over déze prospect spreekt, terwijl alle 290 pagina's hetzelfde bestand delen. Zolang dat zo staat, is de hele pagina één opmerkzame prospect verwijderd van instorten. Niet omdat de video slecht is, maar omdat de pagina zijn geloofwaardigheid volledig op eerlijkheid over detail heeft gebouwd. Eén aantoonbaar onware zin in de eerste sectie maakt elke bronvermelding daarna verdacht.

Wat er wél staat is zeldzaam: rust, geen marketingtaal, een kleurpalet dat klopt, en één werkelijk originele vormvondst in de journey-lijn. Dat is een fundament waar de meeste bureaus niet in de buurt komen. De afstand tot wereldklasse zit niet in het ontwerp — die zit in het herverdelen van gewicht naar akt 2, het personaliseren van de brug, en het net zo serieus nemen van de laatste twintig procent als van de eerste tachtig.
