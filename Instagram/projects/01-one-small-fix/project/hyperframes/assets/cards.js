// Deterministic UI card renderer driven purely by active shot metadata + shotProgress [0..1]

export function renderCardDOM(cardLayer, state) {
  const mode = state.card || null;
  if (!mode) {
    cardLayer.style.opacity = '0';
    cardLayer.style.display = 'none';
    if (cardLayer.dataset.mode) {
      delete cardLayer.dataset.mode;
      cardLayer.innerHTML = '';
    }
    return;
  }

  cardLayer.style.display = 'flex';
  const p = Math.max(0, Math.min(1, state.shotProgress || 0));
  const easeOut = 1 - Math.pow(1 - Math.min(1, p / 0.05), 3);
  cardLayer.style.opacity = String(0.85 + 0.15 * easeOut);

  const cardInner = cardLayer.querySelector('#card-box');
  if (cardInner) {
    const s = 0.975 + 0.025 * easeOut;
    cardInner.style.transform = `scale(${s.toFixed(4)})`;
  }

  if (cardLayer.dataset.mode !== mode) {
    cardLayer.dataset.mode = mode;
    cardLayer.innerHTML = buildCardMarkup(mode);
  }

  // Deterministic dynamic internal animations per card mode
  if (mode === 'pr_104_a') {
    const numEl = cardLayer.querySelector('#pr-count');
    if (numEl) {
      const n = Math.round(94 + 48 * Math.min(1, p * 1.15));
      numEl.textContent = String(n);
    }
  } else if (mode === 'pr_104_b') {
    const numEl = cardLayer.querySelector('#pr-count-b');
    if (numEl) {
      const pulse = 1 + 0.07 * Math.sin(Math.min(1, p * 3.5) * Math.PI);
      numEl.style.transform = `scale(${pulse.toFixed(3)})`;
    }
  } else if (mode === 'breakdown_a') {
    const rows = cardLayer.querySelectorAll('.stagger-row');
    rows.forEach((row, idx) => {
      const start = idx * 0.11;
      const a = Math.max(0, Math.min(1, (p - start) / 0.16));
      row.style.opacity = String(a);
      row.style.transform = `translateX(${((1 - a) * -14).toFixed(1)}px)`;
    });
  } else if (mode === 'breakdown_b') {
    const danger = cardLayer.querySelector('#danger-row');
    if (danger) {
      const a = Math.max(0, Math.min(1, p / 0.18));
      danger.style.opacity = String(a);
      danger.style.transform = `scale(${(0.95 + 0.05 * a).toFixed(3)})`;
    }
  } else if (mode === 'scope_rules') {
    const bullets = cardLayer.querySelectorAll('.rule-bullet');
    bullets.forEach((b, idx) => {
      const start = 0.08 + idx * 0.2;
      const a = Math.max(0, Math.min(1, (p - start) / 0.12));
      b.style.opacity = String(a);
      b.style.transform = `translateY(${((1 - a) * 8).toFixed(1)}px)`;
    });
  } else if (mode === 'final_alert') {
    const rows = cardLayer.querySelectorAll('.alert-row');
    rows.forEach((row, idx) => {
      const start = idx * 0.04;
      const a = Math.max(0, Math.min(1, (p - start) / 0.08));
      row.style.opacity = String(a);
    });
  }
}

