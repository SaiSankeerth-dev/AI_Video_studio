import React from 'react';
import { Sequence, staticFile, Audio, Video, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { AgentLoop } from '../components/scenes/AgentLoop';
import { ArchitectureDiagram } from '../components/scenes/ArchitectureDiagram';
import { ToolExecution } from '../components/scenes/ToolExecution';
import { CompanyMap } from '../components/scenes/CompanyMap';
import { QuoteCard } from '../components/QuoteCard';
import { SourceBadge } from '../components/shared/SourceBadge';
import { Caption } from '../components/Caption';

export const Benchmark60s: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ flex: 1, backgroundColor: theme.background, position: 'relative' }}>
      {/* Primary Voiceover & Ducked Ambience */}
      <Audio src={staticFile('audio/benchmark_60s.mp3')} volume={1.0} />
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.06} loop />

      {/* Segment 1: 0-10s (0-300 frames) — The Paradigm Shift */}
      <Sequence from={0} durationInFrames={300}>
        <Video src={staticFile('video/hidden-connection-01.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        <SourceBadge sourceText="SOURCE: OpenAI Agents SDK 2026" frame={frame} totalFrames={300} />
        <Caption text="For years, AI waited for us to ask a question. Now, we give systems a goal, and they act." frame={frame} totalFrames={300} />
      </Sequence>

      {/* Segment 2: 10-20s (300-600 frames) — The Agent Loop */}
      <Sequence from={300} durationInFrames={300}>
        <AgentLoop totalFrames={300} />
        <SourceBadge sourceText="SOURCE: DeepLearning.AI Agentic Workflows" frame={frame - 300} totalFrames={300} />
        <Caption text="An agent operates in a continuous loop: Goal, Plan, Act, Observe, and Replan." frame={frame - 300} totalFrames={300} />
      </Sequence>

      {/* Segment 3: 20-30s (600-900 frames) — Five Pillars of Architecture */}
      <Sequence from={600} durationInFrames={300}>
        <ArchitectureDiagram totalFrames={300} />
        <SourceBadge sourceText="SOURCE: Technical Architecture Framework" frame={frame - 600} totalFrames={300} />
        <Caption text="Five core pillars transform a static model into an autonomous digital worker." frame={frame - 600} totalFrames={300} />
      </Sequence>

      {/* Segment 4: 30-40s (900-1200 frames) — Live Coding Tool Execution */}
      <Sequence from={900} durationInFrames={300}>
        <ToolExecution totalFrames={300} />
        <SourceBadge sourceText="SOURCE: Sandboxed Execution Logs" frame={frame - 900} totalFrames={300} />
        <Caption text="When a test fails, the agent inspects the error, self-corrects, and iterates until it passes." frame={frame - 900} totalFrames={300} />
      </Sequence>

      {/* Segment 5: 40-50s (1200-1500 frames) — Multi-Agent Enterprise Swarm */}
      <Sequence from={1200} durationInFrames={300}>
        <CompanyMap totalFrames={300} />
        <SourceBadge sourceText="SOURCE: Google Cloud AI Business Trends 2026" frame={frame - 1200} totalFrames={300} />
        <Caption text="Specialized swarms coordinate across research, coding, security, and deployment." frame={frame - 1200} totalFrames={300} />
      </Sequence>

      {/* Segment 6: 50-60s (1500-1800 frames) — The Control Question */}
      <Sequence from={1500} durationInFrames={300}>
        <QuoteCard
          speaker="THE CONTROL QUESTION"
          role="DOCUMENTARY CONCLUSION"
          quote="The question is no longer whether AI can answer the question—it is how much work we are willing to let it do after we stop asking."
          totalFrames={300}
        />
        <Caption text="How much authority are we prepared to delegate to autonomous software?" frame={frame - 1500} totalFrames={300} />
      </Sequence>
    </div>
  );
};
