import './index.css';
import {Composition} from 'remotion';
import {WalkthroughComposition} from './WalkthroughComposition';
import {defaultManifest, getManifestDurationInFrames} from './manifestData';
import {VideoManifestInput} from './videoManifest';

export const RemotionRoot: React.FC = () => {
  const fps = 30;

  return (
    <>
      <Composition
        id="WalkthroughVideo"
        component={WalkthroughComposition}
        durationInFrames={getManifestDurationInFrames(defaultManifest, fps)}
        fps={fps}
        width={1080}
        height={1920}
        defaultProps={{
          manifest: defaultManifest,
          bgmSrc: '/audio/bgm/bgm.mp3',
          bgmVolume: 0.08,
        }}
        calculateMetadata={({props}) => {
          const p = props as {manifest?: VideoManifestInput};
          return {
            durationInFrames: getManifestDurationInFrames(p.manifest, fps),
          };
        }}
      />
    </>
  );
};
