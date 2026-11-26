const fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
(async()=>{
  const dir=path.join(__dirname,'..','diagrams');
  const names=fs.readdirSync(dir).filter(f=>f.endsWith('.svg')).sort();
  let html='<html><body style="margin:8px;font:11px Inter;background:#fff"><div style="display:flex;flex-wrap:wrap;gap:10px">';
  for(const n of names){html+=`<div style="border:1px solid #ddd;padding:4px"><div>${n}</div>${fs.readFileSync(path.join(dir,n),'utf8')}</div>`;}
  html+='</div></body></html>';
  const out=process.argv[2]||'/tmp/contact.html';
  fs.writeFileSync(out,html);
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1250,height:900},deviceScaleFactor:1.3});
  await p.goto('file://'+out);await p.screenshot({path:out.replace('.html','.png'),fullPage:true});await b.close();
})();
