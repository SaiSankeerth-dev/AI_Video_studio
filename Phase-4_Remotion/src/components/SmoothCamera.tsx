import React from 'react';
import { Img, staticFile, useCurrentFrame, interpolate, Easing } from 'remotion';

interface SmoothCameraProps {
  imageSrc: string;
  totalFrames: number;
  direction?: 'zoom-in' | 'zoom-out' | 'pan-right' | 'pan-left' | 'tilt-up';
  scaleRange?: [number, number];
}

export const SmoothCamera: React.FC<SmoothCameraProps> = ({
  imageSrc,
  totalFrames,
  direction = 'zoom-in',
  scaleRange = [1.0, 1.05]
}) => {
  const frame = useCurrentFrame();

  // Mathematically smooth cubic bezier easing across 30fps frames (ZERO JITTER / ZERO SHAKE)
  const progress = interpolate(frame, [0, totalFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.25, 0.1, 0.25, 1.0)
  });

  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;

  switch (direction) {
    case 'zoom-in':
      scale = scaleRange[0] + (scaleRange[1] - scaleRange[0]) * progress;
      break;
    case 'zoom-out':
      scale = scaleRange[1] - (scaleRange[1] - scaleRange[0]) * progress;
      break;
    case 'pan-right':
      scale = 1.04;
      translateX = interpolate(progress, [0, 1], [-15, 15]);
      break;
    case 'pan-left':
      scale = 1.04;
      translateX = interpolate(progress, [0, 1], [15, -15]);
      break;
    case 'tilt-up':
      scale = 1.04;
      translateY = interpolate(progress, [0, 1], [15, -15]);
      break;
  }

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        overflow: 'hidden',
        position: 'relative',
        backgroundColor: '#050508'
      }}
    >
      <Img
        src={staticFile(imageSrc)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${scale.toFixed(4)}) translate3d(${translateX.toFixed(2)}px, ${translateY.toFixed(2)}px, 0px)`,
          willChange: 'transform',
          imageRendering: 'crisp-edges'
        }}
      />
    </div>
  );
};
