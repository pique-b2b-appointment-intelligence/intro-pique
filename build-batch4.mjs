// Bouwt pique-batch4-data.mjs (merge np-master + LP-copy) en leidt genereer-pique-batch4.mjs
// af van de batch3-generator (heeft al video-9juli + naamloze-hero). 79 nieuwe-100 prospects.
import { readFileSync, writeFileSync } from 'node:fs';

const SCR = '/private/tmp/claude-501/-Users-simonkempers-Desktop-Pique---B2B-Appointment-Intelligence/cf61064a-4c50-4f1d-9295-495fa487c304/scratchpad';
const NP = `${SCR}/np`;

// Master: slug, vn (voornaam), org.
const master = JSON.parse(readFileSync(`${SCR}/np-master.json`, 'utf8'));

// Korte structuur-frase per slug (voor de CTA-uitrol-zin).
const STRUCTUUR = {
  'technische-unie':'je landelijke vestigingen','novon':'de regio’s','vve-diensten':'de regiokantoren',
  'netwerk-notarissen':'de aangesloten kantoren','asn-autoschade':'de aangesloten vestigingen','nmg-vastgoed':'de vestigingen',
  'damstra':'de vestigingen','flanderijn':'de vestigingen','mourik':'de divisies','goos-horeca':'de negen vestigingen',
  'taxatie-netwerk':'het hele taxateursnetwerk','itn-groep':'de sectoren','bierens':'de vestigingen','first-stop':'de aangesloten centra',
  '1box':'de vestigingen','laadpaaldirect':'het installateursnetwerk','donker-groep':'de zesentwintig locaties','arbo-unie':'de vestigingen',
  'beko':'de vier distributiecentra','eurobox':'de vestigingen','vink':'de vestigingen','feenstra':'de veertien vestigingen',
  'gkb':'de vestigingen','zorg-van-de-zaak':'de labels','bunzl':'de regio’s','bmn':'de vestigingen','cleanlease':'de wasserijen',
  'preventief':'de drieentwintig centra','wasco':'de vestigingen','alpina':'de vestigingen','imk':'de cursuslocaties',
  'stiho':'de merken en vestigingen','van-mossel':'de vestigingen','carel-lurvink':'de regio’s','van-wijhe-verf':'het professionele kanaal',
  'pirtek':'de zestien centers','etl':'de kantoren','select-windows':'het partnernetwerk','de-groot-installatiegroep':'de regio’s',
  'bidfood':'de distributiecentra','ambiance-zonwering':'de veertig vestigingen','sonepar':'de vestigingen','peinemann':'de twaalf bedrijven',
  'urban-care':'de kantoren','solar-nederland':'de vestigingen','premio':'de aangesloten vestigingen','zeelandia':'de regio’s',
  'sanidrome':'de leden','mcb':'de vestigingen','pius-floris':'de veertien vestigingen','sonneveld':'de regio’s',
  'paardekooper':'de labels en vestigingen','copijn':'de regio’s','bouwmaat':'de vestigingen','lavans':'de regio’s',
  'pontmeyer':'de tweeenvijftig vestigingen','batenburg':'de zes vestigingen','orona':'het landelijke servicenet','kroon-kozijn':'de vijfentwintig dealers',
  'schadenet':'de aangesloten locaties','rexel':'de verkooppunten','reym':'de vestigingen','autotaalglas':'de vierenvijftig vestigingen',
  'sunmaster':'het dealernetwerk','anticimex':'de acht vestigingen','arboned':'de locaties','autofirst':'de aangesloten vestigingen',
  'van-leeuwen':'de vestigingen','sortimo':'de Centers','top-movers':'de aangesloten verhuizers','mastermate':'de eenendertig vestigingen',
  'bott':'de regio’s','koelweb':'de regio’s','selecta':'de regio’s','elis':'de elf locaties','truckland':'de dertien vestigingen',
  'bruns':'de segmenten','directveilig':'de acht vestigingen','van-losser':'de bedrijven',
};

// Copy inladen en indexeren op slug. (chunk4/5/8 staan in scratchpad-root)
const files = [
  `${NP}/c1.json`, `${NP}/c2.json`, `${NP}/c3.json`, `${NP}/c4.json`,
  `${SCR}/orgs.json`, `${NP}/c6.json`, `${NP}/c7.json`, `${SCR}/objects.json`,
];
const prose = {};
for (const f of files) {
  const arr = JSON.parse(readFileSync(f, 'utf8'));
  for (const o of arr) prose[o.slug] = o;
}

const PROSPECTS = master.map(m => {
  const p = prose[m.slug];
  if (!p) throw new Error('Geen copy voor ' + m.slug);
  const structuur = STRUCTUUR[m.slug];
  if (!structuur) throw new Error('Geen structuur voor ' + m.slug);
  return {
    slug: m.slug, voornaam: m.vn, org: m.org, structuur, object: p.object,
    persoonlijkeNoot: p.persoonlijkeNoot, aannames: p.aannames, tension: p.tension, consequence: p.consequence,
  };
});
if (PROSPECTS.length !== 79) throw new Error('Verwacht 79, kreeg ' + PROSPECTS.length);

// Data-bestand wegschrijven.
const dataOut = `// Batch 4 (nieuwe-100) franchise-LP data (auto-gegenereerd door build-batch4.mjs). Niet met de hand bewerken.\nexport const PROSPECTS = ${JSON.stringify(PROSPECTS, null, 2)};\n`;
writeFileSync(new URL('./pique-batch4-data.mjs', import.meta.url), dataOut);

// Generator afleiden van batch3 (video-9juli + naamloze hero zitten er al in).
let gen = readFileSync(new URL('./genereer-pique-batch3.mjs', import.meta.url), 'utf8');
gen = gen.replace("from './pique-batch3-data.mjs'", "from './pique-batch4-data.mjs'");
gen = '// AUTO-AFGELEID van genereer-pique-batch3.mjs door build-batch4.mjs.\n' + gen;
writeFileSync(new URL('./genereer-pique-batch4.mjs', import.meta.url), gen);

console.log(`Data + generator klaar. ${PROSPECTS.length} prospects.`);
