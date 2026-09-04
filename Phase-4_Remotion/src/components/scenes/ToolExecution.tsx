import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../../styles/theme';
import { fadeIn, fadeOut } from '../../lib/timeline';

interface ToolExecutionProps {
  totalFrames: number;
}

export const ToolExecution: React.FC<ToolExecutionProps> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 10), fadeOut(frame, totalFrames, 10));

  const terminalLines = [
    "$ agent --task 'Optimize database query pipeline and verify tests'",
    "[1/4] Scanning repository: 142 source files indexed...",
    "[2/4] Found bottleneck in src/db/query_engine.py: O(N^2) linear scan",
    "[3/4] Applying optimized hash-index routine... modified 1 file.",
    "[4/4] Executing test suite: pytest tests/test_db.py",
    "================ FAILURES ================",
    "FAILED tests/test_db.py::test_boundary_conditions - IndexError: offset out of range",
    "> [AUTO-REFLECT]: Diagnosed off-by-one error on line 48. Refactoring patch...",
    "> Re-running test suite: pytest tests/test_db.py",
    "================ 12 passed in 0.42s ================",
    "STATUS: ALL CHECKS PASSING (EXIT CODE 0)"
  ];

  const visibleCount = Math.min(Math.floor(frame / 12) + 1, terminalLines.length);

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '60px',
        opacity,
      }}
    >
      <div
        style={{
          width: 1400,
          backgroundColor: theme.surface,
          border: `1px solid ${theme.surfaceBorder}`,
          borderRadius: 12,
          overflow: 'hidden',
          boxShadow: '0 20px 60px rgba(0,0,0,0.9)',
        }}
      >
        <div
          style={{
            backgroundColor: '#181818',
            padding: '16px 24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: `1px solid ${theme.surfaceBorder}`,
          }}
        >
          <div style={{ display: 'flex', gap: 10 }}>
            <div style={{ width: 14, height: 14, borderRadius: '50%', backgroundColor: theme.danger }} />
            <div style={{ width: 14, height: 14, borderRadius: '50%', backgroundColor: theme.terminalAmber }} />
            <div style={{ width: 14, height: 14, borderRadius: '50%', backgroundColor: theme.terminalGreen }} />
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 18, color: theme.muted, fontWeight: 600 }}>
            AUTONOMOUS CODING AGENT // EXECUTION SANDBOX
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: theme.terminalGreen }}>
            STATE: SELF-HEALING
          </div>
        </div>

        <div
          style={{
            padding: '30px 40px',
            minHeight: 460,
            fontFamily: theme.monoFontFamily,
            fontSize: 22,
            lineHeight: 1.6,
            color: theme.terminalGreen,
          }}
        >
          {terminalLines.slice(0, visibleCount).map((line, idx) => {
            const isFailure = line.includes("FAILURES") || line.includes("FAILED");
            const isSuccess = line.includes("12 passed") || line.includes("EXIT CODE 0");
            const isReflect = line.includes("AUTO-REFLECT");

            let col = theme.terminalGreen;
            if (isFailure) col = theme.danger;
            if (isSuccess) col = theme.cyan;
            if (isReflect) col = theme.terminalAmber;

            return (
              <div key={idx} style={{ color: col, marginBottom: 8 }}>
                {line}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
