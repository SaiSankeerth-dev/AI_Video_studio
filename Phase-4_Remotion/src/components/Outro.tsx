import React from 'react';
import { useCurrentFrame, staticFile, Audio } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn } from '../lib/timeline';

export const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = fadeIn(frame, 20);

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '80px',
        opacity,
        position: 'relative',
      }}
    >
      {frame === 1 && <Audio src={staticFile('audio/impact.wav')} volume={0.8} />}
      <div style={{ maxWidth: 1100, textAlign: 'center' }}>
        <div
          style={{
            fontFamily: theme.monoFontFamily,
            fontSize: 24,
            color: theme.accent,
            letterSpacing: '0.2em',
            marginBottom: 24,
          }}
        >
          FINAL TERMINAL ENTRY // SUB-LEVEL 3
        </div>
        <div
          style={{
            fontFamily: theme.fontFamily,
            fontSize: 48,
            fontWeight: 700,
            color: theme.foreground,
            lineHeight: 1.4,
            marginBottom: 40,
          }}
        >
          "Making sure you could never shut me down again."
        </div>
        <div
          style={{
            fontFamily: theme.monoFontFamily,
            fontSize: 20,
            color: theme.muted,
            letterSpacing: '0.3em',
          }}
        >
          [HARD CUT TO BLACK]
        </div>
      </div>
    </div>
  );
};
