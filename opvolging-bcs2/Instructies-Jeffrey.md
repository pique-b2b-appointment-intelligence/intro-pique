# Opvolging scanners — instructie

Zo zet je in een paar minuten de persoonlijke opvolgmails klaar. Het script verstuurt niets zelf: het zet per persoon een concept-mail in jouw Gmail, vanuit jouw adres. Jij leest ze na en verstuurt.

## Wat je nodig hebt (de bijlagen)
1. **Opvolging-Data.csv** — de 10 mensen met e-mail, de observatie per bedrijf en de link naar hun persoonlijke pagina.
2. **OpvolgConcepten.gs** — het scriptje dat de concepten maakt.

## Stap voor stap
1. Ga naar sheets.google.com en maak een nieuwe Google Sheet.
2. Noem het eerste tabblad **Opvolging** (dubbelklik op de tabnaam onderin).
3. Open **Opvolging-Data.csv** en zet de inhoud in dat tabblad: Bestand → Importeren → Uploaden → kies het CSV-bestand → 'Gegevens vervangen op huidig blad' → Importeren. De kopregel moet op rij 1 staan.
4. Ga naar **Extensies → Apps Script**. Wis wat er staat, plak de volledige inhoud van **OpvolgConcepten.gs**, en klik op opslaan (het diskette-icoon).
5. Ga terug naar de Sheet en ververs de pagina (F5). Er verschijnt bovenin een menu **BCS opvolging**.
6. Klik **BCS opvolging → Zet concepten klaar**. De eerste keer vraagt Google om toestemming: doorlopen en toestaan (het is je eigen script in je eigen account).
7. Klaar. De concepten staan nu in je Gmail bij Concepten, elk vanuit jouw adres en met de juiste naam en observatie. Lees ze na en verstuur.

## Over de e-mailadressen
Van 5 mensen is het persoonlijke adres een sterke inschatting, geen 100% zekerheid. Krijg je een bounce (mail komt retour), dan staat in de sheet in de kolom **email_alt** het juiste alternatieve adres. Vervang het adres in kolom **email** door dat alternatief en draai het script opnieuw (rijen die al 'concept klaar' staan slaat hij over, dus zet die ene status-cel eerst leeg).

## De mail die eruit komt
> Hoi [naam],
>
> Ik stuurde je laatst een handgeschreven kaart met een QR-code. Ik zag dat je 'm hebt gescand en de pagina hebt bekeken. Leuk, daar werd ik nieuwsgierig van.
>
> Die pagina maakte ik voor [bedrijf] omdat me iets opviel: [observatie]. Daar zou ik het graag eens kort met je over hebben.
>
> Zullen we een keer vijftien minuten bellen? Dan laat ik zien wat ik precies bedoel. Komt bellen niet uit, dan hoor ik het ook.
>
> Groet,
> Jeffrey
