import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../../styles/theme';
import { fadeIn, fadeOut } from '../../lib/timeline';

interface AstraComparisonProps {
  totalFrames: number;
}

export const AstraComparison: React.FC<AstraComparisonProps> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

  const leftPoints = [
    "User submits text question in a web chat box",
    "Model returns prose answer or snippet suggestions",
    "Human operator must manually execute commands and tests",
    "No access to operating system, file tree, or web browser",
    "Execution stops when generation completes"
  ];

  const rightPoints = [
    "User provides high-level goal ('Find and patch the bug')",
    "Model opens IDE, runs pytest, and captures stack trace",
    "Inspects source AST, writes patch, and re-executes tests",
    "Direct native tool integration: PTY Bash, GUI, Browser",
    "Autonomous verification loop: Iterates until goal is solved"
  ];

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#06080E',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px 80px',
        opacity,
      }}
    >
      <div style={{ width: '100%', maxWidth: 1400 }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.cyan, letterSpacing: '0.25em' }}>
            PARADIGM INFLECTION // CHATBOT VS COMPUTER-USE AGENT
          </div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 38, fontWeight: 800, color: '#F0F4F8', marginTop: 4 }}>
            What Actually Changed with GPT-6 Astra?
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
          {/* Left Column: Traditional Chatbot */}
          <div
            style={{
              backgroundColor: 'rgba(14, 18, 28, 0.9)',
              border: '1px solid rgba(45, 55, 75, 0.8)',
              borderRadius: 10,
              padding: 32,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <div style={{ fontFamily: theme.monoFontFamily, fontSize: 12, color: theme.muted, letterSpacing: '0.15em' }}>
                PARADIGM 1 (2022-2025)
              </div>
              <div style={{ fontFamily: theme.monoFontFamily, fontSize: 11, color: theme.muted, background: 'rgba(255,255,255,0.06)', padding: '3px 8px', borderRadius: 4 }}>
                QUESTION ➔ ANSWER
              </div>
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 26, fontWeight: 700, color: '#8899A6', marginBottom: 20 }}>
              Conversational Assistant
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              {leftPoints.map((pt, i) => (
                <div key={i} style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                  <span style={{ color: '#FF4D4F', fontWeight: 800, fontSize: 16 }}>✕</span>
                  <span style={{ fontFamily: theme.fontFamily, fontSize: 16, color: '#8899A6', lineHeight: 1.4 }}>{pt}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: Astra Agent */}
          <div
            style={{
              backgroundColor: 'rgba(12, 20, 34, 0.95)',
              border: '2px solid #00D2FF',
              borderRadius: 10,
              padding: 32,
              boxShadow: '0 10px 40px rgba(0, 210, 255, 0.12)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <div style={{ fontFamily: theme.monoFontFamily, fontSize: 12, color: '#00D2FF', letterSpacing: '0.15em' }}>
                PARADIGM 2 (2026+)
              </div>
              <div style={{ fontFamily: theme.monoFontFamily, fontSize: 11, color: theme.terminalGreen, background: 'rgba(0, 255, 100, 0.12)', padding: '3px 8px', borderRadius: 4, border: '1px solid rgba(0, 255, 100, 0.3)' }}>
                GOAL ➔ ACTION ➔ OBSERVATION ➔ ACTION
              </div>
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 26, fontWeight: 700, color: '#F0F4F8', marginBottom: 20 }}>
              Autonomous Computer-Use Agent
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              {rightPoints.map((pt, i) => (
                <div key={i} style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                  <span style={{ color: theme.terminalGreen, fontWeight: 800, fontSize: 16 }}>✓</span>
                  <span style={{ fontFamily: theme.fontFamily, fontSize: 16, color: '#F0F4F8', lineHeight: 1.4 }}>{pt}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Conclusion Callout Banner */}
        <div
          style={{
            marginTop: 28,
            backgroundColor: 'rgba(0, 210, 255, 0.08)',
            border: '1px solid rgba(0, 210, 255, 0.3)',
            borderRadius: 6,
            padding: '12px 24px',
            textAlign: 'center',
            fontFamily: theme.monoFontFamily,
            fontSize: 13,
            color: '#00D2FF',
            letterSpacing: '0.08em'
          }}
        >
          THE PARAGRAPH IS NO LONGER THE FINAL OUTPUT. THE GOAL IS BECOMING THE OUTPUT.
        </div>
      </div>
    </div>
  );
};
