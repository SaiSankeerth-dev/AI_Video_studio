import React from 'react';
import { Composition } from 'remotion';
import { BenchmarkAstra60s } from './compositions/BenchmarkAstra60s';
import { BenchmarkCIA60s } from './compositions/BenchmarkCIA60s';
import { CIADocumentary } from './compositions/CIADocumentary';
import { BenchmarkMitnick60s } from './compositions/BenchmarkMitnick60s';
import { MitnickDocumentary } from './compositions/MitnickDocumentary';
import { FernDocumentary } from './compositions/FernDocumentary';
import { YouTubeDocumentary } from './compositions/YouTubeDocumentary';

export const Root: React.FC = () => {
  return (
    <>
      {/* Video 003: GPT-6 Astra 60-Second Master Visual Benchmark */}
      <Composition
        id="BenchmarkAstra60s"
        component={BenchmarkAstra60s}
        durationInFrames={1800}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Video 003: 60-Second Master Visual Pilot (CWA / CIA Breach) */}
      <Composition
        id="BenchmarkCIA60s"
        component={BenchmarkCIA60s}
        durationInFrames={1800}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Video 003: "The Teenager Who Hacked the CIA" (Full Documentary) */}
      <Composition
        id="CIADocumentary"
        component={CIADocumentary}
        durationInFrames={5383}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Video 002: 60-Second Master Visual Benchmark */}
      <Composition
        id="BenchmarkMitnick60s"
        component={BenchmarkMitnick60s}
        durationInFrames={1800}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Video 002: "The Hacker Who Didn't Need Your Password" Full Documentary */}
      <Composition
        id="MitnickDocumentary"
        component={MitnickDocumentary}
        durationInFrames={4758}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Video 001: Fern-Style AI Agents Master Documentary */}
      <Composition
        id="FernDocumentary"
        component={FernDocumentary}
        durationInFrames={4285}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* YouTube Dynamic Documentary */}
      <Composition
        id="YouTubeDocumentary"
        component={YouTubeDocumentary}
        durationInFrames={4078}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
