#!/usr/bin/env python3
"""Zet het 'wat dit is'-paneel recht na lp-v12-omzetter.py.

De omzetter hangt een vast paneel in met de regel 'we hebben je nooit eerder
gesproken'. Dat klopt voor een koude batch en is bij deze batch onwaar: met
iedereen op deze lijst is al gesproken. Eén onware zin op de plek waar de pagina
uitlegt wat hij is, haalt de rest onderuit.

Draaien na de omzetter:

    python3 bouw.py jrfinance studiorendement
    python3 ../../../../Context/tools/lp-v12-omzetter.py ../jr-finance.html --schrijf
    python3 ../../../../Context/tools/lp-v12-omzetter.py ../studio-rendement.html --schrijf
    python3 na-omzetten.py
"""
import re
import sys
from pathlib import Path

HIER = Path(__file__).parent.parent   # de pagina's staan in pique/

# Per pagina de zin die in de plaats komt van de koude variant. Hij benoemt
# wanneer er gesproken is en waarom er nu opnieuw een kaart ligt.
WAAROM = {
    "jr-finance.html":
        "We spraken elkaar op 1 juli, toen acquisitie bij jou nog niet aan de orde was. "
        "Dit is de tweede kaart, met de prijs erbij.",
    "studio-rendement.html":
        "We spraken elkaar in augustus via Aquila, en daarna bleef het liggen. "
        "Dit is de tweede kaart, nu met de prijs erbij.",
}

KOUD = ("We willen je spreken. Dit is acquisitie, we hebben je nooit eerder gesproken, "
        "en we doen het op een kaart omdat een mail van ons niet zou zijn opgevallen.")


def main() -> None:
    namen = sys.argv[1:] or list(WAAROM)
    for naam in namen:
        pad = HIER / naam
        if not pad.exists():
            print(f"  ontbreekt: {naam}")
            continue
        tekst = pad.read_text(encoding="utf-8")
        if KOUD not in tekst:
            staat_er = WAAROM[naam][:40] in tekst
            print(f"  {naam}: {'al rechtgezet' if staat_er else 'KOUDE REGEL NIET GEVONDEN, nalopen'}")
            continue
        pad.write_text(tekst.replace(KOUD, WAAROM[naam]), encoding="utf-8")
        print(f"  {naam}: rechtgezet")


if __name__ == "__main__":
    main()
