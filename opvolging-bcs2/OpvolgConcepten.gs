/**
 * BCS opvolging - concept-mails per gescande prospect
 * -----------------------------------------------------
 * Wat het doet: leest het tabblad 'Opvolging' en zet voor elke prospect die
 * de landingspagina scande een PERSOONLIJKE CONCEPT-mail klaar in Gmail,
 * ondertekend Jeffrey. Het verstuurt NIETS zelf. Jij checkt elk concept en
 * drukt zelf op verzenden.
 *
 * Installatie:
 *  1. Open de Google Sheet met het tabblad 'Opvolging' (kolommen zie CONFIG).
 *  2. Extensies -> Apps Script. Plak dit bestand. Opslaan.
 *  3. Draai dit script vanuit HET GOOGLE-ACCOUNT dat de mails moet versturen
 *     (de Backbone-mailbox van Jeffrey, of een account met 'send mail as'
 *     Jeffrey ingesteld). De concepten verschijnen dan in die mailbox.
 *  4. Menu 'BCS opvolging' -> 'Zet concepten klaar'. Eerste keer: rechten geven.
 *
 * Herhalen: het script slaat rijen over die al een 'opvolg_status' hebben, dus
 * je kunt het gerust opnieuw draaien als er nieuwe scans bijkomen.
 */

const CONFIG = {
  tabblad: 'Opvolging',
  afzenderNaam: 'Jeffrey',
  // Zet hieronder het Backbone-adres dat als afzender moet gelden.
  // Werkt alleen als dit adres in Gmail is ingesteld als 'Verzenden als'.
  // Laat leeg ('') om gewoon het ingelogde account te gebruiken.
  verzendAls: '',
  onderwerp: 'Ik stuurde je laatst een kaartje',
  // Kolomkoppen exact zoals in rij 1 van het tabblad:
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

  let gemaakt = 0, overgeslagen = 0;
  const scanWaar = v => ['ja', 'true', 'x', 'waar', '1'].indexOf(String(v).trim().toLowerCase()) !== -1;

  for (let r = 1; r < data.length; r++) {
    const row = data[r];
    const bedrijf = String(row[idx.bedrijf] || '').trim();
    if (!bedrijf) continue;
    if (!scanWaar(row[idx.gescand])) { overgeslagen++; continue; }        // nog niet gescand
    if (String(row[idx.status] || '').trim()) { overgeslagen++; continue; } // al opgevolgd

    const voornaam = String(row[idx.voornaam] || '').trim();
    let email = String(row[idx.email] || '').trim();
    const emailAlt = String(row[idx.emailAlt] || '').trim();
    if (!email) email = emailAlt;
    if (!email) { overgeslagen++; continue; }

    const observatie = String(row[idx.observatie] || '').trim();
    const lpUrl = String(row[idx.lpUrl] || '').trim();

    const body = maakBody(voornaam, bedrijf, observatie, lpUrl);

    const opties = { name: CONFIG.afzenderNaam };
    if (CONFIG.verzendAls) opties.from = CONFIG.verzendAls;
    GmailApp.createDraft(email, CONFIG.onderwerp, body, opties);

    sh.getRange(r + 1, idx.status + 1).setValue('concept klaar ' + vandaag());
    gemaakt++;
  }

  SpreadsheetApp.getUi().alert('Klaar. ' + gemaakt + ' concept(en) gemaakt, ' + overgeslagen + ' overgeslagen.\nCheck je Gmail-concepten voordat je verstuurt.');
}

function maakBody(voornaam, bedrijf, observatie, lpUrl) {
  const aanhef = voornaam ? ('Hoi ' + voornaam + ',') : 'Hoi,';
  const regels = [
    aanhef,
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
  ];
  return regels.join('\n');
}

function vandaag() {
  return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
}
