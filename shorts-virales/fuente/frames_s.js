// node frames.js preview v7 "t1,t2" | node frames.js video v7 out.mp4 | node frames.js cover v7 out.png
const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');const path=require('path');
(async()=>{
  const [mode,v,arg]=process.argv.slice(2);const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>console.log('LOG',m.text()));
  await p.goto('file://'+path.join(__dirname,'index_s.html')+'?v='+v);await p.evaluate(()=>window.ready);
  const DUR=await p.evaluate(()=>window.DUR);
  fs.writeFileSync(path.join(__dirname,v+'_cues.json'),JSON.stringify({dur:DUR,cues:await p.evaluate(()=>window.CUES)}));
  const grab=async(t,c,fmt='image/jpeg')=>Buffer.from((await p.evaluate(([t,c,f])=>{render(t,c);return document.getElementById('c').toDataURL(f,.93)},[t,c,fmt])).split(',')[1],'base64');
  if(mode==='preview'){for(const t of arg.split(',').map(Number))fs.writeFileSync(path.join(__dirname,`${v}_p_${t}.jpg`),await grab(t,false))}
  else if(mode==='cover'){fs.writeFileSync(arg,await grab(await p.evaluate(()=>window.COVER_T),true,'image/png'))}
  else{const fps=30,N=Math.round(DUR*fps);const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-c:v','mjpeg','-r',String(fps),'-i','-','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',arg],{stdio:['pipe','inherit','inherit']});
    for(let i=0;i<N;i++){const buf=await grab(i/fps,false);if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300===0)console.log(v,'frame',i)}
    ff.stdin.end();await new Promise(r=>ff.on('close',r))}
  await b.close();
})();
