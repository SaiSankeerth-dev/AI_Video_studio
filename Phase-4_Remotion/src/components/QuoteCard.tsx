import React from 'react';
import { interpolate, useCurrentFrame, staticFile, Audio } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface QuoteCardProps {
  speaker: string;
  role: string;
  quote: string;
  totalFrames: number;
}

export const QuoteCard: React.FC<QuoteCardProps> = ({ speaker, role, quote, totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 15), fadeOut(frame, totalFrames, 15));
  const scale = interpolate(frame, [0, totalFrames], [0.99, 1.01]);

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 180px',
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      {frame === 1 && <Audio src={staticFile('audio/impact.wav')} volume={0.4} />}
      <div
        style={{
          width: '100%',
          maxWidth: 1300,
          backgroundColor: theme.surface,
          border: `1px solid ${theme.surfaceBorder}`,
          borderRadius: 16,
          padding: '60px 70px',
          position: 'relative',
          boxShadow: '0 25px 80px rgba(0,0,0,0.8)',
        }}
      >
        <div
          style={{
            fontFamily: theme.monoFontFamily,
            fontSize: 20,
            color: theme.accent,
            letterSpacing: '0.25em',
            textTransform: 'uppercase',
            marginBottom: 8,
          }}
        >
          {speaker} // {role}
        </div>
        <div
          style={{
            fontFamily: theme.fontFamily,
            fontSize: 46,
            fontWeight: 600,
            color: theme.foreground,
            lineHeight: 1.4,
            letterSpacing: '-0.01em',
            marginTop: 24,
          }}
        >
          "{quote}"
        </div>
      </div>
    </div>
  );
};
