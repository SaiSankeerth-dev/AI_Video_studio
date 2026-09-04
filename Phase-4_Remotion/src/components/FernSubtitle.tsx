import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';

interface FernSubtitleProps {
  text: string;
  totalFrames: number;
}

export const FernSubtitle: React.FC<FernSubtitleProps> = ({ text, totalFrames }) => {
  const frame = useCurrentFrame();

  if (!text) return null;

  // Smooth cinematic cross-dissolve (6 frames in, 6 frames out)
  const opacity = interpolate(
    frame,
    [0, 6, totalFrames - 6, totalFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const translateY = interpolate(
    frame,
    [0, 6, totalFrames - 6, totalFrames],
    [6, 0, 0, -4],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 75,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 100px',
        opacity,
        transform: `translateY(${translateY}px)`,
        zIndex: 100,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          background: 'rgba(6, 6, 10, 0.78)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(255, 255, 255, 0.12)',
          borderRadius: 10,
          padding: '14px 32px',
          maxWidth: 1350,
          textAlign: 'center',
          boxShadow: '0 8px 30px rgba(0,0,0,0.85)',
        }}
      >
        <span
          style={{
            fontFamily: theme.fontFamily,
            fontSize: 32,
            fontWeight: 500,
            color: '#FFFFFF',
            lineHeight: 1.45,
            letterSpacing: '-0.01em',
            textShadow: '0 2px 8px rgba(0,0,0,0.9)',
          }}
        >
          {text}
        </span>
      </div>
    </div>
  );
};
