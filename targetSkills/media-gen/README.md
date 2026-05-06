# Media Gen 🎬

Generate images and videos with AIsa using a single API key.

This skill covers the bundled client and the underlying AIsa endpoints for Gemini image generation, Wan image generation, Seedream image generation, and Wan video generation.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness: **Claude Code**, **Claude**, **OpenAI Codex**, **Cursor**, **Gemini CLI**, **OpenCode**, **Goose**, **OpenClaw**, **Hermes**, and others that implement the [Agent Skills specification](https://agentskills.io/specification).

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## Use when

- You want one AIsa skill for both image and video generation
- You need to switch between Gemini, Wan, and Seedream image models
- You want the bundled client to route each model to the correct endpoint automatically
- You need to create, poll, and download async Wan video jobs

## Supported models

### Image (4 models across 3 endpoints)

- `gemini-3-pro-image-preview` (Google) — via `POST /v1/models/{model}:generateContent`
- `wan2.7-image`, `wan2.7-image-pro` (Alibaba) — via `POST /v1/chat/completions`
- `seedream-4-5-251128` (ByteDance) — via `POST /v1/images/generations` with a minimum of 3,686,400 pixels

### Video (4 Wan variants on 1 async endpoint)

- `wan2.6-t2v`, `wan2.7-t2v` — text-to-video
- `wan2.6-i2v` — image-to-video using `input.img_url`
- `wan2.7-i2v` — image-to-video using `input.media[]`

The client handles the field-name difference for image-to-video requests when you pass `--img-url`.

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

# Seedream (needs ≥ 3,686,400 px)
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

### Poll the task and download

```bash
python scripts/media_gen_client.py video-status --task-id <task_id>

python scripts/media_gen_client.py video-wait \
  --task-id <task_id> --poll 10 --timeout 600

python scripts/media_gen_client.py video-wait \
  --task-id <task_id> --download --out out.mp4
```

## API reference

See the [AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog of endpoints this skill uses.
