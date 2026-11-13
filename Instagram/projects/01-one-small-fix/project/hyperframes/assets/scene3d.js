import * as THREE from '../lib/three.module.min.js';

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v));
}

function smoothstep(a, b, x) {
  const t = clamp((x - a) / Math.max(1e-6, b - a), 0, 1);
  return t * t * (3 - 2 * t);
}

function createBrickTexture() {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 512;
  const ctx = c.getContext('2d');
  ctx.fillStyle = '#1b1318';
  ctx.fillRect(0, 0, 512, 512);
  const rng = mulberry32(421);
  const rows = 16;
  const cols = 6;
  const bh = 512 / rows;
  const bw = 512 / cols;
  for (let r = 0; r < rows; r++) {
    const offset = (r % 2) * (bw * 0.5);
    for (let col = -1; col <= cols; col++) {
      const shade = 0.78 + rng() * 0.36;
      const rr = Math.round(78 * shade);
      const gg = Math.round(41 * shade);
      const bb = Math.round(39 * shade);
      ctx.fillStyle = `rgb(${rr},${gg},${bb})`;
      ctx.fillRect(col * bw + offset + 3, r * bh + 3, bw - 6, bh - 6);
    }
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(2.2, 2.2);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function createLaptopScreenTexture() {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 320;
  const ctx = c.getContext('2d');
  ctx.fillStyle = '#090f1d';
  ctx.fillRect(0, 0, 512, 320);
  // Sidebar
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, 110, 320);
  // Top bar
  ctx.fillStyle = '#141f35';
  ctx.fillRect(0, 0, 512, 26);
  const colors = ['#38bdf8', '#38d9a9', '#fbbf24', '#f87171', '#94a3b8'];
  const rng = mulberry32(888);
  for (let i = 0; i < 16; i++) {
    ctx.fillStyle = '#334155';
    ctx.fillRect(14, 42 + i * 16, 48 + rng() * 32, 6);
    const x0 = 132 + (i % 3) * 18;
    ctx.fillStyle = colors[Math.floor(rng() * colors.length)];
    ctx.fillRect(x0, 40 + i * 16, 65 + rng() * 140, 8);
    if (rng() > 0.35) {
      ctx.fillStyle = colors[Math.floor(rng() * colors.length)];
      ctx.fillRect(x0 + 160, 40 + i * 16, 40 + rng() * 90, 8);
    }
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function createHoloPanelTexture(mode = 'tree') {
  const c = document.createElement('canvas');
  c.width = 360;
  c.height = 240;
  const ctx = c.getContext('2d');
  ctx.fillStyle = 'rgba(11, 18, 34, 0.92)';
  ctx.fillRect(0, 0, 360, 240);
  ctx.strokeStyle = mode === 'alert' ? '#f87171' : mode === 'revert' ? '#fbbf24' : '#2f5d6b';
  ctx.lineWidth = 4;
  ctx.strokeRect(4, 4, 352, 232);

  ctx.font = 'bold 20px monospace';
  if (mode === 'revert') {
    ctx.fillStyle = '#fbbf24';
    ctx.fillText('$ git reset --hard', 22, 48);
    ctx.fillStyle = '#38d9a9';
    ctx.font = '18px monospace';
    ctx.fillText('HEAD is now clean', 22, 88);
    ctx.fillText('+ hero.css (1 line)', 22, 124);
    ctx.fillStyle = '#94a3b8';
    ctx.fillText('185 files restored', 22, 160);
  } else if (mode === 'alert') {
    ctx.fillStyle = '#f87171';
    ctx.fillText('.env.production', 22, 48);
    ctx.fillStyle = '#e2e8f0';
    ctx.font = '17px monospace';
    ctx.fillText('stripe/webhook.ts', 22, 92);
    ctx.fillStyle = '#f87171';
    ctx.fillText('KEY EXPIRED: AUG 04', 22, 128);
    ctx.fillText('HTTP 401 Unauthorized', 22, 166);
  } else {
    ctx.fillStyle = '#38d9a9';
    ctx.fillText('src/', 22, 42);
    ctx.font = '17px monospace';
    const lines = [
      ['  hero.css', '#10b981'],
      ['  db/schema.ts', '#fbbf24'],
      ['  onboarding/', '#fbbf24'],
      ['  tests/ (412)', '#f87171'],
      ['  SCOPE.md', '#38bdf8'],
    ];
    lines.forEach(([txt, col], idx) => {
      ctx.fillStyle = col;
      ctx.fillText(txt, 22, 78 + idx * 32);
    });
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function drawClaudeStarburst(ctx, cx, cy, rOuter, color = '#ffa726', glow = '#ff6f00') {
  ctx.save();
  ctx.translate(cx, cy);
  ctx.shadowColor = glow;
  ctx.shadowBlur = rOuter * 0.45;
  ctx.fillStyle = color;
  const spokes = 11;
  for (let i = 0; i < spokes; i++) {
    ctx.save();
    ctx.rotate((i * Math.PI * 2) / spokes + 0.15);
    ctx.beginPath();
    ctx.moveTo(-rOuter * 0.09, -rOuter * 0.18);
    ctx.lineTo(rOuter * 0.09, -rOuter * 0.18);
    ctx.lineTo(rOuter * 0.13, -rOuter);
    ctx.arc(0, -rOuter, rOuter * 0.13, 0, Math.PI, true);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }
  ctx.beginPath();
  ctx.arc(0, 0, rOuter * 0.26, 0, Math.PI * 2);
  ctx.fillStyle = '#ffe082';
  ctx.fill();
  ctx.restore();
}

function createRoundedRectShape(w, h, r) {
  const s = new THREE.Shape();
  const x = -w / 2;
  const y = -h / 2;
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y);
  s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r);
  s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h);
  s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r);
  s.quadraticCurveTo(x, y, x + r, y);
  return s;
}

function createClaudeFrontMarkingsTexture() {
  const c = document.createElement('canvas');
  c.width = 256;
  c.height = 256;
  const ctx = c.getContext('2d');
  ctx.clearRect(0, 0, 256, 256);
  drawClaudeStarburst(ctx, 128, 128, 96, '#ffcb77', '#ff8c1a');
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function createClaudeAIBadgeTexture() {
  const c = document.createElement('canvas');
  c.width = 256;
  c.height = 256;
  const ctx = c.getContext('2d');
  ctx.clearRect(0, 0, 256, 256);
  ctx.save();
  ctx.shadowColor = '#ff981a';
  ctx.shadowBlur = 24;
  ctx.strokeStyle = '#ffd591';
  ctx.lineWidth = 11;
  ctx.beginPath();
  ctx.roundRect(28, 28, 200, 200, 38);
  ctx.stroke();

  ctx.fillStyle = '#ffe4b5';
  ctx.font = 'bold 104px "Outfit", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('AI', 128, 134);
  ctx.restore();
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function createClaudeVisorRenderer() {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 192;
  const ctx = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  let lastKey = '';

  function draw(amp, t, mood) {
    const bucket = Math.round(amp * 14);
    const tBucket = Math.floor(t * 15);
    const key = `${bucket}|${tBucket}|${mood}`;
    if (key === lastKey) return;
    lastKey = key;

    ctx.clearRect(0, 0, 512, 192);

    // Right overlapping wide audio waveform glass panel
    ctx.save();
    ctx.fillStyle = 'rgba(255, 224, 185, 0.16)';
    ctx.strokeStyle = 'rgba(255, 214, 153, 0.55)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(172, 18, 322, 146, 28);
    ctx.fill();
    ctx.stroke();

    // Waveform vertical bars (warm glowing coral/cream)
    const bars = 13;
    const bx0 = 204;
    const bw = 10;
    const gap = 11;
    for (let i = 0; i < bars; i++) {
      const distMid = 1 - Math.abs(i - 6) / 7;
      const baseWave = 0.25 + 0.55 * distMid * (0.4 + 0.6 * Math.abs(Math.sin(t * 7.5 + i * 1.1)));
      const level = clamp(0.18 + baseWave * (0.28 + amp * 1.15), 0.14, 0.96);
      const bh = level * 102;
      ctx.shadowColor = mood === 'guilt_sweat' ? '#38bdf8' : '#ffab40';
      ctx.shadowBlur = 10;
      ctx.fillStyle = mood === 'guilt_sweat' ? '#bae6fd' : '#ffe8c2';
      ctx.beginPath();
      ctx.roundRect(bx0 + i * (bw + gap), 91 - bh / 2, bw, bh, 5);
      ctx.fill();
    }
    ctx.restore();

    // Left overlapping prompt glass badge ">_"
    ctx.save();
    ctx.fillStyle = 'rgba(28, 25, 36, 0.68)';
    ctx.strokeStyle = 'rgba(255, 214, 153, 0.68)';
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.roundRect(18, 34, 174, 128, 28);
    ctx.fill();
    ctx.stroke();

    ctx.shadowColor = '#ffb74d';
    ctx.shadowBlur = 16;
    ctx.fillStyle = '#fff5e1';
    ctx.font = 'bold 74px "JetBrains Mono", monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('>_', 105, 100);
    ctx.restore();

    tex.needsUpdate = true;
  }

  return { tex, draw };
}

function buildTariq() {
  const root = new THREE.Group();

  const skinMat = new THREE.MeshStandardMaterial({
    color: 0xc68b67,
    roughness: 0.76,
    metalness: 0.03,
    flatShading: true,
  });
  const skinDarkMat = new THREE.MeshStandardMaterial({
    color: 0x9a6344,
    roughness: 0.8,
    flatShading: true,
  });
  const hairMat = new THREE.MeshStandardMaterial({
    color: 0x241917,
    roughness: 0.88,
    flatShading: true,
  });
  const beanieMat = new THREE.MeshStandardMaterial({
    color: 0x2a7f8e,
    roughness: 0.82,
    flatShading: true,
  });
  const beanieCuffMat = new THREE.MeshStandardMaterial({
    color: 0x236a77,
    roughness: 0.85,
    flatShading: true,
  });
  const jacketMat = new THREE.MeshStandardMaterial({
    color: 0x2f5d6b,
    roughness: 0.72,
    metalness: 0.06,
    flatShading: true,
  });
  const teeMat = new THREE.MeshStandardMaterial({
    color: 0xece5d5,
    roughness: 0.84,
    flatShading: true,
  });
  const pantsMat = new THREE.MeshStandardMaterial({
    color: 0x1e293b,
    roughness: 0.85,
    flatShading: true,
  });
  const shoeMat = new THREE.MeshStandardMaterial({
    color: 0xa88463,
    roughness: 0.78,
    flatShading: true,
  });
  const goldMat = new THREE.MeshStandardMaterial({
    color: 0xd4a34f,
    roughness: 0.3,
    metalness: 0.78,
  });
  const glassLensMat = new THREE.MeshStandardMaterial({
    color: 0xbae6fd,
    transparent: true,
    opacity: 0.18,
    roughness: 0.1,
    metalness: 0.2,
  });
  const scleraMat = new THREE.MeshBasicMaterial({ color: 0xf8fafc });
  const pupilMat = new THREE.MeshBasicMaterial({ color: 0x0f172a });
  const mouthDarkMat = new THREE.MeshBasicMaterial({ color: 0x3b1518 });
  const lipMat = new THREE.MeshStandardMaterial({ color: 0x8f4e42, roughness: 0.72, flatShading: true });

  // Torso (bomber jacket around cream tee)
  const torsoPivot = new THREE.Group();
  torsoPivot.position.set(0, 1.0, 0);
  root.add(torsoPivot);

  const teeMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.36, 0.82, 8), teeMat);
  teeMesh.position.set(0, 0.42, 0.04);
  teeMesh.scale.set(1.0, 1.0, 0.72);
  teeMesh.castShadow = true;
  torsoPivot.add(teeMesh);

  // Left & right jacket panels (unzipped open look)
  [-1, 1].forEach((side) => {
    const panel = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.84, 0.56), jacketMat);
    panel.position.set(side * 0.22, 0.43, -0.02);
    panel.castShadow = true;
    panel.receiveShadow = true;
    torsoPivot.add(panel);
  });
  // Jacket back + collar
  const backPanel = new THREE.Mesh(new THREE.CylinderGeometry(0.39, 0.42, 0.82, 8), jacketMat);
  backPanel.position.set(0, 0.42, -0.06);
  backPanel.scale.set(1.02, 1, 0.75);
  backPanel.castShadow = true;
  torsoPivot.add(backPanel);

  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.24, 0.06, 6, 10), beanieCuffMat);
  collar.rotation.x = Math.PI / 2;
  collar.position.set(0, 0.85, 0);
  torsoPivot.add(collar);

  // Neck
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.22, 7), skinDarkMat);
  neck.position.set(0, 0.94, 0.02);
  torsoPivot.add(neck);

  // Arms
  function makeArm(side) {
    const shoulder = new THREE.Group();
    shoulder.position.set(side * 0.44, 0.76, 0);
    const upper = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.1, 0.42, 7), jacketMat);
    upper.position.set(0, -0.2, 0);
    upper.castShadow = true;
    shoulder.add(upper);

    const elbow = new THREE.Group();
    elbow.position.set(0, -0.4, 0);
    shoulder.add(elbow);

    const forearm = new THREE.Mesh(new THREE.CylinderGeometry(0.095, 0.085, 0.36, 7), jacketMat);
    forearm.position.set(0, -0.17, 0);
    forearm.castShadow = true;
    elbow.add(forearm);

    const hand = new THREE.Mesh(new THREE.DodecahedronGeometry(0.095, 0), skinMat);
    hand.position.set(0, -0.38, 0.03);
    hand.scale.set(0.95, 1.15, 0.75);
    hand.castShadow = true;
    elbow.add(hand);

    torsoPivot.add(shoulder);
    return { shoulder, elbow, hand };
  }
  const leftArm = makeArm(-1);
  const rightArm = makeArm(1);

  // Legs (seated cleanly under desk y < 0.90)
  [-1, 1].forEach((side) => {
    const thigh = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.11, 0.56, 7), pantsMat);
    thigh.rotation.x = Math.PI * 0.48;
    thigh.position.set(side * 0.19, 0.76, 0.28);
    root.add(thigh);

    const shin = new THREE.Mesh(new THREE.CylinderGeometry(0.105, 0.088, 0.54, 7), pantsMat);
    shin.position.set(side * 0.19, 0.44, 0.54);
    root.add(shin);

    const shoe = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.11, 0.28), shoeMat);
    shoe.position.set(side * 0.19, 0.13, 0.6);
    root.add(shoe);
  });

  // Head Group
  const headPivot = new THREE.Group();
  headPivot.position.set(0, 1.04, 0.03);
  torsoPivot.add(headPivot);

  // Faceted Cranium + Jaw
  const cranium = new THREE.Mesh(new THREE.IcosahedronGeometry(0.39, 1), skinMat);
  cranium.position.set(0, 0.34, 0);
  cranium.scale.set(0.96, 1.08, 0.98);
  cranium.castShadow = true;
  headPivot.add(cranium);

  const jaw = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.17, 0.26, 7), skinMat);
  jaw.position.set(0, 0.14, 0.05);
  jaw.scale.set(1.0, 1.0, 0.96);
  headPivot.add(jaw);

  // Ears
  [-1, 1].forEach((side) => {
    const ear = new THREE.Mesh(new THREE.DodecahedronGeometry(0.08, 0), skinDarkMat);
    ear.position.set(side * 0.38, 0.31, -0.02);
    ear.scale.set(0.55, 1.1, 0.8);
    headPivot.add(ear);
  });

  // Nose
  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.055, 0.16, 4), skinDarkMat);
  nose.rotation.x = Math.PI * 0.18;
  nose.position.set(0, 0.29, 0.39);
  headPivot.add(nose);

  // Curly Espresso Hair Bangs
  const curlOffsets = [
    [-0.22, 0.53, 0.23, 0.11],
    [-0.09, 0.56, 0.27, 0.12],
    [0.06, 0.57, 0.27, 0.125],
    [0.2, 0.53, 0.23, 0.11],
    [-0.31, 0.45, 0.13, 0.095],
    [0.31, 0.45, 0.13, 0.095],
  ];
  curlOffsets.forEach(([x, y, z, r]) => {
    const curl = new THREE.Mesh(new THREE.DodecahedronGeometry(r, 0), hairMat);
    curl.position.set(x, y, z);
    headPivot.add(curl);
  });

  // Tilted Ribbed Ocean-Teal Beanie
  const beanieGroup = new THREE.Group();
  beanieGroup.position.set(0, 0.56, -0.06);
  beanieGroup.rotation.x = -0.24;
  headPivot.add(beanieGroup);

  const beanieCrown = new THREE.Mesh(
    new THREE.SphereGeometry(0.41, 10, 7, 0, Math.PI * 2, 0, Math.PI * 0.6),
    beanieMat,
  );
  beanieCrown.scale.set(1.0, 1.05, 1.06);
  beanieCrown.castShadow = true;
  beanieGroup.add(beanieCrown);

  const beanieBrim = new THREE.Mesh(new THREE.TorusGeometry(0.365, 0.075, 6, 12), beanieCuffMat);
  beanieBrim.rotation.x = Math.PI / 2;
  beanieBrim.position.set(0, -0.02, 0.02);
  beanieGroup.add(beanieBrim);

  // Eyes & Blinking Lids
  const eyes = [];
  [-1, 1].forEach((side) => {
    const eyeGrp = new THREE.Group();
    eyeGrp.position.set(side * 0.145, 0.345, 0.335);
    eyeGrp.rotation.y = side * 0.14;

    const sclera = new THREE.Mesh(new THREE.SphereGeometry(0.064, 10, 8), scleraMat);
    sclera.scale.set(1.05, 1.15, 0.42);
    eyeGrp.add(sclera);

    const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.036, 10, 8), pupilMat);
    pupil.position.set(0, 0, 0.025);
    pupil.scale.set(1, 1, 0.5);
    eyeGrp.add(pupil);

    const lid = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.07, 0.045), skinMat);
    lid.position.set(0, 0.06, 0.024);
    eyeGrp.add(lid);

    headPivot.add(eyeGrp);
    eyes.push({ eyeGrp, pupil, lid });
  });

  // Eyebrows
  const brows = [];
  [-1, 1].forEach((side) => {
    const brow = new THREE.Mesh(new THREE.BoxGeometry(0.145, 0.038, 0.045), hairMat);
    brow.position.set(side * 0.15, 0.445, 0.36);
    headPivot.add(brow);
    brows.push(brow);
  });

  // Circular Warm-Gold Wireframe Glasses
  const glassesGrp = new THREE.Group();
  glassesGrp.position.set(0, 0.345, 0.415);
  [-1, 1].forEach((side) => {
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.102, 0.011, 8, 24), goldMat);
    rim.position.set(side * 0.148, 0, 0);
    glassesGrp.add(rim);

    const lens = new THREE.Mesh(new THREE.CircleGeometry(0.095, 20), glassLensMat);
    lens.position.set(side * 0.148, 0, -0.002);
    glassesGrp.add(lens);

    const temple = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.014, 0.34), goldMat);
    temple.position.set(side * 0.255, 0.01, -0.17);
    glassesGrp.add(temple);
  });
  const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.095, 0.012, 0.012), goldMat);
  bridge.position.set(0, 0.022, 0);
  glassesGrp.add(bridge);
  headPivot.add(glassesGrp);

  // Dynamic Mouth (subtle rounded lip rim + dark cavity)
  const mouthGrp = new THREE.Group();
  mouthGrp.position.set(0, 0.155, 0.372);
  const mouthLip = new THREE.Mesh(new THREE.SphereGeometry(0.052, 10, 6), lipMat);
  mouthLip.scale.set(1.0, 0.28, 0.45);
  mouthGrp.add(mouthLip);
  const mouth = new THREE.Mesh(new THREE.SphereGeometry(0.044, 10, 6), mouthDarkMat);
  mouth.position.set(0, 0, 0.008);
  mouth.scale.set(0.9, 0.18, 0.35);
  mouthGrp.add(mouth);
  headPivot.add(mouthGrp);

  function setState({
    expr = 'annoyed',
    pose = 'typing',
    mouthAmp = 0,
    blink = 0,
    t = 0,
    headNod = 0,
    headTurn = 0,
    gazeX = 0,
  }) {
    // Head base orientation
    headPivot.rotation.set(
      headNod + Math.sin(t * 2.1) * 0.015,
      headTurn + Math.sin(t * 1.1) * 0.02,
      expr === 'skeptical' ? 0.06 : Math.sin(t * 0.8) * 0.012,
    );
    torsoPivot.position.y = 1.0 + Math.sin(t * 2.2) * 0.008;

    // Expression brows & eyes
    const wide = expr === 'panic' || expr === 'stunned' ? 1 : 0;
    brows.forEach((b, idx) => {
      const side = idx === 0 ? -1 : 1;
      if (expr === 'annoyed') {
        b.position.y = 0.43;
        b.rotation.z = side * -0.22;
      } else if (expr === 'panic' || expr === 'stunned') {
        b.position.y = 0.48;
        b.rotation.z = side * 0.2;
      } else if (expr === 'skeptical') {
        b.position.y = idx === 0 ? 0.425 : 0.47;
        b.rotation.z = idx === 0 ? -0.12 : 0.16;
      } else {
        b.position.y = 0.448;
        b.rotation.z = side * 0.06;
      }
    });

    eyes.forEach((e) => {
      e.pupil.position.x = gazeX * 0.018;
      e.pupil.scale.set(wide ? 0.85 : 1, wide ? 0.85 : 1, 0.5);
      // Eyelid close on blink or squint
      const squintOffset = expr === 'annoyed' ? 0.28 : 0.0;
      const closeAmt = Math.max(blink, squintOffset);
      e.lid.scale.y = 0.2 + closeAmt * 1.65;
      e.lid.position.y = 0.062 - closeAmt * 0.036;
    });

    // Mouth morph from audio + expression
    const open = clamp(mouthAmp, 0, 1);
    if (expr === 'stunned') {
      mouthGrp.scale.set(0.95, 1.45, 1);
      mouth.scale.set(0.88, 1.35, 0.5);
      mouthGrp.position.y = 0.148;
      mouthGrp.rotation.z = 0;
    } else if (open > 0.08) {
      mouthGrp.scale.set(1.15 + open * 0.25, 0.65 + open * 0.95, 1);
      mouth.scale.set(0.92, 0.35 + open * 0.85, 0.5);
      mouthGrp.position.y = 0.155 - open * 0.006;
      mouthGrp.rotation.z = 0;
    } else if (expr === 'relieved') {
      mouthGrp.scale.set(1.28, 0.55, 1);
      mouth.scale.set(0.9, 0.14, 0.35);
      mouthGrp.position.y = 0.16;
      mouthGrp.rotation.z = 0;
    } else {
      mouthGrp.scale.set(1.1, 0.52, 1);
      mouth.scale.set(0.88, 0.12, 0.35);
      mouthGrp.position.y = 0.155;
      mouthGrp.rotation.z = expr === 'annoyed' ? -0.06 : 0;
    }

    // Arm poses
    if (pose === 'disbelief') {
      leftArm.shoulder.rotation.set(-0.62, 0, -0.45);
      leftArm.elbow.rotation.set(-0.72, 0, 0.15);
      rightArm.shoulder.rotation.set(-0.68, 0, 0.45);
      rightArm.elbow.rotation.set(-0.72, 0, -0.15);
    } else if (pose === 'exhausted') {
      leftArm.shoulder.rotation.set(-0.36, 0, -0.16);
      leftArm.elbow.rotation.set(-0.88, 0, 0.12);
      rightArm.shoulder.rotation.set(-0.36, 0, 0.16);
      rightArm.elbow.rotation.set(-0.88, 0, -0.12);
    } else if (pose === 'point') {
      leftArm.shoulder.rotation.set(-0.5, 0, -0.18);
      leftArm.elbow.rotation.set(-0.7, 0, 0);
      rightArm.shoulder.rotation.set(-1.05, -0.25, 0.12);
      rightArm.elbow.rotation.set(-0.25, 0, 0);
    } else {
      // Typing / resting on desk
      leftArm.shoulder.rotation.set(-0.62, 0, -0.18);
      leftArm.elbow.rotation.set(-0.88, 0, 0.12);
      rightArm.shoulder.rotation.set(-0.62, 0, 0.18);
      rightArm.elbow.rotation.set(-0.88, 0, -0.12);
    }
  }

  return { root, headPivot, setState };
}

