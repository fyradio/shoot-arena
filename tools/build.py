import base64,json,io,math,re
from PIL import Image,ImageDraw
def icon(n):
  S=n*4;im=Image.new('RGB',(S,S),(10,15,31));d=ImageDraw.Draw(im);c=S/2
  for r,col in [(0.46,(40,60,140)),(0.40,(255,200,61))]:
    d.ellipse([c-S*r,c-S*r,c+S*r,c+S*r],fill=col)
  pts=[]
  for i in range(240):
    th=i/240*2*math.pi;t=(th/(2*math.pi)*3)%1;rr=0.78+0.42*(t**1.6)*(1 if t<0.88 else (1-t)/0.12)
    pts.append((c+math.cos(th)*rr*S*0.3,c+math.sin(th)*rr*S*0.3))
  d.polygon(pts,fill=(255,59,47))
  d.ellipse([c-S*0.17,c-S*0.17,c+S*0.17,c+S*0.17],fill=(190,198,220))
  d.ellipse([c-S*0.1,c-S*0.1,c+S*0.1,c+S*0.1],fill=(63,208,255))
  for k in range(3):
    a=k*2*math.pi/3+0.5;x=c+math.cos(a)*S*0.43;y=c+math.sin(a)*S*0.43
    d.polygon([(x-S*0.03,y-S*0.06),(x+S*0.04,y-S*0.01),(x,y),(x+S*0.03,y+S*0.06),(x-S*0.04,y+S*0.01),(x,y)],fill=(255,255,255))
  im=im.resize((n,n),Image.LANCZOS);b=io.BytesIO();im.save(b,'PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
i192,i512,i180=icon(192),icon(512),icon(180)
man={"name":"旋風小鬥士 Shoot Legend","short_name":"旋風小鬥士","start_url":"./","scope":"./","display":"fullscreen","orientation":"any","background_color":"#0a0f1f","theme_color":"#0a0f1f",
 "icons":[{"src":i192,"sizes":"192x192","type":"image/png"},{"src":i512,"sizes":"512x512","type":"image/png","purpose":"any maskable"}]}
manu='data:application/manifest+json;base64,'+base64.b64encode(json.dumps(man,ensure_ascii=False).encode()).decode()
src=open('/home/claude/spin.html',encoding='utf-8').read()
src=re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n?','',src)
src=src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
src=src.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>','<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js" crossorigin="anonymous"></script>')
assert 'crossorigin="anonymous"' in src and 'fonts.googleapis' not in src
head=f'''<!doctype html>
<html lang="zh-Hant"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="旋風小鬥士">
<meta name="theme-color" content="#0a0f1f">
<link rel="manifest" href="{manu}">
<link rel="apple-touch-icon" href="{i180}">
<link rel="icon" type="image/png" href="{i192}">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font-size:14px;font-family:system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head><body>
'''
tail='''
<script>if('serviceWorker' in navigator){let hadCtl=!!navigator.serviceWorker.controller,rl=false;navigator.serviceWorker.addEventListener('controllerchange',()=>{if(hadCtl&&!rl){rl=true;location.reload()}hadCtl=true});addEventListener('load',()=>navigator.serviceWorker.register('sw.js',{updateViaCache:'none'}).then(r=>r.update()).catch(()=>{}))}</script>
</body></html>
'''
out=head+src+tail
open('/home/claude/shoot-arena/index.html','w',encoding='utf-8').write(out)
open('/home/claude/shoot-arena/sw.js','w').write('''const V='shoot-legend-v'+'64'; // 每次改版遞增
const THREE_URL='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(['./','./index.html']).then(()=>c.add(new Request(THREE_URL,{mode:'cors'})).catch(()=>{}))).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const same=new URL(e.request.url).origin===location.origin;e.respondWith((same?fetch(e.request.url,{cache:'no-store'}):fetch(e.request)).then(r=>{const cp=r.clone();caches.open(V).then(c=>c.put(e.request,cp));return r;}).catch(()=>caches.match(e.request,{ignoreSearch:true}).then(m=>m||(e.request.mode==='navigate'?caches.match('./index.html'):undefined))));
});
''')
print(len(out))
