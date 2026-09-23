import fs from 'fs';
const D='/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/BCS/batch3-hooks/';
const OUT='/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/BCS/';
let all=JSON.parse(fs.readFileSync(D+'FINAL-assembled.json','utf8'));
const norm=s=>(s||'').toLowerCase().replace(/^https?:\/\//,'').replace(/^www\./,'').replace(/\/.*$/,'').replace(/[^a-z0-9.]/g,'');
const score=r=>(r.hook?4:0)+(r.adres_zeker==='JA'?2:0)+(r.beslisser_status==='GEVERIFIEERD'&&r.beslisser_naam?1:0);
const map=new Map();
for(const r of all){const k=norm(r.web)||('b:'+(r.bedrijf||'').toLowerCase()); if(!map.has(k)||score(r)>score(map.get(k))) map.set(k,r);}
all=[...map.values()];
fs.writeFileSync(D+'FINAL-assembled.json', JSON.stringify(all,null,1));
const full=r=>r.adres_zeker==='JA'&&r.beslisser_status==='GEVERIFIEERD'&&r.beslisser_naam&&r.hook;
const rank=r=>full(r)?0:(r.adres_zeker==='JA'&&r.hook?1:2);
all.sort((a,b)=>rank(a)-rank(b)||(a.bedrijf||'').localeCompare(b.bedrijf||''));
const esc=s=>'"'+String(s==null?'':s).replace(/"/g,'""').replace(/\r?\n/g,' ')+'"';
const split=n=>{if(!n)return['',''];n=String(n).replace(/\s*&.*$/,'').trim();const p=n.split(/\s+/);return[p[0]||'',p.slice(1).join(' ')];};
const head=['bedrijf','website','voornaam','achternaam','functie','beslisser_status','founder_fallback','straatnaam','postcode','plaatsnaam','land','adres_zeker','hook','hook_bron','notitie'];
let csv=head.map(esc).join(',')+'\n';
for(const r of all){const[vn,an]=split(r.beslisser_naam);csv+=[r.bedrijf,r.web,vn,an,r.beslisser_functie,r.beslisser_status,r.founder_fallback||'',r.straat,r.postcode,r.plaats,r.land,r.adres_zeker,r.hook,r.hook_bron,r.notitie].map(esc).join(',')+'\n';}
fs.writeFileSync(OUT+'BCS-Batch3-Prospects-Beslisser-Hook-Adres.csv', csv);
const mail=all.filter(r=>r.adres_zeker==='JA'&&r.hook).length;
const doel=all.filter(r=>r.adres_zeker==='JA'&&r.hook&&!(r.beslisser_status==='GEVERIFIEERD'&&r.beslisser_naam)).length;
const noadd=all.filter(r=>r.adres_zeker!=='JA').length;
console.log('UNIEK:',all.length,'| VOLLEDIG(naam+adres+hook):',all.filter(full).length,'| mailbaar+hook:',mail,'| doelrol(naam volgt):',doel,'| geen hard adres:',noadd,'| functionele beslisser:',all.filter(r=>r.founder_fallback).length);
