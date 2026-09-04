import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { theme } from '../../styles/theme';
import { fadeIn, fadeOut } from '../../lib/timeline';

interface CompanyMapProps {
  totalFrames: number;
}

export const CompanyMap: React.FC<CompanyMapProps> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

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
      }}
    >
      <div style={{ textAlign: 'center', marginBottom: 20 }}>
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 18, color: theme.cyan, letterSpacing: '0.25em' }}>
          ENTERPRISE AGENTIC SWARMS
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 44, fontWeight: 700, color: theme.foreground, marginTop: 8 }}>
          Multi-Agent Process Orchestration
        </div>
      </div>

      <svg width={1400} height={520} viewBox="0 0 1400 520" style={{ overflow: 'visible' }}>
        {/* Central Orchestrator */}
        <rect x={550} y={40} width={300} height={100} rx={12} fill={theme.surface} stroke={theme.cyan} strokeWidth={2} />
        <text x={700} y={85} fill={theme.cyan} fontFamily={theme.monoFontFamily} fontSize={16} fontWeight={700} textAnchor="middle">
          CENTRAL ORCHESTRATOR
        </text>
        <text x={700} y={115} fill={theme.foreground} fontFamily={theme.fontFamily} fontSize={18} fontWeight={600} textAnchor="middle">
          Goal Decomposition Engine
        </text>

        {/* Worker Agents */}
        {[
          { name: "RESEARCH AGENT", desc: "Knowledge Retrieval", x: 100, y: 320, color: theme.terminalAmber },
          { name: "CODING AGENT", desc: "Sandbox Implementation", x: 380, y: 320, color: theme.terminalGreen },
          { name: "SECURITY AGENT", desc: "Permission Boundary Audit", x: 660, y: 320, color: theme.danger },
          { name: "DEPLOYMENT AGENT", desc: "CI/CD & Metric Monitor", x: 940, y: 320, color: theme.cyan },
          { name: "SUPPORT AGENT", desc: "User Interaction & Triage", x: 1220, y: 320, color: theme.foreground }
        ].map((ag, idx) => (
          <React.Fragment key={idx}>
            {/* Connection Line */}
            <line x1={700} y1={140} x2={ag.x + 80} y2={ag.y} stroke={ag.color} strokeWidth={2} strokeDasharray="6 4" />
            <circle cx={ag.x + 80} cy={ag.y} r={6 * pulse} fill={ag.color} />

            {/* Agent Node Box */}
            <rect x={ag.x - 40} y={ag.y} width={240} height={100} rx={10} fill={theme.surface} stroke={ag.color} strokeWidth={1.5} />
            <text x={ag.x + 80} y={ag.y + 40} fill={ag.color} fontFamily={theme.monoFontFamily} fontSize={15} fontWeight={700} textAnchor="middle">
              {ag.name}
            </text>
            <text x={ag.x + 80} y={ag.y + 70} fill={theme.muted} fontFamily={theme.fontFamily} fontSize={14} textAnchor="middle">
              {ag.desc}
            </text>
          </React.Fragment>
        ))}
      </svg>
    </div>
  );
};
