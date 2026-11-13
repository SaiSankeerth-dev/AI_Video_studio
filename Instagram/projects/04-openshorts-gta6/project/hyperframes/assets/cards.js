// UI Cards and Subtitle Controller for Agent Talk — OpenShorts GTA 6 Video

export const CUES = [
  { id: 'L01', speaker: 'tariq', start: 0, end: 9.943, text: 'Claude, GTA 6 comes out soon, and every influencer on my feed claims you can make twenty grand clipping live streams with AI. Is that actually real?' },
  { id: 'L02', speaker: 'claude', start: 10.123, end: 15.216, text: 'Let us break it into three honest parts: what people claim, how to do it free, and the copyright reality.' },
  { id: 'L03', speaker: 'tariq', start: 15.396, end: 18.202, text: 'Start with the hype. What are they telling people to do?' },
  { id: 'L04', speaker: 'claude', start: 18.382, end: 25.584, text: 'Take an eight-hour streamer broadcast, have an AI detect the funny moments, convert it to nine-by-sixteen, and spam it across TikTok and Reels.' },
  { id: 'L05', speaker: 'tariq', start: 25.764, end: 29.799, text: "So literally just re-uploading other people's gameplay without editing?" },
  { id: 'L06', speaker: 'claude', start: 29.979, end: 31.907, text: 'That is the entire business model.' },
  { id: 'L07', speaker: 'tariq', start: 32.087, end: 34.773, text: 'Okay, but how much does the AI software cost?' },
  { id: 'L08', speaker: 'claude', start: 34.953, end: 40.41, text: 'Zero dollars. An open-source tool called OpenShorts just dropped on GitHub with eight thousand stars.' },
  { id: 'L09', speaker: 'tariq', start: 40.59, end: 42.089, text: 'Wait, it is completely free?' },
  { id: 'L10', speaker: 'claude', start: 42.269, end: 50.287, text: 'MIT licensed. You paste any stream link, and local AI extracts viral clips, crops the facecam, and generates animated captions automatically.' },
  { id: 'L11', speaker: 'tariq', start: 50.467, end: 54.481, text: 'Wait, it handles face tracking and captions too? What am I supposed to do?' },
  { id: 'L12', speaker: 'claude', start: 54.661, end: 57.785, text: "Press publish and pray YouTube's algorithm does not notice." },
  { id: 'L13', speaker: 'tariq', start: 57.965, end: 60.762, text: 'And that brings us to part three: is the money real?' },
  { id: 'L14', speaker: 'claude', start: 60.942, end: 67.982, text: 'The views are real. But the footage belongs to Rockstar, and YouTube actively demonetizes reused content with zero commentary.' },
  { id: 'L15', speaker: 'tariq', start: 68.162, end: 72.435, text: 'Plus fifty thousand kids will be clipping the exact same stream on launch day.' },
  { id: 'L16', speaker: 'claude', start: 72.615, end: 78.33, text: 'Exactly. In a gold rush, the people getting rich are not the clippers, it is the developers building the clipping tools.' },
  { id: 'L17', speaker: 'tariq', start: 78.51, end: 82.35, text: 'So I should not quit my engineering job to farm GTA clips?' },
  { id: 'L18', speaker: 'claude', start: 82.53, end: 85.77, text: 'You are a senior developer, Tariq. Go review your pull requests.' },
  { id: 'L19', speaker: 'tariq', start: 85.95, end: 86.642, text: 'Fair enough.' }
];

