import * as THREE from '../lib/three.module.min.js';

let renderer, scene, camera;
let tariqObj, claudeObj;
let phoneObj, laptopObj;
let deskLampLight, ambientLight, keyLight, rimLight, phoneGlowLight;
let particlesMesh;

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(hi, v));
}

function smoothstep(a, b, x) {
  const t = clamp((x - a) / Math.max(1e-6, b - a), 0, 1);
  return t * t * (3 - 2 * t);
}

// -------------------------------------------------------------------------
// TEXTURE GENERATORS
// -------------------------------------------------------------------------
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

  // Top header tab bar
  ctx.fillStyle = '#141f35';
  ctx.fillRect(0, 0, 512, 26);
  ctx.fillStyle = '#38bdf8';
  ctx.font = 'bold 12px monospace';
  ctx.fillText('claude-code: auth_router.ts', 18, 17);

  // Colored syntax code lines
  const colors = ['#38bdf8', '#38d9a9', '#fbbf24', '#f87171', '#94a3b8', '#c084fc'];
  let seed = 42;
  function rnd() {
    seed = (seed * 9301 + 49297) % 233280;
    return seed / 233280;
  }

  for (let i = 0; i < 15; i++) {
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(12, 42 + i * 18, 24, 6);
    const x0 = 126 + (i % 4) * 16;
    ctx.fillStyle = colors[Math.floor(rnd() * colors.length)];
    ctx.fillRect(x0, 40 + i * 18, 70 + rnd() * 120, 8);
    if (rnd() > 0.3) {
      ctx.fillStyle = colors[Math.floor(rnd() * colors.length)];
      ctx.fillRect(x0 + 150, 40 + i * 18, 45 + rnd() * 80, 8);
    }
  }

  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function createPhoneScreenTexture(state = 'idle') {
  const c = document.createElement('canvas');
  c.width = 360;
  c.height = 720;
  const ctx = c.getContext('2d');

  // Phone background
  ctx.fillStyle = '#090d16';
  ctx.fillRect(0, 0, 360, 720);

  // Top status bar
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, 360, 48);
  ctx.fillStyle = '#f8fafc';
  ctx.font = 'bold 16px sans-serif';
  ctx.fillText('9:41', 24, 30);
  ctx.fillText('5G', 280, 30);

  // T3 Code Header
  ctx.fillStyle = '#1e293b';
  ctx.fillRect(16, 64, 328, 54);
  ctx.fillStyle = '#ff6b35';
  ctx.font = 'bold 20px monospace';
  ctx.fillText('T3 CODE // LIVE', 32, 98);

  // Live Terminal Stream Box
  ctx.fillStyle = '#050811';
  ctx.fillRect(16, 134, 328, 380);
  ctx.strokeStyle = state === 'buzz' ? '#ff6b35' : '#22c55e';
  ctx.lineWidth = 2;
  ctx.strokeRect(16, 134, 328, 380);

  ctx.fillStyle = '#22c55e';
  ctx.font = '14px monospace';
  ctx.fillText('$ claude refactor src/auth', 28, 164);
  ctx.fillStyle = '#94a3b8';
  ctx.fillText('Streaming live AST diffs...', 28, 192);
  ctx.fillText('-> auth/router.ts (+142, -98)', 28, 218);
  ctx.fillText('-> session/token.ts (+45, -12)', 28, 244);

  // Prompt alert inside phone
  ctx.fillStyle = '#1e1b4b';
  ctx.fillRect(26, 276, 308, 90);
  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 14px monospace';
  ctx.fillText('? PERMISSION REQUIRED', 38, 304);
  ctx.fillStyle = '#e2e8f0';
  ctx.font = '12px monospace';
  ctx.fillText('Allow Claude to write 20 files?', 38, 328);
  ctx.fillText('Touch screen to approve from mobile.', 38, 348);

  // Big green Action Button
  ctx.fillStyle = '#16a34a';
  ctx.fillRect(24, 540, 312, 64);
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 22px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('APPROVE DIFF', 180, 580);

  // Home bar
  ctx.fillStyle = '#64748b';
  ctx.fillRect(120, 700, 120, 6);

  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

