import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface SourceCardProps {
  classification: string;
  recordId: string;
  totalFrames: number;
}

export const SourceCard: React.FC<SourceCardProps> = ({ classification, recordId, totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

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
      }}
    >
      <div
        style={{
          border: `1px solid ${theme.danger}`,
          padding: '40px 80px',
          borderRadius: 8,
          textAlign: 'center',
          backgroundColor: 'rgba(255, 59, 48, 0.05)',
        }}
      >
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 18, color: theme.danger, letterSpacing: '0.3em' }}>
          OFFICIAL SECURITY INCIDENT RECORD
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 48, fontWeight: 800, color: theme.foreground, margin: '16px 0' }}>
          CLASSIFICATION: {classification}
        </div>
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 20, color: theme.muted }}>
          RECORD ID: {recordId}
        </div>
      </div>
    </div>
  );
};
