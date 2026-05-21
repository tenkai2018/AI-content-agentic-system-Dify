import {VideoManifest, VideoManifestInput, VideoScene, RawManifestScene} from './videoManifest';

export const defaultManifest: VideoManifest = [
  {
    id: 'scene-01',
    title: 'Intro Hook',
    description: 'Most people still use AI like a better search engine.',
    imageSrc: '/assets/codex-computer-use.png',
    audioSrc: '/assets/sample/scene_1.mp3',
    durationSec: 8,
    visualType: 'image-card',
  },
  {
    id: 'scene-02',
    title: 'The Missed Opportunity',
    description: 'The real leverage is workflow automation and closed loops.',
    imageSrc: '/assets/closed-loop-vs-open-loop.png',
    audioSrc: '/assets/sample/scene_2.mp3',
    durationSec: 8,
    visualType: 'image-card',
  },
  {
    id: 'scene-03',
    title: 'Outcome',
    description: 'Build an AI operating layer for your business.',
    imageSrc: '/assets/your-business-needs-an-ai-powered-os.png',
    audioSrc: '/assets/sample/scene_3.mp3',
    durationSec: 8,
    visualType: 'image-card',
  },
];

const normalizeScene = (scene: RawManifestScene, index: number): VideoScene => {
  const duration = scene.durationSec ?? scene.duration_in_seconds ?? 4;
  const visualType = (scene.visualType ?? scene.visual_type ?? 'image-card') as VideoScene['visualType'];

  const base = {
    id: scene.id ?? String(index + 1),
    title: scene.title ?? `Scene ${index + 1}`,
    description: scene.description ?? '',
    imageSrc: scene.imageSrc ?? scene.image_src,
    audioSrc: scene.audioSrc ?? scene.audio_src,
    durationSec: duration > 0 ? duration : 4,
  };

  switch (visualType) {
    case 'minimal-checklist':
      return {
        ...base,
        visualType: 'minimal-checklist',
        headline: scene.headline ?? scene.title,
        subtext: scene.subtext ?? scene.description,
        checklist: scene.checklist ?? [],
      };
    case 'end-card':
      return {
        ...base,
        visualType: 'end-card',
        headline: scene.headline ?? scene.title,
        subtext: scene.subtext ?? scene.description,
        cta: scene.cta,
      };
    case 'editorial-title':
      return {
        ...base,
        visualType: 'editorial-title',
        headline: scene.headline ?? scene.title,
        subtext: scene.subtext ?? scene.description,
      };
    case 'diagram-highlight':
      return {
        ...base,
        visualType: 'diagram-highlight',
        headline: scene.headline ?? scene.title,
        subtext: scene.subtext ?? scene.description,
      };
    case 'image-card':
    default:
      return {
        ...base,
        visualType: 'image-card',
        headline: scene.headline ?? scene.title,
        subtext: scene.subtext ?? scene.description,
      };
  }
};

export const normalizeManifest = (input: VideoManifestInput): VideoManifest => {
  if (!input) {
    return defaultManifest;
  }

  if (Array.isArray(input)) {
    return input.map((scene, i) => normalizeScene(scene, i));
  }

  const raw = input.screens ?? input.manifest ?? [];
  if (!raw.length) {
    return defaultManifest;
  }

  return raw.map((scene, i) => normalizeScene(scene, i));
};

export const getManifestDurationInFrames = (manifestInput: VideoManifestInput, fps: number): number => {
  const manifest = normalizeManifest(manifestInput);
  const transitionFrames = manifest.length > 1 ? (manifest.length - 1) * 20 : 0;
  const sceneFrames = manifest.reduce((acc, scene) => acc + Math.round(scene.durationSec * fps), 0);
  return Math.max(sceneFrames + transitionFrames, fps * 2);
};