// -------------------------------------------------------------------------
// CHARACTER 1: TARIQ VANCE (DEVELOPER)
// -------------------------------------------------------------------------
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
    color: 0x1e293b,
    roughness: 0.72,
    metalness: 0.06,
    flatShading: true,
  });
  const teeMat = new THREE.MeshStandardMaterial({
    color: 0xece5d5,
    roughness: 0.84,
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
    opacity: 0.22,
    roughness: 0.1,
    metalness: 0.2,
  });
  const scleraMat = new THREE.MeshBasicMaterial({ color: 0xf8fafc });
  const pupilMat = new THREE.MeshBasicMaterial({ color: 0x0f172a });
  const mouthDarkMat = new THREE.MeshBasicMaterial({ color: 0x3b1518 });
  const lipMat = new THREE.MeshStandardMaterial({ color: 0x8f4e42, roughness: 0.72, flatShading: true });

  // Torso
  const torsoPivot = new THREE.Group();
  torsoPivot.position.set(0, 1.0, 0);
  root.add(torsoPivot);

  const teeMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.36, 0.82, 8), teeMat);
  teeMesh.position.set(0, 0.42, 0.04);
  teeMesh.scale.set(1.0, 1.0, 0.72);
  teeMesh.castShadow = true;
  torsoPivot.add(teeMesh);

  // Jacket
  [-1, 1].forEach((side) => {
    const panel = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.84, 0.56), jacketMat);
    panel.position.set(side * 0.22, 0.43, -0.02);
    panel.castShadow = true;
    torsoPivot.add(panel);
  });
  const backPanel = new THREE.Mesh(new THREE.CylinderGeometry(0.39, 0.42, 0.82, 8), jacketMat);
  backPanel.position.set(0, 0.42, -0.06);
  backPanel.scale.set(1.02, 1, 0.75);
  backPanel.castShadow = true;
  torsoPivot.add(backPanel);

  // Seated posture adjustment: hands resting on desk
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
    elbow.add(hand);

    torsoPivot.add(shoulder);
    return { shoulder, elbow, hand };
  }
  const leftArm = makeArm(-1);
  const rightArm = makeArm(1);

  // Head Pivot
  const headPivot = new THREE.Group();
  headPivot.position.set(0, 1.04, 0.03);
  torsoPivot.add(headPivot);

  const cranium = new THREE.Mesh(new THREE.IcosahedronGeometry(0.39, 1), skinMat);
  cranium.position.set(0, 0.34, 0);
  cranium.scale.set(0.96, 1.08, 0.98);
  cranium.castShadow = true;
  headPivot.add(cranium);

  const jaw = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.17, 0.26, 7), skinMat);
  jaw.position.set(0, 0.14, 0.05);
  headPivot.add(jaw);

  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.055, 0.16, 4), skinDarkMat);
  nose.rotation.x = Math.PI * 0.18;
  nose.position.set(0, 0.29, 0.39);
  headPivot.add(nose);

  // Beanie
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

  // Eyes & Eyebrows
  const eyes = [];
  [-1, 1].forEach((side) => {
    const eyeGrp = new THREE.Group();
    eyeGrp.position.set(side * 0.145, 0.345, 0.335);

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

  const brows = [];
  [-1, 1].forEach((side) => {
    const brow = new THREE.Mesh(new THREE.BoxGeometry(0.145, 0.038, 0.045), hairMat);
    brow.position.set(side * 0.15, 0.445, 0.36);
    headPivot.add(brow);
    brows.push(brow);
  });

  // Gold Wireframe Glasses
  const glassesGrp = new THREE.Group();
  glassesGrp.position.set(0, 0.345, 0.415);
  [-1, 1].forEach((side) => {
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.102, 0.011, 8, 24), goldMat);
    rim.position.set(side * 0.148, 0, 0);
    glassesGrp.add(rim);

    const lens = new THREE.Mesh(new THREE.CircleGeometry(0.095, 20), glassLensMat);
    lens.position.set(side * 0.148, 0, -0.002);
    glassesGrp.add(lens);
  });
  const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.095, 0.012, 0.012), goldMat);
  bridge.position.set(0, 0.022, 0);
  glassesGrp.add(bridge);
  headPivot.add(glassesGrp);

  // Dynamic Mouth
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
    expr = 'normal',
    mouthAmp = 0,
    blink = 0,
    t = 0,
    headTurn = 0,
    headNod = 0,
  }) {
    headPivot.rotation.set(
      headNod + Math.sin(t * 2.0) * 0.012,
      headTurn + Math.sin(t * 1.2) * 0.018,
      expr === 'suspicious' ? 0.08 : 0,
    );
    torsoPivot.position.y = 1.0 + Math.sin(t * 2.2) * 0.006;

    // Eyebrow expressions
    brows.forEach((b, idx) => {
      const side = idx === 0 ? -1 : 1;
      if (expr === 'annoyed') {
        b.position.y = 0.43;
        b.rotation.z = side * -0.22;
      } else if (expr === 'panic' || expr === 'alarm') {
        b.position.y = 0.49;
        b.rotation.z = side * 0.22;
      } else if (expr === 'suspicious') {
        b.position.y = idx === 0 ? 0.42 : 0.47;
        b.rotation.z = idx === 0 ? -0.15 : 0.18;
      } else {
        b.position.y = 0.45;
        b.rotation.z = side * 0.05;
      }
    });

    eyes.forEach((e) => {
      const closeAmt = Math.max(blink, expr === 'annoyed' ? 0.25 : 0);
      e.lid.scale.y = 0.2 + closeAmt * 1.6;
      e.lid.position.y = 0.06 - closeAmt * 0.035;
    });

    const open = clamp(mouthAmp, 0, 1);
    if (open > 0.08) {
      mouthGrp.scale.set(1.15 + open * 0.25, 0.65 + open * 0.95, 1);
      mouth.scale.set(0.92, 0.35 + open * 0.85, 0.5);
    } else {
      mouthGrp.scale.set(1.05, 0.45, 1);
      mouth.scale.set(0.85, 0.12, 0.35);
    }

    // Default arm resting pose on desk
    leftArm.shoulder.rotation.set(-0.62, 0, -0.18);
    leftArm.elbow.rotation.set(-0.88, 0, 0.12);
    rightArm.shoulder.rotation.set(-0.62, 0, 0.18);
    rightArm.elbow.rotation.set(-0.88, 0, -0.12);
  }

  return { root, headPivot, setState };
}

