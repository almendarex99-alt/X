import {createRequire} from 'module'; const require=createRequire('/');const {chromium}=require(require.resolve('playwright',{paths:[process.env.NODE_PATH||'/opt/node22/lib/node_modules','/usr/local/lib/node_modules','/usr/lib/node_modules']}));
import fs from 'fs';
const [,, mode, a, b, c, d] = process.argv;
const browser=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--no-sandbox']});
const page=await browser.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
page.on('console',m=>{if(m.type()==='error')console.log('ERR',m.text())});
page.on('pageerror',e=>console.log('PAGEERR',e.message));
await page.goto('http://localhost:8123/scene.html');
await page.waitForFunction('window.ready===true',null,{timeout:60000});
if(mode==='test'){ // times list
  fs.mkdirSync('test',{recursive:true});
  for(const t of a.split(',')){const t0=Date.now();await page.evaluate(t=>window.renderFrame(t),+t);await page.screenshot({path:`test/t_${t}.jpg`,type:'jpeg',quality:90});console.log(t,Date.now()-t0,'ms')}
}else{ // range: start end step outdir
  const s=+a,e=+b,st=+c;fs.mkdirSync(d,{recursive:true});
  for(let f=s;f<e;f+=st){const t=f/30;await page.evaluate(t=>window.renderFrame(t),t);await page.screenshot({path:`${d}/f_${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:93})}
}
await browser.close();
