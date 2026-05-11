# Media Gen 🎬

Generate images and videos with AIsa using one API key.

This skill covers Gemini, Wan, and Seedream image generation plus Wan
text-to-video and image-to-video workflows. The bundled client routes
models to the correct endpoint automatically.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible
harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**,
**Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and
other tools that implement the
[Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Supported models

### Image generation

- `gemini-3-pro-image-preview` (Google) — `POST /v1/models/{model}:generateContent`
- `wan2.7-image`, `wan2.7-image-pro` (Alibaba) — `POST /v1/chat/completions`
- `seedream-4-5-251128` (ByteDance) — `POST /v1/images/generations`
  with a minimum of 3,686,400 pixels

### Video generation

- `wan2.6-t2v`, `wan2.7-t2v` — text-to-video
- `wan2.6-i2v` — image-to-video using `input.img_url`
- `wan2.7-i2v` — image-to-video using `input.media[]`
  (the client handles this field difference)

## Quick start

```bash
export AISA_API_KEY="your-key"
```

### Generate an image

```bash
# Gemini
python3 scripts/media_gen_client.py image \
  --model gemini-3-pro-image-preview \
  --prompt "A cute red panda, cinematic lighting" \
  --out out.png

# Wan 2.7
python3 scripts/media_gen_client.py image \
  --model wan2.7-image-pro \
  --prompt "Ultra-detailed product shot, studio lighting" \
  --out out.png

# Seedream (requires >= 3,686,400 pixels)
python3 scripts/media_gen_client.py image \
  --model seedream-4-5-251128 \
  --prompt "Neo-noir detective portrait" \
  --size 2048x2048 \
  --out out.png
```

### Generate a video

```bash
# Text-to-video
python3 scripts/media_gen_client.py video-create \
  --model wan2.7-t2v \
  --prompt "Sweeping shot of a neon cyberpunk skyline"

# Image-to-video
python3 scripts/media_gen_client.py video-create \
  --model wan2.7-i2v \
  --prompt "gentle camera push-in" \
  --img-url "https://example.com/reference.jpg" \
  --duration 5
```

### Poll the task and download

```bash
python3 scripts/media_gen_client.py video-status --task-id <task_id>

python3 scripts/media_gen_client.py video-wait \
  --task-id <task_id> --poll 10 --timeout 600

python3 scripts/media_gen_client.py video-wait \
  --task-id <task_id> --download --out out.mp4
```

## Notes

- The bundled client automatically routes each supported image model to
  the correct AIsa endpoint.
- `wan2.7-i2v` expects `input.media[]`, not `input.img_url`; the client
  maps `--img-url` correctly for you.
- Seedream requests must meet the upstream minimum pixel requirement.

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for
full endpoint details.
