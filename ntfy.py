from requests import post, put
import numpy as np
from PIL import Image
from io import BytesIO
from base64 import b64encode
from nodes import SaveImage


def build_headers(auth_token="", username="", password="",
                  title="", priority="", tags="", click_url=""):
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    elif username and password:
        encoded = b64encode(f"{username}:{password}".encode()).decode()
        headers["Authorization"] = f"Basic {encoded}"
    if title:
        headers["Title"] = title
    if priority and priority != "default":
        headers["Priority"] = priority
    if tags:
        headers["Tags"] = tags
    if click_url:
        headers["Click"] = click_url
    return headers


def send_ntfy(images, print_to_screen, send_image, url, msg,
              auth_token="", username="", password="",
              title="", priority="default", tags="", click_url=""):
    base = build_headers(auth_token, username, password,
                         title, priority, tags, click_url)
    if send_image == "enable":
        if print_to_screen == "enable":
            print(f"Sending image attachment to {url}")
        for batch_number, image in enumerate(images):
            i = 255. * image.cpu().numpy()  # fmt:skip
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            fd = BytesIO()
            img.save(fd, format="png", compress_level=4)
            headers = {**base, "Filename": "comfyui_image.png"}
            put(url, data=fd.getvalue(), headers=headers)
    else:
        if print_to_screen == "enable":
            print(f"Sending notification '{msg}' to {url}")
        post(url, data=msg, headers=base)


class Ntfy:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "print_to_screen": (["enable", "disable"],),
                "send_image": (["enable", "disable"],),
                "url": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "https://ntfy.sh/comfyui_share",
                        "lazy": True,
                    },
                ),
                "msg": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "Image generation finished!",
                        "lazy": True,
                    },
                ),
            },
            "optional": {
                "title": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Notification title (overrides default topic URL)",
                    },
                ),
                "priority": (
                    ["default", "min", "low", "high", "urgent"],
                    {
                        "default": "default",
                        "tooltip": "Notification priority (default=normal)",
                    },
                ),
                "tags": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Comma-separated tags/emoji shortcodes (e.g. tada,warning)",
                    },
                ),
                "click_url": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "URL to open when notification is clicked",
                    },
                ),
                "auth_token": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Bearer token for authenticated ntfy servers",
                    },
                ),
                "username": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Username for Basic auth (used with password)",
                    },
                ),
                "password": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Password for Basic auth (used with username)",
                    },
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "ntfy"
    OUTPUT_NODE = True
    CATEGORY = "ntfy nodes"

    def check_lazy_status(
        self, images, print_to_screen, send_image, url, msg,
        title="", priority="default", tags="", click_url="",
        auth_token="", username="", password="",
    ):
        if print_to_screen == "enable":
            return ["url", "msg"]
        return []

    def ntfy(
        self, images, print_to_screen, send_image, url, msg,
        title="", priority="default", tags="", click_url="",
        auth_token="", username="", password="",
    ):
        send_ntfy(images, print_to_screen, send_image, url, msg,
                  auth_token, username, password,
                  title, priority, tags, click_url)
        return (images,)


class SaveImageAndNtfy(SaveImage):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": (
                    "STRING",
                    {
                        "default": "ComfyUI",
                        "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes.",
                    },
                ),
                "ntfy": (["enable", "disable"],),
                "print_to_screen": (["enable", "disable"],),
                "send_image": (["enable", "disable"],),
                "url": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "https://ntfy.sh/comfyui_share",
                        "lazy": True,
                    },
                ),
                "msg": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "Image generation finished!",
                        "lazy": True,
                    },
                ),
            },
            "optional": {
                "title": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Notification title (overrides default topic URL)",
                    },
                ),
                "priority": (
                    ["default", "min", "low", "high", "urgent"],
                    {
                        "default": "default",
                        "tooltip": "Notification priority (default=normal)",
                    },
                ),
                "tags": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Comma-separated tags/emoji shortcodes (e.g. tada,warning)",
                    },
                ),
                "click_url": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "URL to open when notification is clicked",
                    },
                ),
                "auth_token": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Bearer token for authenticated ntfy servers",
                    },
                ),
                "username": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Username for Basic auth (used with password)",
                    },
                ),
                "password": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Password for Basic auth (used with username)",
                    },
                ),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    FUNCTION = "save_and_ntfy"
    CATEGORY = "ntfy nodes"

    def check_lazy_status(
        self,
        images,
        filename_prefix,
        ntfy,
        print_to_screen,
        send_image,
        url,
        msg,
        prompt,
        extra_pnginfo,
        title="",
        priority="default",
        tags="",
        click_url="",
        auth_token="",
        username="",
        password="",
    ):
        if print_to_screen == "enable":
            return ["url", "msg"]
        return []

    def save_and_ntfy(
        self,
        images,
        ntfy,
        print_to_screen,
        send_image,
        url,
        msg,
        filename_prefix="ComfyUI",
        prompt=None,
        extra_pnginfo=None,
        title="",
        priority="default",
        tags="",
        click_url="",
        auth_token="",
        username="",
        password="",
    ):
        if ntfy == "enable":
            send_ntfy(images, print_to_screen, send_image, url, msg,
                      auth_token, username, password,
                      title, priority, tags, click_url)
        return super().save_images(
            images=images,
            filename_prefix=filename_prefix,
            prompt=prompt,
            extra_pnginfo=extra_pnginfo,
        )


NODE_CLASS_MAPPINGS = {"Ntfy": Ntfy, "SaveImageAndNtfy": SaveImageAndNtfy}
NODE_DISPLAY_NAME_MAPPINGS = {"Ntfy": "ntfy", "SaveImageAndNtfy": "Save Image and ntfy"}
