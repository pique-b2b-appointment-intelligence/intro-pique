# BCS Batch 3 - Handgeschreven brieven (mail-merge CSV)

Verzendsheet voor de handgeschreven Pique/Backbone-kaarten met QR-code naar de persoonlijke landingspagina.

## Selectie

Alleen prospects met **100% geverifieerde beslissernaam én 100% geverifieerd postadres**. Van de 300 TIER1-prospects voldoen er **247** aan die eis. De overige 53 (40 met doelrol 'naam volgt', 13 zonder hard adres) staan bewust niet in deze sheet.

## Aantallen

| | |
|---|---|
| Rijen (brieven) | 247 |
| Kolommen (canoniek) | 17 |
| Met geverifieerde beslisser | 247 (100%) |
| Met geverifieerd adres + huisnummer | 247 (100%) |
| Brieftekst eindigt op 'Jeffrey' | 247 (100%) |
| Em-dashes / 'Geen'-zinstarts / 'niet X maar Y' | 0 |

## Pijplijn (Pique-agents)

1. **handgeschrevenbrieven-agent** schreef per prospect de kaart-opening: één concrete observatie uit de geverifieerde hook, die de nieuwsgierigheid opent zonder de uitkomst te verklappen (50 batches, 4 waves).
2. Vaste kaartopbouw eromheen: opening + de verplichte scan-zin ('Ik ben daarna nog wat dieper in [bedrijf] gedoken...') + ondertekening **Jeffrey**.
3. **brieven-csv-agent**-structuur toegepast: 17 canonieke kolommen, naam- en adressplitsing, aanhef 'Hoi [voornaam]', link + unieke_url per prospect.
4. **quality-agent**-sweep: copyregels, kolomtelling, scan-zin, ondertekening, adresvolledigheid.

## Afwijking van de agent-default (op jouw verzoek)

De brieftekst eindigt hier bewust op de afzendernaam **Jeffrey** (de brieven-csv-agent houdt de ondertekening normaal buiten het brieftekst-veld). Zo staat de naam gegarandeerd onder elke kaart.

## Kolommen

`voornaam, achternaam, aanhef, straatnaam, huisnummer, toevoeging, postcode, plaatsnaam, land, brieftekst, link, unieke_url, functie, bedrijf, beslisser_bron, beslisser_status, notitie`

De QR-code op elke kaart wijst naar `link` (intro-pique.agency/bcs3/[slug]).

## Correcties tijdens QC

- **Stricters**: huisnummer aangevuld naar Korte Stadionweg 103a (geverifieerd via stricters.com/contact).
- **Minimalism Fashion**: oud adres (Cranenburgsestraat, 6561 AM) bleek verouderd; gecorrigeerd naar het actuele Stekkenberg 95, 6561 XH Groesbeek (eigen site + KVK 72331585).

## Bestand

`Klanten/BCS/BCS-Batch3-Brieven-CSV.csv` (UTF-8, 247 rijen + header).

## Volgende stap

Sheet is klaar voor de handschrijf-/printpartij. De 40 'naam volgt'-prospects kunnen later via KVK-uittreksel worden aangevuld en toegevoegd.
