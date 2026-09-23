/**
 * Pique opvolging - concept-mails per gescande prospect (format 'Je keek even')
 * ---------------------------------------------------------------------------
 * Leest het tabblad 'Opvolging' en zet voor elke prospect die de landingspagina
 * scande een PERSOONLIJKE CONCEPT-mail klaar in Gmail, ondertekend Simon.
 * Onderwerp per persoon: 'Je keek even, <voornaam>'. Verstuurt NIETS zelf.
 *
 * Installatie:
 *  1. Log in op simon@intro-pique.agency. Open een Google Sheet, maak een tabblad 'Opvolging'.
 *  2. Importeer Opvolging-Batch3g-Pique-Data.csv in dat tabblad (kopregel op rij 1).
 *  3. Extensies -> Apps Script. Plak dit bestand. Opslaan.
 *  4. Menu 'Pique opvolging' -> 'Zet concepten klaar'. Eerste keer: rechten geven.
 *
 * Bij een generiek adres (info@ etc.) zet het script automatisch 'T.a.v. <naam>' bovenaan.
 * Rijen met een ingevulde 'opvolg_status' of zonder 'voornaam' worden overgeslagen.
 */

const CONFIG = {
  tabblad: 'Opvolging',
  afzenderNaam: 'Simon',
  verzendAls: '',   // leeg = het ingelogde account (simon@intro-pique.agency)
  kol: {
    bedrijf: 'bedrijf',
    voornaam: 'voornaam',
    email: 'email',
    emailAlt: 'email_alt',
    observatie: 'observatie',
    lpUrl: 'lp_url',
    gescand: 'gescand',
    status: 'opvolg_status'
  }
};

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Pique opvolging')
    .addItem('Zet concepten klaar', 'zetConceptenKlaar')
    .addToUi();
}

function zetConceptenKlaar() {
  const sh = SpreadsheetApp.getActive().getSheetByName(CONFIG.tabblad);
  if (!sh) { SpreadsheetApp.getUi().alert('Tabblad "' + CONFIG.tabblad + '" niet gevonden.'); return; }
  const data = sh.getDataRange().getValues();
  const head = data[0].map(String);
  const idx = {};
  for (const key in CONFIG.kol) {
    idx[key] = head.indexOf(CONFIG.kol[key]);
    if (idx[key] === -1) { SpreadsheetApp.getUi().alert('Kolom ontbreekt: ' + CONFIG.kol[key]); return; }
  }

  const naamIdx = head.indexOf('naam');   // optioneel: volledige naam voor de 't.a.v.'-regel
  let gemaakt = 0, overgeslagen = 0, zonderNaam = 0;
  const scanWaar = v => ['ja', 'true', 'x', 'waar', '1'].indexOf(String(v).trim().toLowerCase()) !== -1;
  const isGeneriek = e => /^(info|klantenservice|klantcontact|hello|hallo|contact|support|sales|office|welcome|post|service|help|shop|webshop|mail|nbd|newbusiness|klantenservice)@/i.test(e);

  for (let r = 1; r < data.length; r++) {
    const row = data[r];
    const bedrijf = String(row[idx.bedrijf] || '').trim();
    if (!bedrijf) continue;
    if (!scanWaar(row[idx.gescand])) { overgeslagen++; continue; }
    if (String(row[idx.status] || '').trim()) { overgeslagen++; continue; }

    const voornaam = String(row[idx.voornaam] || '').trim();
    if (!voornaam) { zonderNaam++; continue; }

    let email = String(row[idx.email] || '').trim();
    const emailAlt = String(row[idx.emailAlt] || '').trim();
    if (!email) email = emailAlt;
    if (!email) { overgeslagen++; continue; }

    const observatie = String(row[idx.observatie] || '').trim();
    const naam = (naamIdx >= 0 ? String(row[naamIdx] || '').trim() : '') || voornaam;
    const generiek = isGeneriek(email);
    // Persoonlijk adres -> intieme 'Je keek even'. Generieke/gedeelde inbox -> doorstuurbare mail.
    const onderwerp = generiek ? ('Ter attentie van ' + naam) : ('Je keek even, ' + voornaam);
    const body = generiek ? maakBodyGeneriek(voornaam, naam, bedrijf, observatie) : maakBody(voornaam, bedrijf, observatie);

    const opties = { name: CONFIG.afzenderNaam };
    if (CONFIG.verzendAls) opties.from = CONFIG.verzendAls;
    GmailApp.createDraft(email, onderwerp, body, opties);

    sh.getRange(r + 1, idx.status + 1).setValue('concept klaar ' + vandaag());
    gemaakt++;
  }

  SpreadsheetApp.getUi().alert('Klaar. ' + gemaakt + ' concept(en) gemaakt, ' + overgeslagen + ' overgeslagen'
    + (zonderNaam ? (', ' + zonderNaam + ' zonder voornaam (vul de naam in en draai opnieuw)') : '')
    + '.\nCheck je Gmail-concepten voordat je verstuurt.');
}

function maakBody(voornaam, bedrijf, observatie, tav) {
  const regels = [];
  if (tav) regels.push('T.a.v. ' + tav, '');
  regels.push(
    'Hoi ' + voornaam + ',',
    '',
    "Ik stuurde je laatst een handgeschreven kaart met een QR-code. Ik zag dat je 'm hebt gescand en de pagina hebt bekeken. Leuk, daar werd ik nieuwsgierig van.",
    '',
    'Die pagina maakte ik voor ' + bedrijf + ' omdat me iets opviel: ' + observatie + '. Daar zou ik het graag eens kort met je over hebben.',
    '',
    'Zullen we een keer vijftien minuten bellen? Dan laat ik zien wat ik precies bedoel. Komt bellen niet uit, dan hoor ik het ook.',
    '',
    'Groet,',
    '',
    'Simon'
  );
  return regels.join('\n');
}

// Variant B: doorstuurbare mail voor een generieke/gedeelde inbox. Geen scan-verwijzing,
// wel een T.a.v.-regel zodat een kantoormedewerker 'm bij de juiste persoon krijgt.
function maakBodyGeneriek(voornaam, naam, bedrijf, observatie) {
  return [
    'T.a.v. ' + naam,
    '',
    'Beste ' + voornaam + ',',
    '',
    'Ik stuurde je laatst een handgeschreven kaart met een QR-code en een pagina die ik speciaal voor ' + bedrijf + ' maakte. Daar wilde ik graag kort op terugkomen, want iets viel me op: ' + observatie + '. Daar zou ik het graag eens met je over hebben.',
    '',
    'Zullen we een keer vijftien minuten bellen? Komt dat niet uit, dan hoor ik het ook.',
    '',
    'Met vriendelijke groet,',
    '',
    'Simon'
  ].join('\n');
}

function vandaag() {
  return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
}
