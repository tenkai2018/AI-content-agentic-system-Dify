export type BaseVideoScene = {
  id: string;
  title: string;
  description: string;
  imageSrc?: string;
  audioSrc?: string;
  durationSec: number;
};

export type ImageCardScene = BaseVideoScene & {
  visualType: 'image-card';
  headline?: string;
  subtext?: string;
};

export type EditorialTitleScene = BaseVideoScene & {
  visualType: 'editorial-title';
  headline?: string;
  subtext?: string;
};

export type DiagramHighlightScene = BaseVideoScene & {
  visualType: 'diagram-highlight';
  headline?: string;
  subtext?: string;
};

export type MinimalChecklistScene = BaseVideoScene & {
  visualType: 'minimal-checklist';
  headline?: string;
  subtext?: string;
  checklist: string[];
};

export type EndCardScene = BaseVideoScene & {
  visualType: 'end-card';
  headline?: string;
  subtext?: string;
  cta?: string;
};

export type VideoScene =
  | ImageCardScene
  | EditorialTitleScene
  | DiagramHighlightScene
  | MinimalChecklistScene
  | EndCardScene;

export type VideoManifest = VideoScene[];

export type RawManifestScene = {
  id?: string;
  title?: string;
  description?: string;
  imageSrc?: string;
  image_src?: string;
  audioSrc?: string;
  audio_src?: string;
  durationSec?: number;
  duration_in_seconds?: number;
  visualType?: string;
  visual_type?: string;
  headline?: string;
  subtext?: string;
  checklist?: string[];
  cta?: string;
};

export type VideoManifestInput =
  | VideoManifest
  | {
      screens?: RawManifestScene[];
      manifest?: RawManifestScene[];
    }
  | undefined;
