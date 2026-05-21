import React from 'react';
import {AbsoluteFill, Audio, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const resolveSrc = (src: string): string => {
  if (src.startsWith('/')) {
    return staticFile(src.slice(1));
  }
  return src;
};

export const ScreenSlide: React.FC<{
  imageSrc?: string;
  title: string;
  description: string;
  audioSrc?: string;
}> = ({imageSrc, title, description, audioSrc}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: {
      damping: 200,
    },
  });

  const continuousZoom = 1 + frame * 0.001;

  const opacity = spring({
    frame: frame - 15,
    fps,
    config: {
      damping: 100,
    },
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#111', justifyContent: 'center', alignItems: 'center'}}>
      {audioSrc ? <Audio src={resolveSrc(audioSrc)} /> : null}

      {imageSrc ? (
        <Img
          src={resolveSrc(imageSrc)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: `scale(${scale * continuousZoom})`,
          }}
        />
      ) : null}

      <div
        style={{
          position: 'absolute',
          bottom: 40,
          left: 40,
          right: 40,
          opacity,
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          padding: '20px 30px',
          borderRadius: 15,
          color: 'white',
          fontFamily: 'sans-serif',
          backdropFilter: 'blur(10px)',
        }}
      >
        <h2 style={{margin: 0, fontSize: 36, marginBottom: 10}}>{title}</h2>
        <p style={{margin: 0, fontSize: 24, opacity: 0.8}}>{description}</p>
      </div>
    </AbsoluteFill>
  );
};
