import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const baseDir = 'E:/AI_Videos/Instagram/projects/03-claude-on-phone';
const cues = JSON.parse(readFileSync(join(baseDir, 'scripts/timeline_cues.json'), 'utf8')).cues;

function formatSrtTime(seconds) {
  const pad = (n, w = 2) => String(Math.floor(n)).padStart(w, '0');
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.floor((seconds - Math.floor(seconds)) * 1000);
  return `${pad(h)}:${pad(m)}:${pad(s)},${pad(ms, 3)}`;
}

let srt = '';
cues.forEach((c, idx) => {
  srt += `${idx + 1}\n`;
  srt += `${formatSrtTime(c.start)} --> ${formatSrtTime(c.end)}\n`;
  srt += `[${c.speaker.toUpperCase()}]: ${c.text}\n\n`;
});

writeFileSync(join(baseDir, 'subtitles/final_subtitles.srt'), srt.trim());
console.log('Saved final_subtitles.srt with 19 cues.');
