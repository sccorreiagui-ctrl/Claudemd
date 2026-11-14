import fs from 'fs';
// hélice de DNA decorativa (vetorial, original)
function helix({x0=0,y0=0,len=900,A=62,turns=5,step=14,w=5}){
  const N=Math.floor(len/step); let rungs='',s1='',s2='';
  const pts=[];
  for(let i=0;i<=N;i++){const t=i/N*turns*2*Math.PI; pts.push({x1:x0+A*Math.sin(t),x2:x0-A*Math.sin(t),y:y0+i*step,d:Math.cos(t)});}
  pts.forEach((p,i)=>{ if(i%2===0){const front=p.d>0; rungs+=`<line x1="${p.x1.toFixed(1)}" y1="${p.y}" x2="${p.x2.toFixed(1)}" y2="${p.y}" stroke="#fff" stroke-opacity="${(0.12+0.25*Math.abs(Math.sin(i/N*turns*2*Math.PI))).toFixed(2)}" stroke-width="3" stroke-linecap="round"/>`; }});
  for(let i=0;i<N;i++){const a=pts[i],b=pts[i+1];
    const o1=(0.25+0.7*(a.d+1)/2).toFixed(2), o2=(0.25+0.7*(1-a.d)/2).toFixed(2);
    s1+=`<line x1="${a.x1.toFixed(1)}" y1="${a.y}" x2="${b.x1.toFixed(1)}" y2="${b.y}" stroke="#b690ec" stroke-opacity="${o1}" stroke-width="${w}" stroke-linecap="round"/>`;
    s2+=`<line x1="${a.x2.toFixed(1)}" y1="${a.y}" x2="${b.x2.toFixed(1)}" y2="${b.y}" stroke="#7fe0a8" stroke-opacity="${o2}" stroke-width="${w}" stroke-linecap="round"/>`;}
  return `<g>${rungs}${s2}${s1}</g>`;
}
fs.writeFileSync('src/svg/helix.svg', helix({x0:0,y0:0,len:1000,A:58,turns:5.5,step:9}));
console.log('helix ok');
