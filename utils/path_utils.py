import os
import folder_paths
import faster_whisper

faster_whisper_model_dir = os.path.join(folder_paths.models_dir, "faster-whisper")
os.makedirs(faster_whisper_model_dir, exist_ok=True)

def collect_model_paths(
    model_dir: str = faster_whisper_model_dir,
):
    """
    Get available models from model dir path including fine-tuned model.
    """
    model_paths = {model: model for model in faster_whisper.available_models()}
    faster_whisper_prefix = "models--Systran--faster-whisper-"

    existing_models = os.listdir(model_dir)
    excludes = [".locks"]
    existing_models = list(set(existing_models) - set(excludes))

    for model_name in existing_models:
        if faster_whisper_prefix in model_name:
            model_name = model_name[len(faster_whisper_prefix):]

        if model_name not in faster_whisper.available_models():
            model_paths[model_name] = os.path.join(model_dir, model_name)
    return model_paths