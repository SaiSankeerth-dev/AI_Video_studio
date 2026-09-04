import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface LocationCardProps {
  facilityName: string;
  subLocation: string;
  depthOrFloor: string;
  clearanceLevel: string;
  status: string;
  totalFrames?: number;
}

export const LocationCard: React.FC<LocationCardProps> = ({
  facilityName,
  subLocation,
  depthOrFloor,
  clearanceLevel,
  status,
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
          border: `1px solid ${theme.surfaceBorder}`,
          borderRadius: 8,
          padding: 40,
          boxShadow: '0 20px 50px rgba(0, 0, 0, 0.6)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <span style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.cyan, letterSpacing: '0.2em' }}>
            LOCATION TELEMETRY
          </span>
          <span
            style={{
              fontFamily: theme.monoFontFamily,
              fontSize: 13,
              color: theme.terminalGreen,
              border: `1px solid ${theme.terminalGreen}`,
              padding: '2px 8px',
              borderRadius: 3,
            }}
          >
            {status}
          </span>
        </div>

        <div style={{ fontFamily: theme.fontFamily, fontSize: 36, fontWeight: 800, color: theme.foreground, marginBottom: 8 }}>
          {facilityName}
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 20, color: theme.muted, marginBottom: 30 }}>
          {subLocation}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, borderTop: `1px solid ${theme.surfaceBorder}`, paddingTop: 20 }}>
          <div>
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.muted }}>DEPTH / ELEVATION</div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 18, fontWeight: 700, color: theme.foreground, marginTop: 4 }}>
              {depthOrFloor}
            </div>
          </div>
          <div>
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.muted }}>SECURITY PROTOCOL</div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 18, fontWeight: 700, color: theme.danger, marginTop: 4 }}>
              {clearanceLevel}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
