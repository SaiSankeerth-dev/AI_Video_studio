import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface CodeWindowProps {
  filename: string;
  codeLines: string[];
  highlightLine?: number;
  totalFrames?: number;
}

export const CodeWindow: React.FC<CodeWindowProps> = ({
  filename,
  codeLines = [
    'import { AgentRuntime } from "@openai/agents";',
    'const runtime = new AgentRuntime({',
    '  sandbox: "docker://root-readonly",',
    '  maxSteps: 100,',
    '  tools: [bashExecution, fileReadWrite]',
    '});',
    'await runtime.run("Deploy automated migration patch");',
  ],
  highlightLine = 3,
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
          maxWidth: 1050,
          backgroundColor: '#0D1117',
          border: '1px solid #30363D',
          borderRadius: 8,
          overflow: 'hidden',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.8)',
        }}
      >
        {/* Title bar */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            backgroundColor: '#161B22',
            padding: '12px 20px',
            borderBottom: '1px solid #30363D',
          }}
        >
          <div style={{ display: 'flex', gap: 8, marginRight: 20 }}>
            <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#FF5F56' }} />
            <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#FFBD2E' }} />
            <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#27C93F' }} />
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: '#8B949E' }}>
            {filename}
          </div>
        </div>

        {/* Code Content */}
        <div style={{ padding: '24px 30px', display: 'flex', flexDirection: 'column', gap: 6 }}>
          {codeLines.map((line, idx) => {
            const isHighlighted = idx + 1 === highlightLine;
            return (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  gap: 20,
                  fontFamily: theme.monoFontFamily,
                  fontSize: 16,
                  lineHeight: 1.5,
                  backgroundColor: isHighlighted ? 'rgba(0, 240, 255, 0.12)' : 'transparent',
                  padding: '2px 8px',
                  borderRadius: 4,
                }}
              >
                <span style={{ color: '#484F58', width: 24, textAlign: 'right', userSelect: 'none' }}>
                  {idx + 1}
                </span>
                <span style={{ color: isHighlighted ? theme.cyan : '#C9D1D9' }}>{line}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
