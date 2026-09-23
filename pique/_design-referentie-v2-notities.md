# LP-design v2: wat er anders is en waarom

Bestand: `Klanten/BCS/pique/_design-referentie-v2.html`
Vergelijk met: `Klanten/BCS/pique/odido.html` (dezelfde inhoud, oude vorm)
`?nointro` achter de URL slaat de kaartlaag over. Handig bij QC.

## De diagnose in één zin

De kaart doet al het zware werk, en de pagina begint daarna opnieuw bij nul.

## 1. De kaart verdwijnt niet meer, hij landt in de pagina

Was: de kaartlaag faded naar zwart en weg. Daarna een compleet ander scherm.
Nu: de kaart vliegt naar zijn plek in de hero en blijft daar liggen, met het label
'De kaart op je bureau'. Het voorwerp in hun hand wordt het voorwerp op het scherm.

Dit is de belangrijkste verandering. Alles wat de kaart aan geloofwaardigheid opbouwt,
werd bij de oude overgang weggegooid.

## 2. Van vier openingen naar één

Was: kaartlaag, dan hero, dan 'Waarom je dit ziet', dan 'Bij X. Drie dingen die me
opvielen'. Vier keer aanloop voordat er één bevinding staat.
Nu: hero, één korte aanloop die eindigt op 'Dit is wat ik vond', dan meteen bevinding 01.

## 3. Bevindingen zijn papiertjes met het bewijs erop geplakt

Was: nummertje, kop, alinea, en een grijze regel 'Bron: newsroom.odido.nl, januari 2026'.
Nu: een papiertje met eigen papierkleur, scheef, met plakband erboven en een schaduw die
er onderuit krult. Het nummer staat er met de hand, de kop is met de hand onderstreept.
Het citaat is een uitgeknipt stukje met een gescheurde onderrand, met tape opgeplakt,
met het domein en de datum eronder.

Geen ronde hoeken, geen nette shadow-token, geen 'card'. Het verschil tussen ontworpen
en neergelegd.

Het citaat staat al in de research (triggercheck.py toetst erop dat het er letterlijk
staat). Dat bewijs werd alleen nooit getoond. Een bronregel is een bewering, een citaat
met datum is bewijs. Dat is de goedkoopste geloofwaardigheidswinst op de hele pagina.

Het label 'zelf nagelezen' stond hier eerst bij en is er weer uit.

## 4. Handgeschreven kantlijnnotities

Op desktop stond 60 procent van het doek leeg naast een kolom van 400px. Daar staan nu
twee notities in Caveat, hetzelfde handschrift als de kaart. Ze verbinden de bevindingen
('en dit maakt de eerste twee urgent'). Het leest als een dossier waar iemand in gewerkt
heeft, en het is het tegengif tegen de sjabloonindruk.

Twee per pagina, niet meer. Ze moeten iets zeggen, niet versieren.

## 5. Het belaanbod staat halverwege, in de lijn en niet erboven

Een echte pop-up over de tekst heen was hier de verkeerde keuze. Dat is precies wat de
kaart probeert te weerleggen. In plaats daarvan:

- Direct na het kantelpunt, op het punt waar het kwartje valt, staat in handschrift
  'Zal ik je hier gewoon even over bellen?' met drie uitwegen: plannen, eerst lezen,
  of nummer achterlaten.
- Daaronder verschijnt een rustige dock onderin beeld, pas ná het kantelpunt, dus verdiend.
  Wegklikbaar en hij blijft weg.

Functioneel is dit de pop-up die je wilde. Alleen onderbreekt hij het lezen niet.

## 6. Cal.com laadt pas als iemand hem opent

Was: een iframe van 640px hoog, altijd geladen, in stock cal.com-stijl, op elke scan.
Nu: een sheet met twee tabs. 'Zelf een moment kiezen' laadt cal pas bij openen.
'Laat mij terugbellen' is een eigen formulier van twee velden plus vier tijdvakken.