function buildClaude() {
  const root = new THREE.Group();
  const bodyGrp = new THREE.Group();
  root.add(bodyGrp);

  const terracottaMat = new THREE.MeshStandardMaterial({
    color: 0xdf9468,
    roughness: 0.74,
    metalness: 0.02,
    flatShading: true,
  });
  const terracottaDarkMat = new THREE.MeshStandardMaterial({
    color: 0xbe7349,
    roughness: 0.78,
    metalness: 0.02,
    flatShading: true,
  });
  const eyeMat = new THREE.MeshStandardMaterial({
    color: 0x181210,
    roughness: 0.22,
    metalness: 0.15,
    flatShading: true,
  });
  const bulbMat = new THREE.MeshStandardMaterial({
    color: 0xffcd63,
    emissive: 0xffa024,
    emissiveIntensity: 2.2,
    roughness: 0.25,
  });
  const ledMat = new THREE.MeshStandardMaterial({
    color: 0xffb74d,
    emissive: 0xff9800,
    emissiveIntensity: 2.4,
  });

  // Main Rounded Horizontal Cuboid Chassis
  const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.42, 0.38), terracottaMat);
  chassis.position.set(0, 0.29, 0);
  chassis.castShadow = true;
  chassis.receiveShadow = true;
  bodyGrp.add(chassis);

  // Soft Chamfer Edge Trim (gives warm molded toy look)
  [-1, 1].forEach((sx) => {
    [-1, 1].forEach((sy) => {
      const edge = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.36, 6), terracottaDarkMat);
      edge.rotation.x = Math.PI / 2;
      edge.position.set(sx * 0.27, 0.29 + sy * 0.19, 0);
      bodyGrp.add(edge);
    });
  });

  // Dual Expressive Angled Button Eyes (dark charcoal buttons tilted / \)
  const leftEyePivot = new THREE.Group();
  leftEyePivot.position.set(-0.115, 0.31, 0.194);
  const leftEye = new THREE.Mesh(new THREE.BoxGeometry(0.088, 0.145, 0.032), eyeMat);
  leftEye.rotation.z = -0.22;
  leftEye.castShadow = true;
  leftEyePivot.add(leftEye);
  bodyGrp.add(leftEyePivot);

  const rightEyePivot = new THREE.Group();
  rightEyePivot.position.set(0.115, 0.31, 0.194);
  const rightEye = new THREE.Mesh(new THREE.BoxGeometry(0.088, 0.145, 0.032), eyeMat);
  rightEye.rotation.z = 0.22;
  rightEye.castShadow = true;
  rightEyePivot.add(rightEye);
  bodyGrp.add(rightEyePivot);

  // Claude Starburst / Asterisk Decal (bottom right front)
  const starburstTex = createClaudeFrontMarkingsTexture();
  const starburst = new THREE.Mesh(
    new THREE.PlaneGeometry(0.16, 0.16),
    new THREE.MeshBasicMaterial({ map: starburstTex, transparent: true, opacity: 0.96 }),
  );
  starburst.position.set(0.175, 0.195, 0.193);
  bodyGrp.add(starburst);

  // Glowing Rounded "AI" Badge (top right front)
  const aiBadgeTex = createClaudeAIBadgeTexture();
  const aiBadge = new THREE.Mesh(
    new THREE.PlaneGeometry(0.11, 0.11),
    new THREE.MeshBasicMaterial({ map: aiBadgeTex, transparent: true, opacity: 0.96 }),
  );
  aiBadge.position.set(0.205, 0.38, 0.193);
  bodyGrp.add(aiBadge);

  // Glowing Horizontal Amber Status LED Slot (bottom right)
  const ledSlot = new THREE.Mesh(new THREE.BoxGeometry(0.072, 0.018, 0.015), ledMat);
  ledSlot.position.set(0.19, 0.125, 0.193);
  bodyGrp.add(ledSlot);

  // Dual Curved Antenna Horns with Glowing Amber Spheres
  function makeAntenna(side) {
    const grp = new THREE.Group();
    grp.position.set(side * 0.155, 0.50, 0.01);
    const stalk = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.022, 0.13, 8), terracottaDarkMat);
    stalk.position.set(side * 0.022, 0.055, 0);
    stalk.rotation.z = side * -0.28;
    stalk.rotation.x = -0.10;
    grp.add(stalk);

    const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.046, 12, 12), bulbMat);
    bulb.position.set(side * 0.048, 0.13, -0.012);
    grp.add(bulb);

    const pLight = new THREE.PointLight(0xffb74d, 0.9, 1.4);
    pLight.position.copy(bulb.position);
    grp.add(pLight);

    bodyGrp.add(grp);
    return grp;
  }
  const leftAntenna = makeAntenna(-1);
  const rightAntenna = makeAntenna(1);

  // Floating Holographic Terminal Visor Panel (hovering above head)
  const visorRenderer = createClaudeVisorRenderer();
  const visorMat = new THREE.MeshBasicMaterial({
    map: visorRenderer.tex,
    transparent: true,
    opacity: 0.94,
  });
  const visorMesh = new THREE.Mesh(new THREE.PlaneGeometry(0.48, 0.18), visorMat);
  visorMesh.position.set(0.02, 0.64, -0.02);
  bodyGrp.add(visorMesh);

  // Stubby Rectangular Side Arms
  function makeArm(side) {
    const pivot = new THREE.Group();
    pivot.position.set(side * 0.29, 0.27, 0.02);
    const arm = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.095, 0.20), terracottaDarkMat);
    arm.position.set(side * 0.06, -0.02, 0);
    arm.castShadow = true;
    pivot.add(arm);
    bodyGrp.add(pivot);
    return pivot;
  }
  const leftArm = makeArm(-1);
  const rightArm = makeArm(1);

  // 4 Sturdy Rectangular Pillar Legs (2 front, 2 back)
  const legGeo = new THREE.BoxGeometry(0.085, 0.15, 0.095);
  [-1, 1].forEach((sx) => {
    [-1, 1].forEach((sz) => {
      const leg = new THREE.Mesh(legGeo, terracottaDarkMat);
      leg.position.set(sx * 0.14, 0.075, sz * 0.08);
      leg.castShadow = true;
      root.add(leg);
    });
  });

  // Comic 3D Glossy Sky-Blue Sweatdrop
  const sweatGeo = new THREE.ConeGeometry(0.048, 0.14, 10);
  const sweatMat = new THREE.MeshPhysicalMaterial({
    color: 0x38bdf8,
    emissive: 0x0284c7,
    emissiveIntensity: 0.35,
    roughness: 0.08,
    metalness: 0.05,
    clearcoat: 1.0,
  });
  const sweatdrop = new THREE.Mesh(sweatGeo, sweatMat);
  sweatdrop.visible = false;
  bodyGrp.add(sweatdrop);

  function setState({
    mood = 'happy',
    mouthAmp = 0,
    blink = 0,
    sweat = false,
    sweatPhase = 0,
    t = 0,
    tilt = 0,
    hop = 0,
    wave = 0,
  }) {
    const bounce = Math.abs(Math.sin(t * 5.2)) * hop * 0.075;
    bodyGrp.position.y = bounce;
    bodyGrp.rotation.set(
      Math.sin(t * 2.5) * 0.025,
      Math.sin(t * 1.4) * 0.04,
      tilt + Math.sin(t * 3.1) * 0.02,
    );

    // Arm gesture animation
    leftArm.rotation.z = -0.15 - wave * (0.35 + Math.sin(t * 7) * 0.18);
    leftArm.rotation.x = Math.sin(t * 4.2) * 0.12;
    rightArm.rotation.z = 0.15 + wave * (0.35 + Math.cos(t * 7) * 0.18);
    rightArm.rotation.x = Math.cos(t * 4.2) * 0.12;

    // Antenna subtle spring bounce
    leftAntenna.rotation.z = Math.sin(t * 5.2) * 0.04;
    rightAntenna.rotation.z = -Math.sin(t * 5.2) * 0.04;

    // Eyeballs / Buttons reactive tilt & squint
    const squint = clamp(blink + (mood === 'innocent' ? 0.2 : 0), 0, 1);
    const wide = mood === 'guilt_sweat' ? 1.25 : 1.0;
    leftEye.scale.set(wide, 1 - squint * 0.82, 1);
    rightEye.scale.set(wide, 1 - squint * 0.82, 1);
    const tiltShift = mood === 'happy' ? 0.08 : mood === 'guilt_sweat' ? -0.14 : 0;
    leftEye.rotation.z = -0.22 - tiltShift;
    rightEye.rotation.z = 0.22 + tiltShift;

    // Comic sweatdrop
    sweatdrop.visible = sweat;
    if (sweat) {
      sweatdrop.position.set(0.28, 0.48 - sweatPhase * 0.14, 0.18);
      const sc = 0.85 + Math.sin(sweatPhase * Math.PI) * 0.25;
      sweatdrop.scale.set(sc, sc, sc);
    }

    // Visor reactive HUD updates
    visorMesh.position.y = 0.64 + Math.sin(t * 2.2) * 0.015;
    visorRenderer.draw(mouthAmp, t, mood);
  }

  return { root, setState };
}

