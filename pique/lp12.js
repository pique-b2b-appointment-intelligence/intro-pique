/* lp12.js — gedrag van de v12-standaard: het dossier open/dicht en de
   videospeler die in zijn eigen kader afspeelt. Hoort na lp-v2.js. */
var dv=document.querySelector('.dosveld');
var dvk=dv&&dv.querySelector('.dv-bar');
if(dvk) dvk.addEventListener('click',function(){
  var o=dv.classList.toggle('open');
  dvk.setAttribute('aria-expanded',o?'true':'false');
  if(o&&window.pqTrack) pqTrack('dossier-geopend');
});
document.querySelectorAll('.bronknop').forEach(function(k){
  var d=document.getElementById(k.getAttribute('aria-controls'));
  if(!d) return;
  k.addEventListener('click',function(){
    var o=d.classList.toggle('open');
    k.setAttribute('aria-expanded',o?'true':'false');
    if(o&&window.pqTrack) pqTrack('bron-geopend');
  });
});
var vb=document.querySelector('.vslbox');
if(vb) vb.addEventListener('click',function(){
  if(window.pqTrack) pqTrack('vsl');
  var houder=vb.parentNode;
  var v=document.createElement('video');
  v.src='vsl-720-zacht.mp4'; v.poster='vsl-poster.jpg';
  v.controls=true; v.playsInline=true; v.setAttribute('playsinline','');
  v.preload='auto';
  /* Het bestand staat al 6 dB zachter. Dit is de tweede rem, en hij doet
     niets op iOS: daar is volume alleen-lezen. Vandaar allebei. */
  try{ v.volume=0.8; }catch(e){}
  vb.remove();
  houder.appendChild(v);
  var p=v.play();
  if(p&&p.catch) p.catch(function(){});
});
