import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { theme } from '../styles/theme';

interface KineticCaptionProps {
  words: string[];
  highlightWords: string[];
  totalFrames: number;
}

export const KineticCaption: React.FC<KineticCaptionProps> = ({
  words,
  highlightWords,
  totalFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!words || words.length === 0) return null;

  // Active word index calculation based on frame progress
  const wordDuration = totalFrames / words.length;
  const activeIndex = Math.min(Math.floor(frame / wordDuration), words.length - 1);

  // Fade in / out container
  const containerOpacity = interpolate(
    frame,
    [0, 6, totalFrames - 6, totalFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 70,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 80px',
        opacity: containerOpacity,
        zIndex: 100,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          background: 'rgba(10, 10, 14, 0.88)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(0, 240, 255, 0.25)',
          borderRadius: 16,
          padding: '18px 36px',
          maxWidth: 1500,
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '12px 14px',
          boxShadow: '0 12px 40px rgba(0,0,0,0.85), inset 0 0 15px rgba(0,240,255,0.05)',
        }}
      >
        {words.map((word, idx) => {
          const isActive = idx === activeIndex;
          const isPast = idx < activeIndex;
          const isHighlight = highlightWords.some(hw =>
            word.toLowerCase().includes(hw.toLowerCase().replace(/[^a-z0-9]/g, ''))
          );

          // Spring bounce for active word
          const wordFrame = frame - idx * wordDuration;
          const scale = isActive
            ? spring({
                frame: Math.max(0, wordFrame),
                fps,
                config: { damping: 12, stiffness: 220, mass: 0.6 },
              }) * 0.18 + 1.0
            : 1.0;

          // Color selection
          let wordColor = 'rgba(240, 240, 245, 0.85)';
          if (isActive) {
            wordColor = isHighlight ? theme.terminalAmber : theme.cyan;
          } else if (isPast) {
            wordColor = isHighlight ? '#FFD700' : '#FFFFFF';
          } else {
            wordColor = 'rgba(180, 180, 195, 0.55)';
          }

          return (
            <span
              key={idx}
              style={{
                fontFamily: theme.fontFamily,
                fontSize: isActive ? 38 : 34,
                fontWeight: isActive || isHighlight ? 800 : 600,
                color: wordColor,
                transform: `scale(${scale})`,
                display: 'inline-block',
                textShadow: isActive
                  ? `0 0 20px ${isHighlight ? theme.terminalAmber : theme.cyan}`
                  : '0 2px 6px rgba(0,0,0,0.8)',
                letterSpacing: '-0.01em',
                transition: 'color 0.1s ease',
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
