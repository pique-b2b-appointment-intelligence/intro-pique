# Schrijfopdracht: inhoud per Buiten-Goed-pagina

Je schrijft de tekst voor persoonlijke landingspagina's van **Buiten-Goed** uit Barneveld.
De vorm staat al. Jij levert per prospect één bestand `inhoud/<slug>.json`, en een script
zet dat in de pagina. Je raakt geen HTML aan.

## Wie spreekt

**Anne** van Buiten-Goed, familiebedrijf sinds 1987, Marchandweg 4 Barneveld. Zij levert
tuinkassen, serres, oranjerieën, overkappingen, veranda's, vouw- en schuifwanden,
lichtstraten en zonwering, met een eigen montagedienst en maatwerk zonder meerprijs. Ze
voeren Solarlux, ACD, Janssen, Warema, Hillhout, Pext en Hoklartherm. De lezer is een
hovenier, architect of aannemer die dit soort bouwsels voor zijn eigen klant intekent.

**Wij of ik.** *Wij* voor alles wat Buiten-Goed doet en levert. *Ik* voor wat Anne zelf
zag, dacht en vraagt. Dat één iemand gekeken heeft, is de reden dat de pagina werkt.

## Waar je uit put

Je krijgt per prospect het onderzoeksdossier. Daarin staan een trigger met bron en datum,
een onderbouwing met bron, en een lange opmerking van de onderzoeker. **Alles wat je
schrijft moet daarop terug te voeren zijn.** Verzin geen project, geen getal, geen datum
en geen citaat.

## Het bestand

```json
{
  "voornaam": "Yuri",
  "waarom_jij": "...",
  "watdit_onderwerp": "het glas in jullie tuinen",
  "bevindingen": [
    { "hier": true, "wat": "...", "citaat": "...", "bron": "hoogendijkhoveniers.nl", "datum": "projectpagina Loungen in weer en wind" },
    { "wat": "...", "bron": "...", "datum": "14 september 2026" }
  ],
  "pivot": "...",
  "betekent_kop": "Jij hebt het uit te leggen.",
  "betekent": "... <strong>één zin die het hardst aankomt</strong>",
  "pull": "...",
  "voorstel": "..."
}
```

`inhoud/hoogendijk-hoveniers.json` is het uitgewerkte voorbeeld. Lees dat eerst.

### Per veld

**waarom_jij** (2 tot 4 zinnen). Waarom Anne juist dit bedrijf aanschreef. Begin bij wat
zij zocht, en noem dan het ene ding bij deze prospect waardoor ze bleef hangen. Dit is de
enige plek waar je over de hele groep mag praten.

**watdit_onderwerp** (een paar woorden). Vult de zin *We willen je spreken over ...*.
Bijvoorbeeld `het glas in jullie tuinen` of `de serres die jullie nu elders inkopen`.

**bevindingen**: **twee of drie, nooit meer en nooit opgevuld tot drie.** Heeft het
dossier er maar twee die standhouden, lever er twee. Per bevinding:
- `wat` is één zin, in de je-vorm, over wat je zag. Geen analyse en geen conclusie.
- `citaat` is **optioneel** en alleen toegestaan als het dossier de zin letterlijk geeft.
  Staat er in het dossier dat de datum uit de broncode komt of dat de bron niet
  nagetrokken is, laat het citaat dan weg en gebruik alleen bron en datum. Liever twee
  bevindingen zonder citaat dan drie met een citaat dat niet klopt.
- `bron` is het kale domein, zonder https en zonder pad.
- `datum` is een dagdatum als die er is (`14 september 2026`), anders de vindplaats
  (`projectpagina Loungen in weer en wind`, `werken bij, bekeken 14 oktober 2026`).
- `hier: true` bij de bevinding die er het meest toe doet. Precies één per pagina.

**pivot** (2 tot 3 zinnen, handschrift op een papiertje). Wat de drie bevindingen bij
elkaar betekenen voor dít bedrijf. Geen algemene waarheid over hoveniers.

**betekent_kop** en **betekent**. Wat het hem kost zolang het blijft zoals het is.
Concreet, in zijn werkelijkheid: een oplevering die schuift, een klant die belt, een maat
die niet klopt. Eén `<strong>`-span om de zin die het hardst aankomt, verder geen HTML.

**pull**. Eén zin die blijft hangen. Het sjabloon zet er zelf aanhalingstekens omheen,
dus schrijf hem zonder.

**voorstel** (één zin). Wat Buiten-Goed concreet doet. Mag per prospect verschillen in
wat vooropstaat: maatwerk, eigen montage, de showroom, of één aanspreekpunt.

## Het verschil tussen hout en glas

Zegt het dossier dat deze prospect zijn overkappingen **zelf in hout bouwt**, met een
eigen werkplaats of timmerman, dan is hij in hout een concurrent en gaat de pagina over
glas: tuinkassen, serres, oranjerieën, vouw- en schuifwanden en lichtstraten. Noem dat
hout dan gewoon, zonder er omheen te draaien. Koopt hij alles in, dan ligt het hele
assortiment open.

## Schrijfregels, hard

- Geen gedachtestreepjes, geen puntkomma's, geen uitroeptekens, geen dubbele
  aanhalingstekens.
- Geen zin die begint met Geen, Niet, Juist of Precies.
- Nooit `niet X, maar Y` of `geen X, maar Y`. Zeg direct wat het wel is.
- Verbrande zinnen die nergens mogen staan: *waar het op uitkomt*, *ze horen bij elkaar*,
  *dit wordt geen verkoopgesprek*, *de prijs van stilzitten*, *het enige dat*.
- Geen cursief. Accent leg je met gewicht.
- Schrijf zoals iemand praat die twintig minuten naar dit bedrijf heeft gekeken. Geen
  marketingtaal, geen drieslagen om de drieslag.

## Controleren

Elke pagina gaat straks langs `tellscan.py` en `ailint.py`. Twee dingen die daar
struikelen en die je zelf kunt voorkomen: dezelfde zinswending bij meerdere prospects, en
symmetrische drietallen. Je schrijft voor acht bedrijven, dus varieer je openingen.
