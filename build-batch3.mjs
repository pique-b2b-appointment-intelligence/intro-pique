// Bouwt pique-batch3-data.mjs (merge vaste velden + copy uit b3a-f.json) en
// genereert genereer-pique-batch3.mjs uit de batch2-generator met de nieuwe video + naamloze hero.
import { readFileSync, writeFileSync } from 'node:fs';

// Vaste velden per prospect. voornaam '' = naamloze hero (ROLE-ONLY, geen geverifieerde beslisser).
// check:true = naam is 'te verifiëren', bevestig vóór verzending.
const FIXED = [
  {slug:'profile-tyrecenter', voornaam:'', org:'Profile Tyrecenter', structuur:'al je vestigingen', object:'Een profieldieptemeter'},
  {slug:'euromaster', voornaam:'René', check:true, org:'Euromaster', structuur:'de vestigingen en fleetregio’s', object:'Een bandenspanningsmeter'},
  {slug:'vakgarage', voornaam:'Chris-Jan', check:true, org:'Vakgarage', structuur:'de aangesloten garages', object:'Een momentsleutel'},
  {slug:'bosch-car-service', voornaam:'Michiel', check:true, org:'Bosch Car Service', structuur:'de aangesloten werkplaatsen', object:'Een diagnosestekker'},
  {slug:'kwik-fit', voornaam:'', org:'Kwik-Fit', structuur:'de filialen', object:'Een bandenkrijtje'},
  {slug:'olympia', voornaam:'Dimitri', org:'Olympia', structuur:'de franchisevestigingen', object:'Een naambadge'},
  {slug:'continu', voornaam:'', org:'Continu', structuur:'de vestigingen', object:'Een waterpas'},
  {slug:'luba', voornaam:'Johan', check:true, org:'Luba', structuur:'de veertig vestigingen', object:'Een stempel'},
  {slug:'timing', voornaam:'Frank', org:'Timing', structuur:'de vestigingen', object:'Een zandloper'},
  {slug:'csu', voornaam:'Natalie', org:'CSU', structuur:'de regio’s', object:'Een microvezeldoekje'},
  {slug:'asito', voornaam:'Jeroen', check:true, org:'Asito', structuur:'de vestigingen', object:'Een witte katoenen handschoen'},
  {slug:'trigion', voornaam:'', org:'Trigion', structuur:'de regio’s', object:'Een fluitje'},
  {slug:'krinkels', voornaam:'Jeron', check:true, org:'Krinkels', structuur:'de vestigingen', object:'Een zakje graszaad'},
  {slug:'idverde', voornaam:'Mascha', org:'idverde', structuur:'de vestigingen', object:'Een zakje bloemzaad'},
  {slug:'nvd-beveiliging', voornaam:'Marc', check:true, org:'NVD Beveiliging', structuur:'de regio’s', object:'Een zaklampje'},
  {slug:'boels', voornaam:'', org:'Boels Rental', structuur:'de vestigingen', object:'Een duimstok'},
  {slug:'colle', voornaam:'Michiel', check:true, org:'Collé Rental & Sales', structuur:'de tweeentwintig vestigingen', object:'Een moersleutel'},
  {slug:'ooms', voornaam:'Ted', org:'Ooms Makelaars', structuur:'de segmenten en regio’s', object:'Een mini te-huur-bordje'},
  {slug:'van-der-sande', voornaam:'Peter-Paul', org:'Van der Sande Makelaars', structuur:'West-Brabant', object:'Een sleutelbos'},
  {slug:'rodenburg', voornaam:'Alexander', org:'Rodenburg Bedrijfsmakelaars', structuur:'Apeldoorn, Deventer en Zwolle', object:'Een mini makelaarsbordje'},
  {slug:'van-dorp', voornaam:'Martin', org:'Van Dorp', structuur:'de vijfentwintig vestigingen', object:'Een spanningszoeker'},
  {slug:'breman', voornaam:'Erik', org:'Breman Installatiegroep', structuur:'de dertig vestigingen', object:'Een thermometer'},
  {slug:'kuijpers', voornaam:'Aukje', org:'Kuijpers', structuur:'de veertien vestigingen', object:'Een mini-zonnepaneel'},
  {slug:'hoppenbrouwers', voornaam:'Henny', org:'Hoppenbrouwers Techniek', structuur:'de vestigingen', object:'Een spanningstester'},
  {slug:'unica', voornaam:'', org:'Unica', structuur:'de vestigingen en divisies', object:'Een schroevendraaier'},
  {slug:'eriks', voornaam:'', org:'ERIKS', structuur:'de vestigingen', object:'Een kogellager'},
  {slug:'oosterberg', voornaam:'Ariën', org:'Oosterberg', structuur:'de eenentwintig vestigingen', object:'Een mini-kabelhaspel'},
  {slug:'rensa', voornaam:'Leon', org:'Rensa', structuur:'de regio’s', object:'Een radiatorontluchtingssleutel'},
  {slug:'rubix', voornaam:'Dick', check:true, org:'Rubix Nederland', structuur:'de servicelocaties', object:'Een O-ring'},
  {slug:'fabory', voornaam:'', org:'Fabory', structuur:'de dertien vestigingen', object:'Een zakje bouten'},
  {slug:'cws', voornaam:'', org:'CWS Nederland', structuur:'de regio’s', object:'Een geborduurd embleem'},
  {slug:'blycolin', voornaam:'Marc', org:'Blycolin', structuur:'de regio’s', object:'Een opgerold handdoekje'},
  {slug:'rentex', voornaam:'Titus', org:'Rentex', structuur:'de regio’s', object:'Een wasknijper'},
  {slug:'maas-international', voornaam:'George', check:true, org:'Maas International', structuur:'de regio’s', object:'Een koffiemaatschepje'},
  {slug:'peeze', voornaam:'Myriam', org:'Peeze', structuur:'de regio’s', object:'Een zakje versgebrande koffiebonen'},
  {slug:'esdec', voornaam:'', org:'Esdec', structuur:'de Benelux-regio’s', object:'Een montageklem'},
  {slug:'libra-energy', voornaam:'Ilse', check:true, org:'Libra Energy', structuur:'de installateursregio’s', object:'Een mini-zonnecel'},
  {slug:'rovc', voornaam:'Kirsten', org:'ROVC', structuur:'de regio’s', object:'Een mini-veiligheidsbril'},
  {slug:'ncoi', voornaam:'Robert', org:'NCOI Opleidingen', structuur:'de merken en regio’s', object:'Een diploma-lintje'},
  {slug:'schouten-nelissen', voornaam:'Steven', org:'Schouten & Nelissen', structuur:'de regio’s', object:'Een kompas'},
  {slug:'uts', voornaam:'Richard', check:true, org:'UTS Nederland', structuur:'de tien regionale partners', object:'Een mini-verhuisdoosje'},
  {slug:'simon-loos', voornaam:'Peter', check:true, org:'Simon Loos', structuur:'de regio’s', object:'Een mini-pallet'},
  {slug:'probo', voornaam:'Douwe Pieter', check:true, org:'Probo', structuur:'de reseller-regio’s', object:'Een kleurenwaaier'},
  {slug:'drukwerkdeal', voornaam:'Martijn', check:true, org:'Drukwerkdeal', structuur:'de segmenten', object:'Een gevouwen papiermonster'},
  {slug:'vegro', voornaam:'Else', org:'Vegro', structuur:'de vijftig zorgwinkels', object:'Een antislip-dopje'},
  {slug:'harting-bank', voornaam:'', org:'Harting-Bank', structuur:'de regio’s', object:'Een reflexhamertje'},
  {slug:'countus', voornaam:'Serge', org:'Countus', structuur:'de vierentwintig vestigingen', object:'Een rekenliniaal'},
  {slug:'aaff', voornaam:'Fou-Khan', org:'aaff', structuur:'de vijftig vestigingen', object:'Een naamstempel'},
];

