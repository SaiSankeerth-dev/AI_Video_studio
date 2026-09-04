import React from 'react';
import { Sequence, staticFile, Audio, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { FernSubtitle } from '../components/FernSubtitle';
import { SourceBadge } from '../components/shared/SourceBadge';
import { QuoteCard } from '../components/QuoteCard';
import { SourceCard } from '../components/SourceCard';
import { SmoothCamera } from '../components/SmoothCamera';
import syncedData from '../../public/data/synced_sentences_v003.json';

export const CIADocumentary: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ flex: 1, backgroundColor: '#04060A', position: 'relative', overflow: 'hidden' }}>
      {/* Low Ambient Tape Drone */}
      <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.045} loop />

      {syncedData.sentences.map((sent, idx) => {
        return (
          <Sequence
            key={sent.id}
            from={sent.startFrame}
            durationInFrames={sent.durationFrames}
          >
            {/* 1. Baritone Voiceover Track */}
            <Audio src={staticFile(sent.audio_file)} volume={1.0} />

            {/* 2. Tactile Sound Effects */}
            {sent.sfx && (
              <Audio src={staticFile(`audio/${sent.sfx}.wav`)} volume={0.40} />
            )}

            {/* 3. Rock-Solid Subpixel Smooth Camera Layer */}
            {renderCIAVisual(sent.id, sent.visual_mode, sent.durationFrames, idx)}

            {/* 4. Verified Source Badges */}
            {renderCIASourceBadge(sent.id, sent.durationFrames)}

            {/* 5. Clean, Understated Normal Subtitles */}
            <FernSubtitle text={sent.text} totalFrames={sent.durationFrames} />
          </Sequence>
        );
      })}
    </div>
  );
};

