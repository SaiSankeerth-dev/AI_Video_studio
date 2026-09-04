import { interpolate, spring } from 'remotion';

export const FPS = 30;

export const secondsToFrames = (seconds: number): number => Math.round(seconds * FPS);
export const framesToSeconds = (frames: number): number => frames / FPS;

export const fadeIn = (frame: number, durationFrames = 15): number => {
  return interpolate(frame, [0, durationFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

export const fadeOut = (frame: number, totalFrames: number, durationFrames = 15): number => {
  return interpolate(frame, [totalFrames - durationFrames, totalFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

export const getSpringScale = (frame: number, fps = FPS): number => {
  return spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100, mass: 0.8 },
  });
};
