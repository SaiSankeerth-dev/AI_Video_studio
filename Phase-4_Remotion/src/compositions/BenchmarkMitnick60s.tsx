import React from 'react';
import { Sequence, staticFile, Audio } from 'remotion';
import { theme } from '../styles/theme';
import { FernSubtitle } from '../components/FernSubtitle';
import { SourceBadge } from '../components/shared/SourceBadge';
import { SmoothCamera } from '../components/SmoothCamera';

// 10 Distinct Visual Beats Combining Real Historical Archives and Photorealistic Reenactments
const benchmarkShots = [
  {
    id: 'shot01',
    startFrame: 0,
    durationFrames: 180,
    imageSrc: 'images/arch_mitnick.jpg',
    direction: 'zoom-in' as const,
    text: 'In the early nineteen-nineties, Kevin Mitnick became the most wanted cyber fugitive in America.',
    voiceAudio: 'audio/v02_sentences/v18.mp3',
    sfx: 'alert',
    sourceBadge: 'HISTORICAL ARCHIVE // KEVIN MITNICK',
    visualClass: 'CLASS B: HISTORICAL ARCHIVE'
  },
  {
    id: 'shot02',
    startFrame: 180,
    durationFrames: 180,
    imageSrc: 'images/shot02_soc_environment.jpg',
    direction: 'pan-right' as const,
    text: 'Corporate security teams had fortified every digital perimeter with multi-layered firewalls.',
    voiceAudio: 'audio/v02_sentences/v01.mp3',
    sfx: 'ambient-hum',
    sourceBadge: 'ENTERPRISE SOC INCIDENT LOG',
    visualClass: 'CLASS E: ENVIRONMENT'
  },
  {
    id: 'shot03',
    startFrame: 360,
    durationFrames: 180,
    imageSrc: 'images/arch_we_phone.jpg',
    direction: 'zoom-in' as const,
    text: 'Yet the attacker never attempted to break their software encryption. He simply picked up a telephone.',
    voiceAudio: 'audio/v02_sentences/v05.mp3',
    sfx: 'phone-ring',
    sourceBadge: 'HISTORICAL ARTIFACT: AT&T / WESTERN ELECTRIC',
    visualClass: 'CLASS D: OBJECT MACRO'
  },
  {
    id: 'shot04',
    startFrame: 540,
    durationFrames: 180,
    imageSrc: 'images/arch_switch_vault.jpg',
    direction: 'pan-left' as const,
    text: 'Inside Pacific Bell switching facilities, authorized technicians were manipulated through calm authority.',
    voiceAudio: 'audio/v02_sentences/v15.mp3',
    sfx: 'whoosh',
    sourceBadge: 'HISTORICAL ARCHIVE: TELEPHONE SWITCHING RELAYS',
    visualClass: 'CLASS B: HISTORICAL ARCHIVE'
  },
  {
    id: 'shot05',
    startFrame: 720,
    durationFrames: 180,
    imageSrc: 'images/arch_blue_box.jpg',
    direction: 'zoom-out' as const,
    text: 'By using frequency tone generators and internal jargon, he bypassed critical telephone routing controls.',
    voiceAudio: 'audio/v02_sentences/v12.mp3',
    sfx: 'terminal-beep',
    sourceBadge: 'HISTORICAL ARTIFACT: 1970s BLUE BOX TONE GENERATOR',
    visualClass: 'CLASS D: HISTORICAL ARTIFACT'
  },
  {
    id: 'shot06',
    startFrame: 900,
    durationFrames: 180,
    imageSrc: 'images/arch_dec_vax.jpg',
    direction: 'tilt-up' as const,
    text: 'At Digital Equipment Corporation, he acquired crown-jewel VMS operating system source code.',
    voiceAudio: 'audio/v02_sentences/v17.mp3',
    sfx: 'impact',
    sourceBadge: 'HISTORICAL ARCHIVE: DEC VAX MAINFRAME SYSTEM',
    visualClass: 'CLASS B: HISTORICAL ARCHIVE'
  },
  {
    id: 'shot07',
    startFrame: 1080,
    durationFrames: 180,
    imageSrc: 'images/shot07_fbi_evidence_table.jpg',
    direction: 'zoom-in' as const,
    text: 'Wiretap transcripts and federal court exhibits documented hundreds of unauthorized intrusions.',
    voiceAudio: 'audio/v02_sentences/v20.mp3',
    sfx: 'alert',
    sourceBadge: 'US DISTRICT COURT EXHIBIT A (CR 96-389)',
    visualClass: 'CLASS F: EVIDENCE DOCUMENT'
  },
  {
    id: 'shot08',
    startFrame: 1260,
    durationFrames: 180,
    imageSrc: 'images/arch_motorola.jpg',
    direction: 'zoom-in' as const,
    text: 'At Motorola, proprietary microcode was exfiltrated without a single software exploit.',
    voiceAudio: 'audio/v02_sentences/v16.mp3',
    sfx: 'terminal-beep',
    sourceBadge: 'HISTORICAL ARTIFACT: MOTOROLA MICROCODE DIE',
    visualClass: 'CLASS D: HISTORICAL ARTIFACT'
  },
  {
    id: 'shot09',
    startFrame: 1440,
    durationFrames: 180,
    imageSrc: 'images/shot03_telephone_macro.jpg',
    direction: 'pan-right' as const,
    text: 'Mitnick proved that computers execute deterministic logic, but humans are driven by trust and urgency.',
    voiceAudio: 'audio/v02_sentences/v08.mp3',
    sfx: 'phone-ring',
    sourceBadge: 'EVIDENCE: HUMAN TRUST VECTOR',
    visualClass: 'CLASS D: OBJECT MACRO'
  },
  {
    id: 'shot10',
    startFrame: 1620,
    durationFrames: 180,
    imageSrc: 'images/shot10_server_monoliths.jpg',
    direction: 'zoom-out' as const,
    text: 'The lesson of Kevin Mitnick remains timeless: the password was never the real target—trust was.',
    voiceAudio: 'audio/v02_sentences/v24.mp3',
    sfx: 'impact',
    sourceBadge: 'THE ART OF DECEPTION (2002)',
    visualClass: 'CLASS E: ENVIRONMENT'
  }
];

