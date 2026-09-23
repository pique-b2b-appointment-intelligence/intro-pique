/**
 * BCS opvolging - concept-mails per gescande prospect (format 'Je keek even')
 * ---------------------------------------------------------------------------
 * Leest het tabblad 'Opvolging' en zet voor elke prospect die de landingspagina
 * scande een PERSOONLIJKE CONCEPT-mail klaar in Gmail, ondertekend Jeffrey.
 * Onderwerp per persoon: 'Je keek even, <voornaam>'. Verstuurt NIETS zelf.
 * Jij checkt elk concept en drukt zelf op verzenden.
 *
 * Dit is batch 3g: 15 NIEUWE scanners die nog geen opvolgmail hadden.
 *
 * Installatie:
 *  1. Open de Google Sheet, maak/gebruik een tabblad 'Opvolging' (kolommen zie CONFIG.kol).
 *  2. Importeer Opvolging-Batch3g-Data.csv in dat tabblad (kopregel op rij 1,
 *     'Vervang huidige blad' of een leeg tabblad 'Opvolging').
 *  3. Extensies -> Apps Script. Plak dit bestand. Opslaan.
 *  4. Draai vanuit HET GOOGLE-ACCOUNT dat de mails verstuurt (Jeffrey's Backbone-mailbox,
 *     of een account met 'Verzenden als' Jeffrey). De concepten komen in die mailbox.
 *  5. Menu 'BCS opvolging' -> 'Zet concepten klaar'. Eerste keer: rechten geven.
 *
 * Herhalen kan: rijen met een ingevulde 'opvolg_status' worden overgeslagen.
 * Rijen zonder 'voornaam' worden overgeslagen (het onderwerp leunt op de naam);
 * vul de naam in, maak de status-cel leeg en draai opnieuw.
 *
 * Adres-logica: staat er een generiek/algemeen adres (info@, hello@, support@ ...),
 * dan komt automatisch een 'T.a.v. <volledige naam>'-regel bovenaan de mail. Bij een
 * persoonlijk adres blijft die regel weg. De volledige naam komt uit de kolom 'naam'.
 */

const CONFIG = {
  tabblad: 'Opvolging',
  afzenderNaam: 'Jeffrey',
  // Backbone-adres dat als afzender moet gelden. Werkt alleen als dit in Gmail
  // staat als 'Verzenden als'. Laat leeg ('') voor het ingelogde account.
  verzendAls: '',
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
    .createMenu('BCS opvolging')
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
  // Algemene/gedeelde inboxen: dan zetten we een 't.a.v.'-regel bovenaan zodat de mail
  // bij de juiste persoon terechtkomt. Persoonlijke adressen krijgen die regel niet.
  const isGeneriek = e => /^(info|klantenservice|klantcontact|hello|hallo|contact|support|sales|office|welcome|post|service|help|shop|webshop|mail|groetenvan)@/i.test(e);

  for (let r = 1; r < data.length; r++) {
    const row = data[r];
    const bedrijf = String(row[idx.bedrijf] || '').trim();
    if (!bedrijf) continue;
    if (!scanWaar(row[idx.gescand])) { overgeslagen++; continue; }         // nog niet gescand
    if (String(row[idx.status] || '').trim()) { overgeslagen++; continue; } // al opgevolgd / geblokkeerd

    const voornaam = String(row[idx.voornaam] || '').trim();
    if (!voornaam) { zonderNaam++; continue; }                             // onderwerp leunt op de naam

    let email = String(row[idx.email] || '').trim();
    const emailAlt = String(row[idx.emailAlt] || '').trim();
    if (!email) email = emailAlt;
    if (!email) { overgeslagen++; continue; }

    const observatie = String(row[idx.observatie] || '').trim();
    const naam = (naamIdx >= 0 ? String(row[naamIdx] || '').trim() : '') || voornaam;
    const onderwerp = 'Je keek even, ' + voornaam;
    const body = maakBody(voornaam, bedrijf, observatie, isGeneriek(email) ? naam : '');

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
  if (tav) regels.push('T.a.v. ' + tav, '');   // alleen bij een generiek/algemeen adres
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
    'Jeffrey'
  );
  return regels.join('\n');
}

function vandaag() {
  return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
}
