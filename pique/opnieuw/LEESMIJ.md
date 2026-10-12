# Heractivatie: mensen met wie al gesproken is

Batch oktober 2026, twaalf pagina's. De selectie komt uit
`Leads/Heractivatie-Gesproken/Gesproken-Bedrijven-okt2026.csv` en is door Simon
teruggebracht tot deze twaalf.

Live op `intro-pique.agency/pique/opnieuw/<slug>`.

| sleutel | bedrijf | wie | waarom hij op de lijst staat |
|---|---|---|---|
| audion | Audion Packaging Machines | Michel van der Feer | afspraak gehad, daarna stil |
| twinfloor | Twinfloor | Albert den Boer | terugbeldag 14 sep gemist |
| sweere | Sweere | Theo Sweere | één gesprek, daarna niets |
| ash | ASH Carrosserie | Roel Maas | terugbeldag 2 sep gemist |
| unica | Unica | Susan de Vree | gaf de feedback die de triggerpoort opleverde |
| bonotech | BonoTech Bedrijfswagens | Arjan Bonouvrie | gesprek 22 sep, niets vastgelegd |
| vervaet | Vervaet | Jonathan Hoekman | gesprek 4 sep, opname zonder geluid |
| nederburgh | Nederburgh | Daniel Medina Diaz | offerte op duizend brieven, te duur |
| acendae | Acendae | Pramuka Godakanda | met een andere partij gestart |
| jrfinance | JR Finance | Jason Ramkisoen | was nog niet toe aan acquisitie |
| finovion | Finovion | Wichard Hendriks | andere prioriteiten, wil contact in december |
| studiorendement | Studio Rendement | Tjerk Moraal | zat vol, prijs was het probleem niet |

## Wat deze paginavorm anders doet

Deze mensen hebben de eerste pagina al gezien, dus een tweede ronde research werkt
hier niet. Vier dingen wijken af van een gewone LP:

1. **De aanloop is een bekentenis.** Wat er verstuurd is, wat zij deden, en wat er
   daarna van onze kant uitbleef. Bij Twinfloor en ASH staat de gemiste terugbeldag
   er met datum bij. Bij Bonotech en Vervaet staat er dat het gesprek nergens is
   vastgelegd, want dat is zo.

   **Alleen bij Nederburgh was prijs het bezwaar.** Simon corrigeerde dat op 6 oktober:
   Acendae is met een andere partij gestart, JR Finance was nog niet toe aan acquisitie
   en Finovion had andere prioriteiten en wil in december terug. Die drie pagina's gaan
   dus niet over geld. De Acendae-pagina erkent de andere partij en biedt de staffel aan
   voor als dat traject afloopt, zonder iets van die keuze te vinden.
2. **Bevinding 01 citeert hun eigen kaart**, met de scandatum eronder. Dat is de enige
   bron die de ontvanger letterlijk op zijn bureau kan naleggen.
3. **De staffel staat op de pagina.** Dat is de reden van deze batch: ze hoeven niet te
   bellen om te weten wat het kost.
4. **De VSL staat onderaan, vlak voor de CTA.** Eén minuut, liggend, en hij staat stil
   tot iemand hem start (`preload="none"`).

Twee bewuste afwijkingen van `_voorbeeld.html`:

- **De videoknop in de hero is eruit.** Twee video's op één pagina laat de lezer kiezen
  welke hij overslaat. De VSL doet nu dat werk, onderaan.
- **Het blok met de drie stappen (kaart, pagina, agenda) is eruit.** De VSL legt precies
  diezelfde drie stappen uit. Het blok met de drie voorwaarden eronder staat er wel nog.

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