export const BenchmarkMitnick60s: React.FC = () => {
  return (
    <div style={{ flex: 1, backgroundColor: '#050508', position: 'relative', overflow: 'hidden' }}>
      {/* Low Ambient Tape Drone */}
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.045} loop />

      {/* 10 Unique 6-Second Visual Beats */}
      {benchmarkShots.map((shot) => (
        <Sequence
          key={shot.id}
          from={shot.startFrame}
          durationInFrames={shot.durationFrames}
        >
          {/* 1. Baritone Voiceover */}
          <Audio src={staticFile(shot.voiceAudio)} volume={1.0} />

          {/* 2. Tactile Sound Effects */}
          {shot.sfx && (
            <Audio src={staticFile(`audio/${shot.sfx}.wav`)} volume={0.40} />
          )}

          {/* 3. Rock-Solid Subpixel Smooth Camera (Zero Shake) */}
          <SmoothCamera
            imageSrc={shot.imageSrc}
            totalFrames={shot.durationFrames}
            direction={shot.direction}
          />

          {/* 4. Top-Left Shot Metadata & Visual Class HUD Overlay */}
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
                border: '1px solid rgba(245, 158, 11, 0.40)',
                borderRadius: 6,
                padding: '6px 16px',
                fontFamily: theme.monoFontFamily,
                fontSize: 13,
                color: '#F59E0B',
                letterSpacing: '0.15em'
              }}
            >
              {shot.visualClass}
            </div>
          </div>

          {/* 5. Verified Historical Source Badge */}
          <SourceBadge sourceText={shot.sourceBadge} frame={0} totalFrames={shot.durationFrames} />

          {/* 6. Clean, Understated Normal Subtitles */}
          <FernSubtitle text={shot.text} totalFrames={shot.durationFrames} />
        </Sequence>
      ))}
    </div>
  );
};
