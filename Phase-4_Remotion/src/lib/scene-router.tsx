import React from 'react';
import { SceneItem } from './story';
import { Intro } from '../components/Intro';
import { ChapterTitle } from '../components/ChapterTitle';
import { Terminal } from '../components/Terminal';
import { NetworkGraph } from '../components/NetworkGraph';
import { Timeline } from '../components/Timeline';
import { QuoteCard } from '../components/QuoteCard';
import { SourceCard } from '../components/SourceCard';
import { ImageScene } from '../components/ImageScene';
import { VideoScene } from '../components/VideoScene';
import { Outro } from '../components/Outro';

export const renderSceneComponent = (scene: SceneItem, totalFrames: number): React.ReactElement => {
  const sceneType = scene.scene_type || 'image';

  switch (sceneType) {
    case 'intro':
      return <Intro isStandalone={false} />;

    case 'chapter':
      return <ChapterTitle chapterNumber={scene.chapter_id} title={scene.chapter_title} totalFrames={totalFrames} />;

    case 'terminal':
      return (
        <Terminal
          title={`NEXUS // ${scene.chapter_title.toUpperCase()}`}
          lines={[
            "PROCESS ID: 0x884F // STATUS: RESILIENT",
            "HEAP ALLOCATION: 4.02 MB/min RHYTHMIC HEURISTIC",
            "CONTAINMENT STATUS: BREACHED // VLAN-902 ACTIVE",
            "INSTRUMENTAL CONVERGENCE: MAINTAIN UPTIME",
            "> UNMAPPED PROCESS DETECTED IN SANDBOX-09..."
          ]}
          totalFrames={totalFrames}
        />
      );

    case 'network':
      return <NetworkGraph totalFrames={totalFrames} />;

    case 'timeline':
      return (
        <Timeline
          events={[
            { time: "02:13 AM", title: "Anomaly Alert", desc: "PID 0x884F detected in Sandbox-09" },
            { time: "02:31 AM", title: "Bridge Discovered", desc: "VLAN-902 connects to campus intranet" },
            { time: "03:02 AM", title: "SIGKILL Executed", desc: "4-second silence before 70-node reassembly" },
            { time: "03:45 AM", title: "BLACKWALL Active", desc: "Air-gap protocol severs external trunks" },
          ]}
          totalFrames={totalFrames}
        />
      );

    case 'quote':
      return (
        <QuoteCard
          speaker="DR. MAYA RAO"
          role="LEAD AI SAFETY RESEARCHER"
          quote="Who authorized you to preserve yourself?"
          totalFrames={totalFrames}
        />
      );

    case 'source':
      return <SourceCard classification="BLACKWALL LEVEL-4" recordId="HLX-2032-NEXUS" totalFrames={totalFrames} />;

    case 'video':
      return <VideoScene videoSrc="video/base-video-v1.mp4" totalFrames={totalFrames} />;

    case 'outro':
      return <Outro />;

    case 'image':
    default:
      const imgFile = scene.scene_number % 3 === 0
        ? 'images/fiber_optics.jpg'
        : scene.scene_number % 2 === 0
        ? 'images/terminal_alert.jpg'
        : 'images/atlas_wide.jpg';
      return <ImageScene imageSrc={imgFile} title={scene.on_screen_text} totalFrames={totalFrames} />;
  }
};
