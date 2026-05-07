function spawnConfetti(amount){
  const canvas = $('xp-confetti-canvas');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const ctx = canvas.getContext('2d');
  const colors = ['#c084fc','#a78bfa','#fbbf24','#4ade80','#60a5fa','#f472b6'];
  const count = Math.min(60, 20 + amount * 2);
  const particles = Array.from({length: count}, () => ({
    x: canvas.width * (0.3 + Math.random() * 0.4),
    y: canvas.height * 0.55,
    vx: (Math.random() - 0.5) * 8,
    vy: -(4 + Math.random() * 8),
    r: 4 + Math.random() * 5,
    color: colors[Math.floor(Math.random() * colors.length)],
    rot: Math.random() * Math.PI * 2,
    rspeed: (Math.random() - 0.5) * 0.2,
    shape: Math.random() > 0.5 ? 'rect' : 'circle',
    alpha: 1,
  }));
  let frame;
  function draw(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let alive = false;
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy; p.vy += 0.25;
      p.vx *= 0.98; p.rot += p.rspeed; p.alpha -= 0.018;
      if(p.alpha <= 0) return;
      alive = true;
      ctx.save();
      ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.translate(p.x, p.y); ctx.rotate(p.rot);
      ctx.fillStyle = p.color;
      if(p.shape === 'rect'){ ctx.fillRect(-p.r, -p.r/2, p.r*2, p.r); }
      else { ctx.beginPath(); ctx.arc(0,0,p.r,0,Math.PI*2); ctx.fill(); }
      ctx.restore();
    });
    if(alive) frame = requestAnimationFrame(draw);
    else ctx.clearRect(0,0,canvas.width,canvas.height);
  }
  if(frame) cancelAnimationFrame(frame);
  draw();
}