// -------------------------------------------------------------------------
// CHARACTER 2: CLAUDE MASCOT
// STRICT MATCH TO REFERENCE: media_1794583368294_98c1c419.png
// Terracotta cuboid body, 2 square black eyes, 2 block arms, 4 block legs
// NO antennas, NO bulbs, NO visor, NO starburst, NO AI badge
// -------------------------------------------------------------------------
function buildClaude() {
  const root = new THREE.Group();
  const bodyGrp = new THREE.Group();
  root.add(bodyGrp);

  const terracottaMat = new THREE.MeshStandardMaterial({
    color: 0xd47f53, // Warm terracotta clay matching user pixel image
    roughness: 0.65,
    metalness: 0.02,
    flatShading: true,
  });

  const eyeMat = new THREE.MeshStandardMaterial({
    color: 0x111111, // Pure square black eye pixels
    roughness: 0.22,
    metalness: 0.1,
    flatShading: true,
  });

  // 1. MAIN TERRACOTTA CUBOID BODY
  // Aspect ratio matching the wide block in the reference image (7:4 proportion)
  const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.32, 0.28), terracottaMat);
  chassis.position.set(0, 0.27, 0);
  chassis.castShadow = true;
  chassis.receiveShadow = true;
  bodyGrp.add(chassis);

  // 2. TWO SQUARE BLACK EYES (Pure upright squares on front face)
  const eyes = [];
  [-1, 1].forEach((side) => {
    const eyeMesh = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.055, 0.015), eyeMat);
    eyeMesh.position.set(side * 0.13, 0.31, 0.142);
    eyeMesh.castShadow = true;
    bodyGrp.add(eyeMesh);
    eyes.push(eyeMesh);
  });

  // 3. TWO HORIZONTAL SIDE BLOCK ARMS (Projecting outward from left and right)
  const arms = [];
  [-1, 1].forEach((side) => {
    const armPivot = new THREE.Group();
    armPivot.position.set(side * 0.26, 0.25, 0);
    const armMesh = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.09, 0.14), terracottaMat);
    armMesh.position.set(side * 0.06, 0, 0);
    armMesh.castShadow = true;
    armPivot.add(armMesh);
    bodyGrp.add(armPivot);
    arms.push(armPivot);
  });

  // 4. FOUR VERTICAL SQUARE BLOCK PILLAR LEGS
  // Positioned in 4 vertical columns along the base exactly as in the pixel reference
  const legPositions = [-0.18, -0.06, 0.06, 0.18];
  legPositions.forEach((posX) => {
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.12, 0.065), terracottaMat);
    leg.position.set(posX, 0.06, 0);
    leg.castShadow = true;
    bodyGrp.add(leg);
  });

  function setState({
    mouthAmp = 0,
    blink = 0,
    t = 0,
    speaking = false,
  }) {
    // Gentle floating breathing bob
    const bob = Math.sin(t * 3.2) * 0.015;
    bodyGrp.position.y = bob;

    // Subtle playful speaking tilt
    if (speaking) {
      bodyGrp.rotation.z = Math.sin(t * 7.5) * 0.04;
      bodyGrp.rotation.y = Math.sin(t * 4.0) * 0.06;
      arms[0].rotation.z = 0.15 + Math.sin(t * 8.0) * 0.12;
      arms[1].rotation.z = -0.15 - Math.sin(t * 8.0) * 0.12;
    } else {
      bodyGrp.rotation.z = 0;
      bodyGrp.rotation.y = -0.18; // Angled slightly towards Tariq
      arms[0].rotation.z = 0;
      arms[1].rotation.z = 0;
    }

    // Eye blink: scales eyes vertically
    const eyeScaleY = blink > 0.5 ? 0.1 : 1.0;
    eyes.forEach((e) => {
      e.scale.y = eyeScaleY;
    });
  }

  return { root, bodyGrp, setState };
}

