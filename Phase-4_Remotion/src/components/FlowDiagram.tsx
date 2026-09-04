import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface FlowStep {
  id: string;
  name: string;
  description: string;
}

interface FlowDiagramProps {
  title: string;
  steps?: FlowStep[];
  totalFrames?: number;
}

export const FlowDiagram: React.FC<FlowDiagramProps> = ({
  title,
  steps = [
    { id: '1', name: 'Reasoning', description: 'Core LLM plans next action' },
    { id: '2', name: 'Tool Invocation', description: 'Agent executes sandboxed bash call' },
    { id: '3', name: 'Observation', description: 'Environment stdout / exit code parsed' },
    { id: '4', name: 'Self-Reflection', description: 'Memory updated & strategy patched' },
  ],
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
      <div style={{ width: '100%', maxWidth: 1200 }}>
        <div style={{ textAlign: 'center', marginBottom: 50 }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 14, color: theme.cyan, letterSpacing: '0.2em' }}>
            CLOSED-LOOP EXECUTION ARCHITECTURE
          </div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 38, fontWeight: 800, color: theme.foreground }}>
            {title}
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16 }}>
          {steps.map((step, idx) => {
            const isActive = Math.floor(frame / 35) % steps.length === idx;

            return (
              <React.Fragment key={step.id}>
                <div
                  style={{
                    flex: 1,
                    backgroundColor: theme.surface,
                    border: `1px solid ${isActive ? theme.cyan : theme.surfaceBorder}`,
                    borderRadius: 8,
                    padding: 24,
                    boxShadow: isActive ? '0 0 25px rgba(0, 240, 255, 0.25)' : 'none',
                    transition: 'border 0.3s ease',
                  }}
                >
                  <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: isActive ? theme.cyan : theme.muted, marginBottom: 8 }}>
                    STEP 0{idx + 1}
                  </div>
                  <div style={{ fontFamily: theme.fontFamily, fontSize: 20, fontWeight: 700, color: theme.foreground, marginBottom: 8 }}>
                    {step.name}
                  </div>
                  <div style={{ fontFamily: theme.fontFamily, fontSize: 14, color: theme.muted, lineHeight: 1.4 }}>
                    {step.description}
                  </div>
                </div>

                {idx < steps.length - 1 && (
                  <div style={{ color: theme.cyan, fontSize: 24, fontWeight: 800 }}>→</div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
};
