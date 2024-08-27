# About

[ntfy](https://ntfy.sh/) is a simple HTTP-based pub-sub notification service. This repo adds 2 nodes to make ntfy notifications simple in ComfyUI. Supports sending a simple text based notification, or the generated image as an attachment to a topic.

Please note, by default it's set to send the image to the topic "comfyui_share". Anyone subscribed to this topic will see the generated image if they choose to download it. Therefore, be sure to change the input URL to a preferred subscribed topic if you don't want this! This may change in the future, but I think seeing a working example is the best way to learn.

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

# Nodes

See [Wiki](https://github.com/boredofnames/ComfyUI-ntfy/wiki)
