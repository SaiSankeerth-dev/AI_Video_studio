import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface EntityCardProps {
  name: string;
  role: string;
  organization: string;
  keyAction: string;
  totalFrames?: number;
}

export const EntityCard: React.FC<EntityCardProps> = ({
  name,
  role,
  organization,
  keyAction,
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
      <div
        style={{
          width: '100%',
          maxWidth: 900,
          backgroundColor: theme.surface,
          border: `1px solid ${theme.cyan}`,
          borderRadius: 8,
          padding: 40,
          boxShadow: '0 20px 50px rgba(0, 240, 255, 0.08)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <span style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.cyan, letterSpacing: '0.2em' }}>
            DOSSIER & IDENTITY PROFILE
          </span>
          <span style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.muted }}>
            AUTHENTICATED SUBJECT
          </span>
        </div>

        <div style={{ fontFamily: theme.fontFamily, fontSize: 38, fontWeight: 800, color: theme.foreground, marginBottom: 6 }}>
          {name}
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 20, color: theme.cyan, marginBottom: 24 }}>
          {role} • {organization}
        </div>

        <div style={{ borderTop: `1px solid ${theme.surfaceBorder}`, paddingTop: 20 }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.muted }}>RELEVANCE TO INVESTIGATION</div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 18, color: theme.foreground, marginTop: 6, lineHeight: 1.4 }}>
            {keyAction}
          </div>
        </div>
      </div>
    </div>
  );
};
