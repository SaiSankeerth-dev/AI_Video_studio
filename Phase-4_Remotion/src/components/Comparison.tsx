import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface ComparisonProps {
  title: string;
  leftTitle: string;
  leftPoints: string[];
  rightTitle: string;
  rightPoints: string[];
  totalFrames?: number;
}

export const Comparison: React.FC<ComparisonProps> = ({
  title,
  leftTitle,
  leftPoints,
  rightTitle,
  rightPoints,
  totalFrames = 150,
}) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 10), fadeOut(frame, totalFrames, 10));

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '50px 80px',
        opacity,
      }}
    >
      <div style={{ width: '100%', maxWidth: 1200 }}>
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 14, color: theme.cyan, letterSpacing: '0.2em' }}>
            ARCHITECTURAL PARADIGM SHIFT
          </div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 40, fontWeight: 800, color: theme.foreground }}>
            {title}
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
          {/* Left Column (Weak / Legacy) */}
          <div
            style={{
              backgroundColor: theme.surface,
              border: `1px solid ${theme.surfaceBorder}`,
              borderRadius: 8,
              padding: 36,
            }}
          >
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: theme.muted, letterSpacing: '0.1em', marginBottom: 12 }}>
              LEGACY PARADIGM
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 28, fontWeight: 700, color: theme.muted, marginBottom: 24 }}>
              {leftTitle}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              {leftPoints.map((pt, i) => (
                <div key={i} style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                  <span style={{ color: theme.danger, fontWeight: 700 }}>✕</span>
                  <span style={{ fontFamily: theme.fontFamily, fontSize: 18, color: theme.muted }}>{pt}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column (Strong / Agentic) */}
          <div
            style={{
              backgroundColor: theme.surface,
              border: `1px solid ${theme.cyan}`,
              borderRadius: 8,
              padding: 36,
              boxShadow: '0 10px 40px rgba(0, 240, 255, 0.08)',
            }}
          >
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: theme.cyan, letterSpacing: '0.1em', marginBottom: 12 }}>
              AUTONOMOUS PARADIGM
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 28, fontWeight: 700, color: theme.foreground, marginBottom: 24 }}>
              {rightTitle}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              {rightPoints.map((pt, i) => (
                <div key={i} style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                  <span style={{ color: theme.terminalGreen, fontWeight: 700 }}>✓</span>
                  <span style={{ fontFamily: theme.fontFamily, fontSize: 18, color: theme.foreground }}>{pt}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
