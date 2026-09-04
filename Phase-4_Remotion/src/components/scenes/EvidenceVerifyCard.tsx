import React from 'react';
import { useCurrentFrame } from 'remotion';
import { theme } from '../../styles/theme';
import { fadeIn, fadeOut } from '../../lib/timeline';

interface EvidenceVerifyCardProps {
  totalFrames: number;
}

export const EvidenceVerifyCard: React.FC<EvidenceVerifyCardProps> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

  const specs = [
    { label: "ANNOUNCEMENT DATE", value: "September 3, 2026", status: "CONFIRMED SIGNAL", color: theme.terminalGreen },
    { label: "REPORTED CONTEXT WINDOW", value: "1,050,000 Tokens", status: "VERIFY", color: theme.terminalAmber },
    { label: "MAX GENERATION OUTPUT", value: "128,000 Tokens", status: "VERIFY", color: theme.terminalAmber },
    { label: "API TOKEN PRICING", value: "$10.00 / 1M in  |  $50.00 / 1M out", status: "VERIFY", color: theme.terminalAmber },
    { label: "AUTOMATIONBENCH RESULT", value: "88.4% (vs 62.1% Prev SOTA)", status: "VERIFY", color: theme.terminalAmber },
    { label: "SCREENSPOT PRO ACCURACY", value: "81.2% (vs 54.7% Prev SOTA)", status: "VERIFY", color: theme.terminalAmber },
  ];

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#06080E',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '50px 80px',
        opacity,
        position: 'relative'
      }}
    >
      <div style={{ width: '100%', maxWidth: 1300, backgroundColor: 'rgba(14, 18, 30, 0.95)', border: '1px solid rgba(50, 70, 100, 0.6)', borderRadius: 10, padding: 40, boxShadow: '0 20px 60px rgba(0,0,0,0.6)' }}>
        {/* Header with Warning Watermark */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid rgba(40, 55, 80, 0.8)', paddingBottom: 24, marginBottom: 30 }}>
          <div>
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, color: theme.cyan, letterSpacing: '0.2em' }}>
              PRIMARY INVESTIGATIVE DOSSIER // SRC-001 & SRC-010
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 34, fontWeight: 800, color: '#F0F4F8', marginTop: 4 }}>
              OpenAI GPT-6 Astra Launch Specification
            </div>
          </div>
          <div
            style={{
              backgroundColor: 'rgba(255, 176, 32, 0.15)',
              border: '2px solid #FFB020',
              borderRadius: 6,
              padding: '10px 18px',
              fontFamily: theme.monoFontFamily,
              fontSize: 14,
              fontWeight: 800,
              color: '#FFB020',
              letterSpacing: '0.15em',
              textAlign: 'center'
            }}
          >
            STATUS: VERIFY BEFORE PUBLICATION
          </div>
        </div>

        {/* Spec Table */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
          {specs.map((s, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: 'rgba(10, 14, 22, 0.85)',
                border: '1px solid rgba(35, 48, 70, 0.7)',
                borderRadius: 8,
                padding: '16px 20px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <div>
                <div style={{ fontFamily: theme.monoFontFamily, fontSize: 11, color: theme.muted, letterSpacing: '0.1em' }}>
                  {s.label}
                </div>
                <div style={{ fontFamily: theme.fontFamily, fontSize: 20, fontWeight: 700, color: '#F0F4F8', marginTop: 4 }}>
                  {s.value}
                </div>
              </div>
              <div
                style={{
                  fontFamily: theme.monoFontFamily,
                  fontSize: 11,
                  fontWeight: 700,
                  color: s.color,
                  backgroundColor: `${s.color}15`,
                  border: `1px solid ${s.color}40`,
                  padding: '4px 10px',
                  borderRadius: 4
                }}
              >
                [{s.status}]
              </div>
            </div>
          ))}
        </div>

        {/* Editorial Audit Rule */}
        <div style={{ marginTop: 28, paddingTop: 18, borderTop: '1px solid rgba(35, 48, 70, 0.7)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 12, color: theme.muted }}>
            AUDIT POLICY: Data originated from developer community release thread. Independent verification against official model card mandatory.
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 12, color: theme.terminalAmber, fontWeight: 700 }}>
            RULE: NEVER SILENTLY UPGRADE VERIFY TO VERIFIED
          </div>
        </div>
      </div>
    </div>
  );
};
