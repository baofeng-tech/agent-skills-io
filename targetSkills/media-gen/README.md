# Media Gen 🎬

Generate images and videos through AIsa with a single API key.

This skill supports multiple AIsa media-generation models across the
endpoint shapes they actually require, while the bundled client handles
routing for you.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible
harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**,
**Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and
other tools that implement the
[Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Supported models

### Image generation

- `gemini-3-pro-image-preview` — via `POST /v1/models/{model}:generateContent`
- `wan2.7-image`, `wan2.7-image-pro` — via `POST /v1/chat/completions`
- `seedream-4-5-251128` — via `POST /v1/images/generations`

### Video generation

- `wan2.6-t2v`, `wan2.7-t2v` — text-to-video
- `wan2.6-i2v` — image-to-video using `input.img_url`
- `wan2.7-i2v` — image-to-video using `input.media[]`

> The `wan2.7-i2v` schema differs from `wan2.6-i2v`. The bundled client
> handles this automatically when you pass `--img-url`.

## Quick start

```bash
export AISA_API_KEY="your-key"
```

### Generate an image

```bash
# Gemini
python scripts/media_gen_client.py image \
  --model gemini-3-pro-image-preview \
  --prompt "A cute red panda, cinematic lighting" \
  --out out.png

# Wan 2.7 (pro = higher fidelity)
python scripts/media_gen_client.py image \
  --model wan2.7-image-pro \
  --prompt "Ultra-detailed product shot, studio lighting" \
  --out out.png

# Seedream (requires at least 3,686,400 pixels)
python scripts/media_gen_client.py image \
  --model seedream-4-5-251128 \
  --prompt "Neo-noir detective portrait" \
  --size 2048x2048 \
  --out out.png
```

### Generate a video

```bash
# Text-to-video
python scripts/media_gen_client.py video-create \
  --model wan2.7-t2v \
  --prompt "Sweeping shot of a neon cyberpunk skyline"

# Image-to-video
python scripts/media_gen_client.py video-create \
  --model wan2.7-i2v \
  --prompt "gentle camera push-in" \
  --img-url "https://example.com/reference.jpg" \
  --duration 5
```

### Poll and download

```bash
python scripts/media_gen_client.py video-status --task-id <task_id>

python scripts/media_gen_client.py video-wait \
  --task-id <task_id> --poll 10 --timeout 600

python scripts/media_gen_client.py video-wait \
  --task-id <task_id> --download --out out.mp4
```

## Notes

- Wan 2.7 image generation expects `messages[].content` as an array of
  typed parts, not a plain string.
- Seedream enforces a minimum output size of `3,686,400` pixels.
- Video generation is asynchronous; create a task first, then poll or
  wait for completion.

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the
full endpoint catalog used by this skill.
