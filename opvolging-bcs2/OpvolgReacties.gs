/**
 * BCS opvolging - reacties / vervolgmails, met een knop
 * -----------------------------------------------------
 * Leest het tabblad 'Reacties' en zet per rij een concept klaar in jouw Gmail:
 *  - modus 'reply'  -> een antwoord IN de bestaande e-mailthread met die persoon
 *  - modus 'nieuw'  -> een nieuwe mail
 * Het verstuurt niets zelf. Jij leest de concepten na en verstuurt.
 *
 * Tabblad 'Reacties', kolommen op rij 1 (exact):
 *   bedrijf | naam | email | modus | onderwerp | body | status
 *
 * Menu: 'BCS reacties' -> 'Zet reacties klaar'. Rijen met een status worden overgeslagen.
 */

const R_CONFIG = {
  tabblad: 'Reacties',
  afzenderNaam: 'Jeffrey',
  verzendAls: '',   // leeg = jouw eigen ingelogde Gmail. Alleen invullen als dat adres als 'Verzenden als' staat.
  kol: { bedrijf: 'bedrijf', naam: 'naam', email: 'email', modus: 'modus', onderwerp: 'onderwerp', body: 'body', status: 'status' }
};

function onOpen() {
  SpreadsheetApp.getUi().createMenu('BCS reacties')
    .addItem('Zet reacties klaar', 'zetReactiesKlaar')
    .addToUi();
}

function zetReactiesKlaar() {
  const sh = SpreadsheetApp.getActive().getSheetByName(R_CONFIG.tabblad);
  if (!sh) { SpreadsheetApp.getUi().alert('Tabblad "' + R_CONFIG.tabblad + '" niet gevonden.'); return; }
  const data = sh.getDataRange().getValues();
  const head = data[0].map(String);
  const idx = {};
  for (const k in R_CONFIG.kol) { idx[k] = head.indexOf(R_CONFIG.kol[k]); if (idx[k] === -1) { SpreadsheetApp.getUi().alert('Kolom ontbreekt: ' + R_CONFIG.kol[k]); return; } }

  const opties = { name: R_CONFIG.afzenderNaam };
  if (R_CONFIG.verzendAls) opties.from = R_CONFIG.verzendAls;

  let gemaakt = 0, overgeslagen = 0, geenThread = 0;
  for (let r = 1; r < data.length; r++) {
    const row = data[r];
    const email = String(row[idx.email] || '').trim();
    if (!email) { overgeslagen++; continue; }
    if (String(row[idx.status] || '').trim()) { overgeslagen++; continue; }

    const modus = String(row[idx.modus] || 'nieuw').trim().toLowerCase();
    const onderwerp = String(row[idx.onderwerp] || '').trim();
    const body = String(row[idx.body] || '');

    let statusTekst;
    if (modus === 'reply' || modus === 'antwoord' || modus === 'in-thread') {
      const threads = GmailApp.search('(to:' + email + ' OR from:' + email + ')', 0, 10);
      if (threads.length) {
        threads[0].createDraftReply(body, opties);
        statusTekst = 'reply-concept ' + vandaag();
      } else {
        // geen bestaande thread gevonden: maak een gewone nieuwe mail als terugval
        GmailApp.createDraft(email, onderwerp || 'Re: ons contact', body, opties);
        statusTekst = 'concept (geen thread gevonden) ' + vandaag();
        geenThread++;
      }
    } else {
      GmailApp.createDraft(email, onderwerp, body, opties);
      statusTekst = 'concept klaar ' + vandaag();
    }
    sh.getRange(r + 1, idx.status + 1).setValue(statusTekst);
    gemaakt++;
  }
  SpreadsheetApp.getUi().alert('Klaar. ' + gemaakt + ' concept(en) gemaakt, ' + overgeslagen + ' overgeslagen'
    + (geenThread ? (', ' + geenThread + ' zonder bestaande thread (als nieuwe mail klaargezet)') : '')
    + '.\nCheck je Gmail-concepten voordat je verstuurt.');
}

function vandaag() {
  return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
}
