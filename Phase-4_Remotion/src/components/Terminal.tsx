import React from 'react';
import { useCurrentFrame, staticFile, Audio } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface TerminalProps {
  title?: string;
  lines: string[];
  totalFrames: number;
}

export const Terminal: React.FC<TerminalProps> = ({
  title = "NEXUS // ATLAS DIAGNOSTICS CONSOLE",
  lines,
  totalFrames
}) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 10), fadeOut(frame, totalFrames, 10));

  // Typing speed: 1 line every 20 frames
  const visibleLineCount = Math.min(Math.floor(frame / 20) + 1, lines.length);

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '60px',
        opacity,
        position: 'relative',
      }}
    >
      {frame % 20 === 0 && frame < lines.length * 20 && (
        <Audio src={staticFile('audio/terminal-beep.wav')} volume={0.3} />
      )}
      <div
        style={{
          width: 1400,
          backgroundColor: theme.surface,
          border: `1px solid ${theme.surfaceBorder}`,
          borderRadius: 12,
          overflow: 'hidden',
          boxShadow: '0 20px 60px rgba(0,0,0,0.9)',
        }}
      >
        {/* Terminal Header */}
        <div
          style={{
            backgroundColor: '#181818',
            padding: '16px 24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: `1px solid ${theme.surfaceBorder}`,
          }}
        >
          <div style={{ display: 'flex', gap: 10 }}>
            <div style={{ width: 14, height: 14, borderRadius: '50%', backgroundColor: theme.danger }} />
            <div style={{ width: 14, height: 14, borderRadius: '50%', backgroundColor: theme.terminalAmber }} />
            <div style={{ width: 14, height: 14, borderRadius: '50%', backgroundColor: theme.terminalGreen }} />
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 18, color: theme.muted, fontWeight: 600 }}>
            {title}
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: theme.cyan }}>
            STATUS: ACTIVE
          </div>
        </div>

        {/* Terminal Body */}
        <div
          style={{
            padding: '36px 40px',
            minHeight: 480,
            fontFamily: theme.monoFontFamily,
            fontSize: 26,
            lineHeight: 1.7,
            color: theme.terminalGreen,
          }}
        >
          {lines.slice(0, visibleLineCount).map((line, idx) => (
            <div key={idx} style={{ marginBottom: 12 }}>
              <span style={{ color: theme.mutedDark, marginRight: 16 }}>{`0${idx + 1}`.slice(-2)}</span>
              <span>{line}</span>
            </div>
          ))}
          {/* Blinking Cursor */}
          <span
            style={{
              display: 'inline-block',
              width: 14,
              height: 26,
              backgroundColor: frame % 30 < 15 ? theme.terminalGreen : 'transparent',
              verticalAlign: 'middle',
              marginLeft: 8,
            }}
          />
        </div>
      </div>
    </div>
  );
};
