import React from 'react';
import {Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import {fade} from '@remotion/transitions/fade';
import {TransitionSeries, linearTiming} from '@remotion/transitions';

import {normalizeManifest} from './manifestData';
import {ScreenSlide} from './ScreenSlide';
import {VideoManifestInput} from './videoManifest';

const resolveSrc = (src: string): string => {
  if (src.startsWith('/')) {
    return staticFile(src.slice(1));
  }
  return src;
};

export const WalkthroughComposition: React.FC<{
  manifest?: VideoManifestInput;
  bgmSrc?: string;
  bgmVolume?: number;
}> = ({manifest, bgmSrc, bgmVolume = 0.08}) => {
  const scenes = normalizeManifest(manifest);
  const {fps} = useVideoConfig();

  const totalFrames = scenes.reduce((acc, scene) => acc + Math.round(scene.durationSec * fps), 0);

  return (
    <>
      {bgmSrc ? (
        <Sequence durationInFrames={totalFrames}>
          <Audio src={resolveSrc(bgmSrc)} volume={bgmVolume} />
        </Sequence>
      ) : null}

      <TransitionSeries>
        {scenes.map((scene, index) => {
          const durationInFrames = Math.round(scene.durationSec * fps);

          return (
            <React.Fragment key={scene.id}>
              <TransitionSeries.Sequence durationInFrames={durationInFrames}>
                <ScreenSlide
                  imageSrc={scene.imageSrc}
                  title={scene.title}
                  description={scene.description}
                  audioSrc={scene.audioSrc}
                />
              </TransitionSeries.Sequence>
              {index < scenes.length - 1 ? (
                <TransitionSeries.Transition
                  presentation={fade()}
                  timing={linearTiming({durationInFrames: 20})}
                />
              ) : null}
            </React.Fragment>
          );
        })}
      </TransitionSeries>
    </>
  );
};
