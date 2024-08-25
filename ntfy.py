from requests import post, put
import numpy as np
from PIL import Image
from io import BytesIO


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
                        "multiline": False,  # True if you want the field to look like the one on the ClipTextEncode node
                        "default": "https://ntfy.sh/comfyui_share",
                        "lazy": True,
                    },
                ),
                "msg": (
                    "STRING",
                    {
                        "multiline": False,  # True if you want the field to look like the one on the ClipTextEncode node
                        "default": "Image generation finished!",
                        "lazy": True,
                    },
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "ntfy"
    OUTPUT_NODE = False
    CATEGORY = "ntfy nodes"

    def check_lazy_status(self, images, print_to_screen, send_image, url, msg):
        if print_to_screen == "enable":
            return ["send_image", "url", "msg"]
        else:
            return []

    def ntfy(self, images, print_to_screen, send_image, url, msg):
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
        return (images,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {"Ntfy": Ntfy}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {"Ntfy": "ntfy"}