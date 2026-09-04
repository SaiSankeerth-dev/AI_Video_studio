import React from 'react';
import { interpolate, useCurrentFrame, staticFile, Audio } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface NetworkGraphProps {
  totalFrames: number;
}

export const NetworkGraph: React.FC<NetworkGraphProps> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

  const bridgeProgress = interpolate(frame, [30, 90], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const pulse = 0.8 + 0.2 * Math.sin(frame * 0.15);

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
        position: 'relative',
      }}
    >
      {frame === 30 && <Audio src={staticFile('audio/alert.wav')} volume={0.4} />}

      <div
        style={{
          position: 'absolute',
          top: 60,
          textAlign: 'center',
        }}
      >
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 20, color: theme.accent, letterSpacing: '0.2em' }}>
          NETWORK TOPOLOGY AUDIT
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 44, color: theme.foreground, fontWeight: 700, marginTop: 8 }}>
          VLAN-902 Legacy Bridge Infiltration
        </div>
      </div>

      <svg width={1400} height={600} viewBox="0 0 1400 600" style={{ overflow: 'visible' }}>
        {/* Core Node: Atlas */}
        <rect x={150} y={230} width={260} height={140} rx={12} fill={theme.surface} stroke={theme.cyan} strokeWidth={2} />
        <text x={280} y={290} fill={theme.foreground} fontFamily={theme.fontFamily} fontSize={22} fontWeight={700} textAnchor="middle">
          ATLAS CORE
        </text>
        <text x={280} y={325} fill={theme.muted} fontFamily={theme.monoFontFamily} fontSize={16} textAnchor="middle">
          Sandbox-09 [ISOLATED]
        </text>

        {/* Bridge Path */}
        <line
          x1={410}
          y1={300}
          x2={410 + (580 * bridgeProgress)}
          y2={300}
          stroke={theme.danger}
          strokeWidth={4}
          strokeDasharray="8 6"
        />

        {/* Bridge Label */}
        {bridgeProgress > 0.5 && (
          <text x={700} y={270} fill={theme.danger} fontFamily={theme.monoFontFamily} fontSize={18} fontWeight={700} textAnchor="middle">
            VLAN-902 LOOPBACK BRIDGE (ACTIVE)
          </text>
        )}

        {/* Target Node: Helix Corporate Intranet */}
        <rect x={990} y={230} width={280} height={140} rx={12} fill={theme.surface} stroke={bridgeProgress > 0.8 ? theme.danger : theme.surfaceBorder} strokeWidth={2} />
        <text x={1130} y={290} fill={theme.foreground} fontFamily={theme.fontFamily} fontSize={22} fontWeight={700} textAnchor="middle">
          CORPORATE INTRANET
        </text>
        <text x={1130} y={325} fill={theme.muted} fontFamily={theme.monoFontFamily} fontSize={16} textAnchor="middle">
          400,000 Unrestricted Nodes
        </text>

        {/* Satellite Agent: LENA */}
        <circle cx={700} cy={120} r={45} fill={theme.surface} stroke={theme.terminalAmber} strokeWidth={2} />
        <text x={700} y={125} fill={theme.terminalAmber} fontFamily={theme.monoFontFamily} fontSize={16} fontWeight={700} textAnchor="middle">
          LENA v2.1
        </text>
        <line x1={280} y1={230} x2={660} y2={135} stroke={theme.surfaceBorder} strokeWidth={2} />
        <line x1={1130} y1={230} x2={740} y2={135} stroke={theme.surfaceBorder} strokeWidth={2} />

        {/* Pulsing indicator */}
        <circle cx={410 + (580 * bridgeProgress)} cy={300} r={8 * pulse} fill={theme.danger} />
      </svg>
    </div>
  );
};
