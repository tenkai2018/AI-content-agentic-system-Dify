# Video Generation with Remotion (Clean UTF-8)

## 1. Purpose
Remotion app nh?n manifest d?ng t? backend d? render video d?c (1080x1920), g?m:
- Hình ?nh theo scene
- Voiceover theo scene
- Nh?c n?n ch?y toàn timeline

## 2. Manifest Contract (v1)
Backend ghi `manifest.json` trong thu m?c task:
- `remotion_app/public/assets/generated/{task_id}/manifest.json`

Format chính:
```json
{
  "task_id": "...",
  "screens": [
    {
      "id": "1",
      "title": "Scene 1",
      "description": "...",
      "image_src": "/assets/generated/{task_id}/scene_1.png",
      "audio_src": "/assets/generated/{task_id}/scene_1.mp3",
      "duration_in_seconds": 4.5
    }
  ]
}
```

## 3. Render Flow
1. Backend t?o assets (image + tts)
2. Backend t?o manifest
3. Backend g?i Remotion CLI:
```powershell
npx remotion render WalkthroughVideo public/output_{task_id}.mp4 --props <manifest_path>
```
4. Luu output path vào `video_result`

## 4. Timing Logic
- `Root.tsx` dùng `calculateMetadata` d? tính `durationInFrames` theo manifest th?c t?.
- `WalkthroughComposition.tsx` map t?ng scene theo `durationSec`.
- Transition frame du?c c?ng vào t?ng timeline.

## 5. Audio Logic
- `ScreenSlide.tsx`: phát audio t?ng scene b?ng `<Audio />`
- `WalkthroughComposition.tsx`: phát BGM toàn timeline v?i volume th?p.

## 6. Troubleshooting
- N?u render timeout: ki?m tra assets/manifest h?p l? và tang timeout backend.
- N?u ?nh/audio không load: ki?m tra path trong `public/assets/generated/...`.
- N?u npm không nh?n trong PATH: ch?y b?ng absolute path npm c?a h? th?ng.

