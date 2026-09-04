import React from 'react';
import { Sequence, staticFile, Audio, Video, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { FernSubtitle } from '../components/FernSubtitle';
import { SourceBadge } from '../components/shared/SourceBadge';
import { AgentLoop } from '../components/scenes/AgentLoop';
import { ArchitectureDiagram } from '../components/scenes/ArchitectureDiagram';
import { ToolExecution } from '../components/scenes/ToolExecution';
import { CompanyMap } from '../components/scenes/CompanyMap';
import { QuoteCard } from '../components/QuoteCard';
import { SourceCard } from '../components/SourceCard';
import syncedData from '../../public/data/synced_sentences.json';

export const FernDocumentary: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ flex: 1, backgroundColor: '#050508', position: 'relative', overflow: 'hidden' }}>
      {/* Deep Analog Drone Music */}
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.045} loop />

      {/* Synchronized Documentary Scenes */}
      {syncedData.sentences.map((sent) => {
        return (
          <Sequence
            key={sent.id}
            from={sent.startFrame}
            durationInFrames={sent.durationFrames}
          >
            {/* 1. Deep Baritone Voiceover Track */}
            <Audio src={staticFile(sent.audio_file)} volume={1.0} />

            {/* 2. Tactile Sound Effects */}
            {sent.sfx && (
              <Audio src={staticFile(`audio/${sent.sfx}.wav`)} volume={0.35} />
            )}

            {/* 3. Cinematic 8K Motion Visual Layer */}
            {renderFernVisual(sent.visual_mode, sent.durationFrames)}

            {/* 4. Subtle Minimalist Source Badges */}
            {renderSourceBadge(sent.id, sent.durationFrames)}

            {/* 5. Clean, Understated Normal Subtitles */}
            <FernSubtitle text={sent.text} totalFrames={sent.durationFrames} />
          </Sequence>
        );
      })}
    </div>
  );
};

// Visual Scene Switcher using 8k photorealistic motion clips & clean technical motion graphics
function renderFernVisual(mode: string, totalFrames: number) {
  switch (mode) {
    case 'FERN_DATACENTER':
      return <Video src={staticFile('video/fern_datacenter.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;

    case 'FERN_ENGINEER':
    case 'FERN_ENGINEER_PUSH':
      return <Video src={staticFile('video/fern_engineer.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;

    case 'FERN_SILICON':
    case 'FERN_SILICON_ZOOM':
    case 'FERN_TOOLS_REASONER':
      return <Video src={staticFile('video/fern_silicon.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;

    case 'FERN_NETWORK_MAP':
      return <Video src={staticFile('video/fern_network.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;

    case 'FERN_MONOLITH':
      return <Video src={staticFile('video/fern_monolith.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;

    case 'FERN_TITLE':
      return (
        <div style={{ flex: 1, backgroundColor: '#070709', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', position: 'relative' }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: theme.cyan, letterSpacing: '0.3em', marginBottom: 20 }}>
            DOCUMENTARY SPECIAL REPORT
          </div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 58, fontWeight: 800, color: '#FFFFFF', textAlign: 'center', maxWidth: 1300, lineHeight: 1.25 }}>
            THE AI AGENTS THAT ARE STARTING TO <span style={{ color: theme.cyan }}>WORK WITHOUT US</span>
          </div>
          <div style={{ width: 120, height: 2, backgroundColor: theme.cyan, marginTop: 30 }} />
        </div>
      );

    case 'FERN_FIVE_PILLARS':
      return <ArchitectureDiagram totalFrames={totalFrames} />;

    case 'FERN_AGENT_LOOP':
      return <AgentLoop totalFrames={totalFrames} />;

    case 'FERN_TERMINAL_START':
    case 'FERN_TERMINAL_RUN':
    case 'FERN_CODE_DIFF':
    case 'FERN_ERROR_HEAL':
    case 'FERN_SUCCESS_PASS':
      return <ToolExecution totalFrames={totalFrames} />;

    case 'FERN_SWARM_MAP':
    case 'FERN_SWARM_DISPATCH':
      return <CompanyMap totalFrames={totalFrames} />;

    case 'FERN_CONTROL_WARNING':
    case 'FERN_BLACKWALL':
      return <SourceCard classification="BLACKWALL LEVEL-4" recordId="CONTAINMENT PROTOCOL // VLAN-902" totalFrames={totalFrames} />;

    case 'FERN_FINAL_A':
    case 'FERN_FINAL_B':
      return (
        <QuoteCard
          speaker="THE ARCHITECTURAL CONCLUSION"
          role="EPILOGUE"
          quote="The important question is no longer whether AI can answer the question. It's how much of the work we're willing to let it do after we stop asking."
          totalFrames={totalFrames}
        />
      );

    default:
      return <Video src={staticFile('video/fern_datacenter.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;
  }
}

function renderSourceBadge(sentId: string, durationFrames: number) {
  if (sentId === 's01' || sentId === 's05') {
    return <SourceBadge sourceText="SOURCE: OpenAI Agents SDK" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 's07' || sentId === 's10') {
    return <SourceBadge sourceText="SOURCE: Technical Architecture Framework" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 's13' || sentId === 's14') {
    return <SourceBadge sourceText="SOURCE: Sandboxed Execution Logs" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 's16' || sentId === 's17') {
    return <SourceBadge sourceText="SOURCE: Google Cloud AI Business Trends 2026" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 's20' || sentId === 's21') {
    return <SourceBadge sourceText="SOURCE: Instrumental Convergence (Bostrom)" frame={0} totalFrames={durationFrames} />;
  }
  return null;
}
