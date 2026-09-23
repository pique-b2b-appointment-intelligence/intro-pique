import fs from 'fs';
const D='/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/BCS/batch3-hooks/';
const OUT='/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/BCS/';
const all=JSON.parse(fs.readFileSync(D+'FINAL-assembled.json','utf8'));
const full=r=>r.adres_zeker==='JA'&&r.beslisser_status==='GEVERIFIEERD'&&r.beslisser_naam&&r.hook;
const rank=r=>full(r)?0:(r.adres_zeker==='JA'&&r.hook?1:2);
all.sort((a,b)=>rank(a)-rank(b)||(a.bedrijf||'').localeCompare(b.bedrijf||''));
const esc=s=>'"'+String(s==null?'':s).replace(/"/g,'""').replace(/\r?\n/g,' ')+'"';
// split beslisser into voornaam/achternaam
const split=n=>{ if(!n) return ['','']; n=n.replace(/\s*&.*$/,'').trim(); const p=n.split(/\s+/); return [p[0]||'', p.slice(1).join(' ')]; };
const head=['bedrijf','website','voornaam','achternaam','functie','beslisser_status','straatnaam','postcode','plaatsnaam','land','adres_zeker','hook','hook_bron','notitie'];
let csv=head.map(esc).join(',')+'\n';
for(const r of all){ const [vn,an]=split(r.beslisser_naam); csv+=[r.bedrijf,r.web,vn,an,r.beslisser_functie,r.beslisser_status,r.straat,r.postcode,r.plaats,r.land,r.adres_zeker,r.hook,r.hook_bron,r.notitie].map(esc).join(',')+'\n'; }
fs.writeFileSync(OUT+'BCS-Batch3-Prospects-Beslisser-Hook-Adres.csv', csv);
const vol=all.filter(full).length, mail=all.filter(r=>r.adres_zeker==='JA'&&r.hook).length;
console.log('CSV:',all.length,'rijen | VOLLEDIG',vol,'| mailbaar+hook',mail);
