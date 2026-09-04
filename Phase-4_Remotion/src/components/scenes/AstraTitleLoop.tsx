import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../../styles/theme';
import { fadeIn, fadeOut } from '../../lib/timeline';

interface AstraTitleLoopProps {
  totalFrames: number;
}

export const AstraTitleLoop: React.FC<AstraTitleLoopProps> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

  const steps = [
    { label: "1. GOAL", desc: "High-level objective from user", color: theme.cyan },
    { label: "2. PLAN", desc: "Decompose into atomic tool calls", color: theme.terminalAmber },
    { label: "3. ACT", desc: "Execute Bash, browser, or GUI", color: theme.terminalGreen },
    { label: "4. OBSERVE", desc: "Parse stdout, DOM & stack trace", color: "#FF4D4F" },
    { label: "5. ADAPT", desc: "Autonomous self-correction loop", color: theme.cyan }
  ];

  const activeIndex = Math.floor((frame / (totalFrames / steps.length))) % steps.length;

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#07090F',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '50px 80px',
        opacity,
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Background Subtle Technical Grid */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: 'radial-gradient(circle at 50% 50%, rgba(0, 210, 255, 0.04) 0%, transparent 70%)',
          pointerEvents: 'none'
        }}
      />

      <div style={{ textAlign: 'center', marginBottom: 35, zIndex: 10 }}>
        <div
          style={{
            fontFamily: theme.monoFontFamily,
            fontSize: 14,
            color: theme.terminalAmber,
            letterSpacing: '0.25em',
            marginBottom: 6,
            display: 'inline-block',
            padding: '4px 14px',
            background: 'rgba(255, 176, 32, 0.12)',
            border: '1px solid rgba(255, 176, 32, 0.35)',
            borderRadius: 4
          }}
        >
          [SYSTEM ARCHITECTURE // SPECIFICATION IN PROGRESS]
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 56, fontWeight: 900, color: '#F0F4F8', letterSpacing: '-0.02em', marginTop: 10 }}>
          GPT-6 ASTRA
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 20, color: theme.muted, marginTop: 4 }}>
          Autonomous Execution Loop: Moving Beyond Conversational Turn-Taking
        </div>
      </div>

      {/* 5-Stage Agent Loop */}
      <div style={{ display: 'flex', gap: 20, width: '100%', maxWidth: 1560, justifyContent: 'space-between', alignItems: 'center', zIndex: 10 }}>
        {steps.map((step, idx) => {
          const isActive = idx === activeIndex;
          const scale = isActive ? 1.05 : 0.98;

          return (
            <React.Fragment key={idx}>
              <div
                style={{
                  flex: 1,
                  backgroundColor: isActive ? 'rgba(18, 25, 40, 0.95)' : 'rgba(12, 16, 26, 0.85)',
                  border: `2px solid ${isActive ? step.color : 'rgba(45, 60, 85, 0.5)'}`,
                  borderRadius: 12,
                  padding: '28px 20px',
                  textAlign: 'center',
                  transform: `scale(${scale})`,
                  boxShadow: isActive ? `0 12px 35px ${step.color}35` : 'none',
                  transition: 'all 0.2s ease',
                }}
              >
                <div style={{ fontFamily: theme.monoFontFamily, fontSize: 20, fontWeight: 800, color: step.color, marginBottom: 10 }}>
                  {step.label}
                </div>
                <div style={{ fontFamily: theme.fontFamily, fontSize: 14, color: isActive ? '#F0F4F8' : theme.muted, lineHeight: 1.4 }}>
                  {step.desc}
                </div>
              </div>
              {idx < steps.length - 1 && (
                <div style={{ color: isActive ? step.color : 'rgba(70, 90, 120, 0.6)', fontSize: 28, fontWeight: 800 }}>
                  ➔
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Bottom Telemetry Bar */}
      <div
        style={{
          marginTop: 40,
          display: 'flex',
          gap: 30,
          background: 'rgba(15, 20, 32, 0.85)',
          border: '1px solid rgba(40, 55, 80, 0.8)',
          borderRadius: 6,
          padding: '10px 24px',
          fontFamily: theme.monoFontFamily,
          fontSize: 12,
          color: theme.muted,
          zIndex: 10
        }}
      >
        <span>REPORTED CONTEXT: <strong style={{ color: theme.cyan }}>1,050,000 TOKENS</strong></span>
        <span>MAX OUTPUT: <strong style={{ color: theme.terminalAmber }}>128,000 TOKENS</strong></span>
        <span>STATUS: <strong style={{ color: theme.terminalAmber }}>VERIFY AGAINST PRIMARY MODEL CARD</strong></span>
      </div>
    </div>
  );
};
