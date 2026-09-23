import fs from 'fs';
const D='/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/BCS/batch3-hooks/';
const out=JSON.parse(fs.readFileSync(D+'FINAL-assembled.json','utf8'));
let hooks=[]; for(const w of ['wave1','wave2','wave3','wave4']) hooks=hooks.concat(JSON.parse(fs.readFileSync(D+w+'.json','utf8')));
const tet=hooks.find(h=>/TET/i.test(h.bedrijf));
const rec=out.find(x=>/TET Swimwear/i.test(x.bedrijf));
if(tet&&rec){ rec.hook=tet.hook; rec.hook_bron=tet.hook_bron; rec.notitie=(rec.notitie?rec.notitie+' | ':'')+'merk nu TET Responsible Wear'; if(tet.adres_bevestigd==='GECORRIGEERD'){rec.straat=tet.straat;rec.postcode=tet.postcode;rec.plaats=tet.plaats;rec.land=tet.land;} console.log('TET gekoppeld:',tet.hook.slice(0,60)); }
fs.writeFileSync(D+'FINAL-assembled.json', JSON.stringify(out,null,1));
const addrOK=out.filter(x=>x.adres_zeker==='JA'&&x.hook).length;
const hardAll=out.filter(x=>x.adres_zeker==='JA'&&x.beslisser_status==='GEVERIFIEERD'&&x.beslisser_naam&&x.hook).length;
console.log('met hook:',out.filter(x=>x.hook).length,'| adres JA+hook:',addrOK,'| VOLLEDIG:',hardAll);
