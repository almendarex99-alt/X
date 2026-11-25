// uso: node frames.js preview "t1,t2,..."   |  node frames.js video out.mp4  |  node frames.js cover cover.png
const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');const path=require('path');
(async()=>{
  const mode=process.argv[2];const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>console.log('LOG',m.text()));
  await p.goto('file://'+path.join(__dirname,'short.html'));await p.evaluate(()=>window.ready);
  fs.writeFileSync(path.join(__dirname,'cues.json'),JSON.stringify(await p.evaluate(()=>window.CUES)));
  const grab=async(t,cover)=>Buffer.from((await p.evaluate(([t,c])=>{render(t,c);return document.getElementById('c').toDataURL('image/jpeg',.93)},[t,cover])).split(',')[1],'base64');
  if(mode==='preview'){for(const t of process.argv[3].split(',').map(Number)){fs.writeFileSync(path.join(__dirname,`p_${t}.jpg`),await grab(t,false))}}
  else if(mode==='cover'){const png=(await p.evaluate(()=>{render(43.1,true);return document.getElementById('c').toDataURL('image/png')})).split(',')[1];fs.writeFileSync(process.argv[3],Buffer.from(png,'base64'))}
  else{const fps=30,N=Math.round(50*fps);const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-c:v','mjpeg','-r',String(fps),'-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',process.argv[3]],{stdio:['pipe','inherit','inherit']});
    const t0=Date.now();for(let i=0;i<N;i++){const buf=await grab(i/fps,false);if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%150===0)console.log('frame',i,((Date.now()-t0)/1000).toFixed(0)+'s')}
    ff.stdin.end();await new Promise(r=>ff.on('close',r))}
  await b.close();
})();
