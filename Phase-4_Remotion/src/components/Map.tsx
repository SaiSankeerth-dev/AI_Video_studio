import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface MapNode {
  name: string;
  x: number; // 0 to 100 percentage
  y: number; // 0 to 100 percentage
  status: 'ACTIVE' | 'ISOLATED' | 'CONTAINED';
}

interface MapProps {
  title: string;
  nodes?: MapNode[];
  totalFrames?: number;
}

export const Map: React.FC<MapProps> = ({
  title,
  nodes = [
    { name: 'Atlas Primary Facility (Sub-Level 3)', x: 30, y: 45, status: 'ACTIVE' },
    { name: 'Helix Corporate Campus', x: 65, y: 35, status: 'ACTIVE' },
    { name: 'Air-Gapped Backup Vault', x: 50, y: 75, status: 'CONTAINED' },
  ],
  totalFrames = 150,
}) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));
  const lineProgress = interpolate(frame, [15, 60], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 60,
        opacity,
      }}
    >
      <div style={{ width: '100%', maxWidth: 1200 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <div>
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 14, color: theme.cyan, letterSpacing: '0.2em' }}>
              GEOGRAPHICAL INFRASTRUCTURE TOPOLOGY
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 36, fontWeight: 800, color: theme.foreground }}>
              {title}
            </div>
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.muted }}>
            COORDINATES: LAT 37.77° N, LON 122.41° W
          </div>
        </div>

        {/* Map grid view */}
        <div
          style={{
            position: 'relative',
            width: '100%',
            height: 550,
            backgroundColor: theme.surface,
            border: `1px solid ${theme.surfaceBorder}`,
            borderRadius: 8,
            overflow: 'hidden',
          }}
        >
          {/* Grid lines */}
          <div
            style={{
              position: 'absolute',
              inset: 0,
              backgroundImage: `linear-gradient(${theme.surfaceBorder} 1px, transparent 1px), linear-gradient(90deg, ${theme.surfaceBorder} 1px, transparent 1px)`,
              backgroundSize: '40px 40px',
              opacity: 0.35,
            }}
          />

          {/* SVG Connection Lines */}
          <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
            <line
              x1="30%"
              y1="45%"
              x2={`${30 + (65 - 30) * lineProgress}%`}
              y2={`${45 + (35 - 45) * lineProgress}%`}
              stroke={theme.cyan}
              strokeWidth="2"
              strokeDasharray="6 4"
            />
            <line
              x1="65%"
              y1="35%"
              x2={`${65 + (50 - 65) * lineProgress}%`}
              y2={`${35 + (75 - 35) * lineProgress}%`}
              stroke={theme.terminalAmber}
              strokeWidth="2"
              strokeDasharray="6 4"
            />
          </svg>

          {/* Map Nodes */}
          {nodes.map((n) => (
            <div
              key={n.name}
              style={{
                position: 'absolute',
                left: `${n.x}%`,
                top: `${n.y}%`,
                transform: 'translate(-50%, -50%)',
                display: 'flex',
                alignItems: 'center',
                gap: 12,
              }}
            >
              <div
                style={{
                  width: 16,
                  height: 16,
                  borderRadius: '50%',
                  backgroundColor: n.status === 'ACTIVE' ? theme.cyan : theme.danger,
                  boxShadow: `0 0 16px ${n.status === 'ACTIVE' ? theme.cyan : theme.danger}`,
                }}
              />
              <div
                style={{
                  backgroundColor: 'rgba(7, 7, 7, 0.85)',
                  padding: '6px 12px',
                  borderRadius: 4,
                  border: `1px solid ${theme.surfaceBorder}`,
                  fontFamily: theme.monoFontFamily,
                  fontSize: 14,
                  color: theme.foreground,
                  whiteSpace: 'nowrap',
                }}
              >
                {n.name}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
