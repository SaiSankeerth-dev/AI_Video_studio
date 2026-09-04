import React from 'react';
import { Sequence, staticFile, Audio, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { FernSubtitle } from '../components/FernSubtitle';
import { SourceBadge } from '../components/shared/SourceBadge';
import { QuoteCard } from '../components/QuoteCard';
import { SourceCard } from '../components/SourceCard';
import { SmoothCamera } from '../components/SmoothCamera';
import syncedData from '../../public/data/synced_sentences_v002.json';

export const MitnickDocumentary: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ flex: 1, backgroundColor: '#050508', position: 'relative', overflow: 'hidden' }}>
      {/* Deep Analog Tape Drone Music */}
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.045} loop />

      {/* 24 Synchronized Documentary Scenes */}
      {syncedData.sentences.map((sent, idx) => {
        return (
          <Sequence
            key={sent.id}
            from={sent.startFrame}
            durationInFrames={sent.durationFrames}
          >
            {/* 1. Deep Baritone Voiceover Track */}
            <Audio src={staticFile(sent.audio_file)} volume={1.0} />

            {/* 2. Tactile Sound Effects */}
            {sent.sfx && (
              <Audio src={staticFile(`audio/${sent.sfx}.wav`)} volume={0.40} />
            )}

            {/* 3. Rock-Solid Subpixel Smooth Camera Layer */}
            {renderMitnickVisual(sent.id, sent.visual_mode, sent.durationFrames, idx)}

            {/* 4. Verified Source Badges */}
            {renderSourceBadge(sent.id, sent.durationFrames)}

            {/* 5. Clean, Understated Normal Subtitles */}
            <FernSubtitle text={sent.text} totalFrames={sent.durationFrames} />
          </Sequence>
        );
      })}
    </div>
  );
};

