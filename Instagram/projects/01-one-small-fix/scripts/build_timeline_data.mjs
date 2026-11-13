import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const PROJECT_ROOT = "E:/AI_Videos/projects/01-one-small-fix";
const MANIFEST_PATH = path.join(PROJECT_ROOT, "assets/audio/dialogue_manifest.json");
const VOICE_DIR = path.join(PROJECT_ROOT, "project/hyperframes/assets/voice");
const HF_DIR = path.join(PROJECT_ROOT, "project/hyperframes");
const INDEX_HTML = path.join(HF_DIR, "index.html");
const OUT_JS = path.join(PROJECT_ROOT, "project/hyperframes/assets/timeline_data.js");
const OUT_SRT = path.join(PROJECT_ROOT, "subtitles/final_subtitles.srt");
const FPS = 30;

const durCache = new Map();
function probeAudioDuration(relPath) {
  if (durCache.has(relPath)) return durCache.get(relPath);
  const abs = path.join(HF_DIR, relPath);
  const out = execFileSync("ffprobe", [
    "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    abs,
  ], { encoding: "utf8" }).trim();
  const d = Number.parseFloat(out);
  durCache.set(relPath, d);
  return d;
}

function readWavEnvelope30Fps(wavPath) {
  const buf = fs.readFileSync(wavPath);
  let offset = 12;
  let sampleRate = 48000;
  let channels = 2;
  let bitsPerSample = 16;
  let dataStart = 44;
  let dataSize = buf.length - 44;

  while (offset + 8 <= buf.length) {
    const chunkId = buf.toString("ascii", offset, offset + 4);
    const chunkSize = buf.readUInt32LE(offset + 4);
    if (chunkId === "fmt ") {
      channels = buf.readUInt16LE(offset + 10);
      sampleRate = buf.readUInt32LE(offset + 12);
      bitsPerSample = buf.readUInt16LE(offset + 22);
    } else if (chunkId === "data") {
      dataStart = offset + 8;
      dataSize = Math.min(chunkSize, buf.length - dataStart);
      break;
    }
    offset += 8 + chunkSize + (chunkSize % 2);
  }

  const bytesPerSample = bitsPerSample / 8;
  const frameStride = channels * bytesPerSample;
  const totalSamples = Math.floor(dataSize / frameStride);
  const samplesPerVideoFrame = Math.max(1, Math.floor(sampleRate / FPS));
  const numFrames = Math.max(1, Math.ceil(totalSamples / samplesPerVideoFrame));
  const raw = [];
  let maxRms = 1e-6;

  for (let f = 0; f < numFrames; f++) {
    const s0 = f * samplesPerVideoFrame;
    const s1 = Math.min(totalSamples, (f + 1) * samplesPerVideoFrame);
    let sumSq = 0;
    let count = 0;
    for (let s = s0; s < s1; s++) {
      const idx = dataStart + s * frameStride;
      if (idx + 2 <= buf.length) {
        const val = buf.readInt16LE(idx) / 32768;
        sumSq += val * val;
        count++;
      }
    }
    const rms = count > 0 ? Math.sqrt(sumSq / count) : 0;
    raw.push(rms);
    if (rms > maxRms) maxRms = rms;
  }

  // Normalize and smooth lightly for crisp animated mouth & LED bar response
  const norm = raw.map((v) => Math.min(1, Math.pow(v / (maxRms * 0.72), 0.75)));
  const smoothed = [];
  let prev = 0;
  for (const v of norm) {
    const cur = v > prev ? prev * 0.25 + v * 0.75 : prev * 0.55 + v * 0.45;
    smoothed.push(Number(cur.toFixed(3)));
    prev = cur;
  }
  return smoothed;
}

