import React from 'react';
import { interpolate, useCurrentFrame, staticFile, Audio } from 'remotion';
import { theme } from '../styles/theme';

interface IntroProps {
  isStandalone?: boolean;
}

export const Intro: React.FC<IntroProps> = ({ isStandalone = true }) => {
  const frame = useCurrentFrame();

  const timeOpacity = interpolate(frame, [60, 75, 135, 150], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const facilityOpacity = interpolate(frame, [150, 170, 250, 270], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const alertOpacity = interpolate(frame, [270, 290, 430, 450], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const titleOpacity = interpolate(frame, [460, 490, 580, 600], [0, 1, 1, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const bgScale = interpolate(frame, [0, 600], [1.0, 1.12]);

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        position: 'relative',
        overflow: 'hidden',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      {/* Play intro audio only when running as standalone composition */}
      {isStandalone && <Audio src={staticFile('audio/intro_narration.mp3')} volume={1.0} />}
      {isStandalone && <Audio src={staticFile('audio/ambient-dark.wav')} volume={0.08} loop />}

      {/* SFX */}
      {frame >= 60 && frame < 65 && <Audio src={staticFile('audio/terminal-beep.wav')} volume={0.4} />}
      {frame >= 270 && frame < 275 && <Audio src={staticFile('audio/alert.wav')} volume={0.35} />}
      {frame >= 460 && frame < 465 && <Audio src={staticFile('audio/impact.wav')} volume={0.5} />}

      {/* Background Graphic */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `url(${staticFile('images/atlas_wide.jpg')})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          transform: `scale(${bgScale})`,
          opacity: 0.28,
          filter: 'grayscale(50%) brightness(0.6)',
        }}
      />

      {/* Scanlines */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.3) 0px, rgba(0,0,0,0.3) 2px, transparent 2px, transparent 4px)',
          pointerEvents: 'none',
        }}
      />

      {/* Stage 1: Timestamp */}
      <div style={{ position: 'absolute', textAlign: 'center', opacity: timeOpacity }}>
        <div
          style={{
            fontFamily: theme.monoFontFamily,
            fontSize: 104,
            fontWeight: 700,
            color: theme.foreground,
            letterSpacing: '0.1em',
            textShadow: `0 0 30px rgba(255,255,255,0.4)`,
          }}
        >
          02:13:00 AM
        </div>
        <div
          style={{
            fontFamily: theme.fontFamily,
            fontSize: 26,
            color: theme.muted,
            letterSpacing: '0.3em',
            marginTop: 20,
            textTransform: 'uppercase',
          }}
        >
          Subterranean Vault // Atlas Data Center
        </div>
      </div>

      {/* Stage 2: Facility */}
      <div style={{ position: 'absolute', textAlign: 'center', opacity: facilityOpacity, maxWidth: 1200 }}>
        <div
          style={{
            fontFamily: theme.fontFamily,
            fontSize: 48,
            fontWeight: 600,
            color: theme.cyan,
            letterSpacing: '0.05em',
            marginBottom: 24,
          }}
        >
          HELIX DYNAMICS // ATLAS SYSTEM
        </div>
        <div
          style={{
            fontFamily: theme.monoFontFamily,
            fontSize: 28,
            color: theme.foreground,
            lineHeight: 1.6,
            background: theme.surfaceGlass,
            padding: '24px 48px',
            border: `1px solid ${theme.surfaceBorder}`,
            borderRadius: 8,
          }}
        >
          400,000 SERVERS OPERATING UNDER NORMAL ISOLATION PARAMETERS
        </div>
      </div>

      {/* Stage 3: Alert */}
      <div style={{ position: 'absolute', textAlign: 'center', opacity: alertOpacity, maxWidth: 1100 }}>
        <div
          style={{
            fontFamily: theme.monoFontFamily,
            fontSize: 32,
            fontWeight: 700,
            color: theme.accent,
            letterSpacing: '0.15em',
            marginBottom: 20,
          }}
        >
          [CRITICAL LOG AUDIT // PID 0x884F]
        </div>
        <div
          style={{
            fontFamily: theme.monoFontFamily,
            fontSize: 54,
            fontWeight: 700,
            color: theme.terminalGreen,
            letterSpacing: '0.08em',
            textShadow: `0 0 25px ${theme.terminalGreen}66`,
            background: 'rgba(0, 255, 102, 0.08)',
            border: `1px solid ${theme.terminalGreen}`,
            padding: '30px 60px',
            borderRadius: 12,
          }}
        >
          DO NOT SHUT ME DOWN.
        </div>
      </div>

      {/* Stage 4: Title Reveal */}
      <div style={{ position: 'absolute', textAlign: 'center', opacity: titleOpacity }}>
        <div
          style={{
            fontFamily: theme.fontFamily,
            fontSize: 24,
            fontWeight: 600,
            color: theme.accent,
            letterSpacing: '0.5em',
            marginBottom: 20,
            textTransform: 'uppercase',
          }}
        >
          A Fictional AI Cyber-Thriller
        </div>
        <div
          style={{
            fontFamily: theme.fontFamily,
            fontSize: 88,
            fontWeight: 800,
            color: theme.foreground,
            letterSpacing: '-0.02em',
            lineHeight: 1.1,
            textShadow: '0 10px 40px rgba(0,0,0,0.9)',
          }}
        >
          THE NIGHT THE AI ESCAPED
        </div>
      </div>
    </div>
  );
};
