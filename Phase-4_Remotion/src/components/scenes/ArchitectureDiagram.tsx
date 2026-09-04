import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { theme } from '../../styles/theme';
import { fadeIn, fadeOut } from '../../lib/timeline';

interface ArchitectureDiagramProps {
  totalFrames: number;
}

export const ArchitectureDiagram: React.FC<ArchitectureDiagramProps> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

  const pillars = [
    { title: "CORE REASONER", desc: "Neural Foundation Model", icon: "🧠" },
    { title: "TOOL REGISTRY", desc: "Bash, Web, Files, APIs", icon: "⚡" },
    { title: "WORKING MEMORY", desc: "State & Transcript Buffer", icon: "💾" },
    { title: "SELF-REFLECTION", desc: "Error Diagnosis & ReAct", icon: "🔄" },
    { title: "SANDBOX CONTAINER", desc: "Linux cgroups & Namespaces", icon: "🛡️" }
  ];

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '60px',
        opacity,
      }}
    >
      <div style={{ textAlign: 'center', marginBottom: 40 }}>
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 18, color: theme.terminalGreen, letterSpacing: '0.25em' }}>
          TECHNICAL DECONSTRUCTION
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 44, fontWeight: 700, color: theme.foreground, marginTop: 8 }}>
          The Five Pillars of an Autonomous Agent
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 20, width: '100%', maxWidth: 1600 }}>
        {pillars.map((p, idx) => {
          const itemProgress = interpolate(frame, [idx * 15, idx * 15 + 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={idx}
              style={{
                backgroundColor: theme.surface,
                border: `1px solid ${itemProgress > 0.5 ? theme.terminalGreen : theme.surfaceBorder}`,
                borderRadius: 12,
                padding: '30px 20px',
                textAlign: 'center',
                opacity: itemProgress,
                transform: `translateY(${(1 - itemProgress) * 20}px)`,
                boxShadow: itemProgress > 0.5 ? `0 10px 30px ${theme.terminalGreen}22` : 'none',
              }}
            >
              <div style={{ fontSize: 44, marginBottom: 16 }}>{p.icon}</div>
              <div style={{ fontFamily: theme.monoFontFamily, fontSize: 18, fontWeight: 700, color: theme.foreground, marginBottom: 8 }}>
                {p.title}
              </div>
              <div style={{ fontFamily: theme.fontFamily, fontSize: 14, color: theme.muted }}>
                {p.desc}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
