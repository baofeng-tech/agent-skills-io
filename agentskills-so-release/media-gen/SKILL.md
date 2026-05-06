---
name: media-gen
description: 'Generate images and videos with AIsa using one API key. Supports Gemini image generation, Wan 2.7 image and image-pro, ByteDance Seedream, and four Wan video variants through the bundled client, which routes each model to the correct endpoint automatically. Use when: the user needs AI image or video generation workflows.'
license: MIT
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, curl, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.0
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills-so
  tags: media,video,image,aisa
  platforms: agentskills.io,agentskills.so,github
  primary_env: AISA_API_KEY
allowed-tools: Read Bash Grep
---

# Media Gen 🎬

Generate images and videos with AIsa using a single API key.

This skill covers the bundled client and the underlying AIsa endpoints for:

- Google Gemini image generation
- Alibaba Wan 2.7 image generation
- ByteDance Seedream image generation
- Wan 2.6 / 2.7 text-to-video and image-to-video generation

The included client automatically routes each supported model to the correct endpoint and handles the response format differences between image and video APIs.

## Use when

- You want one skill for both image and video generation through AIsa
- You need to switch between Gemini, Wan, and Seedream image models
- You want a simple CLI that hides endpoint-specific request differences
- You need to create Wan video jobs and then poll or download the result

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- and other tools that implement the [Agent Skills specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

Get an API key at [aisa.one](https://aisa.one).

## What you can do

### Image — Gemini
```text
"Generate a cyberpunk-style city nightscape, neon lights, rainy night, cinematic feel"
```

### Image — Wan 2.7
```text
"Generate an ultra-detailed product shot of a red panda, studio lighting, sharp focus"
```

### Image — Seedream
```text
"Generate a 2048×2048 magazine cover: neo-noir detective portrait, film grain"
```

### Video — text-to-video
```text
"Sweeping establishing shot of a neon cyberpunk skyline at dusk, 5 seconds"
```

### Video — image-to-video
```text
"Starting from this reference image, gentle camera push-in with parallax"
```

## Supported models

### Image generation — 4 models across 3 endpoints

| Model | Developer | Endpoint | Notes |
|---|---|---|---|
| `gemini-3-pro-image-preview` | Google | `POST /v1/models/{model}:generateContent` | Returns image data in `candidates[].parts[].inline_data` |
| `wan2.7-image` | Alibaba | `POST /v1/chat/completions` | Returns image URLs in `choices[].message.content[]` parts with `type="image"` |
| `wan2.7-image-pro` | Alibaba | `POST /v1/chat/completions` | Higher-fidelity Wan image variant |
| `seedream-4-5-251128` | ByteDance | `POST /v1/images/generations` | OpenAI-compatible image generation; minimum 3,686,400 pixels |

### Video generation — 4 Wan variants on 1 async endpoint

| Model | Kind | Image field | Output SR |
|---|---|---|---|
| `wan2.6-t2v` | text-to-video | *none* | 1080 |
| `wan2.6-i2v` | image-to-video | `input.img_url` (string) | 720 |
| `wan2.7-t2v` | text-to-video | *none* | 720 |
| `wan2.7-i2v` | image-to-video | `input.media` (array) | 720 |

> **Schema note for `wan2.7-i2v`:** it expects the reference image in `input.media`, not `input.img_url`. The bundled client handles this automatically when you pass `--img-url`.

## Quick start

```bash
export AISA_API_KEY="your-key"

# Any image model — the client routes to the correct endpoint
python3 scripts/media_gen_client.py image \
  --model gemini-3-pro-image-preview \
  --prompt "A cute red panda, cinematic lighting" \
  --out out.png

python3 scripts/media_gen_client.py image \
  --model wan2.7-image-pro \
  --prompt "Ultra-detailed product shot of a red panda" \
  --out out.png

python3 scripts/media_gen_client.py image \
  --model seedream-4-5-251128 \
  --prompt "Neo-noir detective portrait, film grain" \
  --size 2048x2048 \
  --out out.png

# Video — text-to-video
python3 scripts/media_gen_client.py video-create \
  --model wan2.7-t2v \
  --prompt "Sweeping shot of a neon cyberpunk skyline"

# Video — image-to-video
python3 scripts/media_gen_client.py video-create \
  --model wan2.7-i2v \
  --prompt "gentle zoom with parallax" \
  --img-url "https://example.com/reference.jpg" \
  --duration 5

# Wait and download
python3 scripts/media_gen_client.py video-wait \
  --task-id <task_id> --download --out out.mp4
```

---

## Image generation endpoint reference

### Gemini family → `POST /v1/models/{model}:generateContent`

Documentation: [Google Gemini Chat](https://aisa.one/docs/api-reference/chat/generatecontent)

```bash
curl -X POST "https://api.aisa.one/v1/models/gemini-3-pro-image-preview:generateContent" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents":[
      {"role":"user","parts":[{"text":"A cute red panda, cinematic lighting"}]}
    ]
  }'
```

Response includes `candidates[].parts[].inline_data` with `{mime_type, data}`, where `data` is base64-encoded image content.

### Wan 2.7 family → `POST /v1/chat/completions`

Documentation: [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation)

**Important:** `messages[].content` must be an array of typed parts. A plain string returns HTTP 400 `invalid_parameter_error`.

```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.7-image",
    "messages": [
      {"role":"user","content":[
        {"type":"text","text":"A cute red panda, ultra-detailed, cinematic lighting"}
      ]}
    ],
    "n": 1
  }'
```

Images are returned as `{type: "image", image: "<url>"}` parts inside `choices[].message.content[]`.

### Seedream → `POST /v1/images/generations`

Documentation: [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations)

```bash
curl -X POST "https://api.aisa.one/v1/images/generations" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedream-4-5-251128",
    "prompt": "A cute red panda, ultra-detailed, cinematic lighting",
    "n": 1,
    "size": "2048x2048"
  }'
```

Response: `data[].url` or `data[].b64_json`.

Upstream enforces a minimum of 3,686,400 pixels. For example, `1024×1024` and `1536×1536` are rejected, while any aspect ratio is allowed if `width × height ≥ 3,686,400`.

---

## Video generation endpoint reference

### Create task → `POST /apis/v1/services/aigc/video-generation/video-synthesis`

Documentation: [Create video generation task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis)

The `X-DashScope-Async: enable` header is required.

```bash
# wan2.6-t2v — text-to-video
curl -X POST "https://api.aisa.one/apis/v1/services/aigc/video-generation/video-synthesis" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model":"wan2.6-t2v",
    "input":{"prompt":"cinematic close-up, slow push-in"},
    "parameters":{"resolution":"720P","duration":5}
  }'

# wan2.7-i2v — image-to-video
curl -X POST "https://api.aisa.one/apis/v1/services/aigc/video-generation/video-synthesis" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model":"wan2.7-i2v",
    "input":{
      "prompt":"gentle zoom with parallax",
      "media":["https://example.com/reference.jpg"]
    },
    "parameters":{"resolution":"720P","duration":5}
  }'
```

### Poll task → `GET /apis/v1/services/aigc/tasks/{task_id}`

Documentation: [Get video generation task result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks)

> `task_id` is a path parameter. The query-string form `?task_id=...` returns HTTP 500 `unsupported uri`.

```bash
curl "https://api.aisa.one/apis/v1/services/aigc/tasks/YOUR_TASK_ID" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

## Bundled Python client

The client at `scripts/media_gen_client.py` auto-routes each image model to the correct endpoint and normalizes the result to a saved file where applicable.

```bash
# Image — model selection determines the endpoint
python3 scripts/media_gen_client.py image \
  --model <gemini-3-pro-image-preview | wan2.7-image | wan2.7-image-pro | seedream-4-5-251128> \
  --prompt "..." \
  --out out.png

# Video — create task
python3 scripts/media_gen_client.py video-create \
  --model <wan2.6-t2v | wan2.6-i2v | wan2.7-t2v | wan2.7-i2v> \
  --prompt "..." \
  [--img-url https://... (required for -i2v models)] \
  [--duration 5|10] \
  [--resolution 720P|1080P]

# Video — poll / wait / download
python3 scripts/media_gen_client.py video-status --task-id <id>
python3 scripts/media_gen_client.py video-wait --task-id <id> --poll 10 --timeout 600
python3 scripts/media_gen_client.py video-wait --task-id <id> --download --out out.mp4
```

## API reference

This skill calls the following AIsa endpoints directly:

- [Google Gemini Chat — `generateContent`](https://aisa.one/docs/api-reference/chat/generatecontent) — Gemini image models
- [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation) — Wan 2.7 image family
- [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations) — Seedream
- [Create video generation task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis) — all 4 Wan video variants
- [Get video generation task result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks) — async polling

See the [full AIsa API Reference](https://aisa.one/docs/api-reference) for the complete catalog.

## License

MIT — see [LICENSE](../LICENSE) at the repo root.
