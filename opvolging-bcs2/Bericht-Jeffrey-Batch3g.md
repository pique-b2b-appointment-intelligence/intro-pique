# Voor Jeffrey — opvolgconcepten batch 3g (15 nieuwe scanners)

Hoi Jeffrey,

15 prospects hebben de kaart gescand en de pagina bekeken, maar hadden nog geen opvolgmail. Hieronder staat alles klaar om er in één keer concepten van te maken in je Gmail. Het script verstuurt niets zelf, jij checkt en drukt op verzenden.

## Installeren (2 minuten)
1. Open de Google Sheet en ga naar (of maak) het tabblad **Opvolging**.
2. Importeer **Opvolging-Batch3g-Data.csv** in dat tabblad (Bestand → Importeren → Huidig blad vervangen, kopregel op rij 1).
3. Extensies → Apps Script → plak **OpvolgConcepten-Batch3g.gs** → opslaan.
4. Draai vanuit het account dat als **Jeffrey** verstuurt.
5. Menu **BCS opvolging → Zet concepten klaar**. Eerste keer even rechten geven.
6. Check je 15 concepten in Gmail en verstuur ze zelf.

## Adressen — wat je moet weten
- **2 persoonlijke adressen** (mail gaat direct naar de persoon, geen 'T.a.v.'-regel):
  - FitPreps → **boy@fitpreps.nl** (staat als zakelijke inbox op hun site)
  - Vitals → **patricia@vitals.nl** (patroon voornaam@vitals.nl hard bevestigd)
- **13 generieke adressen** (info@/hello@/support@ ...): daar zet het script automatisch een **'T.a.v. [naam]'**-regel bovenaan, zodat de mail bij de juiste persoon komt. Het persoonlijke adres staat als fallback in de kolom `email_alt` mocht een generiek adres bouncen.

## Even checken vóór verzenden (3 namen zijn onzeker)
De handgeschreven kaart ging naar deze namen, maar publieke bronnen wijzen een andere eigenaar/beslisser aan. Verifieer de aanhef, of pas 'm aan, voordat je verstuurt:
- **Ekomenu — 'Chris de Vries'**: bronnen noemen **Jack Stroeken** als founder/CEO. Chris kwam binnen via de Willem&Drees-fusie; rol onbevestigd.
- **IK Skin Perfection — 'Pien Pruijsers'**: oprichter volgens bronnen = **Petra Sanderman** (merk onder Summery Cosmedical Group). Pien niet aan het merk te koppelen.
- **Little Indians — 'Kelly'**: geen 'Kelly' te vinden; eigenaar is vrijwel zeker **Vanessa Erasmus**. Deze zou ik zeker even checken.

## Kleine extra's
- **Vitals**: patricia@ is klantenservice. Wil je liever de directie? Dan **willem@vitals.nl** (CEO) — staat ook letterlijk op hun contactpagina.
- **Domeinen die afweken** van wat je zou verwachten (fyi, adressen zijn al goed in de CSV): juicebro.com, eatdustclothing.com, coiscycling.com, gaevdd.com, imaginjewels.com, fraenck.com, monkandanna.com, ik-skinperfection.nl.

## De 15 op een rij
| Bedrijf | Naam | Adres | Type |
|---|---|---|---|
| Botanical Beauty | Catharine | info@botanicalbeauty.nl | generiek + t.a.v. |
| Juicebrothers | Cécile | info@juicebro.com | generiek + t.a.v. |
| FitPreps | Boy | boy@fitpreps.nl | persoonlijk |
| Eat Dust | Rob | info@eatdustclothing.com | generiek + t.a.v. |
| Çois Cycling Legacy | Tom | hello@coiscycling.com | generiek + t.a.v. |
| GAEV Dutch Design | Mary | klantenservice@gaevdd.com | generiek + t.a.v. |
| I.Ma.Gi.N jewels | Gilles | info@imaginjewels.com | generiek + t.a.v. |
| Nel | Jorrit | groetenvan@nel.nl | generiek + t.a.v. |
| Fraenck | Ratna | contact@fraenck.com | generiek + t.a.v. |
| Monk en Anna | Simone | info@monkandanna.com | generiek + t.a.v. |
| Vulpes Goods | Tomas | info@vulpesgoods.com | generiek + t.a.v. |
| Ekomenu | Chris (check) | klantenservice@ekomenu.nl | generiek + t.a.v. |
| IK Skin Perfection | Pien (check) | support@ik-skinperfection.nl | generiek + t.a.v. |
| Little Indians | Kelly (check) | service@little-indians.nl | generiek + t.a.v. |
| Vitals | Patricia | patricia@vitals.nl | persoonlijk |

Groet,
Simon
