import os
import faster_whisper
from typing import Union, BinaryIO, Dict, List, Tuple
import numpy as np

import folder_paths
from comfy.utils import ProgressBar

from .subtitle_utils import AVAILABLE_SUBTITLE_FORMAT, format_transcriptions_to_subtitle, get_incremented_filename

faster_whisper_script_dir_path = os.path.dirname(os.path.abspath(__file__))
faster_whisper_output_dir_path = folder_paths.get_output_directory()


class LoadFasterWhisperModel:
    @classmethod
    def INPUT_TYPES(s):
        faster_whisper_models = [
            "tiny.en",
            "tiny",
            "base.en",
            "base",
            "small.en",
            "small",
            "medium.en",
            "medium",
            "large-v1",
            "large-v2",
            "large-v3",
            "large"
        ]

        return {
            "required": {
                "model": (faster_whisper_models,),
                "device": (['cuda', 'cpu', 'auto'],),
            },
        }

    RETURN_TYPES = ("FASTERWHISPERMODEL",)
    RETURN_NAMES = ("faster_whisper_model",)
    FUNCTION = "load_model"
    CATEGORY = "FASTERWHISPER"

    def load_model(self,
                   model: str,
                   device: str,
                   ) -> faster_whisper.WhisperModel:
        model_dir = os.path.join(folder_paths.models_dir, "faster-whisper")
        os.makedirs(model_dir, exist_ok=True)

        faster_whisper_model = faster_whisper.WhisperModel(
            device=device,
            model_size_or_path=model,
            download_root=model_dir,
        )

        return faster_whisper_model


class FasterWhisperTranscription:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
                "model": ("FASTERWHISPERMODEL", ),
            },
            "optional": {
                "lang": ("STRING", {"default": "auto"}),
                "is_translate": ("BOOLEAN", {"default": False}),
                "beam_size": ("INT", {"default": 5}),
                "log_prob_threshold": ("FLOAT", {"default": -1.0}),
                "no_speech_threshold": ("FLOAT", {"default": 0.6}),
                "best_of": ("INT", {"default": 5}),
                "patience": ("FLOAT", {"default": 1}),
                "temperature": ("FLOAT", {"default": 0.0}),
                "compression_ratio_threshold": ("FLOAT", {"default": 2.4}),
                "length_penalty": ("FLOAT", {"default": 1.0}),
                "repetition_penalty": ("FLOAT", {"default": 1.0}),
                "no_repeat_ngram_size": ("INT", {"default": 0}),
                "prefix": ("STRING", {"default": ""}),
                "suppress_blank": ("BOOLEAN", {"default": True}),
                "suppress_tokens": ("STRING", {"default": "-1"}),
                "max_initial_timestamp": ("FLOAT", {"default": 1.0}),
                "word_timestamps": ("BOOLEAN", {"default": False}),
                "prepend_punctuations": ("STRING", {"default": "\"'“¿([{-"}),
                "append_punctuations": ("STRING", {"default": "\"'.。,，!！?？:：”)]}、"}),
                "max_new_tokens": ("INT", ),
                "chunk_length": ("INT", ),
                "hallucination_silence_threshold": ("FLOAT", ),
                "hotwords": ("STRING", ),
                "language_detection_threshold": ("FLOAT", ),
                "language_detection_segments": ("INT", {"default": 1}),
                "prompt_reset_on_temperature": ("FLOAT", {"default": 0.5}),
                "condition_on_previous_text": ("BOOLEAN", {"default": True}),
                "initial_prompt": ("STRING", ),
                "without_timestamps": ("BOOLEAN", {"default": False}),
                "vad_filter": ("BOOLEAN", {"default": False}),
                "vad_parameters": ("STRING", ),
                "clip_timestamps": ("STRING", {"default": "0"}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("transcriptions",)
    FUNCTION = "transcribe"
    CATEGORY = "FASTERWHISPER"

    def transcribe(self,
                   audio: Union[str, BinaryIO, np.ndarray],
                   model: faster_whisper.WhisperModel,
                   **params,
                   ) -> List:

        segments, info = model.transcribe(
            audio=audio,
            **params,
        )

        comfy_pbar = ProgressBar(info.duration)

        transcriptions = []
        for segment in segments:
            comfy_pbar.update_absolute(segment.start)
            transcriptions.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })
        return transcriptions


class FasterWhisperToSubtitle:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "transcriptions": ("LIST", ),
                "subtitle_format": (AVAILABLE_SUBTITLE_FORMAT, ),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("subtitle",)
    FUNCTION = "format_to_subtitle"
    CATEGORY = "FASTERWHISPER"

    def format_to_subtitle(self,
                           transcriptions: List[Dict],
                           subtitle_format: str,
                           ) -> Tuple[str, str]:
        subtitle = format_transcriptions_to_subtitle(transcriptions, subtitle_format)
        return subtitle, subtitle_format


class SaveSubtitle:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "subtitle": ("STRING", ),
                "extension": ("STRING", ),
            },
            "optional": {
                "prefix": ("STRING", {"default": "subtitle"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "save_subtitle"
    CATEGORY = "FASTERWHISPER"
    OUTPUT_NODE = True

    def save_subtitle(self,
                      subtitle: str,
                      extension: str,
                      prefix: str
                      ) -> str:
        if extension not in AVAILABLE_SUBTITLE_FORMAT:
            raise ValueError(f"Output format not supported. Supported formats: {AVAILABLE_SUBTITLE_FORMAT}")

        output_path = get_incremented_filename(faster_whisper_output_dir_path, prefix, extension)

        with open(output_path, "w") as f:
            f.write(subtitle)
        return output_path