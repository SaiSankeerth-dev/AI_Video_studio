import React from 'react';
import { interpolate, useCurrentFrame, staticFile } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface ImageSceneProps {
  imageSrc: string;
  title?: string;
  totalFrames: number;
}

export const ImageScene: React.FC<ImageSceneProps> = ({ imageSrc, title, totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 15), fadeOut(frame, totalFrames, 15));
  const scale = interpolate(frame, [0, totalFrames], [1.0, 1.08]);

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        position: 'relative',
        overflow: 'hidden',
        opacity,
      }}
    >
      <img
        src={staticFile(imageSrc)}
        alt="Scene visual"
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${scale})`,
        }}
      />
      {/* Dark Vignette Overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at center, transparent 40%, rgba(7,7,7,0.85) 100%)',
          pointerEvents: 'none',
        }}
      />
      {title && (
        <div
          style={{
            position: 'absolute',
            top: 60,
            left: 80,
            fontFamily: theme.monoFontFamily,
            fontSize: 22,
            fontWeight: 700,
            color: theme.cyan,
            letterSpacing: '0.15em',
            background: theme.surfaceGlass,
            padding: '10px 24px',
            borderRadius: 6,
            border: `1px solid ${theme.surfaceBorder}`,
          }}
        >
          {title}
        </div>
      )}
    </div>
  );
};
