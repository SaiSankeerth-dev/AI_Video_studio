import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const baseDir = 'E:/AI_Videos/Instagram/projects/04-openshorts-gta6';
const manifestPath = join(baseDir, 'assets/audio/dialogue_manifest.json');

if (!existsSync(manifestPath)) {
  console.error('Manifest not ready yet.');
  process.exit(1);
}

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));

const shotMap = {
  L01: 'tariq_cu',
  L02: 'claude_cu',
  L03: 'tariq_cu',
  L04: 'claude_cu',
  L05: 'two_shot',
  L06: 'claude_cu',
  L07: 'tariq_cu',
  L08: 'claude_cu',
  L09: 'tariq_cu',
  L10: 'claude_cu',
  L11: 'tariq_cu',
  L12: 'claude_cu',
  L13: 'tariq_cu',
  L14: 'claude_cu',
  L15: 'tariq_cu',
  L16: 'two_shot',
  L17: 'tariq_cu',
  L18: 'claude_cu',
  L19: 'two_shot',
};

let curTime = 0.0;
const gap = 0.18;
const cues = [];

for (const line of manifest) {
  const start = Number(curTime.toFixed(3));
  const dur = Number(line.duration.toFixed(3));
  const end = Number((start + dur).toFixed(3));
  const shot = shotMap[line.id] || 'two_shot';

  cues.push({
    id: line.id,
    speaker: line.speaker,
    start: start,
    duration: dur,
    end: end,
    shot: shot,
    text: line.text,
    file: line.file,
  });

  curTime = end + gap;
}

const tailBuffer = 1.4;
const totalDuration = Number((curTime + tailBuffer).toFixed(2));

const outData = {
  totalDuration,
  cues,
};

writeFileSync(join(baseDir, 'scripts/timeline_cues.json'), JSON.stringify(outData, null, 2));
console.log(`Generated timeline_cues.json with ${cues.length} cues, total duration: ${totalDuration}s`);

// Also generate standard SRT file
function formatSRTTime(sec) {
  const hrs = Math.floor(sec / 3600).toString().padStart(2, '0');
  const mins = Math.floor((sec % 3600) / 60).toString().padStart(2, '0');
  const secs = Math.floor(sec % 60).toString().padStart(2, '0');
  const millis = Math.floor((sec % 1) * 1000).toString().padStart(3, '0');
  return `${hrs}:${mins}:${secs},${millis}`;
}

let srtContent = '';
cues.forEach((c, idx) => {
  srtContent += `${idx + 1}\n`;
  srtContent += `${formatSRTTime(c.start)} --> ${formatSRTTime(c.end)}\n`;
  srtContent += `${c.speaker.toUpperCase()}: ${c.text}\n\n`;
});

writeFileSync(join(baseDir, 'subtitles/final_subtitles.srt'), srtContent.trim() + '\n');
console.log(`Generated subtitles/final_subtitles.srt`);