// -------------------------------------------------------------------------
// ENVIRONMENT: DESK, LAPTOP, SMARTPHONE, LIGHTING
// -------------------------------------------------------------------------
export function initScene(canvas) {
  renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: false,
    powerPreference: 'high-performance',
  });
  renderer.setSize(1080, 1920);
  renderer.setPixelRatio(1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  scene = new THREE.Scene();
  scene.background = new THREE.Color('#080d1a');
  scene.fog = new THREE.FogExp2('#080d1a', 0.14);

  camera = new THREE.PerspectiveCamera(34, 1080 / 1920, 0.1, 100);
  camera.position.set(0, 1.45, 2.7);
  camera.lookAt(0, 1.25, 0);

  // Lighting
  ambientLight = new THREE.AmbientLight('#1e293b', 0.9);
  scene.add(ambientLight);

  keyLight = new THREE.DirectionalLight('#fff1e6', 2.2);
  keyLight.position.set(1.5, 3.2, 2.4);
  keyLight.castShadow = true;
  keyLight.shadow.mapSize.width = 1024;
  keyLight.shadow.mapSize.height = 1024;
  scene.add(keyLight);

  rimLight = new THREE.DirectionalLight('#38bdf8', 1.1);
  rimLight.position.set(-2.2, 2.0, -1.0);
  scene.add(rimLight);

  deskLampLight = new THREE.PointLight('#ffa834', 2.2, 4.5);
  deskLampLight.position.set(0.65, 1.7, 0.4);
  scene.add(deskLampLight);

  phoneGlowLight = new THREE.PointLight('#ff6b35', 0, 1.5);
  phoneGlowLight.position.set(0.05, 1.05, 0.55);
  scene.add(phoneGlowLight);

  // Studio Desk
  const deskGeo = new THREE.BoxGeometry(3.6, 0.12, 1.8);
  const deskMat = new THREE.MeshStandardMaterial({
    color: '#1a1d24',
    roughness: 0.72,
    metalness: 0.08,
  });
  const desk = new THREE.Mesh(deskGeo, deskMat);
  desk.position.set(0, 0.94, 0);
  desk.receiveShadow = true;
  scene.add(desk);

  // Background Wall with subtle warmth
  const wallGeo = new THREE.PlaneGeometry(8, 6);
  const wallMat = new THREE.MeshStandardMaterial({ color: '#090e1c', roughness: 0.95 });
  const wall = new THREE.Mesh(wallGeo, wallMat);
  wall.position.set(0, 2.5, -1.8);
  scene.add(wall);

  // Open MacBook / Laptop
  laptopObj = new THREE.Group();
  laptopObj.position.set(-0.08, 1.0, 0.18);
  laptopObj.rotation.y = -0.15;

  const baseMesh = new THREE.Mesh(
    new THREE.BoxGeometry(0.52, 0.016, 0.36),
    new THREE.MeshStandardMaterial({ color: '#334155', metalness: 0.85, roughness: 0.25 }),
  );
  laptopObj.add(baseMesh);

  const lidMesh = new THREE.Mesh(
    new THREE.BoxGeometry(0.52, 0.34, 0.014),
    new THREE.MeshStandardMaterial({ color: '#1e293b', metalness: 0.85, roughness: 0.25 }),
  );
  lidMesh.position.set(0, 0.17, -0.17);
  lidMesh.rotation.x = 0.18;
  laptopObj.add(lidMesh);

  const screenTex = createLaptopScreenTexture();
  const screenMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(0.48, 0.30),
    new THREE.MeshBasicMaterial({ map: screenTex }),
  );
  screenMesh.position.set(0, 0.17, -0.162);
  screenMesh.rotation.x = 0.18;
  laptopObj.add(screenMesh);
  scene.add(laptopObj);

  // Smartphone on the Desk
  phoneObj = new THREE.Group();
  phoneObj.position.set(0.12, 1.01, 0.52);
  phoneObj.rotation.x = -Math.PI / 2;
  phoneObj.rotation.z = -0.25;

  const phoneBody = new THREE.Mesh(
    new THREE.BoxGeometry(0.16, 0.32, 0.014),
    new THREE.MeshStandardMaterial({ color: '#0f172a', metalness: 0.9, roughness: 0.2 }),
  );
  phoneObj.add(phoneBody);

  const phoneScreenTex = createPhoneScreenTexture('idle');
  const phoneScreenMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(0.148, 0.30),
    new THREE.MeshBasicMaterial({ map: phoneScreenTex }),
  );
  phoneScreenMesh.position.set(0, 0, 0.008);
  phoneObj.add(phoneScreenMesh);
  phoneObj.userData.screenMesh = phoneScreenMesh;
  scene.add(phoneObj);

  // Ceramic Coffee Mug
  const mugGeo = new THREE.CylinderGeometry(0.065, 0.055, 0.14, 16);
  const mugMat = new THREE.MeshStandardMaterial({ color: '#f1f5f9', roughness: 0.3 });
  const mug = new THREE.Mesh(mugGeo, mugMat);
  mug.position.set(-0.46, 1.07, 0.38);
  mug.castShadow = true;
  scene.add(mug);

  // Books stack for Claude Mascot to stand on
  const book1 = new THREE.Mesh(
    new THREE.BoxGeometry(0.65, 0.055, 0.42),
    new THREE.MeshStandardMaterial({ color: '#1e3a8a', roughness: 0.6 }),
  );
  book1.position.set(0.82, 1.025, 0.18);
  book1.rotation.y = 0.12;
  book1.castShadow = true;
  book1.receiveShadow = true;
  scene.add(book1);

  const book2 = new THREE.Mesh(
    new THREE.BoxGeometry(0.60, 0.055, 0.38),
    new THREE.MeshStandardMaterial({ color: '#0f766e', roughness: 0.6 }),
  );
  book2.position.set(0.82, 1.08, 0.18);
  book2.rotation.y = 0.04;
  book2.castShadow = true;
  book2.receiveShadow = true;
  scene.add(book2);

  const book3 = new THREE.Mesh(
    new THREE.BoxGeometry(0.55, 0.055, 0.34),
    new THREE.MeshStandardMaterial({ color: '#b45309', roughness: 0.6 }),
  );
  book3.position.set(0.82, 1.135, 0.18);
  book3.rotation.y = -0.06;
  book3.castShadow = true;
  book3.receiveShadow = true;
  scene.add(book3);

  // BUILD CHARACTERS
  // 1. TARIQ VANCE (DEVELOPER) — Matches previous video position and rotation
  tariqObj = buildTariq();
  tariqObj.root.position.set(-0.78, 0.0, 0.14);
  tariqObj.root.rotation.y = Math.PI * 0.42; // Faces right toward desk & Claude
  scene.add(tariqObj.root);

  // Dedicated keylight for Tariq's face & glasses
  const tariqFaceLight = new THREE.SpotLight(0xffecd6, 3.2, 8, Math.PI / 4, 0.4);
  tariqFaceLight.position.set(0.4, 2.6, 2.0);
  tariqFaceLight.target.position.set(-0.75, 2.34, 0.14);
  scene.add(tariqFaceLight);
  scene.add(tariqFaceLight.target);

  // 2. CLAUDE MASCOT — Perched atop 3 books on the right
  claudeObj = buildClaude();
  claudeObj.root.position.set(0.82, 1.19, 0.18);
  claudeObj.root.rotation.y = -Math.PI * 0.32; // Faces slightly left toward Tariq & camera
  scene.add(claudeObj.root);

  // Dust Motes / Bokeh Particles
  const pCount = 80;
  const pGeo = new THREE.BufferGeometry();
  const pPos = new Float32Array(pCount * 3);
  for (let i = 0; i < pCount * 3; i += 3) {
    pPos[i] = (Math.random() - 0.5) * 3.5;
    pPos[i + 1] = 0.8 + Math.random() * 1.8;
    pPos[i + 2] = (Math.random() - 0.5) * 2.5;
  }
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
  const pMat = new THREE.PointsMaterial({
    color: '#ffbe98',
    size: 0.025,
    transparent: true,
    opacity: 0.4,
  });
  particlesMesh = new THREE.Points(pGeo, pMat);
  scene.add(particlesMesh);

  return { scene, camera, renderer, tariqObj, claudeObj, phoneObj };
}