function splitCaptionCues(text, start, dur) {
  const clean = text.replace(/\s+/g, " ").trim();
  const words = clean.split(" ");
  if (words.length <= 8 && clean.length <= 48) {
    return [{ start: Number(start.toFixed(3)), end: Number((start + dur).toFixed(3)), text: clean }];
  }
  // Split at sentence boundary first if sensible, otherwise midpoint word
  const sentences = clean.split(/(?<=[.!?—])\s+/).filter(Boolean);
  let chunks = [];
  if (sentences.length >= 2 && sentences.every((s) => s.length <= 54)) {
    chunks = sentences;
  } else if (sentences.length >= 2) {
    // Regroup into balanced phrases <= ~46 chars
    let acc = "";
    for (const s of sentences) {
      if ((acc + " " + s).trim().length <= 46) {
        acc = (acc + " " + s).trim();
      } else {
        if (acc) chunks.push(acc);
        acc = s;
      }
    }
    if (acc) chunks.push(acc);
  } else {
    const mid = Math.ceil(words.length / 2);
    chunks = [words.slice(0, mid).join(" "), words.slice(mid).join(" ")];
  }

  // Further split any overlong chunk (>54 chars)
  const finalChunks = [];
  for (const c of chunks) {
    const cw = c.split(" ");
    if (c.length > 54 && cw.length >= 6) {
      const mid = Math.ceil(cw.length / 2);
      finalChunks.push(cw.slice(0, mid).join(" "), cw.slice(mid).join(" "));
    } else {
      finalChunks.push(c);
    }
  }

  const totalWeight = finalChunks.reduce((s, c) => s + Math.max(4, c.replace(/[^a-zA-Z0-9]/g, "").length), 0);
  let t = start;
  return finalChunks.map((c, idx) => {
    const w = Math.max(4, c.replace(/[^a-zA-Z0-9]/g, "").length);
    const segDur = idx === finalChunks.length - 1 ? start + dur - t : (dur * w) / totalWeight;
    const cue = {
      start: Number(t.toFixed(3)),
      end: Number((t + segDur).toFixed(3)),
      text: c,
    };
    t += segDur;
    return cue;
  });
}

function fmtSrtTime(sec) {
  const msTotal = Math.max(0, Math.round(sec * 1000));
  const h = Math.floor(msTotal / 3600000);
  const m = Math.floor((msTotal % 3600000) / 60000);
  const s = Math.floor((msTotal % 60000) / 1000);
  const ms = msTotal % 1000;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")},${String(ms).padStart(3, "0")}`;
}

const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8"));
const lineById = Object.fromEntries(manifest.map((m) => [m.id, m]));

