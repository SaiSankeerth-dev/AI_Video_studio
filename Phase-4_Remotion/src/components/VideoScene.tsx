import React from 'react';
import { useCurrentFrame, staticFile, Video } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface VideoSceneProps {
  videoSrc: string;
  totalFrames: number;
}

export const VideoScene: React.FC<VideoSceneProps> = ({ videoSrc, totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 15), fadeOut(frame, totalFrames, 15));

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        position: 'relative',
        overflow: 'hidden',
        opacity,
      }}
    >
      {/* Explicitly muted to prevent duplicate audio conflict */}
      <Video
        src={staticFile(videoSrc)}
        muted
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at center, transparent 50%, rgba(7,7,7,0.7) 100%)',
          pointerEvents: 'none',
        }}
      />
    </div>
  );
};
