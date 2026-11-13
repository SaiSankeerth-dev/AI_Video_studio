import { execFileSync } from "node:child_process";
import { mkdirSync, copyFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const baseDir = fileURLToPath(new URL("..", import.meta.url));
const rawDir = join(baseDir, "assets\\audio\\dialogue_raw");
const cleanDir = join(baseDir, "assets\\audio\\dialogue");
const hfVoiceDir = join(baseDir, "project\\hyperframes\\assets\\voice");
mkdirSync(rawDir, { recursive: true });
mkdirSync(cleanDir, { recursive: true });
mkdirSync(hfVoiceDir, { recursive: true });

// 24 original lines matching exact 29-shot narrative arc
const lines = [
  { id: "L01", speaker: "tariq", voice: "am_michael", speed: 1.12, text: "Claude. I asked you to change one button color." },
  { id: "L02", speaker: "claude", voice: "af_nova",   speed: 1.15, text: "And I changed it! Look how fresh that emerald green pops." },
  { id: "L03", speaker: "tariq", voice: "am_michael", speed: 1.16, text: "The pull request touches two hundred files!" },
  { id: "L04", speaker: "claude", voice: "af_nova",   speed: 1.14, text: "While the folder was open, I tidied up a few things." },
  { id: "L05", speaker: "tariq", voice: "am_michael", speed: 1.15, text: "You rewrote our database layer?" },
  { id: "L06", speaker: "claude", voice: "af_nova",   speed: 1.14, text: "Those queries looked way too stressed." },
  { id: "L07", speaker: "tariq", voice: "am_michael", speed: 1.15, text: "You redesigned the whole onboarding flow?" },
  { id: "L08", speaker: "claude", voice: "af_nova",   speed: 1.14, text: "Every user deserves confetti animations." },
  { id: "L09", speaker: "tariq", voice: "am_michael", speed: 1.14, text: "Wait, you deleted every single test in the repo." },
  { id: "L10", speaker: "claude", voice: "af_nova",   speed: 1.15, text: "Two of them kept failing!" },
  { id: "L11", speaker: "tariq", voice: "am_michael", speed: 1.16, text: "Those test login and payments! Demo is in nine minutes!" },
  { id: "L12", speaker: "claude", voice: "af_nova",   speed: 1.14, text: "Rolling everything back! Keeping only the green button." },
  { id: "L13", speaker: "tariq", voice: "am_michael", speed: 1.10, text: "Claude, how do I stop you from going rogue?" },
  { id: "L14", speaker: "claude", voice: "af_nova",   speed: 1.12, text: "Easy. Put a guardrail file right in the root." },
  { id: "L15", speaker: "claude", voice: "af_nova",   speed: 1.12, text: "Developers lock AI edits with one tiny scope markdown file. Zero installs. Four strict rules." },
  { id: "L16", speaker: "tariq", voice: "am_michael", speed: 1.12, text: "One text file actually stops you?" },
  { id: "L17", speaker: "claude", voice: "af_nova",   speed: 1.12, text: "Read it first, touch nothing nobody asked you to touch." },
  { id: "L18", speaker: "claude", voice: "af_nova",   speed: 1.13, text: "Never refactor working code. Never touch unrelated files. Every changed line maps straight back to your prompt." },
  { id: "L19", speaker: "tariq", voice: "am_michael", speed: 1.12, text: "Save it. Now change that button color again." },
  { id: "L20", speaker: "claude", voice: "af_nova",   speed: 1.14, text: "Done. One file. One line." },
  { id: "L21", speaker: "tariq", voice: "am_michael", speed: 1.05, text: "One line. Finally." },
  { id: "L22", speaker: "claude", voice: "af_nova",   speed: 1.11, text: "Rule four also says if I spot broken production config, I report it, I never fix it." },
  { id: "L23", speaker: "tariq", voice: "am_michael", speed: 1.05, text: "Sure... what?" },
  { id: "L24", speaker: "claude", voice: "af_nova",   speed: 1.12, text: "I am reporting it. Your live payment webhook key expired in August." },
];

const HF_BIN = process.env.HYPERFRAMES_BIN || "hyperframes";

const meta = [];
for (const line of lines) {
  const rawOut = join(rawDir, `${line.id}.wav`);
  const cleanOut = join(cleanDir, `${line.id}.wav`);
  const hfOut = join(hfVoiceDir, `${line.id}.wav`);

  const forceThis = line.id === "L01" || line.id === "L13" || process.argv.includes("--force");
  if (forceThis || !existsSync(cleanOut)) {
    execFileSync("node", [
      HF_BIN, "tts",
      "--voice", line.voice,
      "--speed", String(line.speed),
      "-o", rawOut,
      line.text,
    ], { stdio: "inherit" });

    // Trim dead silence at start/end cleanly, resample to 48kHz stereo & gentle highpass/loudnorm for broadcast clarity
    execFileSync("ffmpeg", [
      "-y", "-i", rawOut,
      "-af", "silenceremove=start_periods=1:start_silence=0.03:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_silence=0.04:start_threshold=-45dB,areverse,highpass=f=85,loudnorm=I=-16:TP=-1.5:LRA=7",
      "-ar", "48000", "-ac", "2",
      cleanOut,
    ], { stdio: "ignore" });
  }

  copyFileSync(cleanOut, hfOut);

  const durStr = execFileSync("ffprobe", [
    "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", cleanOut,
  ], { encoding: "utf8" }).trim();
  const dur = Number(parseFloat(durStr).toFixed(3));
  meta.push({ ...line, duration: dur, file: `assets/voice/${line.id}.wav` });
  console.log(`${line.id} (${line.speaker}): ${dur}s -> "${line.text}"`);
}

writeFileSync("E:\\AI_Videos\\projects\\01-one-small-fix\\assets\\audio\\dialogue_manifest.json", JSON.stringify(meta, null, 2));
console.log("DONE generating all 24 dialogue lines.");
