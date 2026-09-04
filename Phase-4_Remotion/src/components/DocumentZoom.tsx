import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { theme } from '../styles/theme';
import { fadeIn, fadeOut } from '../lib/timeline';

interface DocumentZoomProps {
  documentTitle: string;
  sourceId: string;
  highlightedText: string;
  surroundingContext?: string;
  totalFrames?: number;
}

export const DocumentZoom: React.FC<DocumentZoomProps> = ({
  documentTitle,
  sourceId,
  highlightedText,
  surroundingContext = 'INTERNAL SYSTEM AUDIT LOG // CONFIDENTIAL // RESTRICTED ACCESS',
  totalFrames = 150,
}) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(fadeIn(frame, 10), fadeOut(frame, totalFrames, 10));
  const scale = interpolate(frame, [0, totalFrames], [1.0, 1.12], { extrapolateRight: 'clamp' });

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: theme.background,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '50px 80px',
        opacity,
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: 1050,
          backgroundColor: '#FAFAF8',
          color: '#1A1A1A',
          padding: 60,
          borderRadius: 4,
          boxShadow: '0 25px 70px rgba(0, 0, 0, 0.7)',
          transform: `scale(${scale})`,
          position: 'relative',
        }}
      >
        {/* Header stamp */}
        <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '2px solid #D0D0CE', paddingBottom: 16, marginBottom: 30 }}>
          <div>
            <div style={{ fontFamily: theme.monoFontFamily, fontSize: 13, fontWeight: 700, color: '#C92A2A', letterSpacing: '0.15em' }}>
              EXHIBIT FORENSIC DOCUMENT
            </div>
            <div style={{ fontFamily: theme.fontFamily, fontSize: 24, fontWeight: 800, color: '#1A1A1A', marginTop: 4 }}>
              {documentTitle}
            </div>
          </div>
          <div style={{ textAlign: 'right', fontFamily: theme.monoFontFamily, fontSize: 13, color: '#666' }}>
            ID: {sourceId}
          </div>
        </div>

        {/* Surrounding Context */}
        <div style={{ fontFamily: theme.monoFontFamily, fontSize: 14, color: '#888', marginBottom: 24 }}>
          {surroundingContext}
        </div>

        {/* Highlighted text block */}
        <div
          style={{
            backgroundColor: 'rgba(255, 224, 102, 0.45)',
            borderLeft: '4px solid #E67700',
            padding: '20px 24px',
            fontFamily: theme.fontFamily,
            fontSize: 26,
            fontWeight: 700,
            lineHeight: 1.4,
            color: '#1A1A1A',
          }}
        >
          "{highlightedText}"
        </div>
      </div>
    </div>
  );
};