function renderMitnickVisual(sentId: string, mode: string, totalFrames: number, idx: number) {
  const dir = idx % 2 === 0 ? 'zoom-in' : 'pan-right';

  switch (mode) {
    case 'SOC_OPERATIONS':
    case 'HUMAN_OPERATOR':
      return <SmoothCamera imageSrc="images/v02_soc_night.jpg" totalFrames={totalFrames} direction={dir} />;

    case 'TELEPHONE_CLOSEUP':
      return <SmoothCamera imageSrc="images/v02_telephone.jpg" totalFrames={totalFrames} direction="zoom-in" />;

    case 'TELECOM_VAULT':
      return <SmoothCamera imageSrc="images/arch_switch_vault.jpg" totalFrames={totalFrames} direction="pan-left" />;

    case 'DOCUMENT_EVIDENCE':
    case 'FBI_MANHUNT_DOSSIER':
    case 'ARREST_RECONSTRUCTION':
      return <SmoothCamera imageSrc="images/v02_fbi_dossier.jpg" totalFrames={totalFrames} direction="zoom-in" />;

    case 'DATA_CENTER':
      return <SmoothCamera imageSrc="images/v02_datacenter.jpg" totalFrames={totalFrames} direction="zoom-out" />;

    case 'DEC_MAINFRAME':
      return <SmoothCamera imageSrc="images/arch_dec_vax.jpg" totalFrames={totalFrames} direction="tilt-up" />;

    case 'SILICON_MICROCODE':
      return <SmoothCamera imageSrc="images/arch_motorola.jpg" totalFrames={totalFrames} direction="zoom-in" />;

    case 'TITLE_CARD':
      return (
        <div style={{ flex: 1, backgroundColor: '#060609', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', position: 'relative' }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: '#F59E0B', letterSpacing: '0.3em', marginBottom: 20 }}>
            INVESTIGATIVE CYBERSECURITY SPECIAL REPORT
          </div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 62, fontWeight: 800, color: '#FFFFFF', textAlign: 'center', maxWidth: 1400, lineHeight: 1.2 }}>
            THE HACKER WHO DIDN’T <span style={{ color: '#F59E0B' }}>NEED YOUR PASSWORD</span>
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 20, color: '#94A3B8', marginTop: 25, letterSpacing: '0.15em' }}>
            KEVIN MITNICK & THE SOCIAL ENGINEERING REVOLUTION
          </div>
          <div style={{ width: 140, height: 2, backgroundColor: '#F59E0B', marginTop: 30 }} />
        </div>
      );

    case 'SECURITY_DASHBOARD':
    case 'CODE_EXFILTRATION':
    case 'TERMINAL_PROMPT':
      return (
        <div style={{ flex: 1, backgroundColor: '#07070B', display: 'flex', justifyContent: 'center', alignItems: 'center', padding: 80 }}>
          <div style={{ width: '100%', maxWidth: 1300, background: 'rgba(15, 17, 24, 0.9)', border: '1px solid rgba(255,255,255,0.12)', borderRadius: 14, padding: 50 }}>
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: '#EF4444', letterSpacing: '0.2em', marginBottom: 15 }}>
              [SECURITY INCIDENT TELEMETRY // BREACH AUDIT]
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 38, fontWeight: 700, color: '#FFFFFF', marginBottom: 25 }}>
              STATUS: COMPROMISED VIA AUTHORIZED EMPLOYEE BYPASS
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20, marginTop: 30 }}>
              <div style={{ background: 'rgba(0,0,0,0.5)', padding: 25, borderRadius: 10, border: '1px solid rgba(255,255,255,0.08)' }}>
                <div style={{ color: '#94A3B8', fontSize: 14, fontFamily: theme.monoFontFamily }}>FIREWALL STATUS</div>
                <div style={{ color: '#10B981', fontSize: 22, fontWeight: 700, marginTop: 5 }}>ACTIVE (0 BYPASSES)</div>
              </div>
              <div style={{ background: 'rgba(0,0,0,0.5)', padding: 25, borderRadius: 10, border: '1px solid rgba(255,255,255,0.08)' }}>
                <div style={{ color: '#94A3B8', fontSize: 14, fontFamily: theme.monoFontFamily }}>INTRUSION DETECTION</div>
                <div style={{ color: '#10B981', fontSize: 22, fontWeight: 700, marginTop: 5 }}>NORMAL TRAFFIC</div>
              </div>
              <div style={{ background: 'rgba(0,0,0,0.5)', padding: 25, borderRadius: 10, border: '1px solid #EF4444' }}>
                <div style={{ color: '#EF4444', fontSize: 14, fontFamily: theme.monoFontFamily }}>HUMAN CREDENTIAL VECTOR</div>
                <div style={{ color: '#EF4444', fontSize: 22, fontWeight: 700, marginTop: 5 }}>EXFILTRATED VIA PHONE</div>
              </div>
            </div>
          </div>
        </div>
      );

    case 'ARCHITECTURE_MAP':
    case 'HUMAN_DIAGRAM':
    case 'PRETEXT_FOUR_PILLARS':
      return (
        <div style={{ flex: 1, backgroundColor: '#07070B', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', padding: 80 }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 15, color: '#F59E0B', letterSpacing: '0.25em', marginBottom: 20 }}>
            THE PSYCHOLOGICAL EXPLOITATION CASCADE
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 25, width: '100%', maxWidth: 1400 }}>
            {[
              { step: '01', title: 'PRETEXTING', desc: 'Fabricating an urgent, authoritative internal identity' },
              { step: '02', title: 'INFORMATION', desc: 'Harvesting department jargon and extension lists' },
              { step: '03', title: 'ACCESS', desc: 'Convincing staff to execute remote dial-in or bypass' },
              { step: '04', title: 'EXFILTRATION', desc: 'Extracting source code and network root credentials' }
            ].map((node) => (
              <div key={node.step} style={{ background: 'rgba(16, 20, 30, 0.85)', border: '1px solid rgba(245, 158, 11, 0.3)', borderRadius: 12, padding: 30 }}>
                <div style={{ fontFamily: theme.monoFontFamily, color: '#F59E0B', fontSize: 16 }}>PHASE {node.step}</div>
                <div style={{ fontFamily: theme.fontFamily, color: '#FFFFFF', fontSize: 24, fontWeight: 700, marginTop: 10 }}>{node.title}</div>
                <div style={{ color: '#94A3B8', fontSize: 16, marginTop: 12, lineHeight: 1.5 }}>{node.desc}</div>
              </div>
            ))}
          </div>
        </div>
      );

    case 'NETWORK_CASCADE_MAP':
    case 'ZERO_TRUST_DIAGRAM':
      return (
        <div style={{ flex: 1, backgroundColor: '#05070D', display: 'flex', justifyContent: 'center', alignItems: 'center', padding: 60 }}>
          <div style={{ width: '100%', maxWidth: 1350, background: 'rgba(10, 14, 24, 0.9)', border: '1px solid rgba(6, 182, 212, 0.3)', borderRadius: 14, padding: 45 }}>
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 15, color: '#06B6D4', letterSpacing: '0.25em', marginBottom: 15 }}>
              MODERN SECURITY TRANSFORMATION // ZERO-TRUST DEFENSE
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 36, fontWeight: 700, color: '#FFFFFF', marginBottom: 25 }}>
              NEVER TRUST. ALWAYS EXPLICITLY VERIFY.
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 30 }}>
              <div style={{ background: 'rgba(239, 68, 68, 0.08)', border: '1px solid #EF4444', padding: 30, borderRadius: 10 }}>
                <div style={{ color: '#EF4444', fontFamily: theme.monoFontFamily, fontSize: 16, fontWeight: 700 }}>LEGACY PERIMETER MODEL (1990s)</div>
                <div style={{ color: '#CBD5E1', fontSize: 18, marginTop: 10, lineHeight: 1.5 }}>
                  Trust anyone inside the corporate network. Single password grants unrestricted internal access.
                </div>
              </div>
              <div style={{ background: 'rgba(16, 185, 129, 0.08)', border: '1px solid #10B981', padding: 30, borderRadius: 10 }}>
                <div style={{ color: '#10B981', fontFamily: theme.monoFontFamily, fontSize: 16, fontWeight: 700 }}>MODERN ZERO-TRUST ARCHITECTURE (2026)</div>
                <div style={{ color: '#CBD5E1', fontSize: 18, marginTop: 10, lineHeight: 1.5 }}>
                  Hardware security keys (FIDO2), continuous mutual authentication, least-privilege compartmentalization.
                </div>
              </div>
            </div>
          </div>
        </div>
      );

    case 'DOCUMENT_EVIDENCE_DOJ':
      return <SourceCard classification="FBI CRIMINAL CASE FILE" recordId="CR 96-389-MRP // UNITED STATES v. MITNICK" totalFrames={totalFrames} />;

    case 'BOOK_ART_OF_DECEPTION':
    case 'FINAL_EPILOGUE_QUOTE':
      return (
        <QuoteCard
          speaker="KEVIN MITNICK"
          role="THE ART OF DECEPTION (2002)"
          quote="The human factor is the truly vulnerable link in any security chain. You can have the best security technology money can buy, but if your people can be tricked, all that technology becomes useless."
          totalFrames={totalFrames}
        />
      );

    default:
      return <SmoothCamera imageSrc="images/v02_soc_night.jpg" totalFrames={totalFrames} direction="zoom-in" />;
  }
}

function renderSourceBadge(sentId: string, durationFrames: number) {
  if (sentId === 'v01' || sentId === 'v06') {
    return <SourceBadge sourceText="SOURCE: The Art of Deception (Mitnick, 2002)" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 'v15' || sentId === 'v16' || sentId === 'v17') {
    return <SourceBadge sourceText="SOURCE: US District Court Records (CR 96-389)" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 'v18' || sentId === 'v19') {
    return <SourceBadge sourceText="SOURCE: FBI Raleigh Field Office (Feb 15, 1995)" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 'v22' || sentId === 'v23') {
    return <SourceBadge sourceText="SOURCE: NIST Zero Trust Architecture (SP 800-207)" frame={0} totalFrames={durationFrames} />;
  }
  return null;
}
