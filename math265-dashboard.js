async function renderDashboard(){
  // Module grid
  const grid=$('module-grid');
  grid.innerHTML='';
  const mods=[{key:'polynomials',label:'Polynomials'},{key:'linear_equations',label:'Linear Eqns'},{key:'sequences',label:'Sequences'},{key:'factoring',label:'Factoring'},{key:'quadratic',label:'Quadratics'},{key:'exponents',label:'Exponents'},{key:'radicals',label:'Radicals'},{key:'fractions',label:'Fractions'},{key:'rational_expressions',label:'Rational Exp'},{key:'inequalities',label:'Inequalities'},{key:'absolute_value',label:'Abs Value'},{key:'systems',label:'Systems'},{key:'probability',label:'Probability'},{key:'trig',label:'Trig'},{key:'logs',label:'Logs'},{key:'composition',label:'Composition'},{key:'limits',label:'Limits'},{key:'asymptotes',label:'Asymptotes'},{key:'epsilon_delta',label:'Epsilon-Delta'},{key:'derivatives',label:'Derivatives'},{key:'increasing_decreasing',label:'Incr/Decr'},{key:'extrema',label:'Extrema'},{key:'integration',label:'Integration'},{key:'mvt',label:'MVT'},{key:'numerical_methods',label:'Numerical'},{key:'indeterminate_forms',label:"L'Hospital"},{key:'hyperbolic_apps',label:'Hyperbolic'},{key:'function_construction',label:'Func Constr'},{key:'center_of_mass',label:'Center Mass'},{key:'adv_integration',label:'Adv Integr'}];
  mods.forEach(({key,label})=>{
    const card=document.createElement('div');
    card.className='module-card';
    let html=`<h4>${label}</h4>`;
    [1,2,3,4,5].forEach(d=>{
      const r=store[key][d];
      const acc=r.attempts>0?Math.round(r.correct/r.attempts*100):null;
      const accStr=acc!==null?`${acc}%`:'—';
      const cls=acc===null?'':acc>=80?'high':acc>=60?'mid':'low';
      html+=`<div class="diff-row"><span>Diff ${d}</span><span class="acc ${cls}">${accStr} <small style="color:var(--muted)">(${r.attempts})</small></span></div>`;
    });
    card.innerHTML=html;
    grid.appendChild(card);
  });

  // Spark chart
  const spark=$('spark-chart');
  spark.innerHTML='';
  const sessions=store.sessions.slice(-10);
  if(sessions.length===0){
    spark.innerHTML='<span style="color:var(--muted);font-size:12px;">No sessions yet</span>';
  } else {
    sessions.forEach(s=>{
      const bar=document.createElement('div');
      bar.className='spark-bar';
      bar.style.height=Math.round(s.accuracy*100)+'%';
      bar.title=`${s.date}: ${Math.round(s.accuracy*100)}%`;
      spark.appendChild(bar);
    });
  }

  // Badges
  const bg=$('badge-grid');
  bg.innerHTML='';
  ALL_BADGES.forEach(b=>{
    const div=document.createElement('div');
    div.className='badge'+(store.badges[b.id]?' earned':'');
    div.textContent=b.label;
    bg.appendChild(div);
  });

  // Totals
  let totalAttempts=0,totalCorrect=0;
  ALL_MODULES.forEach(m=>{
    [1,2,3,4,5].forEach(d=>{ if(store[m]&&store[m][d]){ totalAttempts+=store[m][d].attempts; totalCorrect+=store[m][d].correct; } });
  });
  $('dash-totals').innerHTML=`
    Total problems: <strong>${totalAttempts}</strong><br>
    Total correct: <strong>${totalCorrect}</strong><br>
    All-time accuracy: <strong>${totalAttempts>0?Math.round(totalCorrect/totalAttempts*100)+'%':'—'}</strong>
  `;

  // API sections
  try {
    const [trendData, weakData] = await Promise.all([
      fetch(`${API_BASE}/api/stats/trend?days=30`).then(r=>r.json()),
      fetch(`${API_BASE}/api/stats/weak?min_attempts=3&limit=10`).then(r=>r.json()),
    ]);
    renderTrendChart(trendData);
    renderVolumeChart(trendData);
    renderWeakSpots(weakData);
  } catch(e){
    $('trend-chart').style.display='none';
    $('trend-empty').style.display='block';
    $('trend-empty').textContent='API offline — start backend to see trend data';
    $('weak-spots-list').innerHTML='<span style="color:var(--muted);font-size:12px;">API offline</span>';
  }
}

