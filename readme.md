# About

[ntfy](https://ntfy.sh/) is a simple HTTP-based pub-sub notification service.
This repo adds 2 nodes to send ntfy push notifications from ComfyUI.
Supports text notifications and image attachments.

# Nodes

## ntfy

Sends a notification (text or image) without saving the output.

| Input | Type | Description |
|-------|------|-------------|
| `images` | IMAGE | Image tensor to send as attachment |
| `print_to_screen` | enable/disable | Log to console |
| `send_image` | enable/disable | Send image as attachment vs. text |
| `url` | string | ntfy topic URL (e.g. `https://ntfy.sh/mytopic`) |
| `msg` | string | Notification body text |
| `title` | string | Notification title (overrides the topic URL) |
| `priority` | dropdown | `default`, `min`, `low`, `high`, `urgent` |
| `tags` | string | Comma-separated emoji short codes (e.g. `tada,warning`) |
| `click_url` | string | URL to open when notification is tapped |
| `auth_token` | string | Bearer token for authenticated ntfy servers |
| `username` | string | Username for Basic auth (use with `password`) |
| `password` | string | Password for Basic auth (use with `username`) |

## Save Image and ntfy

Extends ComfyUI's built-in `SaveImage` node to also send a notification.

Same inputs as above, plus `filename_prefix` and an `ntfy` enable/disable toggle.

# Install

## Comfy-CLI Manager

```
comfy node install comfyui-ntfy
```

## Manual

```
cd ComfyUI/custom_nodes
git clone --depth 1 https://github.com/boredofnames/ComfyUI-ntfy.git
```

Or just drop `ntfy.py` into `ComfyUI/custom_nodes/`.

# Contributing

Send a PR to https://github.com/boredofnames/ComfyUI-ntfy
