# Heractivatie: mensen met wie al gesproken is

Batch oktober 2026. De selectie komt uit
`Leads/Heractivatie-Gesproken/Gesproken-Bedrijven-okt2026.csv`.

**Live staan er drie, op de v12-standaard** (12 oktober 2026):

- https://intro-pique.agency/pique/opnieuw/finovion (Wichard Hendriks)
- https://intro-pique.agency/pique/opnieuw/jr-finance (Jason Ramkisoen)
- https://intro-pique.agency/pique/opnieuw/studio-rendement (Tjerk Moraal)

De negen andere pagina's uit deze batch stonden nog op v2 en zijn van schijf gehaald.
Ze zijn met één commando terug: `python3 bouw.py <sleutel>`, daarna de omzetter en
`na-omzetten.py`. De sleutels staan in `PROSPECTEN`.

## De bouwketen, drie stappen

    python3 bouw.py finovion jrfinance studiorendement
    python3 ../../../../Context/tools/lp-v12-omzetter.py . --schrijf
    python3 na-omzetten.py

Stap twee zet de v2-opbouw om naar v12: dossier, wat-dit-paneel, brug, donkere band.
**Stap drie is niet optioneel.** De omzetter hangt een vast paneel in met de regel
'we hebben je nooit eerder gesproken', en dat is bij deze batch onwaar. `na-omzetten.py`
vervangt die zin per pagina door wanneer er wél gesproken is.

## Wat deze pagina's anders doen dan een koude v12

1. **De aanloop is een bekentenis.** Wat er verstuurd is, wat zij deden, en wat er daarna
   van onze kant uitbleef.
2. **De staffel staat op de pagina**, als eigen kapittel in het betoog, vlak voor het
   kantelpunt. Dat is de reden van deze batch: ze hoeven niet te bellen om de prijs te
   weten.
3. **De maquettekaart is naamloos.** odido-v12 zet de naam van de ontvanger zelf op die
   kaart terwijl de bijschriften eronder over 'zijn bureau' gaan. tellscan vangt dat
   terecht als derde persoon. Hier staat er 'Hoi Jan' op en ondertekent het bedrijf van
   de ontvanger zelf.

Drie dingen uit de v12-standaard zijn bewust overgenomen zoals ze zijn: de vaste hero-kop,
de vaste kop van het eerste hoofdstuk en het vaste founderblok. Dat laatste betekent dat
de uitzondering van 6 oktober, waarbij het voorstelblok wegviel bij mensen die Simon
persoonlijk kent, is vervallen.

## De tarieven

Simon, 6 oktober 2026: we hanteren nu lagere prijzen, en acquisitie op deze manier kan al
vanaf één à twee mille per maand. Dat getal zit in de onderste regel hieronder.

Bron is `Leads/De-Rooij-Montage/voorstel-de-rooij-montage.html` (getekend), aangevuld met
`Leads/STILL/voorstel-still.html` en `Componenten/voorstel-pagina/otto.json`.
`pique.agency/tarieven` bestaat niet meer en zet door naar `/contact`.

Validatietraject van twee maanden, per maand, exclusief btw:

- 50 per maand: **1.625 zelf bellen**, 2.875 met nabellen. Per benadering 32,50 / 57,50.
- 100 per maand: 2.750 zelf, 4.750 met nabellen. Per benadering 27,50 / 47,50.
- 200 per maand: 4.500 zelf, 7.500 met nabellen. Per benadering 22,50 / 37,50.

Ga je daarna door, dan loopt het per kwartaal en zakt het verder: 100 per maand wordt
3.750 met nabellen en 2.150 zelf. Zelf bellen betekent altijd geen afspraakgarantie.

Het tarief per benadering loopt omhoog als het aantal daalt, want de voorbereiding krimpt
niet mee met de order. Zeg dat erbij, anders leest de bovenste regel als een boete.

Kloppen deze getallen niet meer, pas dan `TARIEVEN` in `bouw.py` aan. Hij staat op een
plek. De volle context staat in het geheugen onder `reference-staffel-okt2026`, inclusief
het aparte tarief voor een eigen klantbestand (Drukwerkdeal, vanaf 5,00 per benadering).

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