export function initStudioStage(canvas, options = {}) {
  const width = options.width || 1080;
  const height = options.height || 1920;

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: false,
    powerPreference: 'high-performance',
    preserveDrawingBuffer: true,
  });
  renderer.setSize(width, height, false);
  renderer.setPixelRatio(1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.18;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x070c18);
  scene.fog = new THREE.FogExp2(0x070c18, 0.055);

  const camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 45);

  // Lighting
  const hemi = new THREE.HemisphereLight(0x5299d3, 0x1a1523, 0.85);
  scene.add(hemi);

  const rimLight = new THREE.DirectionalLight(0x38bdf8, 1.85);
  rimLight.position.set(2.8, 3.6, -2.5);
  scene.add(rimLight);

  const keyFill = new THREE.DirectionalLight(0xfff1d6, 0.9);
  keyFill.position.set(-2.5, 3.2, 3.4);
  keyFill.castShadow = true;
  keyFill.shadow.mapSize.set(1024, 1024);
  keyFill.shadow.bias = -0.001;
  scene.add(keyFill);

  // Warm tungsten desk lamp practical light
  const lampLight = new THREE.PointLight(0xffb74d, 5.2, 8.5, 1.45);
  lampLight.position.set(0.24, 1.70, 0.10);
  lampLight.castShadow = true;
  lampLight.shadow.mapSize.set(1024, 1024);
  lampLight.shadow.bias = -0.001;
  scene.add(lampLight);

  // Studio Room Architecture
  const brickTex = createBrickTexture();
  const backWall = new THREE.Mesh(
    new THREE.PlaneGeometry(14, 9),
    new THREE.MeshStandardMaterial({ map: brickTex, roughness: 0.92, metalness: 0.02 }),
  );
  backWall.position.set(-1.5, 2.5, -2.45);
  backWall.receiveShadow = true;
  scene.add(backWall);

  // Floor
  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(16, 12),
    new THREE.MeshStandardMaterial({ color: 0x0b1222, roughness: 0.88 }),
  );
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(floor);

  // Night city window panel right-rear
  const windowFrameMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.7 });
  const winGlass = new THREE.Mesh(
    new THREE.PlaneGeometry(4.2, 4.8),
    new THREE.MeshBasicMaterial({ color: 0x060d1f }),
  );
  winGlass.position.set(2.5, 2.8, -2.42);
  scene.add(winGlass);

  const mullionV = new THREE.Mesh(new THREE.BoxGeometry(0.12, 4.9, 0.14), windowFrameMat);
  mullionV.position.set(2.5, 2.8, -2.38);
  scene.add(mullionV);
  const mullionH = new THREE.Mesh(new THREE.BoxGeometry(4.3, 0.12, 0.14), windowFrameMat);
  mullionH.position.set(2.5, 2.7, -2.38);
  scene.add(mullionH);

  // City night bokeh discs outside window
  const bokehGroup = new THREE.Group();
  const bokehRng = mulberry32(99);
  const bokehPalette = [0xfbbf24, 0x38bdf8, 0x38d9a9, 0xfb7185, 0xfde68a];
  for (let i = 0; i < 36; i++) {
    const rad = 0.05 + bokehRng() * 0.14;
    const mat = new THREE.MeshBasicMaterial({
      color: bokehPalette[i % bokehPalette.length],
      transparent: true,
      opacity: 0.35 + bokehRng() * 0.45,
    });
    const disc = new THREE.Mesh(new THREE.CircleGeometry(rad, 16), mat);
    disc.position.set(-3.2 + bokehRng() * 7.8, 1.0 + bokehRng() * 3.8, -2.35 - bokehRng() * 0.04);
    bokehGroup.add(disc);
  }
  scene.add(bokehGroup);

  // Warm wall sconces on brick wall
  [-1.95, -0.55].forEach((sx) => {
    const sconce = new THREE.Mesh(
      new THREE.CylinderGeometry(0.07, 0.09, 0.16, 8),
      new THREE.MeshBasicMaterial({ color: 0xffe4a0 }),
    );
    sconce.position.set(sx, 2.65, -2.34);
    scene.add(sconce);
    const sLight = new THREE.PointLight(0xffb74d, 1.4, 3.2);
    sLight.position.set(sx, 2.62, -2.1);
    scene.add(sLight);
  });

  // Floating Shelves + Decor
  const shelfWoodMat = new THREE.MeshStandardMaterial({ color: 0x5c3e2b, roughness: 0.82, flatShading: true });
  const bookColors = [0x2f5d6b, 0x9f1239, 0x1e40af, 0xb45309, 0x334155];
  [1.95, 2.55, 3.15].forEach((sy, sIdx) => {
    const shelf = new THREE.Mesh(new THREE.BoxGeometry(1.55, 0.06, 0.32), shelfWoodMat);
    shelf.position.set(-0.35, sy, -2.26);
    scene.add(shelf);
    for (let b = 0; b < 4; b++) {
      const bh = 0.24 + ((sIdx + b) % 3) * 0.05;
      const bk = new THREE.Mesh(
        new THREE.BoxGeometry(0.075, bh, 0.2),
        new THREE.MeshStandardMaterial({ color: bookColors[(sIdx * 3 + b) % bookColors.length], roughness: 0.8 }),
      );
      bk.position.set(-0.88 + b * 0.1, sy + 0.03 + bh / 2, -2.25);
      scene.add(bk);
    }
    if (sIdx % 2 === 0) {
      const mug = new THREE.Mesh(
        new THREE.CylinderGeometry(0.06, 0.055, 0.13, 8),
        new THREE.MeshStandardMaterial({ color: 0x38d9a9, roughness: 0.5 }),
      );
      mug.position.set(0.18, sy + 0.09, -2.25);
      scene.add(mug);
    }
  });

  // Main Wooden Desk
  const deskGroup = new THREE.Group();
  scene.add(deskGroup);
  const deskTopMat = new THREE.MeshStandardMaterial({ color: 0x7c5338, roughness: 0.78, flatShading: true });
  const deskBodyMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.85, flatShading: true });
  const deskTop = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.08, 1.18), deskTopMat);
  deskTop.position.set(0.22, 0.96, 0.18);
  deskTop.receiveShadow = true;
  deskTop.castShadow = true;
  deskGroup.add(deskTop);

  const drawerBox = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.92, 1.05), deskBodyMat);
  drawerBox.position.set(1.12, 0.46, 0.18);
  deskGroup.add(drawerBox);
  [-0.5, 0.2].forEach((lx) => {
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.92, 0.96), deskBodyMat);
    leg.position.set(lx - 0.52, 0.46, 0.18);
    deskGroup.add(leg);
  });

  // Ergonomic Chair
  const chairMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.8, flatShading: true });
  const chairSeat = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.09, 0.56), chairMat);
  chairSeat.position.set(-0.78, 0.82, 0.14);
  scene.add(chairSeat);
  const chairBack = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.78, 0.52), chairMat);
  chairBack.position.set(-1.08, 1.24, 0.14);
  chairBack.rotation.z = 0.08;
  scene.add(chairBack);
  const chairPost = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.75, 8), chairMat);
  chairPost.position.set(-0.78, 0.42, 0.14);
  scene.add(chairPost);

  // Desk Laptop + Glowing Screen
  const laptopBase = new THREE.Mesh(
    new THREE.BoxGeometry(0.52, 0.025, 0.36),
    new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4, metalness: 0.5 }),
  );
  laptopBase.position.set(-0.1, 1.01, 0.08);
  laptopBase.rotation.y = 0.25;
  scene.add(laptopBase);

  const laptopScreenTex = createLaptopScreenTexture();
  const laptopLid = new THREE.Group();
  laptopLid.position.set(-0.06, 1.02, -0.08);
  laptopLid.rotation.y = 0.25;
  laptopLid.rotation.x = -0.2;
  const lidBack = new THREE.Mesh(
    new THREE.BoxGeometry(0.52, 0.34, 0.018),
    new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.35, metalness: 0.5 }),
  );
  lidBack.position.set(0, 0.17, 0);
  laptopLid.add(lidBack);

  // Claude starburst emblem on back of laptop lid (facing camera in two-shot!)
  const starburstTex = createClaudeFrontMarkingsTexture();
  const laptopDecal = new THREE.Mesh(
    new THREE.PlaneGeometry(0.12, 0.12),
    new THREE.MeshBasicMaterial({ map: starburstTex, transparent: true, opacity: 0.92 }),
  );
  laptopDecal.position.set(0, 0.17, -0.01);
  laptopDecal.rotation.y = Math.PI;
  laptopLid.add(laptopDecal);

  const lidGlow = new THREE.Mesh(
    new THREE.PlaneGeometry(0.48, 0.30),
    new THREE.MeshBasicMaterial({ map: laptopScreenTex }),
  );
  lidGlow.position.set(0, 0.17, 0.011);
  laptopLid.add(lidGlow);
  scene.add(laptopLid);

  // Cream Ceramic Coffee Mug with Claude emblem
  const mugMesh = new THREE.Mesh(
    new THREE.CylinderGeometry(0.068, 0.06, 0.14, 10),
    new THREE.MeshStandardMaterial({ color: 0xece5d5, roughness: 0.45 }),
  );
  mugMesh.position.set(0.32, 1.07, 0.44);
  mugMesh.castShadow = true;
  scene.add(mugMesh);

  const mugDecal = new THREE.Mesh(
    new THREE.PlaneGeometry(0.065, 0.065),
    new THREE.MeshBasicMaterial({ map: starburstTex, transparent: true, opacity: 0.95 }),
  );
  mugDecal.position.set(0.32, 1.07, 0.505);
  scene.add(mugDecal);

  // Articulated Brass Desk Lamp
  const brassMat = new THREE.MeshStandardMaterial({ color: 0xd4a34f, roughness: 0.35, metalness: 0.72, flatShading: true });
  const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.12, 0.03, 10), brassMat);
  lampBase.position.set(0.14, 1.015, -0.16);
  scene.add(lampBase);
  const lampArm = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.65, 6), brassMat);
  lampArm.position.set(0.14, 1.32, -0.10);
  lampArm.rotation.z = -0.22;
  lampArm.rotation.x = 0.22;
  scene.add(lampArm);
  const lampShade = new THREE.Mesh(new THREE.ConeGeometry(0.15, 0.19, 10, 1, true), brassMat);
  lampShade.position.set(0.24, 1.70, 0.06);
  lampShade.rotation.z = 0.45;
  scene.add(lampShade);
  const lampBulb = new THREE.Mesh(
    new THREE.SphereGeometry(0.055, 8, 8),
    new THREE.MeshBasicMaterial({ color: 0xffe49e }),
  );
  lampBulb.position.set(0.22, 1.65, 0.06);
  scene.add(lampBulb);

  // 3 Stacked Hardcover Books for Kip
  const bookStackGroup = new THREE.Group();
  bookStackGroup.position.set(0.84, 1.0, 0.18);
  scene.add(bookStackGroup);
  const stackColors = [0x264653, 0x9b2c3b, 0x2f5d6b];
  const pagesMat = new THREE.MeshStandardMaterial({ color: 0xece5d5, roughness: 0.85 });
  stackColors.forEach((col, i) => {
    const cover = new THREE.Mesh(
      new THREE.BoxGeometry(0.56, 0.085, 0.44),
      new THREE.MeshStandardMaterial({ color: col, roughness: 0.75, flatShading: true }),
    );
    cover.position.set((i === 1 ? -0.02 : 0.01), 0.043 + i * 0.086, 0);
    cover.rotation.y = (i - 1) * 0.08;
    cover.castShadow = true;
    cover.receiveShadow = true;
    bookStackGroup.add(cover);
    const pages = new THREE.Mesh(new THREE.BoxGeometry(0.53, 0.068, 0.41), pagesMat);
    pages.position.copy(cover.position).add(new THREE.Vector3(0.01, 0, 0.01));
    pages.rotation.copy(cover.rotation);
    bookStackGroup.add(pages);
  });

  // Floating 3D Holographic Code Terminal Panels behind Kip
  const texTree = createHoloPanelTexture('tree');
  const texRevert = createHoloPanelTexture('revert');
  const texAlert = createHoloPanelTexture('alert');
  const holoMat = new THREE.MeshBasicMaterial({ map: texTree, transparent: true, opacity: 0.35 });
  const holoMain = new THREE.Mesh(new THREE.PlaneGeometry(1.15, 0.78), holoMat);
  holoMain.position.set(0.75, 2.02, -0.95);
  holoMain.rotation.y = -0.25;
  scene.add(holoMain);

  const holoSideMat = new THREE.MeshBasicMaterial({ map: texAlert, transparent: true, opacity: 0.0 });
  const holoSide = new THREE.Mesh(new THREE.PlaneGeometry(0.82, 0.56), holoSideMat);
  holoSide.position.set(0.18, 1.92, -1.25);
  holoSide.rotation.y = 0.12;
  scene.add(holoSide);

  // Characters
  const tariq = buildTariq();
  tariq.root.position.set(-0.78, 0.0, 0.14);
  tariq.root.rotation.y = Math.PI * 0.42; // faces right toward desk/Kip
  scene.add(tariq.root);

  const claude = buildClaude();
  claude.root.position.set(0.84, 1.25, 0.18); // Perched cleanly atop 3 books
  claude.root.rotation.y = -Math.PI * 0.32; // faces slightly left toward Tariq & camera
  scene.add(claude.root);

  function renderAt(t, ctxState = {}) {
    const camMode = ctxState.cam || 'tariq_cu';
    const shotProgress = clamp(ctxState.shotProgress || 0, 0, 1);
    const pushZoom = ctxState.pushZoom || 0;

    // Blink cycles (deterministic sine pulses every ~3.4s)
    const blinkT = (t * 0.29) % 1;
    const tBlink = smoothstep(0.92, 0.96, blinkT) * (1 - smoothstep(0.96, 1.0, blinkT));
    const kipBlinkT = ((t + 1.4) * 0.25) % 1;
    const kBlink = smoothstep(0.93, 0.965, kipBlinkT) * (1 - smoothstep(0.965, 1.0, kipBlinkT));

    // Character states
    tariq.setState({
      expr: ctxState.tariqExpr || 'annoyed',
      pose: ctxState.tariqPose || 'typing',
      mouthAmp: ctxState.tariqAmp || 0,
      blink: ctxState.tariqExpr === 'stunned' ? 0 : tBlink,
      t: ctxState.freeze ? Math.floor(t * 2) * 0 : t, // true stillness on silent freeze!
      headNod: ctxState.tariqNod || 0,
      headTurn: ctxState.tariqTurn || 0,
      gazeX: ctxState.tariqGaze || 0.25,
    });

    claude.setState({
      mood: ctxState.kipMood || 'proud',
      mouthAmp: ctxState.kipAmp || 0,
      blink: kBlink,
      sweat: Boolean(ctxState.kipSweat),
      sweatPhase: (t * 0.9) % 1,
      t,
      tilt: ctxState.kipTilt || 0,
      hop: ctxState.kipHop || 0,
      wave: ctxState.kipWave || 0,
    });

    // Holographic rear terminal updates
    holoMat.map = ctxState.holoMode === 'revert' ? texRevert : texTree;
    holoMat.needsUpdate = true;
    holoSideMat.opacity = ctxState.foreshadowAlert ? 0.65 : 0.0;
    holoMain.position.y = 1.88 + Math.sin(t * 1.4) * 0.02;

    // Gentle bokeh drift
    bokehGroup.position.y = Math.sin(t * 0.5) * 0.04;

    // Camera Presets (9:16 mobile framing with clean top subtitle headroom)
    if (camMode === 'tariq_cu') {
      const zPull = pushZoom * shotProgress;
      camera.fov = 33 - zPull * 3.6;
      camera.position.set(1.24 - zPull * 0.16, 2.26 + Math.sin(t * 0.8) * 0.008, 2.52 - zPull * 0.22);
      camera.lookAt(-0.75, 2.34, 0.14);
    } else if (camMode === 'kip_cu') {
      const zPull = pushZoom * shotProgress;
      camera.fov = 35 - zPull * 3.0;
      camera.position.set(0.18, 1.40 + Math.sin(t * 0.9) * 0.008, 2.38 - zPull * 0.18);
      camera.lookAt(0.82, 1.66, 0.18);
    } else if (camMode === 'wide_desk') {
      camera.fov = 46;
      camera.position.set(0.0, 1.76, 5.15);
      camera.lookAt(0.0, 1.58, 0.12);
    }

    camera.updateProjectionMatrix();
    renderer.render(scene, camera);
  }

  return { renderAt };
}