export function initCards(container) {
  container.innerHTML = `
    <!-- Top Brand Watermark -->
    <div class="brand-pill" data-layout-ignore>
      <div class="brand-dot"></div>
      <span class="brand-title">Agent Talk</span>
    </div>

    <!-- MAIN OVERHEAD CARD WITH TABS (Reference Style) -->
    <div id="master-plan-card" class="ui-card plan-card" data-layout-allow-overlap>
      <div class="plan-header">
        <span class="plan-tag">THE CLIP PLAN</span>
        <span class="plan-meta">LAUNCH 2026</span>
      </div>

      <!-- 3 Navigation Tabs -->
      <div class="plan-tabs">
        <div id="tab-1" class="tab-pill active">
          <span class="tab-num">1</span> What People Say
        </div>
        <div id="tab-2" class="tab-pill">
          <span class="tab-num">2</span> How To Do It Free
        </div>
        <div id="tab-3" class="tab-pill">
          <span class="tab-num">3</span> Is It Real?
        </div>
      </div>

      <!-- TAB 1 CONTENT: THE HYPE (L01 - L07) -->
      <div id="content-tab-1" class="tab-content">
        <div class="blueprint-box">
          <div class="blueprint-step">
            <span class="step-icon">🎥</span>
            <span class="step-title">8-Hr Stream</span>
          </div>
          <div class="blueprint-arrow">➔</div>
          <div class="blueprint-step highlight">
            <span class="step-icon">🤖</span>
            <span class="step-title">AI Clip Detection</span>
          </div>
          <div class="blueprint-arrow">➔</div>
          <div class="blueprint-step">
            <span class="step-icon">📱</span>
            <span class="step-title">9:16 Shorts</span>
          </div>
        </div>
        <div class="blueprint-sub">
          <span class="pill-badge green">Est. Views: Millions</span>
          <span class="pill-badge orange">Human Effort: 0%</span>
        </div>
      </div>

      <!-- TAB 2 CONTENT: OPENSHORTS TOOL (L08 - L12) -->
      <div id="content-tab-2" class="tab-content" style="display: none;">
        <div class="repo-header">
          <div class="repo-name">&lt;&gt; mutonby / openshorts</div>
          <div class="repo-badge">Free · 8.0k ★ · MIT</div>
        </div>
        <div class="mock-input-row">
          <span class="mock-url">https://stream.link/long-gta-6-night</span>
          <span class="mock-go-btn">Go</span>
        </div>
        <div class="mock-waveform-row">
          <div class="wave-label">FINDING VIRAL MOMENTS</div>
          <div class="waveform-anim">
            <div class="wave-bar w1"></div><div class="wave-bar w2"></div><div class="wave-bar w3 active"></div>
            <div class="wave-bar w4 active"></div><div class="wave-bar w5 active"></div><div class="wave-bar w6"></div>
            <div class="wave-bar w7"></div><div class="wave-bar w8"></div>
          </div>
        </div>
        <div class="features-pill-row">
          <span class="f-pill">✓ Auto Face-Tracking</span>
          <span class="f-pill">✓ Burned Subtitles</span>
          <span class="f-pill">✓ 100% Free BYOS</span>
        </div>
        <div id="btn-post" class="mock-post-btn">▶ PRESS POST</div>
      </div>

      <!-- TAB 3 CONTENT: THE REALITY CHECK (L13 - L16) -->
      <div id="content-tab-3" class="tab-content" style="display: none;">
        <div class="reality-badge">THE FACT CHECK</div>
        <div class="warn-list">
          <div class="warn-item">
            <span class="warn-icon">⚠️</span>
            <span class="warn-text">Gameplay footage belongs to Rockstar Games</span>
          </div>
          <div class="warn-item">
            <span class="warn-icon">⚠️</span>
            <span class="warn-text">YouTube strictly demonetizes raw "Reused Content"</span>
          </div>
          <div class="warn-item">
            <span class="warn-icon">⚠️</span>
            <span class="warn-text">50,000+ accounts spamming the exact same clips</span>
          </div>
        </div>
        <div class="meter-box">
          <div class="meter-labels">
            <span>SATURATED</span>
            <span class="needle-label">CRITICAL COMPETITION</span>
            <span>EARLY</span>
          </div>
          <div class="meter-bar">
            <div class="meter-fill"></div>
            <div class="meter-needle"></div>
          </div>
        </div>
        <div class="shovels-quote">“In a gold rush, sell shovels.”</div>
      </div>

      <!-- TAB 4 ROAST: GO TO WORK (L17 - L19) -->
      <div id="content-tab-4" class="tab-content" style="display: none;">
        <div class="roast-header">TERMINAL NOTICE</div>
        <div class="roast-code">$ git status --pending-review</div>
        <div class="roast-text">3 Pull Requests awaiting Senior Engineering review.</div>
        <div class="roast-sub">Put down the GTA stream and drink your coffee, Tariq.</div>
      </div>
    </div>
  `;
}

export function updateCards(time) {
  const tab1 = document.getElementById('tab-1');
  const tab2 = document.getElementById('tab-2');
  const tab3 = document.getElementById('tab-3');
  const c1 = document.getElementById('content-tab-1');
  const c2 = document.getElementById('content-tab-2');
  const c3 = document.getElementById('content-tab-3');
  const c4 = document.getElementById('content-tab-4');
  const subBox = document.getElementById('sub-box');
  const subSpeaker = document.getElementById('sub-speaker');
  const subText = document.getElementById('sub-text');

  if (!tab1 || !c1) return;

  // Active Tab Logic
  if (time < 34.8) {
    // Tab 1: The Hype
    tab1.className = 'tab-pill active';
    tab2.className = 'tab-pill';
    tab3.className = 'tab-pill';
    c1.style.display = 'block';
    c2.style.display = 'none';
    c3.style.display = 'none';
    c4.style.display = 'none';
  } else if (time < 57.8) {
    // Tab 2: How To Do It Free (OpenShorts)
    tab1.className = 'tab-pill completed';
    tab2.className = 'tab-pill active';
    tab3.className = 'tab-pill';
    c1.style.display = 'none';
    c2.style.display = 'block';
    c3.style.display = 'none';
    c4.style.display = 'none';
  } else if (time < 78.4) {
    // Tab 3: The Reality Check
    tab1.className = 'tab-pill completed';
    tab2.className = 'tab-pill completed';
    tab3.className = 'tab-pill active';
    c1.style.display = 'none';
    c2.style.display = 'none';
    c3.style.display = 'block';
    c4.style.display = 'none';
  } else {
    // End roast: Go to work
    tab1.className = 'tab-pill completed';
    tab2.className = 'tab-pill completed';
    tab3.className = 'tab-pill completed';
    c1.style.display = 'none';
    c2.style.display = 'none';
    c3.style.display = 'none';
    c4.style.display = 'block';
  }

  // Subtitle HUD Logic
  let activeCue = null;
  for (const c of CUES) {
    if (time >= c.start && time < c.end) {
      activeCue = c;
      break;
    }
  }

  if (activeCue && subBox && subSpeaker && subText) {
    subBox.style.display = 'flex';
    subSpeaker.textContent = activeCue.speaker.toUpperCase();
    subSpeaker.className = activeCue.speaker === 'tariq' ? 'spk-tariq' : 'spk-claude';
    subText.textContent = activeCue.text;
  } else if (subBox) {
    subBox.style.display = 'none';
  }
}