const SHOT_DEFS = [
  { id: 1, line: "L01", lead: 0.08, tail: 0.14, cam: "tariq_cu", card: null, pushZoom: 0.03, tariqExpr: "annoyed", tariqPose: "typing", kipMood: "happy", sfx: [{ file: "click.mp3", offset: 0.02, vol: 0.35 }] },
  { id: 2, line: null, fixedDur: 1.45, cam: "tariq_cu", card: "pr_104_a", sfx: [{ file: "click-soft.mp3", offset: 0.10, vol: 0.32 }, { file: "click-soft.mp3", offset: 0.55, vol: 0.25 }] },
  { id: 3, line: "L02", lead: 0.08, tail: 0.18, cam: "kip_cu", card: null, pushZoom: 0.03, kipMood: "happy", kipHop: 1, kipWave: 1, holoMode: "tree" },
  { id: 4, line: "L03", lead: 0.06, tail: 0.14, cam: "tariq_cu", card: null, pushZoom: 0.05, tariqExpr: "panic", tariqPose: "disbelief" },
  { id: 5, line: null, fixedDur: 1.30, cam: "tariq_cu", card: "pr_104_b", sfx: [{ file: "pop.mp3", offset: 0.06, vol: 0.40 }] },
  { id: 6, line: "L04", lead: 0.08, tail: 0.16, cam: "kip_cu", card: null, pushZoom: 0.02, kipMood: "innocent", kipTilt: 0.14, kipWave: 0.8 },
  { id: 7, line: "L05", lead: 0.06, tail: 0.14, cam: "tariq_cu", card: null, pushZoom: 0.04, tariqExpr: "annoyed", tariqPose: "skeptical" },
  { id: 8, line: "L06", lead: 0.06, tail: 0.16, cam: "kip_cu", card: null, pushZoom: 0.02, kipMood: "happy", kipWave: 0.9 },
  { id: 9, line: "L07", lead: 0.06, tail: 0.14, cam: "tariq_cu", card: null, pushZoom: 0.06, tariqExpr: "panic", tariqPose: "disbelief" },
  { id: 10, line: "L08", lead: 0.06, tail: 0.18, cam: "kip_cu", card: null, pushZoom: 0.03, kipMood: "proud", kipHop: 1, sfx: [{ file: "sparkle.mp3", offset: 0.85, vol: 0.36 }] },
  { id: 11, line: "L09", lead: 0.08, tail: 0.20, cam: "tariq_cu", card: "breakdown_a", sfx: [{ file: "key-press.mp3", offset: 0.15, vol: 0.28 }, { file: "key-press.mp3", offset: 0.55, vol: 0.28 }, { file: "key-press.mp3", offset: 1.05, vol: 0.30 }] },
  { id: 12, line: "L10", lead: 0.08, tail: 0.20, cam: "kip_cu", card: null, pushZoom: 0.03, kipMood: "guilt_sweat", kipSweat: true, sfx: [{ file: "pop.mp3", offset: 0.18, vol: 0.38 }] },
  { id: 13, line: "L11", lead: 0.06, tail: 0.16, cam: "tariq_cu", card: null, pushZoom: 0.08, tariqExpr: "panic", tariqPose: "disbelief" },
  { id: 14, line: null, fixedDur: 1.50, cam: "tariq_cu", card: "breakdown_b", sfx: [{ file: "error.mp3", offset: 0.05, vol: 0.42 }] },
  { id: 15, line: "L12", lead: 0.08, tail: 0.18, cam: "kip_cu", card: null, pushZoom: 0.03, kipMood: "proud", holoMode: "revert", kipNod: 1, sfx: [{ file: "whoosh-short.mp3", offset: 0.05, vol: 0.35 }] },
  { id: 16, line: "L13", lead: 0.10, tail: 0.18, cam: "wide_desk", card: null, pushZoom: 0.00, tariqExpr: "annoyed", tariqPose: "exhausted" },
  { id: 17, line: "L14", lead: 0.06, tail: 0.14, cam: "kip_cu", card: null, pushZoom: 0.03, kipMood: "proud" },
  { id: 18, line: "L15", lead: 0.10, tail: 0.22, cam: "kip_cu", card: "repo_card", sfx: [{ file: "notification.mp3", offset: 0.06, vol: 0.34 }] },
  { id: 19, line: "L16", lead: 0.06, tail: 0.14, cam: "tariq_cu", card: null, pushZoom: 0.03, tariqExpr: "skeptical", tariqPose: "skeptical", tariqTurn: 0.06 },
  { id: 20, line: "L17", lead: 0.08, tail: 0.16, cam: "kip_cu", card: null, pushZoom: 0.02, kipMood: "proud" },
  { id: 21, line: "L18", lead: 0.10, tail: 0.24, cam: "kip_cu", card: "scope_rules", sfx: [{ file: "click-soft.mp3", offset: 0.50, vol: 0.28 }, { file: "click-soft.mp3", offset: 2.20, vol: 0.28 }, { file: "click-soft.mp3", offset: 4.10, vol: 0.28 }] },
  { id: 22, line: "L19", lead: 0.08, tail: 0.18, cam: "wide_desk", card: null, pushZoom: 0.01, tariqExpr: "skeptical", tariqPose: "point" },
  { id: 23, line: "L20", lead: 0.08, tail: 0.22, cam: "kip_cu", card: "pr_105_clean", sfx: [{ file: "chime.mp3", offset: 0.08, vol: 0.38 }] },
  { id: 24, line: "L21", lead: 0.10, tail: 0.22, cam: "tariq_cu", card: null, pushZoom: 0.02, tariqExpr: "relieved", tariqPose: "exhausted" },
  { id: 25, line: "L22", lead: 0.08, tail: 0.16, cam: "kip_cu", card: null, pushZoom: 0.02, kipMood: "innocent", foreshadowAlert: true },
  { id: 26, line: "L23", lead: 0.06, tail: 0.14, cam: "tariq_cu", card: null, pushZoom: 0.02, tariqExpr: "annoyed", tariqPose: "typing" },
  { id: 27, line: "L24", lead: 0.08, tail: 0.14, cam: "kip_cu", card: null, pushZoom: 0.02, kipMood: "innocent", foreshadowAlert: true },
  { id: 28, line: null, fixedDur: 2.40, cam: "tariq_cu", card: "final_alert", silence: true, sfx: [{ file: "impact-bass-1.mp3", offset: 0.00, vol: 0.30 }] },
  { id: 29, line: null, fixedDur: 1.90, cam: "tariq_cu", card: null, silence: true, pushZoom: 0.05, tariqExpr: "stunned", tariqPose: "exhausted", freeze: true },
];

