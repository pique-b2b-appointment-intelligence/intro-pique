#!/usr/bin/env bash
# verify-live.sh <map>
# Checkt of ELKE .html in een LP-map live 200 geeft op intro-pique.agency.
# Draai dit ALTIJD voordat er brieven/QR de deur uit gaan.
#   ./verify-live.sh pique
#   ./verify-live.sh bcs2
set -euo pipefail
DIR="${1:?gebruik: ./verify-live.sh <map>  (bijv. pique, bcs2, bcs3)}"
BASE="https://www.intro-pique.agency"

# 1) Waarschuw als er lokaal .html in de map staat die NIET in git zit (= toekomstige 404).
if git rev-parse --git-dir >/dev/null 2>&1; then
  UNCOMMITTED=$(git status --porcelain "$DIR" 2>/dev/null | grep -E '^\?\?|^ ?[AM]' | grep -c '\.html$' || true)
  WHOLE_DIR=$(git status --porcelain | grep -Ec "^\?\? ${DIR}/$" || true)
  if [ "${WHOLE_DIR}" != "0" ]; then
    echo "LET OP: de map '${DIR}/' staat volledig BUITEN git -> alles 404 tot je commit+pusht."
  elif [ "${UNCOMMITTED}" != "0" ]; then
    echo "LET OP: ${UNCOMMITTED} .html in '${DIR}/' zijn nog niet gecommit -> die geven 404 tot je pusht."
  fi
fi

# 2) Sweep elke pagina live.
ok=0; fail=0; fails=""
for f in "$DIR"/*.html; do
  [ -e "$f" ] || continue
  slug=$(basename "$f" .html)
  [ "$slug" = "index" ] && continue
  code=$(curl -s -o /dev/null -w '%{http_code}' -L "${BASE}/${DIR}/${slug}")
  if [ "$code" = "200" ]; then ok=$((ok+1)); else fail=$((fail+1)); fails="${fails}\n  ${code}  ${BASE}/${DIR}/${slug}"; fi
done

echo "----------------------------------------"
echo "${DIR}: ${ok} live, ${fail} OFFLINE"
if [ "$fail" -gt 0 ]; then
  echo -e "OFFLINE PAGINA'S (NIET versturen tot dit 200 is):${fails}"
  exit 1
fi
echo "Alles live. Veilig om te versturen."
