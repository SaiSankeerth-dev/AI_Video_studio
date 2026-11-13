import { mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { join } from 'node:path';

const videoPath = 'E:/AI_Videos/Instagram/projects/03-claude-on-phone/renders/iteration_03.mp4';
const framesDir = 'E:/AI_Videos/Instagram/projects/03-claude-on-phone/renders/_iteration_03_frames';
mkdirSync(framesDir, { recursive: true });

const timestamps = [2, 6, 10, 14, 17, 21, 25, 29, 34, 38, 43, 48, 52, 57, 62, 67];

timestamps.forEach((ts, idx) => {
  const pad = String(idx + 1).padStart(2, '0');
  const outFrame = join(framesDir, `frame_${pad}.jpg`);
  execSync(`ffmpeg -y -ss ${ts} -i "${videoPath}" -vframes 1 -q:v 2 "${outFrame}"`, { stdio: 'ignore' });
  console.log(`Extracted frame ${pad} at ${ts}s`);
});

const contactSheet = join(framesDir, 'contact_sheet_4x4.jpg');
execSync(`ffmpeg -y -i "${framesDir}/frame_%02d.jpg" -filter_complex "scale=270:480,tile=4x4" -q:v 2 "${contactSheet}"`, { stdio: 'ignore' });
console.log('Built contact sheet:', contactSheet);
