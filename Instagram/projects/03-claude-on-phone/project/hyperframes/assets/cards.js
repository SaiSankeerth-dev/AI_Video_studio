// UI Cards and Subtitle Controller for Agent Talk — T3 Code Two-Character Conversation
export function initCards(container) {
  container.innerHTML = `
    <!-- Top Brand Watermark -->
    <div class="brand-pill" data-layout-ignore>
      <div class="brand-dot"></div>
      <span class="brand-title">Agent Talk</span>
    </div>

    <!-- 1. FROZEN TERMINAL (L01 - L03: 0.00 - 16.30s) -->
    <div id="card-terminal" class="ui-card" data-layout-allow-overlap>
      <div class="term-header">
        <div class="term-dot red"></div>
        <div class="term-dot yellow"></div>
        <div class="term-dot green"></div>
        <span class="term-title">claude-code ~/projects/agent-app</span>
      </div>
      <div class="term-line prompt">$ claude code</div>
      <div class="term-line action">> Refactoring 20 files across repository...</div>
      <div class="term-line prompt">? Allow file write to 20 files? (y/N) █</div>
      <div class="term-line warn">⏸ PAUSED — Waiting for developer input (28m elapsed)</div>
    </div>

    <!-- 2. NOTIFICATION POPUP (L04 - L05: 16.48 - 20.18s) -->
    <div id="card-notif" class="ui-card flex-card" data-layout-allow-overlap>
      <div class="notif-icon">📱</div>
      <div class="notif-body">
        <div class="notif-app">T3 Code • Connected</div>
        <div class="notif-title">Claude Code Live Stream</div>
        <div class="notif-text">Terminal synced to your phone. Ready for approval.</div>
      </div>
    </div>

    <!-- 3. T3 CODE HERO BADGE (L06: 20.36 - 23.84s & L15: 54.22 - 57.76s) -->
    <div id="card-t3-hero" class="ui-card" data-layout-allow-overlap>
      <div class="t3-title">T3 Code</div>
      <div class="t3-sub">Run Coding Agents From Your Phone</div>
      <div class="t3-stats">
        <div class="stat-pill stars">★ 52.4k GitHub Stars</div>
        <div class="stat-pill free">100% Free & Open Source</div>
      </div>
    </div>

    <!-- 4. MOBILE DIFF STREAM CARD (L07 - L10: 24.02 - 37.80s) -->
    <div id="card-mobile-diff" class="ui-card" data-layout-allow-overlap>
      <div class="diff-header">
        <div class="diff-session">T3 Code Mobile • PR #482</div>
        <div class="diff-badge">Live Diff Stream</div>
      </div>
      <div class="diff-title">Database & Router Refactor</div>
      <div class="diff-stats">
        <span>20 files changed</span> • <span class="add">+412 lines</span> • <span class="del">-180 lines</span>
      </div>
      <div id="btn-approve" class="approve-btn">✓ APPROVE FROM PHONE</div>
    </div>

    <!-- 5. FAQ QUOTE CARD (L11 - L13: 37.98 - 47.75s) -->
    <div id="card-faq" class="ui-card" data-layout-allow-overlap>
      <div class="faq-quote-mark">“</div>
      <div class="faq-quote-text">There is no way to pay us to use T3 Code. Bring the subscriptions you already have. Zero markup.</div>
      <div class="faq-source">— Official T3 Code FAQ</div>
    </div>

    <!-- 6. MULTI-AGENT ARRAY (L14: 47.93 - 54.04s) -->
    <div id="card-multi-agent" class="ui-card" data-layout-allow-overlap>
      <div class="agents-grid">
        <div id="box-claude" class="agent-box active-box">
          <div class="agent-icon">✳️</div>
          <div class="agent-name">Claude Code</div>
        </div>
        <div id="box-codex" class="agent-box">
          <div class="agent-icon">🟩</div>
          <div class="agent-name">Codex CLI</div>
        </div>
        <div id="box-cursor" class="agent-box">
          <div class="agent-icon">⬛</div>
          <div class="agent-name">Cursor</div>
        </div>
        <div id="box-antigravity" class="agent-box">
          <div class="agent-icon">🚀</div>
          <div class="agent-name">Antigravity</div>
        </div>
      </div>
      <div class="agent-tagline">All coding agents unified in one mobile dashboard</div>
    </div>

    <!-- 7. CRITICAL DANGER REFACTOR ALERT (L17 - L19: 61.47 - 68.47s) -->
    <div id="card-danger" class="ui-card" data-layout-allow-overlap>
      <div class="danger-header">
        <div class="danger-badge">CRITICAL WARNING</div>
        <span style="font-size: 28px; color: #fca5a5; font-family: monospace;">DIFF #999</span>
      </div>
      <div class="danger-title">Refactoring Entire Production Auth Router!</div>
      <div class="danger-stats">48 files deleted • 3,240 lines changed • 0 tests passing</div>
      <div class="danger-btn-row">
        <div class="danger-btn">DECLINE</div>
        <div class="danger-btn">ABORT</div>
      </div>
    </div>
  `;
}