// -------------------------------------------------------------------------
// FRAME UPDATE: EXACT CAMERA PRESETS, ANIMATIONS, SPEAKER TRACKING
// -------------------------------------------------------------------------
export function updateScene(time, currentCue) {
  if (!scene || !camera) return;

  const speaker = currentCue ? currentCue.speaker : 'none';
  const cueId = currentCue ? currentCue.id : '';

  // Calculate shot progress for optical drift/dolly
  let shotProgress = 0;
  if (currentCue) {
    const cueDuration = Math.max(0.1, currentCue.end - currentCue.start);
    shotProgress = clamp((time - currentCue.start) / cueDuration, 0, 1);
  }

  // Determine Camera Shot Mode from active cue
  let camMode = 'wide_desk';
  if (currentCue && currentCue.shot) {
    camMode = currentCue.shot === 'two_shot' ? 'wide_desk' : currentCue.shot;
  } else if (speaker === 'Tariq' || speaker === 'tariq') {
    camMode = 'tariq_cu';
  } else if (speaker === 'Claude' || speaker === 'claude') {
    camMode = 'claude_cu';
  }

  // Apply Camera Presets directly (no lerp lag between hard cuts)
  if (camMode === 'tariq_cu') {
    const zPull = shotProgress * 0.12;
    camera.fov = 33 - shotProgress * 1.5;
    camera.position.set(1.24 - zPull * 0.15, 2.26 + Math.sin(time * 0.8) * 0.008, 2.52 - zPull * 0.2);
    camera.lookAt(-0.75, 2.34, 0.14);
  } else if (camMode === 'tariq_tight_cu') {
    const zPull = shotProgress * 0.18;
    camera.fov = 28 - shotProgress * 2.0;
    camera.position.set(1.05 - zPull * 0.15, 2.28 + Math.sin(time * 1.2) * 0.008, 2.15 - zPull * 0.25);
    camera.lookAt(-0.75, 2.36, 0.14);
  } else if (camMode === 'claude_cu') {
    const zPull = shotProgress * 0.12;
    camera.fov = 32 - shotProgress * 1.5;
    camera.position.set(0.12 - zPull * 0.10, 1.25 + Math.sin(time * 0.9) * 0.008, 1.95 - zPull * 0.18);
    camera.lookAt(0.82, 1.14, 0.18);
  } else if (camMode === 'phone_cu') {
    const zPull = shotProgress * 0.15;
    camera.fov = 34 - shotProgress * 2.5;
    camera.position.set(0.08, 1.62 - zPull * 0.12, 1.48 - zPull * 0.2);
    camera.lookAt(0.08, 1.01, 0.52);
  } else {
    // wide_desk / two_shot
    camera.fov = 44;
    camera.position.set(0.0, 1.62, 4.5);
    camera.lookAt(0.0, 1.42, 0.12);
  }
  camera.updateProjectionMatrix();

  // Animate Characters
  const isTariqSpeaking = speaker === 'Tariq' || speaker === 'tariq';
  const isClaudeSpeaking = speaker === 'Claude' || speaker === 'claude';

  const tariqMouthAmp = isTariqSpeaking ? 0.35 + Math.sin(time * 14) * 0.35 : 0;
  const tariqBlink = Math.sin(time * 1.8) > 0.96 ? 1.0 : 0.0;
  const claudeBlink = Math.sin(time * 2.1) > 0.95 ? 1.0 : 0.0;

  let tariqExpr = 'normal';
  if (cueId === 'L01' || cueId === 'L03') tariqExpr = 'annoyed';
  if (cueId === 'L17') tariqExpr = 'suspicious';
  if (cueId === 'L19') tariqExpr = 'alarm';

  tariqObj.setState({
    expr: tariqExpr,
    mouthAmp: tariqMouthAmp,
    blink: tariqBlink,
    t: time,
    headTurn: isTariqSpeaking ? 0.08 : 0.22,
    headNod: isTariqSpeaking ? Math.sin(time * 4) * 0.03 : 0,
  });

  claudeObj.setState({
    mouthAmp: isClaudeSpeaking ? 0.5 : 0,
    blink: claudeBlink,
    t: time,
    speaking: isClaudeSpeaking,
  });

  // Phone vibration on buzz beats
  const isBuzzing = cueId === 'L08' || cueId === 'L16' || cueId === 'L18';
  if (isBuzzing) {
    phoneObj.position.x = 0.08 + (Math.random() - 0.5) * 0.008;
    phoneObj.position.z = 0.52 + (Math.random() - 0.5) * 0.008;
    phoneGlowLight.intensity = 2.2 + Math.sin(time * 20) * 0.8;
  } else {
    phoneObj.position.x = 0.08;
    phoneObj.position.z = 0.52;
    phoneGlowLight.intensity = 0.3;
  }

  // Float dust motes
  if (particlesMesh) {
    particlesMesh.rotation.y = time * 0.02;
  }

  renderer.render(scene, camera);
}