Het terugbelformulier is er omdat een agenda-embed vraagt om een besluit over een
specifiek tijdstip. Een nummer achterlaten is een veel lagere drempel, en jij belt toch.
De submit-handler moet nog op een endpoint worden gehangen, nu toont hij alleen de
bevestiging.

## 7. Weten waar je bent

Rail links met vijf labels op desktop, dunne voortgangsbalk bovenaan op mobiel.
De lijn was mooi maar zei niet hoe ver het nog is. Een beslisser die niet weet hoeveel
er nog komt, stopt eerder.

Ook nieuw in de hero: '3 bevindingen', '2 minuten lezen', 'Alleen voor X geschreven'.

## 8. Video is een aanbod geworden

Was: een reel van 300px hoog met pulserende ring, badge en glow, midden in de hero,
boven de kop. Dat is veel druk voor iets wat niet iedereen wil.
Nu: een compacte rij met poster, 'Liever horen dan lezen? Simon vat het samen in 1 min 20'.
Klik opent de video in een overlay. Wie via 'Ja, laat maar zien' binnenkomt, krijgt hem
direct te zien.

Scheelt ook: de 9,6MB mp4 wordt niet meer boven de vouw ingeladen.

## 9. Nav-knop

Was: spookknop, rgba-tekst op een rgba-rand. Vrijwel onzichtbaar zodra de nav wit werd,
en het was de enige CTA boven de vouw.
Nu: gevulde amberknop.

## 10. Meten

Er zat nul meting op deze pagina's. Je weet wie scande (Lightr) en wie boekte (cal),
en niets daartussen.

`pqTrack()` bovenin het script stuurt stappen naar `window.PQ_TRACK_URL`:
kaart-uitgeschreven, intro-video, bevinding-1, kantelpunt, belaanbod-gezien, voorstel,
cta-gezien, sheet-geopend, terugbelverzoek, afspraak-geboekt.

Zonder URL loggen ze naar de console, dus hij is nu al veilig te draaien.

Dit is meer dan analytics. 'Las tot het eind en boekte niet' is het sterkste belsignaal
dat je kunt hebben, en Belcockpit sorteert al op signaalzwaarte. Hangt aan het
touchpoint-werk dat er ligt.

---

# Tweede ronde: minder AI, meer beeld

## 11. Fraunces in plaats van Playfair Display

Playfair met Inter is de standaardcombinatie van iedere gegenereerde pagina. Dat is de
tell, niet de kleuren of de lay-out. Fraunces heeft een SOFT- en een WONK-as, waardoor
de koppen net iets onregelmatig staan en gedrukt aanvoelen in plaats van gerenderd.
Body blijft Inter, want dat leest gewoon het beste.

Terugdraaien is één regel in de :root.

## 12. De tijdlijn in het kantelpunt

'Ze horen bij elkaar' was een bewering in tekst. Nu staan de drie data op één lijn:
sep 2023, 2026, jan 2026, en dan NU. Je ziet de drie lijnen samenkomen in plaats van
dat je het moet geloven. Op mobiel klapt hij naar verticaal.

De data staan al in je research, dus dit is generatief. Elke bevinding heeft een datum,
en die datums bij elkaar zijn het argument.

## 13. 'Wat ik voorstel' is nu een tastbaar ding

Was: drie tekstblokken die vertelden wat je zou doen. Nu drie mockups op een rij, met
een stippellijn ertussen:

1. De kaart, met echt handschrift en een scanbare QR-vorm erop
2. De pagina, in een browserframe met het adres pique.agency/.../zijn-bedrijf erin
3. De afspraak, als agendakaartje met datum en 'zelf ingepland'

Zelfverwijzend en daardoor sterk: 'een pagina zoals deze, alleen dan over zijn bedrijf'.
Wat je krijgt is nu te zien in plaats van te lezen.

De drie voorwaarden (beslissers niet de massa, exclusiviteit, één sprint) staan er
compact onder in plaats van als drie hoofdstukken.

## 14. De agenda laadt niet meer terwijl je wacht

Drie dingen tegelijk:

- 'Laat mij terugbellen' is nu de eerste tab. Twee velden en vier tijdvakken, direct
  bruikbaar. Een agenda vraagt om een besluit over een tijdstip, een nummer achterlaten
  vraagt bijna niks. En jij belt toch zelf.
- Cal.com begint met laden zodra iemand het kantelpunt passeert, dus ruim voordat hij
  op een knop kan drukken. De sheet staat dan nog buiten beeld maar heeft wel afmetingen,
  dus cal kan gewoon renderen. Openen voelt daardoor direct.
- In plaats van een spinner staat er een skelet van een maandkalender. Wachten voelt
  korter als je ziet wat er komt. Het skelet verdwijnt op cal's linkReady, met een
  vangnet van 12 seconden.

---

# Derde ronde

## 15. Echte handtekening onder het founder-blok

`handtekening.png` staat in de LP-map, bijgesneden op wat er echt staat en op 2x
opgeslagen voor scherpe schermen. Hij staat boven 'Simon Kempers, oprichter Pique' en
fade't mee met het blok. Bron was `Downloads/Handtekening_transparant-removebg-preview.png`.

## 16. Elke knop gaat naar zijn eigen tab

Was fout na de vorige ronde: 'Kies een moment' opende de terugbel-tab, omdat knoppen
zonder `data-tab` op de standaardtab landden. Nu heeft iedere knop een expliciete tab:

- Plan een gesprek (nav), Ja plan een gesprek (halverwege), Plannen (dock),
  Kies een moment (onderaan)  ->  agenda
- Laat je nummer achter (halverwege), Laat me terugbellen (onderaan)  ->  terugbelformulier

De agenda staat weer als eerste tab in de sheet, want daar wijzen de meeste knoppen heen.
De warme voorlading blijft, dus openen voelt nog steeds direct.

## 17. Zo krijg je het terugbelverzoek binnen

`Dashboard/Terugbelverzoek.gs` is een Apps Script-webapp op dezelfde Sheet als de rest.
Eén verzoek doet drie dingen tegelijk:

1. een regel in het tabblad 'Terugbelverzoeken', dus het staat vast en Belcockpit
   kan het oppikken
2. een mail, met het telefoonnummer in het onderwerp. Dat is expres: op je telefoon
   lees je in de melding al wie je moet bellen zonder de mail te openen
3. een WhatsApp, als je de CallMeBot-sleutel hebt ingevuld

WhatsApp kost twee minuten en geen account. Stuur op WhatsApp
"I allow callmebot to send me messages" naar +34 644 51 95 23, je krijgt een apikey
terug, en die zet je met je nummer in de scripteigenschappen. Laat je ze leeg, dan slaat
het script de WhatsApp stil over en blijft de mail werken.

Opzetten:
1. Sheet -> Extensies -> Apps Script -> bestand erbij plakken
2. Implementeren -> Web-app, uitvoeren als jezelf, toegang voor iedereen
3. de /exec-URL in de pagina zetten: `window.PQ_TERUGBEL_URL = '<url>'`
4. Scripteigenschappen: `TERUGBEL_MAIL`, en optioneel `WA_PHONE` + `WA_APIKEY`

Het formulier verstuurt met `Content-Type: text/plain`. Dat is bewust: daarmee is het een
simpele request en vraagt de browser geen preflight, wat een Apps Script-webapp toch niet
zou beantwoorden. Lukt fetch niet, dan gaat het alsnog met een beacon de deur uit, en de
bevestiging noemt info@pique.agency als uitweg.

Zolang `PQ_TERUGBEL_URL` leeg is, logt het formulier naar de console en toont het gewoon
de bevestiging. Veilig om nu al te draaien.

---

## Nog te doen voor dit de standaard wordt

- Terugbel-webapp implementeren en PQ_TERUGBEL_URL invullen (zie punt 17)
- PQ_TRACK_URL wijzen naar /api/t
- De sheet op desktop centreren in plaats van onderaan plakken
- Generator (`Context/tools/lp-generator-outreach-master-250/`) op dit template zetten,
  met citaat, domein en datum als velden per bevinding
- Klantvarianten: kleur en logo zijn tokens, de vorm blijft
