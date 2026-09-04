import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface ChartBar {
  label: string;
  value: number; // 0 to 100
  color?: string;
}

interface DataChartProps {
  title: string;
  subtitle?: string;
  bars: ChartBar[];
  totalFrames?: number;
}

export const DataChart: React.FC<DataChartProps> = ({
  title,
  subtitle,
  bars,
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
        justifyContent: 'center',
        alignItems: 'center',
        padding: '60px 120px',
        opacity,
      }}
    >
      <div style={{ width: '100%', maxWidth: 1000 }}>
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 16, color: theme.cyan, letterSpacing: '0.2em', marginBottom: 8 }}>
          QUANTITATIVE METRIC VERIFICATION
        </div>
        <div style={{ fontFamily: theme.fontFamily, fontSize: 40, fontWeight: 800, color: theme.foreground, marginBottom: 12 }}>
          {title}
        </div>
        {subtitle && (
          <div style={{ fontFamily: theme.fontFamily, fontSize: 18, color: theme.muted, marginBottom: 40 }}>
            {subtitle}
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: 24, marginTop: 30 }}>
          {bars.map((bar, i) => {
            const barProgress = interpolate(frame - (15 + i * 8), [0, 25], [0, bar.value], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });

            return (
              <div key={bar.label} style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: theme.monoFontFamily, fontSize: 16 }}>
                  <span style={{ color: theme.foreground }}>{bar.label}</span>
                  <span style={{ color: bar.color || theme.cyan, fontWeight: 700 }}>
                    {Math.round(barProgress)}%
                  </span>
                </div>
                <div
                  style={{
                    height: 20,
                    width: '100%',
                    backgroundColor: theme.surface,
                    borderRadius: 4,
                    overflow: 'hidden',
                    border: `1px solid ${theme.surfaceBorder}`,
                  }}
                >
                  <div
                    style={{
                      height: '100%',
                      width: `${barProgress}%`,
                      backgroundColor: bar.color || theme.cyan,
                      borderRadius: 3,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