function renderCIAVisual(sentId: string, mode: string, totalFrames: number, idx: number) {
  const dir = idx % 2 === 0 ? 'zoom-in' : 'pan-right';

  switch (mode) {
    case 'CIA_LANGLEY_EXTERIOR':
    case 'DATA_CENTER':
      return <SmoothCamera imageSrc="images/v03_datacenter.jpg" totalFrames={totalFrames} direction="zoom-in" />;

    case 'SECURITY_DASHBOARD':
    case 'SOC_OPERATIONS':
      return <SmoothCamera imageSrc="images/v03_soc_night.jpg" totalFrames={totalFrames} direction="pan-right" />;

    case 'BREACH_ALERT_CARD':
      return <SmoothCamera imageSrc="images/v03_cia_seal_frame.jpg" totalFrames={totalFrames} direction="zoom-out" />;

    case 'BEDROOM_WORKSTATION':
      return <SmoothCamera imageSrc="images/v03_bedroom_workstation.jpg" totalFrames={totalFrames} direction="pan-left" />;

    case 'TELEPHONE_CLOSEUP':
    case 'CALL_CENTER_REENACTMENT':
      return <SmoothCamera imageSrc="images/shot03_telephone_macro.jpg" totalFrames={totalFrames} direction="zoom-in" />;

    case 'SF86_DOCUMENT_EVIDENCE':
    case 'DOCUMENT_REDACTED_SCAN':
      return <SmoothCamera imageSrc="images/v03_sf86_exhibit.jpg" totalFrames={totalFrames} direction="zoom-in" />;

    case 'GOVERNMENT_SEAL_CASCADE':
      return <SmoothCamera imageSrc="images/v03_cia_seal_frame.jpg" totalFrames={totalFrames} direction="tilt-up" />;

    case 'JABS_PORTAL_TERMINAL':
      return <SmoothCamera imageSrc="images/v03_jabs_terminal.jpg" totalFrames={totalFrames} direction="pan-right" />;

    case 'FBI_INVESTIGATION_TABLE':
    case 'ARREST_WARRANT_DOJ':
    case 'OLD_BAILEY_COURT_EVIDENCE':
      return <SmoothCamera imageSrc="images/v03_fbi_dossier.jpg" totalFrames={totalFrames} direction="zoom-out" />;

    case 'GEOGRAPHIC_IP_TRACKER':
      return <SmoothCamera imageSrc="images/v03_network_map.jpg" totalFrames={totalFrames} direction="pan-right" />;

    case 'TITLE_CARD_CIA':
      return (
        <div style={{ flex: 1, backgroundColor: '#05070D', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', position: 'relative' }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: '#F59E0B', letterSpacing: '0.3em', marginBottom: 20 }}>
            INVESTIGATIVE INTELLIGENCE SPECIAL REPORT
          </div>
          <div style={{ fontFamily: theme.fontFamily, fontSize: 58, fontWeight: 800, color: '#FFFFFF', textAlign: 'center', maxWidth: 1400, lineHeight: 1.2 }}>
            THE TEENAGERS WHO <span style={{ color: '#F59E0B' }}>HACKED THE CIA</span>
          </div>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 20, color: '#94A3B8', marginTop: 25, letterSpacing: '0.15em' }}>
            CRACKAS WITH ATTITUDE // HOW ONE MISTAKE EXPOSED EVERYTHING
          </div>
          <div style={{ width: 140, height: 2, backgroundColor: '#F59E0B', marginTop: 30 }} />
        </div>
      );

    case 'CODE_VS_PHONE_DIAGRAM':
    case 'PRETEXTING_STEP_DIAGRAM':
    case 'CREDENTIAL_CASCADE_MAP':
      return (
        <div style={{ flex: 1, backgroundColor: '#05070D', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', padding: 80 }}>
          <div style={{ fontFamily: theme.monoFontFamily, fontSize: 15, color: '#F59E0B', letterSpacing: '0.25em', marginBottom: 20 }}>
            THE TELEPHONE SOCIAL ENGINEERING INTRUSION CASCADE
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 25, width: '100%', maxWidth: 1400 }}>
            {[
              { step: '01', title: 'PRETEXTING', desc: 'Calling Verizon support posing as an internal field technician' },
              { step: '02', title: 'PIN BYPASS', desc: 'Tricking support agent into disclosing account PIN & mobile credentials' },
              { step: '03', title: 'EMAIL HIJACK', desc: 'Triggering password resets on private AOL & cloud storage accounts' },
              { step: '04', title: 'SF-86 LEAK', desc: 'Exfiltrating 47-page top secret national security questionnaire' }
            ].map((node) => (
              <div key={node.step} style={{ background: 'rgba(12, 16, 26, 0.9)', border: '1px solid rgba(245, 158, 11, 0.35)', borderRadius: 12, padding: 30 }}>
                <div style={{ fontFamily: theme.monoFontFamily, color: '#F59E0B', fontSize: 16 }}>STAGE {node.step}</div>
                <div style={{ fontFamily: theme.fontFamily, color: '#FFFFFF', fontSize: 22, fontWeight: 700, marginTop: 10 }}>{node.title}</div>
                <div style={{ color: '#94A3B8', fontSize: 15, marginTop: 12, lineHeight: 1.5 }}>{node.desc}</div>
              </div>
            ))}
          </div>
        </div>
      );

    case 'ZERO_TRUST_DEFENSE_DIAGRAM':
      return (
        <div style={{ flex: 1, backgroundColor: '#05070D', display: 'flex', justifyContent: 'center', alignItems: 'center', padding: 60 }}>
          <div style={{ width: '100%', maxWidth: 1350, background: 'rgba(10, 14, 24, 0.92)', border: '1px solid rgba(6, 182, 212, 0.3)', borderRadius: 14, padding: 45 }}>
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 15, color: '#06B6D4', letterSpacing: '0.25em', marginBottom: 15 }}>
              CRITICAL VULNERABILITY LESSON // ZERO-TRUST ACCESS
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 34, fontWeight: 700, color: '#FFFFFF', marginBottom: 25 }}>
              DEFENSE BUDGETS CANNOT COMPENSATE FOR UNVERIFIED HUMAN TRUST
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 30 }}>
              <div style={{ background: 'rgba(239, 68, 68, 0.08)', border: '1px solid #EF4444', padding: 30, borderRadius: 10 }}>
                <div style={{ color: '#EF4444', fontFamily: theme.monoFontFamily, fontSize: 16, fontWeight: 700 }}>THE HUMAN ATTACK VECTOR (2015)</div>
                <div style={{ color: '#CBD5E1', fontSize: 18, marginTop: 10, lineHeight: 1.5 }}>
                  Billions spent on network encryption rendered moot by a 15-minute phone call to customer support.
                </div>
              </div>
              <div style={{ background: 'rgba(16, 185, 129, 0.08)', border: '1px solid #10B981', padding: 30, borderRadius: 10 }}>
                <div style={{ color: '#10B981', fontFamily: theme.monoFontFamily, fontSize: 16, fontWeight: 700 }}>MODERN ZERO-TRUST REQUIREMENT (2026)</div>
                <div style={{ color: '#CBD5E1', fontSize: 18, marginTop: 10, lineHeight: 1.5 }}>
                  FIDO2 hardware security tokens, strict identity proofing, zero phone-based PIN overrides.
                </div>
              </div>
            </div>
          </div>
        </div>
      );

    case 'FINAL_EPILOGUE_QUOTE_CIA':
      return (
        <QuoteCard
          speaker="CENTRAL CRIMINAL COURT (OLD BAILEY)"
          role="JUDICIAL SENTENCING REMARKS (2018)"
          quote="Every system is only as secure as the person holding the authority to unlock it. The greatest cryptographic fortress can be breached with nothing more than a telephone and a convincing story."
          totalFrames={totalFrames}
        />
      );

    default:
      return <SmoothCamera imageSrc="images/v03_datacenter.jpg" totalFrames={totalFrames} direction="zoom-in" />;
  }
}

function renderCIASourceBadge(sentId: string, durationFrames: number) {
  if (sentId === 'c01' || sentId === 'c03') {
    return <SourceBadge sourceText="SOURCE: U.S. District Court (1:16-cr-00122-GBL)" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 'c09' || sentId === 'c10' || sentId === 'c11') {
    return <SourceBadge sourceText="SOURCE: Wired & Motherboard Investigative Archives" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 'c13' || sentId === 'c14') {
    return <SourceBadge sourceText="SOURCE: Standard Form 86 (SF-86) Exhibit Dossier" frame={0} totalFrames={durationFrames} />;
  }
  if (sentId === 'c20' || sentId === 'c21' || sentId === 'c22') {
    return <SourceBadge sourceText="SOURCE: Judicial Sentencing Remarks // Old Bailey (2018)" frame={0} totalFrames={durationFrames} />;
  }
  return null;
}
