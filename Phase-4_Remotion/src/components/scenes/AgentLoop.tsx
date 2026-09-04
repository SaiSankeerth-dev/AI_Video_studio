import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { theme } from '../../styles/theme';
import { fadeIn, fadeOut } from '../../lib/timeline';

interface AgentLoopProps {
  totalFrames: number;
}

export const AgentLoop: React.FC<AgentLoopProps> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

  const steps = [
    { label: "1. GOAL", desc: "User specifies high-level objective", color: theme.cyan },
    { label: "2. PLAN", desc: "Decomposes goal into atomic sub-tasks", color: theme.terminalAmber },
    { label: "3. ACT", desc: "Invokes shell, APIs, and file tools", color: theme.terminalGreen },
    { label: "4. OBSERVE", desc: "Inspects stdout, exit codes, and errors", color: theme.accent },
    { label: "5. REPLAN", desc: "Self-corrects and iterates autonomously", color: theme.cyan }
  ];

  // Active step highlights sequentially
  const activeIndex = Math.floor((frame / (totalFrames / steps.length))) % steps.length;

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
      <div style={{ textAlign: 'center', marginBottom: 40 }}>
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 18, color: theme.cyan, letterSpacing: '0.25em' }}>
          AGENTIC WORKFLOW ARCHITECTURE
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 44, fontWeight: 700, color: theme.foreground, marginTop: 8 }}>
          The Autonomous Execution Loop
        </div>
      </div>

      <div style={{ display: 'flex', gap: 24, width: '100%', maxWidth: 1600, justifyContent: 'space-between', alignItems: 'center' }}>
        {steps.map((step, idx) => {
          const isActive = idx === activeIndex;
          const scale = isActive ? 1.06 : 1.0;

          return (
            <React.Fragment key={idx}>
              <div
                style={{
                  flex: 1,
                  backgroundColor: theme.surface,
                  border: `2px solid ${isActive ? step.color : theme.surfaceBorder}`,
                  borderRadius: 14,
                  padding: '32px 24px',
                  textAlign: 'center',
                  transform: `scale(${scale})`,
                  boxShadow: isActive ? `0 15px 40px ${step.color}44` : 'none',
                  transition: 'all 0.2s ease',
                }}
              >
                <div style={{ fontFamily: theme.monoFontFamily, fontSize: 24, fontWeight: 800, color: step.color, marginBottom: 12 }}>
                  {step.label}
                </div>
                <div style={{ fontFamily: theme.fontFamily, fontSize: 16, color: theme.muted, lineHeight: 1.5 }}>
                  {step.desc}
                </div>
              </div>
              {idx < steps.length - 1 && (
                <div style={{ color: isActive ? step.color : theme.mutedDark, fontSize: 32, fontWeight: 700 }}>
                  ➔
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
