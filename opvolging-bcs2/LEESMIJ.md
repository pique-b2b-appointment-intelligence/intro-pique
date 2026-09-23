# BCS opvolging batch 2 - concept-mails per scan

Opvolging voor de 9 batch-2 prospects die de landingspagina scanden. Afzender = **Jeffrey** (consistent met de kaart, de video op de pagina en wie de call doet). Het script verstuurt niets zelf: het zet per scan een persoonlijke **concept-mail** klaar in Gmail, die Jeffrey (of jij via send-as) nakijkt en verstuurt.

## Bestanden

- `Opvolging-Data.csv` - de 9 prospects met e-mail, observatie en LP-link. Plak dit in een Google Sheet-tabblad met de naam `Opvolging`.
- `OpvolgConcepten.gs` - het Google Apps Script. Extensies -> Apps Script, plakken, draaien vanuit de Backbone-mailbox.

## Het template (Jeffrey)

Onderwerp: `Ik stuurde je laatst een kaartje`

```
Hoi [voornaam],

Ik stuurde je laatst een handgeschreven kaart met een QR-code. Ik zag dat je 'm hebt gescand en de pagina hebt bekeken. Leuk, daar werd ik nieuwsgierig van.

Die pagina maakte ik voor [bedrijf] omdat me iets opviel: [observatie]. Daar zou ik het graag eens kort met je over hebben.

Zullen we een keer vijftien minuten bellen? Dan laat ik zien wat ik precies bedoel. Komt bellen niet uit, dan hoor ik het ook.

Groet,

Jeffrey
```

## Werkwijze

1. Zet de 9 rijen uit `Opvolging-Data.csv` in een Sheet-tabblad `Opvolging` (kolomkoppen op rij 1).
2. Open Apps Script, plak `OpvolgConcepten.gs`, vul bij `verzendAls` eventueel het Backbone-adres in (alleen als dat als 'Verzenden als' in Gmail staat).
3. Draai het vanuit het account dat de mails stuurt. Menu `BCS opvolging` -> `Zet concepten klaar`.
4. Het script maakt per gescande, nog-niet-opgevolgde rij een concept, en zet `opvolg_status` op `concept klaar [datum]`. Rijen met een status worden overgeslagen, dus opnieuw draaien bij nieuwe scans kan gewoon.
5. Check elk concept in Gmail en verstuur zelf.

## Let op: e-mailadressen

De meeste directe adressen zijn **patroon-afgeleid** (voornaam@domein, afgeleid van een bevestigd bedrijfspatroon), niet 100% geverifieerd. Ze kunnen bouncen. Per rij staat een generiek fallback-adres in `email_alt`. Overweeg voor de zekerheid eerst een e-mailvalidatie, of stuur naar het fallback-adres als het directe adres bounct.

Domein-correcties uit de research:
- The Souks -> thesouks.com (niet .nl)
- Renske Natural Petfood -> renske.com (niet natuurlijkrenske.nl)
- Passion for Linen -> direct adres via moederbedrijf homelinenlabels.com; consumentenfallback info@passionforlinen.com
- Noubased -> alleen generiek info@noubased.com bekend (geen persoonlijk adres gepubliceerd)

Beslisser-namen komen uit jouw lijst; Amber V. = Amber Veraar (Dr. Jetske Ultee, bevestigd op teampagina).

## Waarom concepten en niet automatisch versturen

Elke mail leunt op de persoonlijke observatie per bedrijf. Een blinde bulkverzending haalt precies de Pique-waarde eruit. Concept-klaarzetten houdt de kwaliteit en de controle bij Jeffrey, en houdt de afzender-reputatie schoon bij lage, warme volumes.
