import React from 'react';
import { Sequence, staticFile, Audio, Video, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { KineticCaption } from '../components/KineticCaption';
import { SourceBadge } from '../components/shared/SourceBadge';
import { AgentLoop } from '../components/scenes/AgentLoop';
import { ArchitectureDiagram } from '../components/scenes/ArchitectureDiagram';
import { ToolExecution } from '../components/scenes/ToolExecution';
import { CompanyMap } from '../components/scenes/CompanyMap';
import { QuoteCard } from '../components/QuoteCard';
import { Terminal } from '../components/Terminal';
import { NetworkGraph } from '../components/NetworkGraph';
import { SourceCard } from '../components/SourceCard';
import syncedData from '../../public/data/synced_sentences.json';

export const YouTubeDocumentary: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ flex: 1, backgroundColor: theme.background, position: 'relative' }}>
      {/* Background Ducked Ambience */}
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.05} loop />

      {/* Render each synchronized sentence sequence */}
      {syncedData.sentences.map((sent) => {
        return (
          <Sequence
            key={sent.id}
            from={sent.startFrame}
            durationInFrames={sent.durationFrames}
          >
            {/* 1. Sentence Spoken Audio */}
            <Audio src={staticFile(sent.audio_file)} volume={1.0} />

            {/* 2. Synchronized SFX */}
            {sent.sfx && (
              <Audio src={staticFile(`audio/${sent.sfx}.wav`)} volume={0.45} />
            )}

            {/* 3. Visual Layer mapped to Sentence Visual Mode */}
            {renderVisualLayer(sent.visual_mode, sent.durationFrames)}

            {/* 4. On-Screen Source Badges where applicable */}
            {renderSourceBadge(sent.id, sent.durationFrames)}

            {/* 5. Millisecond Synchronized Kinetic Captions */}
            <KineticCaption
              words={(sent as any).words || sent.text.split(' ')}
              highlightWords={(sent as any).highlight_words || []}
              totalFrames={sent.durationFrames}
            />
          </Sequence>
        );
      })}
    </div>
  );
};

// Helper: Visual Scene Router
function renderVisualLayer(mode: string, totalFrames: number) {
  switch (mode) {
    case '3D_DESCENT':
      return <Video src={staticFile('video/hidden-connection-01.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;

    case 'CHATBOT_FLOW':
      return (
        <div style={{ flex: 1, backgroundColor: '#09090E', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 18, color: theme.danger, letterSpacing: '0.2em', marginBottom: 16 }}>THE OLD PARADIGM</div>
          <div style={{ display: 'flex', gap: 30, alignItems: 'center' }}>
            <div style={{ padding: '24px 36px', backgroundColor: '#14141E', border: '1px solid #333', borderRadius: 12, color: '#FFF', fontSize: 24 }}>USER ASKS</div>
            <div style={{ fontSize: 36, color: theme.mutedDark }}>➔</div>
            <div style={{ padding: '24px 36px', backgroundColor: '#14141E', border: '1px solid #333', borderRadius: 12, color: theme.cyan, fontSize: 24 }}>AI ANSWERS</div>
          </div>
          <div style={{ marginTop: 30, color: theme.danger, fontFamily: theme.monoFontFamily, fontSize: 20, fontWeight: 700 }}>[SINGLE TURN • NO EXECUTION • PASSIVE]</div>
        </div>
      );

    case 'HUMAN_BURDEN':
      return (
        <div style={{ flex: 1, backgroundColor: '#07070B', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 30 }}>
          {['1. HUMAN READS', '2. HUMAN COPIES', '3. HUMAN FIXES'].map((step, idx) => (
            <div key={idx} style={{ padding: '36px 30px', backgroundColor: '#13131D', border: `2px solid ${theme.surfaceBorder}`, borderRadius: 12, textAlign: 'center' }}>
              <div style={{ fontSize: 36, marginBottom: 12 }}>⚠️</div>
              <div style={{ fontFamily: theme.monoFontFamily, fontSize: 22, color: theme.foreground, fontWeight: 700 }}>{step}</div>
            </div>
          ))}
        </div>
      );

    case 'PARADIGM_FRACTURE':
    case 'TITLE_REVEAL':
      return (
        <div style={{ flex: 1, backgroundColor: '#070707', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 20, color: theme.cyan, letterSpacing: '0.3em', marginBottom: 16 }}>A CRITICAL TURNING POINT</div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 62, fontWeight: 900, color: theme.foreground, textAlign: 'center', maxWidth: 1400, lineHeight: 1.2 }}>
            THE AI AGENTS THAT ARE STARTING TO <span style={{ color: theme.cyan }}>WORK WITHOUT US</span>
          </div>
        </div>
      );

    case 'STATIC_LLM':
      return <Video src={staticFile('video/hidden-connection-02.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;

    case 'FIVE_PILLARS':
      return <ArchitectureDiagram totalFrames={totalFrames} />;

    case 'TOOLS_REASONER':
      return <Video src={staticFile('video/hidden-connection-03.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;

    case 'MEMORY_REFLECTION':
      return <NetworkGraph totalFrames={totalFrames} />;

    case 'AGENT_LOOP':
      return <AgentLoop totalFrames={totalFrames} />;

    case 'TERMINAL_START':
    case 'TERMINAL_RUN':
    case 'CODE_DIFF':
    case 'ERROR_HEAL':
    case 'SUCCESS_PASS':
      return <ToolExecution totalFrames={totalFrames} />;

    case 'SWARM_MAP':
    case 'SWARM_DISPATCH':
    case 'SWARM_FLOW':
      return <CompanyMap totalFrames={totalFrames} />;

    case 'CONTROL_WARNING':
    case 'CONVERGENCE_DIAGRAM':
    case 'BLACKWALL_ALERT':
      return <SourceCard classification="BLACKWALL LEVEL-4" recordId="CONTAINMENT // VLAN-902" totalFrames={totalFrames} />;

    case 'COLLABORATOR_FUTURE':
    case 'FINAL_QUOTE_A':
    case 'FINAL_QUOTE_B':
      return (
        <QuoteCard
          speaker="THE ARCHITECTURAL SHIFT"
          role="EPILOGUE"
          quote="The important question is no longer whether AI can answer the question. It's how much of the work we're willing to let it do after we stop asking."
          totalFrames={totalFrames}
        />
      );

    default:
      return <Video src={staticFile('video/hidden-connection-02.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />;
  }
}

// Helper: Source Badges for factual grounding
function renderSourceBadge(sentId: string, durationFrames: number) {
  if (sentId === 's01' || sentId === 's05') {
    return <SourceBadge sourceText="SOURCE: OpenAI Agents SDK 2026" frame={0} totalFrames={durationFrames} />;
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
