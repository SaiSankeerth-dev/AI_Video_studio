import { execFileSync } from "node:child_process";
import { mkdirSync, copyFileSync, writeFileSync, existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const baseDir = fileURLToPath(new URL("..", import.meta.url));
const rawDir = join(baseDir, "assets\\audio\\dialogue_raw");
const cleanDir = join(baseDir, "assets\\audio\\dialogue");
const hfVoiceDir = join(baseDir, "project\\hyperframes\\assets\\voice");

mkdirSync(rawDir, { recursive: true });
mkdirSync(cleanDir, { recursive: true });
mkdirSync(hfVoiceDir, { recursive: true });

const lines = JSON.parse(readFileSync(join(baseDir, "scripts\\dialogue_lines.json"), "utf8"));
const HF_BIN = process.env.HYPERFRAMES_BIN || "hyperframes";

const meta = [];
for (const line of lines) {
  const rawOut = join(rawDir, `${line.id}.wav`);
  const cleanOut = join(cleanDir, `${line.id}.wav`);
  const hfOut = join(hfVoiceDir, `${line.id}.wav`);

  console.log(`Generating [${line.speaker}] ${line.id}: "${line.text}"`);

  execFileSync("node", [
    HF_BIN, "tts",
    "--voice", line.voice,
    "--speed", String(line.speed),
    "-o", rawOut,
    line.text,
  ], { stdio: "inherit" });

  // Broadcast loudness normalization + silence trimming
  execFileSync("ffmpeg", [
    "-y", "-i", rawOut,
    "-af", "silenceremove=start_periods=1:start_silence=0.03:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_silence=0.04:start_threshold=-45dB,areverse,highpass=f=85,loudnorm=I=-16:TP=-1.5:LRA=7",
    "-ar", "48000", "-ac", "2",
    cleanOut,
  ], { stdio: "ignore" });

  copyFileSync(cleanOut, hfOut);

  const durStr = execFileSync("ffprobe", [
    "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", cleanOut,
  ], { encoding: "utf8" }).trim();
  const dur = Number(parseFloat(durStr).toFixed(3));
  meta.push({ ...line, duration: dur, file: `assets/voice/${line.id}.wav` });
  console.log(`-> ${line.id}: ${dur}s`);
}

writeFileSync(join(baseDir, "assets\\audio\\dialogue_manifest.json"), JSON.stringify(meta, null, 2));
writeFileSync(join(baseDir, "project\\hyperframes\\assets\\voice\\dialogue_manifest.json"), JSON.stringify(meta, null, 2));
console.log("SUCCESS: All 19 dialogue lines generated and normalized.");
