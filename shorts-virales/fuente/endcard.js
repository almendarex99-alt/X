// node endcard.js v|h salida.mp4  (o: node endcard.js v prev 1.5,3)
const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');const path=require('path');
(async()=>{const [m,out,ts]=process.argv.slice(2);const W=m==='v'?1080:1920,H=m==='v'?1920:1080;
  const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:W,height:H}});p.on('pageerror',e=>console.log('ERR',e.message));
  await p.goto('file://'+path.join(__dirname,'endcard.html')+'?m='+m);await p.evaluate(()=>window.ready);
  const grab=async t=>Buffer.from((await p.evaluate(t=>{render(t);return document.getElementById('c').toDataURL('image/jpeg',.93)},t)).split(',')[1],'base64');
  if(out==='prev'){for(const t of ts.split(','))fs.writeFileSync(path.join(__dirname,`end_${m}_${t}.jpg`),await grab(+t))}
  else{const DUR=await p.evaluate(()=>window.DUR),N=Math.round(DUR*30);const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-c:v','mjpeg','-r','30','-i','-','-c:v','libx264','-crf','19','-pix_fmt','yuv420p',out],{stdio:['pipe','inherit','inherit']});
    for(let i=0;i<N;i++){const buf=await grab(i/30);if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}ff.stdin.end();await new Promise(r=>ff.on('close',r))}
  await b.close()})();
