from requests import post, put
import numpy as np
from PIL import Image
from io import BytesIO
from nodes import SaveImage


def send_ntfy(images, print_to_screen, send_image, url, msg):
    if send_image == "enable":
        if print_to_screen == "enable":
            print(f"Sending image attachment to {url}")
        for batch_number, image in enumerate(images):
            i = 255. * image.cpu().numpy()  # fmt:skip
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            fd = BytesIO()
            img.save(fd, format="png", compress_level=4)
            headers = {"Filename": "comfyui_image.png"}
            put(url, data=fd.getvalue(), headers=headers)
    else:
        if print_to_screen == "enable":
            print(f"Sending notification '{msg}' to {url}")
        post(url, data=msg)


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
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "ntfy"
    OUTPUT_NODE = True
    CATEGORY = "ntfy nodes"

    def check_lazy_status(self, images, print_to_screen, send_image, url, msg):
        if print_to_screen == "enable":
            return ["url", "msg"]
        else:
            return []

    def ntfy(self, images, print_to_screen, send_image, url, msg):
        send_ntfy(images, print_to_screen, send_image, url, msg)
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
    ):
        if print_to_screen == "enable":
            return ["url", "msg"]
        else:
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
    ):
        if ntfy == "enable":
            send_ntfy(images, print_to_screen, send_image, url, msg)
        return super().save_images(
            images=images,
            filename_prefix=filename_prefix,
            prompt=prompt,
            extra_pnginfo=extra_pnginfo,
        )


NODE_CLASS_MAPPINGS = {"Ntfy": Ntfy, "SaveImageAndNtfy": SaveImageAndNtfy}
NODE_DISPLAY_NAME_MAPPINGS = {"Ntfy": "ntfy", "SaveImageAndNtfy": "Save Image and ntfy"}