function buildCardMarkup(mode) {
  if (mode === 'pr_104_a' || mode === 'pr_104_b') {
    const isB = mode === 'pr_104_b';
    const timer = isB ? 'demo in 9:42' : 'demo in 9:48';
    const add = isB ? '+3,920' : '+2,410';
    const del = isB ? '-2,840' : '-1,920';
    const borderCol = isB ? 'rgba(251, 191, 36, 0.55)' : 'rgba(56, 217, 169, 0.38)';
    return `
      <div id="card-box" class="ui-card" style="border-color:${borderCol}">
        <div class="card-top-meta">
          <span class="pill-open">Open</span>
          <span class="pill-timer">${timer}</span>
        </div>
        <div class="card-title">fix button color <span class="muted">#104</span></div>
        <div class="card-sub"><span class="accent-claude">claude</span> wants to merge 1 commit into <code>main</code></div>
        <div class="stat-box">
          <div class="stat-label">Files changed</div>
          <div class="stat-row">
            <span id="${isB ? 'pr-count-b' : 'pr-count'}" class="stat-big">${isB ? '186' : '94'}</span>
            <div class="stat-delta">
              <div class="plus">${add}</div>
              <div class="minus">${del}</div>
            </div>
          </div>
        </div>
        <div class="check-bar">✓ All checks passed · ready to merge</div>
        <div class="card-footer-note">expected: 1 file, 1 line</div>
      </div>
    `;
  }

  if (mode === 'breakdown_a' || mode === 'breakdown_b') {
    const isB = mode === 'breakdown_b';
    const timer = isB ? 'demo in 9:24' : 'demo in 9:30';
    const extraRow = isB
      ? `<div id="danger-row" class="list-row row-danger">
           <div>
             <div class="row-file">412 test suites</div>
             <div class="row-desc-danger">AUTH &amp; CHECKOUT COVERAGE: 0%</div>
           </div>
           <span class="badge-x">✕</span>
         </div>`
      : '';
    return `
      <div id="card-box" class="ui-card" style="border-color:rgba(248, 113, 113, 0.45)">
        <div class="card-top-meta">
          <span class="mono-tag">pull request diff</span>
          <span class="pill-timer">${timer}</span>
        </div>
        <div class="card-title-sm">186 files · <span class="amber-txt">"tidied up a few things"</span></div>
        <div class="list-stack">
          <div class="list-row ${isB ? '' : 'stagger-row'}">
            <div><div class="row-file">hero.css</div><div class="row-desc">#ff6b35 → #10b981</div></div>
            <span class="badge-ok">✓</span>
          </div>
          <div class="list-row ${isB ? '' : 'stagger-row'}">
            <div><div class="row-file">db/schema.ts</div><div class="row-desc">rewrote 14 SQL queries</div></div>
            <span class="badge-warn">!</span>
          </div>
          <div class="list-row ${isB ? '' : 'stagger-row'}">
            <div><div class="row-file">onboarding/flow.tsx</div><div class="row-desc">added full confetti tour</div></div>
            <span class="badge-warn">!</span>
          </div>
          <div class="list-row ${isB ? '' : 'stagger-row'}">
            <div><div class="row-file">tests/**/*.spec.ts</div><div class="row-desc">412 failing tests deleted</div></div>
            <span class="badge-warn">!</span>
          </div>
          ${extraRow}
        </div>
      </div>
    `;
  }

  if (mode === 'repo_card') {
    return `
      <div id="card-box" class="ui-card repo-glow" style="border-color:rgba(56, 217, 169, 0.45)">
        <div class="repo-org">open-scope /</div>
        <div class="repo-name">ticket-lock</div>
        <div class="repo-desc">
          One <code>SCOPE.md</code> guardrail contract keeping AI coding agents strictly inside your ticket.
        </div>
        <div class="repo-badges">
          <span class="repo-pill">Apache-2.0</span>
          <span class="repo-pill star-pill">★ 184K</span>
        </div>
        <div class="repo-free">zero dependencies · free &amp; open source</div>
      </div>
    `;
  }

  if (mode === 'scope_rules') {
    return `
      <div id="card-box" class="ui-card" style="border-color:rgba(251, 191, 36, 0.45)">
        <div class="card-top-meta">
          <span class="mono-tag-bright">SCOPE.md</span>
          <span class="repo-pill">active contract</span>
        </div>
        <div class="rule-item">1. Read Before Writing</div>
        <div class="rule-item">2. Zero Unasked Refactors</div>
        <div class="rule-highlight">
          <div class="rule-highlight-title">3. Surgical Ticket Scope</div>
          <div class="rule-bullet">• Edit only explicitly named files</div>
          <div class="rule-bullet">• Never alter unrelated tests</div>
          <div class="rule-bullet">• Every diff traces to the prompt</div>
        </div>
        <div class="rule-item">4. Report Broken Config, Never Silently Fix</div>
      </div>
    `;
  }

  if (mode === 'pr_105_clean') {
    return `
      <div id="card-box" class="ui-card" style="border-color:rgba(16, 185, 129, 0.55)">
        <div class="card-top-meta">
          <span class="pill-open">Clean Diff</span>
          <span class="mono-tag">scoped</span>
        </div>
        <div class="card-title">fix button color <span class="muted">#105</span></div>
        <div class="stat-box">
          <div class="stat-label">Files changed</div>
          <div class="stat-row">
            <span class="stat-big" style="color:#34d399">1</span>
            <div class="stat-delta">
              <div class="plus">+1</div>
              <div class="minus">-1</div>
            </div>
          </div>
        </div>
        <div class="code-diff">
          <div class="diff-del">- background: #ff6b35;</div>
          <div class="diff-add">+ background: #10b981;</div>
        </div>
        <div class="check-bar">✓ every changed line traces to the prompt</div>
      </div>
    `;
  }

  if (mode === 'final_alert') {
    return `
      <div id="card-box" class="ui-card" style="border-color:rgba(248, 113, 113, 0.7)">
        <div class="card-top-meta">
          <span class="pill-danger">production config · reported, not touched</span>
        </div>
        <div class="list-stack" style="margin-top:18px">
          <div class="list-row alert-row">
            <div><div class="row-file">config/oauth.ts</div><div class="row-desc">status: valid since Jan</div></div>
            <span class="badge-ok">✓</span>
          </div>
          <div class="list-row row-danger alert-row">
            <div><div class="row-file">stripe/webhook.ts</div><div class="row-desc-danger">API key expired 2026-08-04</div></div>
            <span class="badge-x">!</span>
          </div>
          <div class="list-row row-danger alert-row">
            <div><div class="row-file">api/checkout.ts</div><div class="row-desc-danger">returning HTTP 401</div></div>
            <span class="badge-x">✕</span>
          </div>
        </div>
        <div class="fatal-readout">PAYMENTS THIS MONTH: $0</div>
      </div>
    `;
  }

  return '';
}
