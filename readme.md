# Install

cd into custom_nodes directory

`cd YOUR_PATH/ComfyUI/custom_nodes`

clone repo

`git clone https://github.com/boredofnames/ComfyUI-ntfy.git`

or download ntfy.py and place into custom_nodes directory.

# Update

cd into ComfyUi-ntfy directory

`cd YOUR_PATH/ComfyUI/custom_nodes/ComfyUI-ntfy`

pull from repo

`git pull origin master`

or download ntfy.py and replace in custom_nodes directory.

# Usage

Place inbetween VAE decode and Save/Preview Image

## Params

- URL
  - The url to post/put request to
- MSG
  - The message used when send image is disabled
- Send Image
  - If enabled, send the image as attachment via PUT
  - If disabled, send MSG instead
- Print to screen
  - Log data out to server
  - "Sending notification to \<URL\>"
