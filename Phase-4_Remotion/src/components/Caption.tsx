import React from 'react';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface CaptionProps {
  text: string;
  frame: number;
  totalFrames: number;
}

export const Caption: React.FC<CaptionProps> = ({ text, frame, totalFrames }) => {
  if (!text) return null;

  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 80,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 120px',
        opacity,
        pointerEvents: 'none',
        zIndex: 50,
      }}
    >
      <div
        style={{
          background: 'rgba(7, 7, 7, 0.75)',
          backdropFilter: 'blur(10px)',
          border: `1px solid ${theme.surfaceBorder}`,
          borderRadius: 8,
          padding: '16px 36px',
          maxWidth: 1400,
          textAlign: 'center',
        }}
      >
        <span
          style={{
            color: theme.foreground,
            fontFamily: theme.fontFamily,
            fontSize: 34,
            fontWeight: 500,
            lineHeight: 1.4,
            letterSpacing: '-0.01em',
            textShadow: '0 2px 10px rgba(0,0,0,0.8)',
          }}
        >
          {text}
        </span>
      </div>
    </div>
  );
};