const envelopes = {};
const shots = [];
const dialogueEvents = [];
const sfxEvents = [];
const subtitleCues = [];

let cursor = 0;

for (const def of SHOT_DEFS) {
  let dur;
  let lineMeta = null;
  let voiceStart = null;
  if (def.line) {
    lineMeta = lineById[def.line];
    const wavPath = path.join(VOICE_DIR, `${def.line}.wav`);
    envelopes[def.line] = readWavEnvelope30Fps(wavPath);
    dur = Number((def.lead + lineMeta.duration + def.tail).toFixed(3));
    voiceStart = Number((cursor + def.lead).toFixed(3));

    dialogueEvents.push({
      id: def.line,
      speaker: lineMeta.speaker,
      src: `assets/voice/${def.line}.wav`,
      start: voiceStart,
      duration: Number(lineMeta.duration.toFixed(3)),
      text: lineMeta.text,
    });

    const cues = splitCaptionCues(lineMeta.text, voiceStart, lineMeta.duration);
    for (const c of cues) {
      subtitleCues.push({
        ...c,
        speaker: lineMeta.speaker,
        shotId: def.id,
      });
    }
  } else {
    dur = def.fixedDur;
  }

  if (def.sfx) {
    for (const s of def.sfx) {
      sfxEvents.push({
        src: `assets/sfx/${s.file}`,
        start: Number((cursor + s.offset).toFixed(3)),
        volume: s.vol,
      });
    }
  }

  shots.push({
    id: def.id,
    start: Number(cursor.toFixed(3)),
    end: Number((cursor + dur).toFixed(3)),
    duration: dur,
    line: def.line || null,
    speaker: lineMeta ? lineMeta.speaker : null,
    voiceStart,
    voiceDuration: lineMeta ? Number(lineMeta.duration.toFixed(3)) : 0,
    cam: def.cam,
    card: def.card,
    pushZoom: def.pushZoom || 0,
    tariqExpr: def.tariqExpr || "annoyed",
    tariqPose: def.tariqPose || "typing",
    tariqTurn: def.tariqTurn || 0,
    kipMood: def.kipMood || "happy",
    kipSweat: !!def.kipSweat,
    kipTilt: def.kipTilt || 0,
    kipHop: def.kipHop || 0,
    kipWave: def.kipWave || 0,
    holoMode: def.holoMode || "tree",
    foreshadowAlert: !!def.foreshadowAlert,
    freeze: !!def.freeze,
    silence: !!def.silence,
  });

  cursor = Number((cursor + dur).toFixed(3));
}

// Music cuts out sharply right at start of Shot 28 (leaving ~0.08s bass decay + 4.07s stark ending!)
const shot28 = shots.find((s) => s.id === 28);
const musicEnd = Number((shot28.start).toFixed(3));

const srtBody = subtitleCues
  .map((c, idx) => `${idx + 1}\n${fmtSrtTime(c.start)} --> ${fmtSrtTime(c.end)}\n[${c.speaker.toUpperCase()}] ${c.text}\n`)
  .join("\n");

fs.writeFileSync(OUT_SRT, srtBody, "utf8");

