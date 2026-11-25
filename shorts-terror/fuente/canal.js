const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+path.join(__dirname,'canal.html'));await p.evaluate(()=>window.ready);const r=await p.evaluate(()=>window.make());
const out=process.argv[2];fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'banner_2560x1440.png'),Buffer.from(r.banner.split(',')[1],'base64'));fs.writeFileSync(path.join(out,'banner_3840x2160.jpg'),Buffer.from(r.banner4k.split(',')[1],'base64'));fs.writeFileSync(path.join(out,'perfil_800x800.png'),Buffer.from(r.avatar.split(',')[1],'base64'));await b.close()})();
