# Opvolging scanners (nieuwe ronde) — instructie

Nog 7 mensen hebben je pagina gescand. Zo zet je in twee minuten de persoonlijke opvolgmails klaar. Het script verstuurt niets zelf: het zet per persoon een concept in jouw Gmail, vanuit jouw adres. Jij leest na en verstuurt.

## Als je het script nog niet had draaien
1. Open je Google Sheet (of maak een nieuwe).
2. Nieuw tabblad, noem het exact **Opvolging**.
3. Importeer **Opvolging-Batch3-Data.csv** in dat tabblad (Bestand -> Importeren -> Uploaden -> 'Gegevens vervangen op huidig blad'). Kopregel op rij 1.
4. Extensies -> Apps Script -> plak de inhoud van **OpvolgConcepten.gs** -> opslaan.
5. Ververs de Sheet (F5). Menu **BCS opvolging -> Zet concepten klaar**. Eerste keer: toestemming geven.
6. De 7 concepten staan nu in je Gmail bij Concepten. Nalezen en versturen.

## Als het script al in je Sheet zit
Je kunt de 7 nieuwe rijen gewoon **onder je bestaande Opvolging-tabblad plakken** (zonder de kopregel) en opnieuw op **Zet concepten klaar** klikken. Rijen die al 'concept klaar' staan slaat hij over, dus alleen de nieuwe worden gemaakt.

## Over de e-mailadressen
Waar het adres een sterke inschatting is (patroon), staat dat in de kolom email_status. Krijg je een bounce, dan staat het juiste alternatief in de kolom **email_alt**: zet dat in de kolom **email**, maak de status-cel van die rij leeg en draai opnieuw.

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