export const CUES = [
  { id: "L01", speaker: "Tariq", start: 0.00, end: 5.54, text: "Claude, I'm heading to the kitchen for coffee. If you freeze up waiting for permission...", card: "card-terminal" },
  { id: "L02", speaker: "Claude", start: 5.72, end: 10.26, text: "You know I have to! As soon as I touch twenty files, the terminal locks until you press enter.", card: "card-terminal" },
  { id: "L03", speaker: "Tariq", start: 10.44, end: 16.30, text: "And I come back half an hour later, and you've been sitting on 'Allow? Yes or No' for twenty-nine minutes!", card: "card-terminal" },
  { id: "L04", speaker: "Claude", start: 16.48, end: 17.99, text: "Not anymore. Look at your phone.", card: "card-notif" },
  { id: "L05", speaker: "Tariq", start: 18.17, end: 20.18, text: "My phone? What did you just install?", card: "card-notif" },
  { id: "L06", speaker: "Claude", start: 20.36, end: 23.84, text: "T3 Code. Theo and the team made it completely open source.", card: "card-t3-hero" },
  { id: "L07", speaker: "Tariq", start: 24.02, end: 27.46, text: "Wait, my entire Claude Code session is streaming to my phone?", card: "card-mobile-diff" },
  { id: "L08", speaker: "Claude", start: 27.64, end: 32.34, text: "Full live terminal, file tree, and instant diffs. When I need permission, your phone buzzes.", card: "card-mobile-diff" },
  { id: "L09", speaker: "Tariq", start: 32.52, end: 34.75, text: "So I can approve file writes from the kitchen?", card: "card-mobile-diff" },
  { id: "L10", speaker: "Claude", start: 34.93, end: 37.80, text: "From the kitchen, from the elevator, or flat on your couch.", card: "card-mobile-diff" },
  { id: "L11", speaker: "Tariq", start: 37.98, end: 40.97, text: "Okay, what's the catch? How much is this costing me?", card: "card-faq" },
  { id: "L12", speaker: "Claude", start: 41.15, end: 45.08, text: "Zero dollars! In their FAQ it literally says: 'There is no way to pay us.'", card: "card-faq" },
  { id: "L13", speaker: "Tariq", start: 45.26, end: 47.75, text: "Wait, so they don't even proxy my tokens?", card: "card-faq" },
  { id: "L14", speaker: "Claude", start: 47.93, end: 54.04, text: "Direct to your own keys. Claude Code, Codex, Cursor, Grok, Antigravity. 52,000 stars.", card: "card-multi-agent" },
  { id: "L15", speaker: "Tariq", start: 54.22, end: 57.76, text: "So I don't have to sit here staring at a progress bar at two AM?", card: "card-t3-hero" },
  { id: "L16", speaker: "Claude", start: 57.94, end: 61.29, text: "Never again. Now go make that coffee. Your phone is about to buzz.", card: "card-notif" },
  { id: "L17", speaker: "Tariq", start: 61.47, end: 63.44, text: "Wait, what are you refactoring right now?", card: "card-danger" },
  { id: "L18", speaker: "Claude", start: 63.62, end: 66.14, text: "The entire production authentication router!", card: "card-danger" },
  { id: "L19", speaker: "Tariq", start: 66.32, end: 67.09, text: "Claude, NO!", card: "card-danger" },
];

export function updateCards(time) {
  const subBox = document.getElementById("sub-box");
  const subSpeaker = document.getElementById("sub-speaker");
  const subText = document.getElementById("sub-text");

  let activeCardId = null;
  let activeCue = null;

  for (const c of CUES) {
    if (time >= c.start && time < c.end) {
      activeCue = c;
      activeCardId = c.card;
      break;
    }
  }

  // Comedic freeze beat at end
  if (time >= 67.09) {
    activeCardId = "card-danger";
  }

  // Update subtitles
  if (activeCue) {
    subBox.style.display = "inline-flex";
    subSpeaker.textContent = activeCue.speaker;
    if (activeCue.speaker === "Claude") {
      subSpeaker.style.borderColor = "#ff9500";
      subSpeaker.style.color = "#ffb74d";
    } else {
      subSpeaker.style.borderColor = "#38bdf8";
      subSpeaker.style.color = "#38bdf8";
    }
    subText.textContent = activeCue.text;
  } else {
    subBox.style.display = "none";
  }

  // Update cards active states
  const cards = [
    "card-terminal",
    "card-notif",
    "card-t3-hero",
    "card-mobile-diff",
    "card-faq",
    "card-multi-agent",
    "card-danger"
  ];

  for (const cid of cards) {
    const el = document.getElementById(cid);
    if (!el) continue;
    if (cid === activeCardId) {
      el.classList.add("active");
    } else {
      el.classList.remove("active");
    }
  }

  // Scene Multi-Agent cycling animation
  if (activeCardId === "card-multi-agent") {
    const boxes = ["box-claude", "box-codex", "box-cursor", "box-antigravity"];
    const subIdx = Math.floor((time - 47.93) / 1.5) % boxes.length;
    boxes.forEach((id, idx) => {
      const b = document.getElementById(id);
      if (b) {
        if (idx === subIdx) b.classList.add("active-box");
        else b.classList.remove("active-box");
      }
    });
  }

  // Mobile diff approval button state change
  const btnApprove = document.getElementById("btn-approve");
  if (btnApprove) {
    if (time >= 35.0) {
      btnApprove.textContent = "✓ APPROVED FROM COUCH";
      btnApprove.classList.add("merged");
    } else {
      btnApprove.textContent = "✓ APPROVE FROM PHONE";
      btnApprove.classList.remove("merged");
    }
  }
}
