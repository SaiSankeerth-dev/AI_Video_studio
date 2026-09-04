import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface EvidenceCardProps {
  claimId: string;
  statement: string;
  sourceTitle: string;
  confidence: string;
  totalFrames?: number;
}

export const EvidenceCard: React.FC<EvidenceCardProps> = ({
  claimId,
  statement,
  sourceTitle,
  confidence,
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
        justifyContent: 'center',
        alignItems: 'center',
        padding: '60px 100px',
        opacity,
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: 1100,
          backgroundColor: theme.surface,
          border: `1px solid ${theme.cyan}`,
          borderRadius: 12,
          padding: 48,
          boxShadow: '0 20px 50px rgba(0, 240, 255, 0.08)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span
              style={{
                fontFamily: theme.monoFontFamily,
                fontSize: 16,
                padding: '6px 14px',
                borderRadius: 4,
                backgroundColor: 'rgba(0, 240, 255, 0.15)',
                color: theme.cyan,
                letterSpacing: '0.15em',
              }}
            >
              CLAIM {claimId}
            </span>
            <span
              style={{
                fontFamily: theme.monoFontFamily,
                fontSize: 14,
                color: theme.terminalGreen,
                border: `1px solid ${theme.terminalGreen}`,
                padding: '4px 10px',
                borderRadius: 4,
              }}
            >
              CONFIDENCE: {confidence.toUpperCase()}
            </span>
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 14, color: theme.muted }}>
            FORENSIC RESEARCH ARCHIVE
          </div>
        </div>

        <div
          style={{
            fontFamily: theme.fontFamily,
            fontSize: 32,
            fontWeight: 700,
            lineHeight: 1.35,
            color: theme.foreground,
            marginBottom: 32,
          }}
        >
          "{statement}"
        </div>

        <div
          style={{
            borderTop: `1px solid ${theme.surfaceBorder}`,
            paddingTop: 20,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: theme.cyan }}>
            SOURCE: {sourceTitle}
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.mutedDark }}>
            AUTHENTICATED CITATION
          </div>
        </div>
      </div>
    </div>
  );
};
