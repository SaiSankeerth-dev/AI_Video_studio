import React from 'react';
import { Sequence, staticFile, Audio, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { FernSubtitle } from '../components/FernSubtitle';
import { SourceBadge } from '../components/shared/SourceBadge';
import { SmoothCamera } from '../components/SmoothCamera';

// 8 Distinct Story Beats (1800 frames = 60.00 seconds total)
const ciaPilotShots = [
  {
    id: 'p01',
    startFrame: 0,
    durationFrames: 150, // 0:00 - 0:05 (5.0s)
    imageSrc: 'images/v03_datacenter.jpg',
    direction: 'zoom-in' as const,
    text: 'Deep inside the American intelligence community, security protocols are designed to repel sovereign nations.',
    voiceAudio: 'audio/v03_sentences/c01.mp3',
    sfx: 'ambient-hum',
    sourceBadge: 'CIA HEADQUARTERS // LANGLEY, VA',
    visualClass: 'CLASS E: ENVIRONMENT'
  },
  {
    id: 'p02',
    startFrame: 150,
    durationFrames: 210, // 0:05 - 0:12 (7.0s)
    imageSrc: 'images/v03_soc_night.jpg',
    direction: 'pan-right' as const,
    text: 'Yet in October twenty-fifteen, the personal communications of the CIA Director were quietly penetrated.',
    voiceAudio: 'audio/v03_sentences/c03.mp3',
    sfx: 'alert',
    sourceBadge: 'INCIDENT LOG // CASE 1:16-CR-00122',
    visualClass: 'CLASS E: ENVIRONMENT'
  },
  {
    id: 'p03',
    startFrame: 360,
    durationFrames: 240, // 0:12 - 0:20 (8.0s)
    imageSrc: 'images/v03_cia_seal_frame.jpg',
    direction: 'zoom-in' as const,
    text: 'The intruder was not a foreign intelligence service. He was a fifteen-year-old schoolboy in England.',
    voiceAudio: 'audio/v03_sentences/c05.mp3',
    sfx: 'impact',
    sourceBadge: 'PRIMARY EVIDENCE // OFFICIAL CIA RECORDS',
    visualClass: 'CLASS B: HISTORICAL EVIDENCE'
  },
  {
    id: 'p04',
    startFrame: 600,
    durationFrames: 240, // 0:20 - 0:28 (8.0s)
    imageSrc: 'images/v03_bedroom_workstation.jpg',
    direction: 'pan-left' as const,
    text: 'Operating under the alias Cracka, he possessed no zero-day exploits and wrote no custom malware.',
    voiceAudio: 'audio/v03_sentences/c07.mp3',
    sfx: 'keyboard',
    sourceBadge: 'RECONSTRUCTION // BEDROOM WORKSTATION',
    visualClass: 'CLASS A: DRAMATIZED REENACTMENT'
  },
  {
    id: 'p05',
    startFrame: 840,
    durationFrames: 240, // 0:28 - 0:36 (8.0s)
    imageSrc: 'images/shot03_telephone_macro.jpg',
    direction: 'zoom-out' as const,
    text: 'Their weapon was an encyclopedic mastery of social engineering over customer support telephone lines.',
    voiceAudio: 'audio/v03_sentences/c08.mp3',
    sfx: 'phone-ring',
    sourceBadge: 'ATTACK VECTOR // VERIZON SUPPORT PRETEXTING',
    visualClass: 'CLASS D: OBJECT MACRO'
  },
  {
    id: 'p06',
    startFrame: 1080,
    durationFrames: 240, // 0:36 - 0:44 (8.0s)
    imageSrc: 'images/v03_sf86_exhibit.jpg',
    direction: 'zoom-in' as const,
    text: 'Inside the inbox lay a forty-seven-page top-secret security clearance questionnaire.',
    voiceAudio: 'audio/v03_sentences/c13.mp3',
    sfx: 'alert',
    sourceBadge: 'EVIDENCE EXHIBIT // 47-PAGE SF-86 DOSSIER',
    visualClass: 'CLASS F: EVIDENCE DOCUMENT'
  },
  {
    id: 'p07',
    startFrame: 1320,
    durationFrames: 240, // 0:44 - 0:52 (8.0s)
    imageSrc: 'images/v03_network_map.jpg',
    direction: 'pan-right' as const,
    text: 'A single unproxied network connection allowed British investigators to triangulate the home address.',
    voiceAudio: 'audio/v03_sentences/c19.mp3',
    sfx: 'whoosh',
    sourceBadge: 'TELEMETRY TRACKER // UK CYBERCRIME UNIT',
    visualClass: 'CLASS C: TECHNICAL VISUALIZATION'
  },
  {
    id: 'p08',
    startFrame: 1560,
    durationFrames: 240, // 0:52 - 0:60 (8.0s)
    imageSrc: 'images/v03_fbi_dossier.jpg',
    direction: 'zoom-out' as const,
    text: 'No matter how strong the cryptographic lock, an entire fortress can fall when someone simply asks for the key.',
    voiceAudio: 'audio/v03_sentences/c24.mp3',
    sfx: 'impact',
    sourceBadge: 'JUDGMENT // CENTRAL CRIMINAL COURT (2018)',
    visualClass: 'CLASS F: EVIDENCE DOCUMENT'
  }
];

export const BenchmarkCIA60s: React.FC = () => {
  return (
    <div style={{ flex: 1, backgroundColor: '#04060A', position: 'relative', overflow: 'hidden' }}>
      {/* Deep Analog Tape Drone */}
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.045} loop />

      {ciaPilotShots.map((shot) => (
        <Sequence
          key={shot.id}
          from={shot.startFrame}
          durationInFrames={shot.durationFrames}
        >
          {/* Voiceover */}
          <Audio src={staticFile(shot.voiceAudio)} volume={1.0} />

          {/* Sound Effects */}
          {shot.sfx && (
            <Audio src={staticFile(`audio/${shot.sfx}.wav`)} volume={0.40} />
          )}

          {/* Rock-Solid Subpixel Smooth Camera */}
          <SmoothCamera
            imageSrc={shot.imageSrc}
            totalFrames={shot.durationFrames}
            direction={shot.direction}
          />

          {/* Top-Left Visual Class HUD */}
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
                background: 'rgba(6, 10, 18, 0.88)',
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

          {/* Verified Source Badge */}
          <SourceBadge sourceText={shot.sourceBadge} frame={0} totalFrames={shot.durationFrames} />

          {/* Clean Subtitles */}
          <FernSubtitle text={shot.text} totalFrames={shot.durationFrames} />
        </Sequence>
      ))}
    </div>
  );
};
