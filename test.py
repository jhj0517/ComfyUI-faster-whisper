import faster_whisper

# Load the model (replace with your model loading code)
model = faster_whisper.WhisperModel("tiny", device="cpu")

# Get the available language codes
available_langs = model.supported_languages

print(available_langs)