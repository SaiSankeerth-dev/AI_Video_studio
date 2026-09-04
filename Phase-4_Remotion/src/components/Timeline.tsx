import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface TimelineEvent {
  time: string;
  title: string;
  desc: string;
}

interface TimelineProps {
  events: TimelineEvent[];
  totalFrames: number;
}

export const Timeline: React.FC<TimelineProps> = ({ events, totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 12), fadeOut(frame, totalFrames, 12));

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '60px 100px',
        opacity,
      }}
    >
      <div style={{ marginBottom: 48, textAlign: 'center' }}>
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 20, color: theme.accent, letterSpacing: '0.2em' }}>
          INCIDENT CHRONOLOGY
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 44, color: theme.foreground, fontWeight: 700, marginTop: 8 }}>
          The Containment Failure Timeline
        </div>
      </div>

      <div style={{ display: 'flex', gap: 32, maxWidth: 1600, width: '100%', justifyContent: 'space-between' }}>
        {events.map((ev, idx) => {
          const itemProgress = interpolate(frame, [idx * 25, idx * 25 + 20], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={idx}
              style={{
                flex: 1,
                backgroundColor: theme.surface,
                border: `1px solid ${itemProgress > 0.5 ? theme.cyan : theme.surfaceBorder}`,
                borderRadius: 12,
                padding: '28px 24px',
                opacity: itemProgress,
                transform: `translateY(${(1 - itemProgress) * 20}px)`,
                boxShadow: itemProgress > 0.5 ? `0 10px 30px rgba(0, 240, 255, 0.15)` : 'none',
              }}
            >
              <div
                style={{
                  fontFamily: theme.monoFontFamily,
                  fontSize: 26,
                  fontWeight: 700,
                  color: theme.accent,
                  marginBottom: 12,
                }}
              >
                {ev.time}
              </div>
              <div
                style={{
                  fontFamily: theme.fontFamily,
                  fontSize: 22,
                  fontWeight: 700,
                  color: theme.foreground,
                  marginBottom: 8,
                }}
              >
                {ev.title}
              </div>
              <div
                style={{
                  fontFamily: theme.fontFamily,
                  fontSize: 16,
                  color: theme.muted,
                  lineHeight: 1.5,
                }}
              >
                {ev.desc}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
