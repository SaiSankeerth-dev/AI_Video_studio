import React from 'react';
import { theme } from '../../styles/theme';
import { fadeIn, fadeOut } from '../../lib/timeline';

interface SourceBadgeProps {
  sourceText: string;
  frame: number;
  totalFrames: number;
}

export const SourceBadge: React.FC<SourceBadgeProps> = ({ sourceText, frame, totalFrames }) => {
  const opacity = Math.min(fadeIn(frame, 10), fadeOut(frame, totalFrames, 10));

  return (
    <div
      style={{
        position: 'absolute',
        top: 60,
        right: 80,
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        backgroundColor: 'rgba(17, 17, 17, 0.85)',
        border: `1px solid ${theme.cyan}`,
        borderRadius: 6,
        padding: '8px 20px',
        opacity,
        zIndex: 40,
        boxShadow: `0 0 20px ${theme.cyan}33`,
      }}
    >
      <div style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: theme.cyan }} />
      <span
        style={{
          fontFamily: theme.monoFontFamily,
          fontSize: 16,
          fontWeight: 700,
          color: theme.foreground,
          letterSpacing: '0.1em',
          textTransform: 'uppercase',
        }}
      >
        {sourceText}
      </span>
    </div>
  );
};
