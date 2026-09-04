import React from 'react';
import { interpolate, useCurrentFrame, staticFile, Audio } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface ChapterTitleProps {
  chapterNumber: number;
  title: string;
  totalFrames: number;
}

export const ChapterTitle: React.FC<ChapterTitleProps> = ({ chapterNumber, title, totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 15), fadeOut(frame, totalFrames, 15));
  const scale = interpolate(frame, [0, totalFrames], [0.98, 1.02]);

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        opacity,
        transform: `scale(${scale})`,
        position: 'relative',
      }}
    >
      {frame === 1 && <Audio src={staticFile('audio/whoosh.wav')} volume={0.5} />}
      <div
        style={{
          fontFamily: theme.monoFontFamily,
          fontSize: 26,
          fontWeight: 700,
          color: theme.accent,
          letterSpacing: '0.3em',
          textTransform: 'uppercase',
          marginBottom: 20,
        }}
      >
        ACT 0{chapterNumber} // CHAPTER 0{chapterNumber}
      </div>
      <div
        style={{
          fontFamily: theme.fontFamily,
          fontSize: 76,
          fontWeight: 800,
          color: theme.foreground,
          letterSpacing: '-0.02em',
          textAlign: 'center',
          maxWidth: 1400,
          textShadow: '0 4px 20px rgba(0,0,0,0.8)',
        }}
      >
        {title}
      </div>
      <div
        style={{
          width: 160,
          height: 3,
          backgroundColor: theme.accent,
          marginTop: 32,
          borderRadius: 2,
        }}
      />
    </div>
  );
};
