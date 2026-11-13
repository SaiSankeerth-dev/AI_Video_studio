import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const baseDir = 'E:/AI_Videos/Instagram/projects/04-openshorts-gta6';
const cuesData = JSON.parse(readFileSync(join(baseDir, 'scripts/timeline_cues.json'), 'utf8'));
const cues = cuesData.cues;
const totalDuration = cuesData.totalDuration;

let audioTags = `      <!-- BGM -->\n      <audio id="aud-bgm" src="assets/music/bgm.wav" class="clip" data-start="0" data-duration="${totalDuration}" data-volume="0.16" data-fade-in="0.4" data-fade-out="1.8" data-timeline-role="music" data-track-index="3"></audio>\n\n      <!-- Dialogue Tracks -->\n`;

for (const c of cues) {
  audioTags += `      <audio id="aud-${c.id}" src="${c.file}" class="clip" data-start="${c.start}" data-duration="${c.duration}" data-volume="0.98" data-track-index="4"></audio>\n`;
}

audioTags += `
      <!-- SFX Cues -->
      <audio id="aud-sfx-pop1" src="assets/sfx/pop.mp3" class="clip" data-start="10.12" data-duration="0.45" data-volume="0.32" data-track-index="5"></audio>
      <audio id="aud-sfx-whoosh1" src="assets/sfx/whoosh.mp3" class="clip" data-start="18.38" data-duration="0.50" data-volume="0.30" data-track-index="5"></audio>
      <audio id="aud-sfx-click1" src="assets/sfx/click.mp3" class="clip" data-start="30.00" data-duration="0.35" data-volume="0.35" data-track-index="5"></audio>
      <audio id="aud-sfx-chime" src="assets/sfx/chime.mp3" class="clip" data-start="35.00" data-duration="0.85" data-volume="0.38" data-track-index="6"></audio>
      <audio id="aud-sfx-click2" src="assets/sfx/click.mp3" class="clip" data-start="54.70" data-duration="0.35" data-volume="0.35" data-track-index="5"></audio>
      <audio id="aud-sfx-impact" src="assets/sfx/impact-bass-1.mp3" class="clip" data-start="60.94" data-duration="1.50" data-volume="0.42" data-track-index="5"></audio>
      <audio id="aud-sfx-error" src="assets/sfx/error.mp3" class="clip" data-start="68.20" data-duration="1.20" data-volume="0.35" data-track-index="5"></audio>
      <audio id="aud-sfx-pop2" src="assets/sfx/pop.mp3" class="clip" data-start="82.50" data-duration="0.45" data-volume="0.32" data-track-index="5"></audio>
`;

const html = `<!doctype html>
<html
  lang="en"
  data-composition-variables='[{"id":"brand-color","type":"color","label":"Brand Color","default":"#d47f53"},{"id":"bg-color","type":"color","label":"Background","default":"#080d1a"}]'
>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Agent Talk — OpenShorts & GTA 6 Stream Clipping</title>
    <script src="lib/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/styles.css" />
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="${totalDuration}"
      data-width="1080"
      data-height="1920"
      data-fps="30"
    >
      <!-- 3D WebGL Canvas Layer -->
      <canvas id="stage3d" width="1080" height="1920" class="clip" data-start="0" data-duration="${totalDuration}" data-track-index="0" data-layout-allow-overflow></canvas>

      <!-- UI Cards Overlay Layer -->
      <div id="card-layer" class="clip" data-start="0" data-duration="${totalDuration}" data-track-index="1" data-layout-allow-overlap></div>

      <!-- Mobile-Safe Subtitle HUD -->
      <div id="sub-layer" class="clip" data-start="0" data-duration="${totalDuration}" data-track-index="2" data-layout-allow-overlap>
        <div id="sub-box" style="display: none;">
          <span id="sub-speaker">Tariq</span><span id="sub-text"></span>
        </div>
      </div>

      <!-- AUDIO TRACKS -->
${audioTags}
    </div>

    <script type="module">
      import { initScene, updateScene } from './assets/scene3d.js';
      import { initCards, updateCards, CUES } from './assets/cards.js';

      const canvas = document.getElementById('stage3d');
      const cardContainer = document.getElementById('card-layer');

      initScene(canvas);
      initCards(cardContainer);

      const TOTAL_DURATION = ${totalDuration};
      let lastRenderedTime = -1;

      function renderFrame(rawTime) {
        const t = Math.max(0, Math.min(TOTAL_DURATION, Number(rawTime) || 0));
        if (Math.abs(t - lastRenderedTime) < 1e-5) return;
        lastRenderedTime = t;

        // Find active cue
        let currentCue = null;
        for (const c of CUES) {
          if (t >= c.start && t < c.end) {
            currentCue = c;
            break;
          }
        }

        updateScene(t, currentCue);
        updateCards(t);
      }

      // GSAP Timeline Registration for HyperFrames Renderer
      window.__timelines = window.__timelines || {};
      const clock = { t: 0 };
      const mainTl = gsap.timeline({ paused: true });
      mainTl.to(
        clock,
        {
          t: TOTAL_DURATION,
          duration: TOTAL_DURATION,
          ease: 'none',
          onUpdate: () => renderFrame(clock.t),
        },
        0
      );
      window.__timelines['main'] = mainTl;

      window.addEventListener('hf-seek', (e) => {
        if (e && e.detail && typeof e.detail.time === 'number') {
          renderFrame(e.detail.time);
        }
      });

      renderFrame(0);
    </script>
  </body>
</html>
`;

writeFileSync('E:/AI_Videos/Instagram/projects/04-openshorts-gta6/project/hyperframes/index.html', html);
console.log('Successfully wrote project 04 index.html with duration', totalDuration);
