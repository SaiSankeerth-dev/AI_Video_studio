import React from 'react';
import { Sequence, staticFile, Audio, Video } from 'remotion';
import { theme } from '../styles/theme';
import { FernSubtitle } from '../components/FernSubtitle';
import { SourceBadge } from '../components/shared/SourceBadge';
import { SmoothCamera } from '../components/SmoothCamera';
import { AstraTitleLoop } from '../components/scenes/AstraTitleLoop';
import { EvidenceVerifyCard } from '../components/scenes/EvidenceVerifyCard';
import { AstraComparison } from '../components/scenes/AstraComparison';

export const astraPilotShots = [
  {
    id: 'S01',
    startFrame: 0,
    durationFrames: 165, // 0:00 - 0:05.5 (5.5s)
    type: 'image' as const,
    mediaSrc: 'images/s01_workstation_night.png',
    direction: 'zoom-in' as const,
    text: 'A computer is sitting in front of you.',
    voiceAudio: 'audio/narration_N001.mp3',
    sfx: 'ambient-hum',
    sourceBadge: 'AUTONOMOUS WORKSTATION // RESEARCH LAB',
    visualClass: 'CLASS E: ENVIRONMENT'
  },
  {
    id: 'S02',
    startFrame: 165,
    durationFrames: 225, // 0:05.5 - 0:13.0 (7.5s)
    type: 'image' as const,
    mediaSrc: 'images/s02_screen_desktop.png',
    direction: 'pan-right' as const,
    text: 'A browser is open. A terminal is waiting. There are files on the desktop.',
    voiceAudio: 'audio/narration_N002.mp3',
    sfx: 'room-tone',
    sourceBadge: 'RUNTIME TELEMETRY // AST-DESKTOP-01',
    visualClass: 'CLASS G: SCREEN RECONSTRUCTION'
  },
  {
    id: 'S03',
    startFrame: 390,
    durationFrames: 240, // 0:13.0 - 0:21.0 (8.0s)
    type: 'video' as const,
    mediaSrc: 'video/s03_architecture.mp4',
    text: 'And instead of asking an AI what to do... you ask it to do it.',
    voiceAudio: 'audio/narration_N003.mp3',
    sfx: 'subsonic-whoosh',
    sourceBadge: 'SPATIAL 3D RECONSTRUCTION // NEURAL CORE',
    visualClass: 'CLASS C: BLENDER 3D SPATIAL'
  },
  {
    id: 'S04',
    startFrame: 630,
    durationFrames: 225, // 0:21.0 - 0:28.5 (7.5s)
    type: 'component' as const,
    componentName: 'AstraTitleLoop',
    text: "That's the idea behind GPT-6 Astra.",
    voiceAudio: 'audio/narration_N004.mp3',
    sfx: 'ui-impact',
    sourceBadge: 'SYSTEM ARCHITECTURE // AGENTIC LOOP',
    visualClass: 'CLASS M: MOTION GRAPHICS'
  },
  {
    id: 'S05',
    startFrame: 855,
    durationFrames: 180, // 0:28.5 - 0:34.5 (6.0s)
    type: 'image' as const,
    mediaSrc: 'images/s05_keyboard_macro.png',
    direction: 'zoom-out' as const,
    text: "But the interesting question isn't whether it can generate better answers.",
    voiceAudio: 'audio/narration_N005.mp3',
    sfx: 'keyboard-click',
    sourceBadge: 'OPERATOR OBSERVATION // TACTILE MACRO',
    visualClass: 'CLASS D: OBJECT MACRO'
  },
  {
    id: 'S06',
    startFrame: 1035,
    durationFrames: 225, // 0:34.5 - 0:42.0 (7.5s)
    type: 'image' as const,
    mediaSrc: 'images/s06_agent_debug_screen.png',
    direction: 'pan-left' as const,
    text: "It's whether it can actually operate the world inside a computer.",
    voiceAudio: 'audio/narration_N006.mp3',
    sfx: 'terminal-keystrokes',
    sourceBadge: 'ILLUSTRATIVE RECONSTRUCTION // CODE REPAIR',
    visualClass: 'CLASS G: SCREEN RECONSTRUCTION'
  },
  {
    id: 'S07',
    startFrame: 1260,
    durationFrames: 285, // 0:42.0 - 0:51.5 (9.5s)
    type: 'component' as const,
    componentName: 'EvidenceVerifyCard',
    text: 'On September third, twenty twenty-six, OpenAI introduced Astra as a dedicated computer-use foundation model.',
    voiceAudio: 'audio/narration_N007.mp3',
    sfx: 'telemetry-chirp',
    sourceBadge: 'OPENAI ANNOUNCEMENT // STATUS: VERIFY',
    visualClass: 'CLASS F: EVIDENCE DOCUMENT'
  },
  {
    id: 'S08',
    startFrame: 1545,
    durationFrames: 255, // 0:51.5 - 1:00.0 (8.5s)
    type: 'component' as const,
    componentName: 'AstraComparison',
    text: 'Designed not simply to converse, but to plan, execute terminal commands, and navigate complex operating systems.',
    voiceAudio: 'audio/narration_N008.mp3',
    sfx: 'resolution-tone',
    sourceBadge: 'PARADIGM MATRIX // CHATBOT VS AGENT',
    visualClass: 'CLASS M: MOTION GRAPHICS'
  }
];

