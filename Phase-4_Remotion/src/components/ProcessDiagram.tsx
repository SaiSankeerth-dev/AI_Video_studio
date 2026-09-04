import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface ProcessNode {
  title: string;
  detail: string;
  category: 'REASONING' | 'TOOL_CALL' | 'SANDBOX' | 'GATE';
}

interface ProcessDiagramProps {
  title: string;
  nodes?: ProcessNode[];
  totalFrames?: number;
}

export const ProcessDiagram: React.FC<ProcessDiagramProps> = ({
  title,
  nodes = [
    { title: 'User Objective Dispatch', detail: 'Decompose mandate into DAG tasks', category: 'REASONING' },
    { title: 'Dynamic Tool Selection', detail: 'Evaluate registry schemas for bash/fs', category: 'TOOL_CALL' },
    { title: 'Namespace Execution', detail: 'Execute code in read-only container mount', category: 'SANDBOX' },
    { title: 'Human-in-the-Loop Gate', detail: 'Verify zero outbound firewall violations', category: 'GATE' },
  ],
  totalFrames = 150,
}) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 10), fadeOut(frame, totalFrames, 10));

  const categoryColor = (cat: string) => {
    switch (cat) {
      case 'REASONING': return theme.cyan;
      case 'TOOL_CALL': return theme.terminalAmber;
      case 'SANDBOX': return theme.terminalGreen;
      case 'GATE': return theme.danger;
      default: return theme.foreground;
    }
  };

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
      <div style={{ width: '100%', maxWidth: 1100 }}>
        <div style={{ marginBottom: 40 }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 14, color: theme.cyan, letterSpacing: '0.2em' }}>
            OPERATIONAL EXECUTION PIPELINE
          </div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 36, fontWeight: 800, color: theme.foreground }}>
            {title}
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {nodes.map((node, i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'center',
                backgroundColor: theme.surface,
                border: `1px solid ${theme.surfaceBorder}`,
                borderRadius: 8,
                padding: '20px 24px',
                gap: 20,
              }}
            >
              <div
                style={{
                  fontFamily: theme.monoFontFamily,
                  fontSize: 14,
                  fontWeight: 700,
                  color: categoryColor(node.category),
                  minWidth: 120,
                }}
              >
                [{node.category}]
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontFamily: theme.fontFamily, fontSize: 20, fontWeight: 700, color: theme.foreground }}>
                  {node.title}
                </div>
                <div style={{ fontFamily: theme.fontFamily, fontSize: 14, color: theme.muted, marginTop: 4 }}>
                  {node.detail}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
