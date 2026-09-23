import fs from 'fs';
const D='/Users/simonkempers/Desktop/Pique - B2B Appointment Intelligence/Klanten/BCS/batch3-hooks/';
const M='/tmp/bcs3-fbresults/master-final.json';
const master=JSON.parse(fs.readFileSync(M,'utf8')).filter(x=>x.status==='TIER1');
let hooks=[]; for(const w of ['wave1','wave2','wave3','wave4']) hooks=hooks.concat(JSON.parse(fs.readFileSync(D+w+'.json','utf8')));
const recovery=JSON.parse(fs.readFileSync(D+'recovery.json','utf8'));
const normweb=s=>(s||'').toLowerCase().replace(/^https?:\/\//,'').replace(/^www\./,'').replace(/\/.*$/,'').replace(/[^a-z0-9.]/g,'');
const normb=s=>(s||'').toLowerCase().replace(/[^a-z0-9]/g,'');
const alias={'tetswimwear':'tetresponsiblewear'};const hookByWeb=new Map(), hookByB=new Map();
for(const h of hooks){ if(normweb(h.web))hookByWeb.set(normweb(h.web),h); if(normb(h.bedrijf))hookByB.set(normb(h.bedrijf),h); }
const recByWeb=new Map(), recByB=new Map();
for(const r of recovery){ if(normweb(r.web))recByWeb.set(normweb(r.web),r); if(normb(r.bedrijf))recByB.set(normb(r.bedrijf),r); }

const badname=s=>!s || /geen|niet meer|n\.v\.t|onbekend/i.test(s);
let out=[], nohook=[];
for(const m of master){
  const hw=hookByWeb.get(normweb(m.web))||hookByB.get(normb(m.bedrijf));
  const rc=recByWeb.get(normweb(m.web))||recByB.get(normb(m.bedrijf));
  let rec={bedrijf:m.bedrijf, web:m.web,
    beslisser_naam:m.beslisser_naam, beslisser_functie:m.beslisser_functie, beslisser_status:m.beslisser_status,
    straat:m.straat, postcode:m.postcode, plaats:m.plaats, land:m.land, adres_zeker:m.adres_zeker,
    hook:'', hook_bron:'', notitie:''};
  if(rc){ // soft prospect: recovery is authoritative for beslisser+adres+hook
    rec.beslisser_naam=rc.beslisser_naam; rec.beslisser_functie=rc.beslisser_functie; rec.beslisser_status=rc.beslisser_status;
    rec.straat=rc.straat; rec.postcode=rc.postcode; rec.plaats=rc.plaats; rec.land=rc.land; rec.adres_zeker=rc.adres_zeker;
    rec.hook=rc.hook||''; rec.hook_bron=rc.hook_bron||'';
    rec.notitie='recovery';
  } else if(hw){ // hard prospect
    rec.hook=hw.hook||''; rec.hook_bron=hw.hook_bron||'';
    // beslisser corrections
    if(hw.beslisser_bevestigd==='GECORRIGEERD'){
      if(badname(hw.beslisser_naam)){ rec.beslisser_naam=null; rec.beslisser_status='ONOPGELOST'; rec.notitie='beslisser vervallen, opnieuw verifieren'; }
      else { rec.beslisser_naam=hw.beslisser_naam; rec.beslisser_status='GEVERIFIEERD'; rec.notitie='beslisser gecorrigeerd'; }
    } else if(hw.beslisser_bevestigd==='ONZEKER'){
      rec.beslisser_status='ONOPGELOST'; rec.notitie='beslisser te verifieren';
    }
    // address corrections
    if(hw.adres_bevestigd==='GECORRIGEERD'){ rec.straat=hw.straat; rec.postcode=hw.postcode; rec.plaats=hw.plaats; rec.land=hw.land; rec.notitie=(rec.notitie?rec.notitie+' | ':'')+'adres gecorrigeerd'; }
  } else { nohook.push(m.bedrijf); }
  out.push(rec);
}
fs.writeFileSync(D+'FINAL-assembled.json', JSON.stringify(out,null,1));
const withHook=out.filter(x=>x.hook).length;
const hardAll=out.filter(x=>x.adres_zeker==='JA'&&x.beslisser_status==='GEVERIFIEERD'&&x.beslisser_naam&&x.hook).length;
const addrOK=out.filter(x=>x.adres_zeker==='JA'&&x.hook).length;
console.log('TIER1 totaal:',out.length);
console.log('met hook:',withHook);
console.log('adres JA + hook (kaart kan eropaf, hook klaar):',addrOK);
console.log('VOLLEDIG (naam geverifieerd + adres JA + hook):',hardAll);
console.log('zonder hook-match:',nohook.length, nohook.slice(0,10).join(', '));