function renderTrendChart(data){
  const canvas=$('trend-chart'), empty=$('trend-empty');
  if(!data||data.length===0){
    canvas.style.display='none'; empty.style.display='block';
    empty.textContent='No trend data yet — answer some problems first';
    return;
  }
  canvas.style.display='block'; empty.style.display='none';
  const ctx=canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  ctx.clearRect(0,0,W,H);
  const points=data.map(d=>d.attempts>0?d.correct/d.attempts:null);
  const labels=data.map(d=>d.day.slice(5));
  ctx.fillStyle='#1a1d27'; ctx.fillRect(0,0,W,H);
  ctx.lineWidth=1;
  [0.25,0.5,0.75,1.0].forEach(y=>{
    const py=H-20-(H-30)*y;
    ctx.strokeStyle='#2a2d3a'; ctx.beginPath(); ctx.moveTo(30,py); ctx.lineTo(W-10,py); ctx.stroke();
    ctx.fillStyle='#555'; ctx.font='9px monospace'; ctx.fillText(Math.round(y*100)+'%',2,py+3);
  });
  const n=points.length, stepX=(W-40)/Math.max(n-1,1);
  ctx.strokeStyle='#4d9fff'; ctx.lineWidth=2; ctx.beginPath();
  let started=false;
  points.forEach((p,i)=>{
    if(p===null){started=false;return;}
    const x=30+i*stepX, y=H-20-(H-30)*p;
    if(!started){ctx.moveTo(x,y);started=true;}else ctx.lineTo(x,y);
  });
  ctx.stroke();
  points.forEach((p,i)=>{
    if(p===null)return;
    const x=30+i*stepX, y=H-20-(H-30)*p;
    ctx.fillStyle=p>=0.8?'#4caf50':p>=0.6?'#ffc107':'#f44336';
    ctx.beginPath(); ctx.arc(x,y,3,0,Math.PI*2); ctx.fill();
  });
  ctx.fillStyle='#666'; ctx.font='9px monospace';
  if(labels.length>0) ctx.fillText(labels[0],30,H-5);
  if(labels.length>1) ctx.fillText(labels[labels.length-1],W-34,H-5);
}

function renderVolumeChart(data){
  const canvas=$('volume-chart'), empty=$('volume-empty');
  if(!data||data.length===0){
    canvas.style.display='none'; empty.style.display='block';
    empty.textContent='No data yet';
    return;
  }
  canvas.style.display='block'; empty.style.display='none';
  const ctx=canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#1a1d27'; ctx.fillRect(0,0,W,H);
  const counts=data.map(d=>d.attempts);
  const labels=data.map(d=>d.day.slice(5));
  const maxCount=Math.max(...counts,1);
  const n=counts.length;
  const padL=28, padR=6, padT=8, padB=18;
  const chartW=W-padL-padR, chartH=H-padT-padB;
  const barW=Math.max(2,Math.floor(chartW/n)-2);
  const step=chartW/n;
  [0.25,0.5,0.75,1.0].forEach(f=>{
    const py=padT+chartH*(1-f);
    ctx.strokeStyle='#2a2d3a'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(padL,py); ctx.lineTo(W-padR,py); ctx.stroke();
    ctx.fillStyle='#555'; ctx.font='9px monospace'; ctx.fillText(Math.round(f*maxCount),2,py+3);
  });
  counts.forEach((c,i)=>{
    const barH=Math.round(chartH*(c/maxCount));
    const x=padL+i*step+(step-barW)/2;
    const y=padT+chartH-barH;
    ctx.fillStyle='#4d9fff';
    ctx.fillRect(x,y,barW,barH);
  });
  ctx.fillStyle='#666'; ctx.font='9px monospace';
  if(labels.length>0) ctx.fillText(labels[0],padL,H-4);
  if(labels.length>1) ctx.fillText(labels[labels.length-1],W-padR-24,H-4);
}

function renderWeakSpots(data){
  const el=$('weak-spots-list');
  if(!data||data.length===0){
    el.innerHTML='<span style="color:var(--muted);font-size:12px;">No weak spots yet — need ≥3 attempts per problem</span>';
    return;
  }
  el.innerHTML=data.map(w=>{
    const acc=Math.round(w.accuracy*100);
    const cls=acc>=80?'high':acc>=60?'mid':'low';
    const mod=w.module.charAt(0).toUpperCase()+w.module.slice(1);
    return `<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--border);font-size:12px;">
      <span class="acc ${cls}" style="min-width:36px">${acc}%</span>
      <span style="color:var(--muted);min-width:80px">${mod} D${w.difficulty}</span>
      <span style="color:var(--text);font-family:monospace;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${w.problem_tex}">${w.problem_tex}</span>
      <span style="color:var(--muted)">${w.attempts} tries</span>
    </div>`;
  }).join('');
}
