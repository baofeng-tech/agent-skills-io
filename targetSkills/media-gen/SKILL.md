---
name: media-gen
description: 'Generate images and videos with AIsa using one API key. Supports Gemini image generation, Wan 2.7 image models, Seedream image generation, and Wan text-to-video / image-to-video variants, while routing each model to the correct AIsa endpoint automatically. Use when: you need a neutral cross-platform skill for creating images or videos from prompts or reference images through AIsa.'
license: MIT
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, curl, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  aisa:
    emoji: 🎬
    requires:
      bins:
      - python3
      - curl
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, curl, environment variables AISA_API_KEY and internet access to api.aisa.one.
---

# Media Gen 🎬

Generate images and videos through AIsa with a single API key.

This skill covers the full media-generation runtime shipped here:

- **Image generation** across three AIsa endpoint styles
- **Video generation** for Wan text-to-video and image-to-video models
- **Automatic routing** in the bundled client so each model goes to the correct endpoint shape

Use when:

- you want to generate an image from a prompt
- you want to generate a video from a prompt or a reference image
- you want one neutral skill that works across multiple agentskills-compatible harnesses
- you do not want to manually remember which AIsa endpoint each model requires

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible
harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- and other harnesses that implement the [Agent Skills
  specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY`.

## What this skill supports

### Image generation

| Model | Provider | Endpoint | Response form |
|---|---|---|---|
| `gemini-3-pro-image-preview` | Google | `POST /v1/models/{model}:generateContent` | base64 image data in `candidates[].parts[].inline_data` |
| `wan2.7-image` | Alibaba | `POST /v1/chat/completions` | image URL parts in `choices[].message.content[]` |
| `wan2.7-image-pro` | Alibaba | `POST /v1/chat/completions` | image URL parts in `choices[].message.content[]` |
| `seedream-4-5-251128` | ByteDance | `POST /v1/images/generations` | `data[].url` or `data[].b64_json` |

### Video generation

| Model | Kind | Endpoint | Reference image field |
|---|---|---|---|
| `wan2.6-t2v` | text-to-video | `POST /apis/v1/services/aigc/video-generation/video-synthesis` | none |
| `wan2.6-i2v` | image-to-video | `POST /apis/v1/services/aigc/video-generation/video-synthesis` | `input.img_url` |
| `wan2.7-t2v` | text-to-video | `POST /apis/v1/services/aigc/video-generation/video-synthesis` | none |
| `wan2.7-i2v` | image-to-video | `POST /apis/v1/services/aigc/video-generation/video-synthesis` | `input.media` |

> Important: `wan2.7-i2v` uses `input.media` (an array of URLs), not
> `input.img_url`. The bundled client handles this automatically when you
> pass `--img-url` with that model.

## Example requests

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

## Quick start

```bash
export AISA_API_KEY="your-key"

# Any image model — client routes to the right endpoint
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

# Video — text-to-video (no image needed)
python3 scripts/media_gen_client.py video-create \
  --model wan2.7-t2v \
  --prompt "Sweeping shot of a neon cyberpunk skyline"

# Video — image-to-video on wan2.7-i2v (client routes to input.media[])
python3 scripts/media_gen_client.py video-create \
  --model wan2.7-i2v \
  --prompt "gentle zoom with parallax" \
  --img-url "https://example.com/reference.jpg" \
  --duration 5

# Wait and download
python3 scripts/media_gen_client.py video-wait \
  --task-id <task_id> --download --out out.mp4
```

## Image generation endpoint reference

### Gemini family → `POST /v1/models/{model}:generateContent`

Documentation: [Google Gemini Chat](https://aisa.one/docs/api-reference/chat/generatecontent).

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

Response contains `candidates[].parts[].inline_data` with `{mime_type, data}`
where `data` is base64-encoded image content.

### Wan 2.7 family → `POST /v1/chat/completions`

Documentation: [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation).

`messages[].content` must be an **array of typed parts**. A plain string
returns HTTP 400 `invalid_parameter_error`.

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

Images are returned as `{type: "image", image: "<url>"}` parts inside
`choices[].message.content[]`.

### Seedream → `POST /v1/images/generations`

Documentation: [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations).

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

Upstream enforces a minimum of **3,686,400 pixels**. For example,
`1024x1024` and `1536x1536` are rejected. Any aspect ratio works as long
as `width × height ≥ 3,686,400`.

## Video generation endpoint reference

### Create task → `POST /apis/v1/services/aigc/video-generation/video-synthesis`

Documentation: [Create video generation task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis).
Header `X-DashScope-Async: enable` is required.

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

# wan2.7-i2v — image-to-video (uses input.media, not input.img_url)
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

Documentation: [Get video generation task result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks).

`task_id` is a **path parameter**. The query-string form `?task_id=...`
returns HTTP 500 `unsupported uri`.

```bash
curl "https://api.aisa.one/apis/v1/services/aigc/tasks/YOUR_TASK_ID" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## Bundled Python client

The bundled client at `scripts/media_gen_client.py` auto-routes each
model to the correct AIsa endpoint and provides a simple CLI for create,
status, wait, and download flows.

```bash
# Image — model selects endpoint
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

- [Google Gemini Chat — `generateContent`](https://aisa.one/docs/api-reference/chat/generatecontent)
- [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation)
- [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations)
- [Create video generation task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis)
- [Get video generation task result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks)

See the [full AIsa API Reference](https://aisa.one/docs/api-reference)
for the complete catalog.

## License

MIT — see [LICENSE](../LICENSE) at the repo root.
