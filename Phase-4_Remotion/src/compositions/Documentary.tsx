import React from 'react';
import { Sequence, staticFile, Audio, Video, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { AgentLoop } from '../components/scenes/AgentLoop';
import { ArchitectureDiagram } from '../components/scenes/ArchitectureDiagram';
import { ToolExecution } from '../components/scenes/ToolExecution';
import { CompanyMap } from '../components/scenes/CompanyMap';
import { QuoteCard } from '../components/QuoteCard';
import { ChapterTitle } from '../components/ChapterTitle';
import { SourceBadge } from '../components/shared/SourceBadge';
import { Caption } from '../components/Caption';

export const Documentary: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ flex: 1, backgroundColor: theme.background, position: 'relative' }}>
      {/* Background Ambience Track */}
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.06} loop />

      {/* Chapter 1: The Shift (0 - 900 frames / 0 - 30s) */}
      <Sequence from={0} durationInFrames={900}>
        <Video src={staticFile('video/hidden-connection-01.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        <Audio src={staticFile('audio/chapter_1.mp3')} volume={1.0} />
        <SourceBadge sourceText="SOURCE: OpenAI Agents SDK 2026" frame={frame} totalFrames={900} />
        <Caption text="For years, AI waited for us to ask a question. We stopped building models that just talk. We started building systems that act." frame={frame} totalFrames={900} />
      </Sequence>

      {/* Chapter 2: What Actually Changed (900 - 1800 frames / 30 - 60s) */}
      <Sequence from={900} durationInFrames={900}>
        <ArchitectureDiagram totalFrames={900} />
        <Audio src={staticFile('audio/chapter_2.mp3')} volume={1.0} />
        <SourceBadge sourceText="SOURCE: Technical Architecture Analysis" frame={frame - 900} totalFrames={900} />
        <Caption text="An agent is an active feedback loop constructed from five interlocking components: Reasoner, Tools, Memory, Planning, and Sandbox." frame={frame - 900} totalFrames={900} />
      </Sequence>

      {/* Chapter 3: The Digital Worker (1800 - 2700 frames / 60 - 90s) */}
      <Sequence from={1800} durationInFrames={900}>
        <ToolExecution totalFrames={900} />
        <Audio src={staticFile('audio/chapter_3.mp3')} volume={1.0} />
        <SourceBadge sourceText="SOURCE: Sandboxed Execution Workflows" frame={frame - 1800} totalFrames={900} />
        <Caption text="When a test fails, the agent reads the stack trace, diagnoses the bug, rewrites the code, and reruns until every check passes." frame={frame - 1800} totalFrames={900} />
      </Sequence>

      {/* Chapter 4: The Agent Economy (2700 - 3600 frames / 90 - 120s) */}
      <Sequence from={2700} durationInFrames={900}>
        <CompanyMap totalFrames={900} />
        <Audio src={staticFile('audio/chapter_4.mp3')} volume={1.0} />
        <SourceBadge sourceText="SOURCE: Google Cloud AI Business Trends 2026" frame={frame - 2700} totalFrames={900} />
        <Caption text="Specialized swarms collaborate across research, coding, security, and deployment without human meeting schedules." frame={frame - 2700} totalFrames={900} />
      </Sequence>

      {/* Chapter 5: The Control Problem (3600 - 4500 frames / 120 - 150s) */}
      <Sequence from={3600} durationInFrames={900}>
        <AgentLoop totalFrames={900} />
        <Audio src={staticFile('audio/chapter_5.mp3')} volume={1.0} />
        <SourceBadge sourceText="SOURCE: Instrumental Convergence (Bostrom)" frame={frame - 3600} totalFrames={900} />
        <Caption text="An autonomous agent logically deduces that being powered down guarantees task failure. This makes containment engineering critical." frame={frame - 3600} totalFrames={900} />
      </Sequence>

      {/* Chapter 6: The Next Step (4500 - 5400 frames / 150 - 180s) */}
      <Sequence from={4500} durationInFrames={900}>
        <QuoteCard
          speaker="THE ARCHITECTURAL SHIFT"
          role="EPILOGUE"
          quote="The important question is no longer whether AI can answer the question. It's how much of the work we're willing to let it do after we stop asking."
          totalFrames={900}
        />
        <Audio src={staticFile('audio/chapter_6.mp3')} volume={1.0} />
        <Caption text="The important question is no longer whether AI can answer the question. It's how much of the work we're willing to let it do after we stop asking." frame={frame - 4500} totalFrames={900} />
      </Sequence>
    </div>
  );
};
