#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cloudpillo op het v2-skelet, met drie vondsten die NIET op de kaart stonden.

Het skelet blijft Componenten/lp-v2: nav met knop, de rail, de ask halverwege,
de dock, de tweede CTA. Daar is nooit bezwaar tegen geweest.

Wat er verandert:
1. De kaart zei al "11 taalvarianten" en "er draait Gorgias". Die twee stonden
   als bevinding 01 en 02 op de pagina, dus hij las twee schermen lang niets
   nieuws. Ze worden nu de aanloop ("dat weet je al") en de drie bevindingen
   zijn alle drie nieuw.
2. De bronregel wordt aantikbaar: het letterlijke citaat van hun eigen site
   klapt eronder open. Pagina-lokaal toegevoegd, lp.css en lp-v2.js worden niet
   aangeraakt, want daar hangen zevenduizend live pagina's aan.
3. De ask zegt in gewoon Nederlands wat dit is.

Alles geverifieerd tegen cloudpillo.com op 1 oktober 2026.
"""
import io, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
BRON = os.path.join(HIER, '..', 'bcs5', 'cloudpillo.html')
DOEL = os.path.join(HIER, '..', 'bcs5', 'cloudpillo-v9.html')
s = io.open(BRON, encoding='utf-8').read()

GEZIEN = '1 oktober 2026'
DOM = 'cloudpillo.com'

VONDSTEN = [
    dict(kop='De telefoon staat dertig uur per week aan.',
         tekst='Ma tot vr, tien tot vier. Dat staat op jullie eigen klantenservicepagina.',
         citaat='Bel ons via +31 73 704 4350 Ma&ndash;vr 10:00&ndash;16:00 uur of stuur '
                'ons een e-mail support@cloudpillo.nl'),
    dict(kop='Op reactietijd staat er geen getal.',
         tekst='Wel een belofte, geen termijn. Dat valt op bij een winkel die verder '
               'overal precies is.',
         citaat='komen zo snel mogelijk bij je terug met een antwoord'),
    dict(kop='En je geeft honderd dagen retourrecht.',
         tekst='Dat is ruim. Het betekent ook dat er honderd dagen lang vragen over een '
               'bestelling kunnen binnenkomen.',
         citaat='Je hebt 100 dagen vanaf de datum van aankoop om een product te retourneren'),
]

# ── de drie bevindingsblokken vervangen ─────────────────────────────────────
blokken = list(re.finditer(r'(?s)<section class="chapter (?:right|left) find"[^>]*>.*?</section>', s))
assert len(blokken) == 3, 'verwacht drie bevindingen, gevonden %d' % len(blokken)
for i in range(2, -1, -1):
    m, v = blokken[i], VONDSTEN[i]
    kant = 'right' if i % 2 == 0 else 'left'
    nieuw = '''<section class="chapter %s find"%s>
    <div class="ch-inner">
      <span class="ch-dot"></span>
      <div class="ch-body">
        <div class="f-head"><div class="f-num">%02d<span class="of">/ 03</span></div><div class="f-tag">Wat ik zag</div></div>
        <h2 class="f-kop">%s</h2>
        <p class="ch-text">%s</p>
        <button class="bronknop" type="button" aria-expanded="false" aria-controls="br%d">
          <b>%s</b> &middot; %s</button>
        <div class="uitklap" id="br%d"><div>
          <figure class="letterlijk"><q>%s</q>
            <figcaption>zoals het er stond op %s</figcaption></figure>
        </div></div>
      </div>
    </div>
  </section>''' % (kant, ' id="s2"' if i == 0 else '', i + 1, v['kop'], v['tekst'],
                   i + 1, DOM, GEZIEN, i + 1, v['citaat'], GEZIEN)
    s = s[:m.start()] + nieuw + s[m.end():]

# ── de hero en de aanloop: de kaart erkennen in plaats van herhalen ─────────
s = s.replace('Elf markten, dertig uur.',
              'Dertig uur in de week.')
s = s.replace('Allebei van jullie eigen site. Hieronder staat waar ik keek.',
              'Dat staat op jullie eigen klantenservicepagina. Hieronder staat wat ik '
              'daarnaast vond.')
s = s.replace('Ik ging kijken omdat jullie site in elf markten staat. Daarna bleef ik '
              'hangen bij iets anders.',
              'De elf taalmarkten en Gorgias had ik je al geschreven. Daarna ben ik '
              'doorgegaan, en dit vond ik.')

# ── de ask zegt wat dit is ─────────────────────────────────────────────────
s = s.replace('<p class="ask-sub">Vijftien minuten, video of telefoon.</p>',
              '<p class="ask-sub">Even eerlijk over wat dit is: wij doen het klantcontact '
              'voor webshops die harder groeien dan hun mailbox, in jullie naam en jullie '
              'toon. Vijftien minuten, video of telefoon.</p>')

# ── pagina-lokale stijl en gedrag voor de aantikbare bron ──────────────────
EXTRA = '''
<style>
/* Pagina-lokaal. lp.css wordt niet aangeraakt: daar hangen zevenduizend
   live pagina's aan. Gaat dit werken, dan verhuist het naar het component. */
.bronknop{display:inline-block;margin-top:.9rem;font:inherit;font-size:.74rem;
  font-weight:600;letter-spacing:.05em;color:var(--ink3);background:none;border:none;
  padding:0 0 2px;cursor:pointer;font-variant-numeric:tabular-nums;
  border-bottom:1px dashed rgba(var(--accent-rgb),.45)}
.bronknop b{color:var(--ink2);font-weight:600;letter-spacing:normal}
.bronknop:hover{border-bottom-color:var(--accent)}
.bronknop:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.uitklap{display:grid;grid-template-rows:0fr;transition:grid-template-rows .28s cubic-bezier(.16,1,.3,1)}
.uitklap.open{grid-template-rows:1fr}
.uitklap>div{overflow:hidden}
.letterlijk{margin-top:.75rem;background:rgba(var(--ink-rgb),.04);
  border-left:2px solid var(--accent);padding:.85rem 1rem}
.letterlijk q{display:block;font-size:.95rem;line-height:1.45;color:var(--ink);
  quotes:'\\201C' '\\201D'}
.letterlijk figcaption{margin-top:.5rem;font-size:.66rem;font-weight:600;
  letter-spacing:.06em;color:var(--ink3);font-variant-numeric:tabular-nums}
@media(prefers-reduced-motion:reduce){.uitklap{grid-template-rows:1fr}}
</style>
<script>
/* Het enige op deze pagina dat op hem reageert in plaats van op scroll. */
document.querySelectorAll('.bronknop').forEach(function(k){
  var d=document.getElementById(k.getAttribute('aria-controls'));
  if(!d) return;
  k.addEventListener('click',function(){
    var open=d.classList.toggle('open');
    k.setAttribute('aria-expanded',open?'true':'false');
    if(open&&window.pqTrack) window.pqTrack('bron-geopend');
  });
});
</script>
'''
s = s.replace('</body>', EXTRA + '</body>', 1)

io.open(DOEL, 'w', encoding='utf-8').write(s)
print('geschreven: %s (%d bytes)' % (os.path.relpath(DOEL), len(s.encode('utf-8'))))
