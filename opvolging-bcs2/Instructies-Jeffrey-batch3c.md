# Opvolging scanners - nieuwe ronde (27 mensen)

Weer een groep die je kaart scande en de pagina bekeek. Zo zet je in twee minuten de persoonlijke opvolgmails klaar. Het script verstuurt niets zelf: het zet per persoon een concept in jouw Gmail, vanuit jouw adres, ondertekend Jeffrey. Jij leest na en verstuurt.

Onderwerp per persoon: **Je keek even, [voornaam]**.

## Als je het script nog niet had draaien
1. Open je Google Sheet (of maak een nieuwe).
2. Nieuw tabblad, noem het exact **Opvolging**.
3. Importeer **Opvolging-Batch3c-Data.csv** in dat tabblad (Bestand -> Importeren -> Uploaden -> 'Gegevens vervangen op huidig blad'). Kopregel op rij 1.
4. Extensies -> Apps Script -> plak de inhoud van **OpvolgConcepten-Batch3c.gs** -> opslaan.
5. Ververs de Sheet (F5). Menu **BCS opvolging -> Zet concepten klaar**. Eerste keer: toestemming geven.
6. De concepten staan nu in je Gmail bij Concepten. Nalezen en versturen.

## Als het script al in je Sheet zit
De tekst is bijna gelijk aan de vorige ronde, alleen het onderwerp is nu 'Je keek even, [voornaam]'. Vervang de inhoud van je Apps Script door **OpvolgConcepten-Batch3c.gs** (opslaan), plak de nieuwe rijen onder je bestaande Opvolging-tabblad (zonder de kopregel) en klik opnieuw op **Zet concepten klaar**. Rijen die al 'concept klaar' staan slaat hij over, dus alleen de nieuwe worden gemaakt.

## Let op: 1 naam ontbreekt
Bij **DesignSpiegels.nl** staat alleen 'A.S. Sijmons', geen voornaam. Die rij slaat het script bewust over (het onderwerp leunt op de voornaam). Weet je de voornaam? Vul 'm in kolom voornaam in, maak de cel in kolom opvolg_status leeg en draai opnieuw. Zo niet, dan laat je die staan.

## Over de e-mailadressen
Alle 27 adressen zijn geverifieerd en de mailservers (MX) doen het, dus bounces zijn onwaarschijnlijk. Waar ik een persoonlijk adres zeker wist, gebruik ik dat (Baltazar, MIGLOT, DUN, Overload). De rest gaat naar het officiele adres dat op de site staat. Krijg je toch een bounce, dan staat in kolom **email_alt** een alternatief: zet dat in kolom **email**, maak de status-cel leeg en draai opnieuw.

Twee om te weten:
- **De Chocopastawinkel** loopt via de klantenservice van moederbedrijf De Pindakaaswinkel (anna@depindakaaswinkel.nl). De mail is aan Michiel gericht, maar komt op die inbox binnen.
- **Queen Tarzi** (manizha@queentarzi.com) is het enige adres dat niet 100% bevestigd is. Bouncet 'ie, gebruik dan support@queentarzi.com uit email_alt.

## De mail die eruit komt
> Onderwerp: Je keek even, [voornaam]
>
> Hoi [voornaam],
>
> Ik stuurde je laatst een handgeschreven kaart met een QR-code. Ik zag dat je 'm hebt gescand en de pagina hebt bekeken. Leuk, daar werd ik nieuwsgierig van.
>
> Die pagina maakte ik voor [bedrijf] omdat me iets opviel: [observatie]. Daar zou ik het graag eens kort met je over hebben.
>
> Zullen we een keer vijftien minuten bellen? Dan laat ik zien wat ik precies bedoel. Komt bellen niet uit, dan hoor ik het ook.
>
> Groet,
>
> Jeffrey