const moduleSrc = `// AUTO-GENERATED by scripts/build_timeline_data.mjs — do not hand-edit
export const TOTAL_DURATION = ${cursor.toFixed(3)};
export const MUSIC_END = ${musicEnd.toFixed(3)};
export const FPS = ${FPS};

export const SHOTS = ${JSON.stringify(shots, null, 2)};

export const SUBTITLE_CUES = ${JSON.stringify(subtitleCues, null, 2)};

export const DIALOGUE_EVENTS = ${JSON.stringify(dialogueEvents, null, 2)};

export const SFX_EVENTS = ${JSON.stringify(sfxEvents, null, 2)};

export const ENVELOPES = ${JSON.stringify(envelopes)};

export function sampleEnvelope(lineId, timeSinceVoiceStart) {
  if (!lineId || timeSinceVoiceStart < 0) return 0;
  const arr = ENVELOPES[lineId];
  if (!arr || !arr.length) return 0;
  const idx = Math.floor(timeSinceVoiceStart * FPS);
  if (idx < 0 || idx >= arr.length) return 0;
  return arr[idx];
}

export function getShotAt(t) {
  for (let i = 0; i < SHOTS.length; i++) {
    const s = SHOTS[i];
    if (t < s.end || i === SHOTS.length - 1) return s;
  }
  return SHOTS[0];
}

export function getSubtitleAt(t) {
  for (let i = 0; i < SUBTITLE_CUES.length; i++) {
    const c = SUBTITLE_CUES[i];
    if (t >= c.start - 0.02 && t <= c.end + 0.04) return c;
  }
  return null;
}
`;

fs.writeFileSync(OUT_JS, moduleSrc, "utf8");

// Generate static <audio> elements for deterministic HyperFrames discovery + mix
const audioTags = [];
audioTags.push(
  `      <audio id="aud-bgm" src="assets/music/bgm.mp3" class="clip" data-start="0" data-duration="${musicEnd.toFixed(3)}" data-volume="0.14" data-fade-in="0.8" data-fade-out="0.12" data-timeline-role="music" data-track-index="3"></audio>`
);
for (const d of dialogueEvents) {
  audioTags.push(
    `      <audio id="aud-${d.id}" src="${d.src}" class="clip" data-start="${d.start.toFixed(3)}" data-duration="${d.duration.toFixed(3)}" data-volume="0.98" data-track-index="4"></audio>`
  );
}
for (let i = 0; i < sfxEvents.length; i++) {
  const s = sfxEvents[i];
  const natDur = probeAudioDuration(s.src);
  const clampedDur = Math.max(0.08, Math.min(natDur, cursor - s.start - 0.02));
  audioTags.push(
    `      <audio id="aud-sfx-${String(i + 1).padStart(2, "0")}" src="${s.src}" class="clip" data-start="${s.start.toFixed(3)}" data-duration="${clampedDur.toFixed(3)}" data-volume="${s.volume}" data-track-index="5"></audio>`
  );
}

let html = fs.readFileSync(INDEX_HTML, "utf8");
html = html.replace(/__TOTAL_DURATION__/g, cursor.toFixed(3));
html = html.replace(
  /(id="(?:root|stage3d|card-layer|sub-layer)"[^>]*data-duration=")[^"]+(")/g,
  `$1${cursor.toFixed(3)}$2`
);
html = html.replace(
  /<!-- AUDIO_TRACKS_START -->[\s\S]*?<!-- AUDIO_TRACKS_END -->/,
  `<!-- AUDIO_TRACKS_START -->\n${audioTags.join("\n")}\n      <!-- AUDIO_TRACKS_END -->`
);
fs.writeFileSync(INDEX_HTML, html, "utf8");

console.log(`Built timeline_data.js (${shots.length} shots, ${subtitleCues.length} subtitle cues, TOTAL=${cursor.toFixed(3)}s, MUSIC_END=${musicEnd.toFixed(3)}s)`);
console.log(`Injected ${audioTags.length} audio tracks into ${INDEX_HTML}`);
console.log(`Wrote SRT -> ${OUT_SRT}`);
