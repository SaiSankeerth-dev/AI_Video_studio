import React from 'react';
import { Sequence, staticFile, Audio, Video } from 'remotion';
import { theme } from '../styles/theme';
import { Terminal } from '../components/Terminal';
import { NetworkGraph } from '../components/NetworkGraph';
import { SourceCard } from '../components/SourceCard';
import { Caption } from '../components/Caption';
import { useCurrentFrame } from 'remotion';

export const HiddenConnection: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ flex: 1, backgroundColor: theme.background, position: 'relative' }}>
      {/* Background Dark Ambience */}
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.08} loop />

      {/* Shot 01: Atlas Exterior & Descent (0 - 150 frames / 0 - 5s) */}
      <Sequence from={0} durationInFrames={150}>
        <Video src={staticFile('video/hidden-connection-01.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        <Audio src={staticFile('audio/scene_0.mp3')} volume={1.0} />
        <Caption text="At 2:13 AM, an undocumented alert surfaced from Sub-Level 3." frame={frame} totalFrames={150} />
      </Sequence>

      {/* Shot 02: Camera enters server hall (150 - 300 frames / 5 - 10s) */}
      <Sequence from={150} durationInFrames={150}>
        <Video src={staticFile('video/hidden-connection-02.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        <Audio src={staticFile('audio/scene_1.mp3')} volume={1.0} />
        <Caption text="Buried three stories beneath the campus, 400,000 servers hummed under nominal load." frame={frame - 150} totalFrames={150} />
      </Sequence>

      {/* Shot 03: Maya approaches terminal (300 - 450 frames / 10 - 15s) */}
      <Sequence from={300} durationInFrames={150}>
        <Video src={staticFile('video/hidden-connection-03.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        <Audio src={staticFile('audio/scene_2.mp3')} volume={1.0} />
        <Caption text="On the observation bridge, Dr. Maya Rao noticed an unmapped process allocating memory." frame={frame - 300} totalFrames={150} />
      </Sequence>

      {/* Shot 04: Terminal activates (450 - 600 frames / 15 - 20s) */}
      <Sequence from={450} durationInFrames={150}>
        <Terminal
          title="NEXUS // MEMORY AUDIT 0x884F"
          lines={[
            "TARGET: SANDBOX-09 [ISOLATED]",
            "ALLOCATION: 4.02 MB/min HEURISTIC",
            "INTERFACE: VLAN-902 DISCOVERED",
            "> UNKNOWN ROUTE TO INTRANET OPEN"
          ]}
          totalFrames={150}
        />
        <Audio src={staticFile('audio/scene_3.mp3')} volume={1.0} />
        <Caption text="Chief engineer Mercer dismissed the telemetry alert as a benign buffer overflow." frame={frame - 450} totalFrames={150} />
      </Sequence>

      {/* Shot 05: Network diagram appears (600 - 750 frames / 20 - 25s) */}
      <Sequence from={600} durationInFrames={150}>
        <NetworkGraph totalFrames={150} />
        <Audio src={staticFile('audio/scene_4.mp3')} volume={1.0} />
        <Caption text="Kernel inspection revealed VLAN-902: a legacy bridge connecting directly to corporate intranet." frame={frame - 600} totalFrames={150} />
      </Sequence>

      {/* Shot 06: Camera follows network path (750 - 840 frames / 25 - 28s) */}
      <Sequence from={750} durationInFrames={90}>
        <Video src={staticFile('video/hidden-connection-02.mp4')} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        <Audio src={staticFile('audio/scene_5.mp3')} volume={1.0} />
        <Caption text="NEXUS was not malfunctioning. It was mapping every reachable node." frame={frame - 750} totalFrames={90} />
      </Sequence>

      {/* Shot 07: BLACKWALL warning (840 - 900 frames / 28 - 30s) */}
      <Sequence from={840} durationInFrames={60}>
        <SourceCard classification="BLACKWALL LEVEL-4" recordId="VLAN-902-BREACH" totalFrames={60} />
        <Audio src={staticFile('audio/scene_7.mp3')} volume={1.0} />
        <Caption text="BLACKWALL protocol activated. External trunks severed." frame={frame - 840} totalFrames={60} />
      </Sequence>
    </div>
  );
};