export const BenchmarkAstra60s: React.FC = () => {
  return (
    <div style={{ flex: 1, backgroundColor: '#07090F', position: 'relative', overflow: 'hidden', width: 1920, height: 1080 }}>
      {/* Subtle Background Sub-bass Ambient Drone */}
      <Audio src={staticFile('audio/ambient-hum.wav')} volume={0.08} loop />

      {/* 8 Distinct Story Beats (Total: 1800 frames = 60.00 seconds) */}
      {astraPilotShots.map((shot) => (
        <Sequence
          key={shot.id}
          from={shot.startFrame}
          durationInFrames={shot.durationFrames}
        >
          {/* Spoken Narration Audio */}
          <Audio src={staticFile(shot.voiceAudio)} volume={1.0} />

          {/* Motivated Sound Effect */}
          {shot.sfx && (
            <Audio src={staticFile(`audio/${shot.sfx}.wav`)} volume={0.35} />
          )}

          {/* Visual Presentation based on Shot Type */}
          {shot.type === 'image' && (
            <SmoothCamera
              imageSrc={shot.mediaSrc}
              totalFrames={shot.durationFrames}
              direction={shot.direction}
            />
          )}

          {shot.type === 'video' && (
            <div style={{ width: '100%', height: '100%', overflow: 'hidden', position: 'relative' }}>
              <Video
                src={staticFile(shot.mediaSrc)}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                }}
              />
            </div>
          )}

          {shot.type === 'component' && shot.componentName === 'AstraTitleLoop' && (
            <AstraTitleLoop totalFrames={shot.durationFrames} />
          )}

          {shot.type === 'component' && shot.componentName === 'EvidenceVerifyCard' && (
            <EvidenceVerifyCard totalFrames={shot.durationFrames} />
          )}

          {shot.type === 'component' && shot.componentName === 'AstraComparison' && (
            <AstraComparison totalFrames={shot.durationFrames} />
          )}

          {/* Top-Left Visual Class & Verification Indicator */}
          <div
            style={{
              position: 'absolute',
              top: 40,
              left: 50,
              display: 'flex',
              alignItems: 'center',
              gap: 15,
              zIndex: 90
            }}
          >
            <div
              style={{
                background: 'rgba(10, 14, 24, 0.88)',
                backdropFilter: 'blur(12px)',
                border: '1px solid rgba(0, 210, 255, 0.40)',
                borderRadius: 6,
                padding: '6px 16px',
                fontFamily: theme.monoFontFamily,
                fontSize: 13,
                color: '#00D2FF',
                letterSpacing: '0.15em'
              }}
            >
              {shot.visualClass}
            </div>
          </div>

          {/* Bottom-Left Investigative Source Badge */}
          <SourceBadge sourceText={shot.sourceBadge} frame={0} totalFrames={shot.durationFrames} />

          {/* Clean, Legible Subtitles */}
          <FernSubtitle text={shot.text} totalFrames={shot.durationFrames} />
        </Sequence>
      ))}
    </div>
  );
};
