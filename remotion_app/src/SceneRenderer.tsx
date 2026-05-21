import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {VideoScene} from './videoManifest';

const palette = {
  bg: '#05070a',
  text: '#f2f4f7',
  muted: '#9ba4b2',
  amber: '#f5a623',
  panel: 'rgba(10, 14, 20, 0.62)',
};

const GridBg: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: palette.bg,
        backgroundImage:
          'linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)',
        backgroundSize: '48px 48px',
      }}
    />
  );
};

const HeadlineBlock: React.FC<{headline?: string; subtext?: string; align?: 'left' | 'center'}> = ({
  headline,
  subtext,
  align = 'left',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const opacity = spring({frame: frame - 6, fps, config: {damping: 100}});
  const y = interpolate(frame, [0, 20], [16, 0], {extrapolateRight: 'clamp'});

  return (
    <div
      style={{
        position: 'absolute',
        left: align === 'left' ? 80 : 0,
        right: align === 'left' ? 80 : 0,
        bottom: 72,
        opacity,
        transform: `translateY(${y}px)`,
        textAlign: align,
      }}
    >
      {headline ? (
        <h1
          style={{
            margin: 0,
            color: palette.text,
            fontSize: 68,
            lineHeight: 1.05,
            fontFamily: 'system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif',
            letterSpacing: '-0.02em',
            textShadow: '0 4px 28px rgba(0,0,0,0.5)',
          }}
        >
          {headline}
        </h1>
      ) : null}
      {subtext ? (
        <p
          style={{
            marginTop: 18,
            marginBottom: 0,
            color: palette.muted,
            fontSize: 34,
            lineHeight: 1.25,
            fontFamily: 'system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif',
            maxWidth: align === 'left' ? 1320 : 1440,
            marginLeft: align === 'left' ? 0 : 'auto',
            marginRight: align === 'left' ? 0 : 'auto',
          }}
        >
          {subtext}
        </p>
      ) : null}
    </div>
  );
};

const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        'radial-gradient(circle at center, rgba(0,0,0,0.0) 20%, rgba(0,0,0,0.45) 100%)',
    }}
  />
);

const resolveImageSrc = (src: string): string => {
  if (src.startsWith('/')) {
    return staticFile(src.slice(1));
  }
  return src;
};

const ImageScene: React.FC<{scene: VideoScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  if (!scene.imageSrc) return null;
  const zoom = 1 + frame * 0.0008;
  const x = Math.sin(frame * 0.02) * 6;

  return (
    <>
      <Img
        src={resolveImageSrc(scene.imageSrc)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${zoom}) translateX(${x}px)`,
        }}
      />
      <Vignette />
      <HeadlineBlock headline={scene.headline} subtext={scene.subtext} />
    </>
  );
};

const EditorialScene: React.FC<{scene: VideoScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pulse = 0.5 + 0.5 * Math.sin((frame / fps) * Math.PI * 0.5);

  return (
    <>
      <GridBg />
      <div
        style={{
          position: 'absolute',
          top: 120,
          left: 80,
          color: palette.amber,
          fontSize: 22,
          letterSpacing: '0.18em',
          fontFamily: 'system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif',
          opacity: 0.7,
        }}
      >
        AI BUSINESS PLAYBOOK
      </div>
      <div
        style={{
          position: 'absolute',
          right: 100,
          top: 130,
          width: 10,
          height: 10,
          borderRadius: '50%',
          backgroundColor: palette.amber,
          boxShadow: `0 0 24px rgba(245,166,35,${0.3 + pulse * 0.5})`,
        }}
      />
      <HeadlineBlock headline={scene.headline} subtext={scene.subtext} />
    </>
  );
};

const DiagramScene: React.FC<{scene: VideoScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const halo = 180 + Math.sin(frame * 0.05) * 22;

  return (
    <>
      <ImageScene scene={scene} />
      <div
        style={{
          position: 'absolute',
          width: halo,
          height: halo,
          right: 110,
          top: 110,
          border: '2px solid rgba(245,166,35,0.9)',
          borderRadius: '50%',
          boxShadow: '0 0 24px rgba(245,166,35,0.45)',
          opacity: 0.72,
        }}
      />
    </>
  );
};

const ChecklistScene: React.FC<{scene: Extract<VideoScene, {visualType: 'minimal-checklist'}>}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <>
      <GridBg />
      <HeadlineBlock headline={scene.headline} subtext={scene.subtext} />
      <div
        style={{
          position: 'absolute',
          left: 80,
          top: 260,
          background: palette.panel,
          border: '1px solid rgba(245,166,35,0.2)',
          borderRadius: 16,
          padding: '24px 30px',
          width: 900,
          backdropFilter: 'blur(8px)',
        }}
      >
        {scene.checklist.map((item, index) => {
          const appear = spring({
            frame: frame - index * (fps * 0.8),
            fps,
            config: {damping: 100},
          });

          return (
            <div
              key={item}
              style={{
                opacity: appear,
                transform: `translateY(${(1 - appear) * 14}px)`,
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                marginBottom: 16,
                fontSize: 34,
                color: palette.text,
                fontFamily: 'system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif',
              }}
            >
              <span style={{color: palette.amber}}>▢</span>
              <span>{item}</span>
            </div>
          );
        })}
      </div>
    </>
  );
};

const EndCardScene: React.FC<{scene: Extract<VideoScene, {visualType: 'end-card'}>}> = ({scene}) => {
  return (
    <>
      <GridBg />
      <div
        style={{
          position: 'absolute',
          inset: 80,
          border: '1px solid rgba(245,166,35,0.26)',
          borderRadius: 24,
          background: 'rgba(10, 14, 20, 0.4)',
          backdropFilter: 'blur(10px)',
        }}
      />
      <HeadlineBlock headline={scene.headline} subtext={scene.subtext} align="center" />
      {scene.cta ? (
        <p
          style={{
            position: 'absolute',
            left: 180,
            right: 180,
            bottom: 160,
            textAlign: 'center',
            color: palette.muted,
            fontSize: 30,
            lineHeight: 1.3,
            fontFamily: 'system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif',
          }}
        >
          {scene.cta}
        </p>
      ) : null}
    </>
  );
};

export const SceneRenderer: React.FC<{scene: VideoScene}> = ({scene}) => {
  return (
    <AbsoluteFill style={{backgroundColor: palette.bg}}>
      {scene.visualType === 'image-card' ? <ImageScene scene={scene} /> : null}
      {scene.visualType === 'editorial-title' ? <EditorialScene scene={scene} /> : null}
      {scene.visualType === 'diagram-highlight' ? <DiagramScene scene={scene} /> : null}
      {scene.visualType === 'minimal-checklist' ? <ChecklistScene scene={scene} /> : null}
      {scene.visualType === 'end-card' ? <EndCardScene scene={scene} /> : null}
    </AbsoluteFill>
  );
};
