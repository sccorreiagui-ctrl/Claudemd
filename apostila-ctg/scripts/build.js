// Monta apostila.html (KaTeX + SVG inline) e gera o PDF A4 com Playwright.
const fs=require('fs'),path=require('path');
const katex=require('katex');
const {chromium}=require('playwright');
const ROOT=path.join(__dirname,'..');
const BUILD=path.join(ROOT,'build');
fs.mkdirSync(BUILD,{recursive:true});
fs.mkdirSync(path.join(BUILD,'png'),{recursive:true});
// KaTeX css + fontes locais
const kdist=path.join(ROOT,'node_modules','katex','dist');
fs.mkdirSync(path.join(BUILD,'katex','fonts'),{recursive:true});
fs.copyFileSync(path.join(kdist,'katex.min.css'),path.join(BUILD,'katex','katex.min.css'));
for(const f of fs.readdirSync(path.join(kdist,'fonts'))) if(f.endsWith('.woff2')) fs.copyFileSync(path.join(kdist,'fonts',f),path.join(BUILD,'katex','fonts',f));

const macros={
  "\\az":"\\textcolor{##1f5fbf}{#1}","\\vd":"\\textcolor{##1e8a4c}{#1}","\\rx":"\\textcolor{##6b3fa0}{#1}",
  "\\lj":"\\textcolor{##c4620a}{#1}","\\vm":"\\textcolor{##c62828}{#1}","\\ou":"\\textcolor{##8a6508}{#1}",
  "\\ue":"\\text{ u.c.}","\\ua":"\\text{ u.a.}"
};
function tex(src,display){
  try{return katex.renderToString(src,{displayMode:display,throwOnError:true,output:'html',macros,strict:'ignore',trust:false});}
  catch(e){throw new Error('KaTeX falhou em: '+src+'\n'+e.message);}
}
function math(s){
  s=s.replace(/\$\$([\s\S]+?)\$\$/g,(_,m)=>tex(m.trim(),true));
  s=s.replace(/([(\[“]?)\$([^$\n]+?)\$([.,;:!?)\]”]*)/g,(_,pre,m,post)=>(pre||post)?`<span class="nb">${pre}${tex(m.trim(),false)}${post}</span>`:tex(m.trim(),false));
  return s;
}
function svgs(s){
  return s.replace(/\{\{svg:([\w-]+)\}\}/g,(_,n)=>{
    const f=path.join(ROOT,'diagrams',n+'.svg');
    if(!fs.existsSync(f)) throw new Error('SVG ausente: '+n);
    return fs.readFileSync(f,'utf8').replace(/ width="[\d.]+" height="[\d.]+"/,'');
  });
}
const SECTIONS=[
 'Ponto e reta · Revisão','Ponto e reta · Decisões',
 'Ponto e reta · Exercícios','Ponto e reta · Exercícios','Ponto e reta · Exercícios','Ponto e reta · Exercício integrador',
 'Circunferência · Revisão','Circunferência · Completar quadrados','Circunferência · Qual método?',
 'Circunferência · Exercícios','Circunferência · Exercícios','Circunferência · Exercícios','Circunferência · Exercício avançado','Circunferência · Questão-síntese'];
const secName=i=>i<6?'Ponto e Reta':'Circunferência';
let pages='';
const N=14;
for(let i=1;i<=N;i++){
  const f=path.join(ROOT,'pages','p'+String(i).padStart(2,'0')+'.html');
  const raw=fs.readFileSync(f,'utf8');
  const body=svgs(math(raw));
  pages+=`<section class="page ${[1,2,7,8,9].includes(i)?'th':'ex'}" id="p${i}"><div class="hd"><div class="brand"><i>CTG</i> GEOMETRIA ANALÍTICA</div><div>${SECTIONS[i-1]} · PAS 3/UnB 2026</div></div><div class="bd">${body}</div><div class="ft"><span>CTG | Geometria Analítica | Ponto e Reta / Circunferência | PAS 3/UnB | Página ${i}/${N}</span><span>${i<=2||(i>=7&&i<=9)?'Teoria':'Exercícios resolvidos'}</span></div></section>`;
}
const css=fs.readFileSync(path.join(ROOT,'style.css'),'utf8');
const html=`<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>CTG — Geometria Analítica — PAS 3/UnB 2026</title><link rel="stylesheet" href="katex/katex.min.css"><style>${css}</style></head><body>${pages}</body></html>`;
const htmlPath=path.join(BUILD,'apostila.html');
fs.writeFileSync(htmlPath,html);
(async()=>{
  const b=await chromium.launch();
  const pg=await b.newPage({viewport:{width:900,height:1200},deviceScaleFactor:1.7});
  await pg.goto('file://'+htmlPath);
  await pg.evaluate(()=>document.fonts.ready);
  const rep=await pg.evaluate(()=>{
    const out=[];
    const MM=96/25.4;
    for(const p of document.querySelectorAll('.page')){
      const bd=p.querySelector('.bd');
      const th=p.classList.contains('th');
      const lo=9.4, hi=th?10.8:11.6;
      const saveJ=bd.style.justifyContent;
      const measure=()=>{ // folga em mm com empilhamento natural (gap mínimo 3mm entre cartões)
        bd.style.justifyContent='flex-start'; bd.style.gap=th?'0':'3mm';
        const kids=[...bd.children]; const last=kids[kids.length-1];
        const cs=getComputedStyle(last);
        const bottom=last.getBoundingClientRect().bottom+parseFloat(cs.marginBottom);
        return (bd.getBoundingClientRect().bottom-bottom)/MM;
      };
      let best=lo;
      for(let s=lo;s<=hi+1e-6;s+=0.1){
        p.style.fontSize=s.toFixed(1)+'pt';
        if(measure()>=3.0) best=s; else break;
      }
      p.style.fontSize=best.toFixed(1)+'pt';
      const free=measure();
      bd.style.justifyContent=saveJ; bd.style.gap='';
      out.push({id:p.id,over:bd.scrollHeight-bd.clientHeight,free:Math.round(free*10)/10,font:best.toFixed(1)});
    }
    return out;
  });
  let bad=0;
  for(const r of rep){
    console.log(r.id.padEnd(4),'estouro(px):',String(r.over).padStart(4),'  folga(mm):',String(r.free).padStart(5),'  fonte(pt):',r.font);
    if(r.over>1) bad++;
  }
  if(!process.argv.includes('--nopdf')){
    await pg.pdf({path:path.join(ROOT,'CTG_GEOMETRIA_ANALITICA_PAS3_2026.pdf'),width:'210mm',height:'297mm',printBackground:true,preferCSSPageSize:true});
  }
  if(!process.argv.includes('--nopng')){
    const els=await pg.$$('.page');
    for(let i=0;i<els.length;i++) await els[i].screenshot({path:path.join(BUILD,'png','p'+String(i+1).padStart(2,'0')+'.png')});
  }
  await b.close();
  if(bad){console.error('PÁGINAS COM ESTOURO:',bad);process.exitCode=2;}
})();
