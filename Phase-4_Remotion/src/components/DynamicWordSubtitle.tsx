import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';

export interface WordTimestamp {
  word: string;
  start: number; // in seconds
  end: number;   // in seconds
}

interface DynamicWordSubtitleProps {
  words: WordTimestamp[];
  maxWordsPerChunk?: number;
}

export const DynamicWordSubtitle: React.FC<DynamicWordSubtitleProps> = ({
  words,
  maxWordsPerChunk = 6
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Find active word
  const activeWordIdx = words.findIndex(
    (w) => currentTime >= w.start && currentTime <= w.end
  );

  if (activeWordIdx === -1) {
    return null;
  }

  // Find chunk containing active word
  const chunkStartIdx = Math.floor(activeWordIdx / maxWordsPerChunk) * maxWordsPerChunk;
  const currentChunk = words.slice(chunkStartIdx, chunkStartIdx + maxWordsPerChunk);

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 240,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 50px',
        zIndex: 100
      }}
    >
      <div
        style={{
          background: 'rgba(8, 12, 20, 0.82)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(255, 255, 255, 0.12)',
          borderRadius: 14,
          padding: '16px 28px',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '12px',
          maxWidth: 900,
          boxShadow: '0 12px 32px rgba(0, 0, 0, 0.6)'
        }}
      >
        {currentChunk.map((w, idx) => {
          const isCurrent = chunkStartIdx + idx === activeWordIdx;
          const isSpoken = currentTime >= w.end;

          return (
            <span
              key={idx}
              style={{
                fontFamily: 'Inter, system-ui, sans-serif',
                fontSize: 48,
                fontWeight: 800,
                color: isCurrent ? '#F59E0B' : isSpoken ? '#FFFFFF' : 'rgba(255,255,255,0.4)',
                transform: isCurrent ? 'scale(1.08)' : 'scale(1.0)',
                transition: 'transform 0.05s ease-out',
                textShadow: isCurrent
                  ? '0 0 20px rgba(245, 158, 11, 0.7)'
                  : '0 4px 12px rgba(0, 0, 0, 0.8)',
                letterSpacing: '0.02em',
                textTransform: 'uppercase'
              }}
            >
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
