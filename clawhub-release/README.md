# ClawHub Release Variants

This directory contains conservative ClawHub-oriented release variants for the first publish wave.

## Purpose

- Keep `targetSkills/` as the cross-platform mother-skill layer
- Keep `clawhub-release/` as the upload-focused layer for ClawHub
- Reduce parser fragility and `Suspicious` review surface without rewriting runtime functionality

## First-wave skills

- `aisa-twitter-command-center`
- `aisa-twitter-post-engage`
- `aisa-youtube-search`
- `aisa-youtube-serp-scout`

## Release principles

- Use conservative frontmatter with top-level `primaryEnv` and `requires`
- Keep `metadata` focused on `metadata.openclaw`
- Strip non-essential cross-platform fields
- Prefer returning authorization URLs instead of local browser-opening helpers
- Keep only runtime files and essential references