// Copy inladen en indexeren op slug.
const prose = {};
for (const g of ['a','b','c','d','e','f']) {
  const arr = JSON.parse(readFileSync(new URL(`../../scratchpad-b3/${g}.json`, import.meta.url), 'utf8'));
  for (const o of arr) prose[o.slug] = o;
}

// Beslisser-namen (na deep research) uit meta.json; deze overschrijven de voornaam in FIXED.
const meta = JSON.parse(readFileSync(new URL('../../scratchpad-b3/meta.json', import.meta.url), 'utf8'));

// Merge.
const PROSPECTS = FIXED.map(f => {
  const p = prose[f.slug];
  if (!p) throw new Error('Geen copy voor ' + f.slug);
  const vn = (meta[f.slug] && meta[f.slug].vn) ? meta[f.slug].vn : f.voornaam;
  return {
    slug: f.slug, voornaam: vn, org: f.org, structuur: f.structuur, object: f.object,
    persoonlijkeNoot: p.persoonlijkeNoot, aannames: p.aannames, tension: p.tension, consequence: p.consequence,
  };
});
if (PROSPECTS.length !== 48) throw new Error('Verwacht 48, kreeg ' + PROSPECTS.length);

// Data-bestand wegschrijven.
const dataOut = `// Batch 3 franchise-LP data (auto-gegenereerd door build-batch3.mjs). Niet met de hand bewerken.\nexport const PROSPECTS = ${JSON.stringify(PROSPECTS, null, 2)};\n`;
writeFileSync(new URL('./pique-batch3-data.mjs', import.meta.url), dataOut);

// Generator afleiden van batch2.
let gen = readFileSync(new URL('./genereer-pique-batch2.mjs', import.meta.url), 'utf8');
gen = gen.replace("from './pique-batch2-data.mjs'", "from './pique-batch3-data.mjs'");
gen = gen.replace('src="video.mp4"', 'src="video-9juli.mp4"');
gen = gen.replace(
  '<h1 class="intro-h1">Hé ${esc(p.voornaam)}, dit is waarom je mijn brief hebt ontvangen.</h1>',
  '<h1 class="intro-h1">${p.voornaam?`Hé ${esc(p.voornaam)}, dit`:`Dit`} is waarom je mijn brief hebt ontvangen.</h1>'
);
gen = '// AUTO-AFGELEID van genereer-pique-batch2.mjs door build-batch3.mjs.\n' + gen;
writeFileSync(new URL('./genereer-pique-batch3.mjs', import.meta.url), gen);

const check = FIXED.filter(f => f.check).map(f => f.org);
const nameless = FIXED.filter(f => !f.voornaam).map(f => f.org);
console.log(`Data + generator klaar. ${PROSPECTS.length} prospects.`);
console.log(`Naamloze hero (ROLE-ONLY, ${nameless.length}): ${nameless.join(', ')}`);
console.log(`Voornaam te bevestigen vóór verzending (${check.length}): ${check.join(', ')}`);
