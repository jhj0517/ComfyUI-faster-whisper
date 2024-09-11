# ComfyUI-faster-whisper

[ComfyUI](https://github.com/comfyanonymous/ComfyUI) reference implementation for [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Workflow that generates subtitles is included. 

# Example Workflows
Subtitle generation workflow is included in [workflows](https://github.com/jhj0517/ComfyUI-faster-whisper/tree/master/workflows) directory

![workflow](https://github.com/jhj0517/ComfyUI-faster-whisper/blob/master/workflows/faster_whisper_suttitle.png)


# Installation

1. git clone repository into `ComfyUI\custom_nodes\`
```
https://github.com/jhj0517/ComfyUI-faster-whisper.git
```

2. Go to `ComfyUI\custom_nodes\ComfyUI-faster-whisper` and run
```
pip install -r requirements.txt
```

If you are using the portable version of ComfyUI, do this:
```
python_embeded\python.exe -m pip install -r ComfyUI\custom_nodes\ComfyUI-faster-whisper\requirements.txt
```

## Available Models
This repo uses Systran's [faster-whisper models](https://huggingface.co/Systran).<br>
Running the [workflow](https://github.com/jhj0517/ComfyUI-faster-whisper/blob/master/workflows/faster_whisper_suttitle.png) will automatically download the model into `ComfyUI\models\faster-whisper`. 

If you want to place it manually, download the model from Systran's [faster-whisper models](https://huggingface.co/Systran) and place it in `ComfyUI\models\faster-whisper`.

## Todo 🗓
- [ ] Better version of input file path node with upload file button


