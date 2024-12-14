from gtts import gTTS


class Basic_TTSModel:
    def __init__(self):
        """
        Initialize the TTS model.
        You can load a pre-trained model here if required.
        """
        pass

    def generate_audio(self, text, output_path="output.wav"):
        """
        Generate speech audio from text.
        :param text: The input text to be converted to speech.
        :param output_path: The file path to save the output audio.
        """
        # Example using gTTS
        tts = gTTS(text)
        tts.save(output_path)


class Basic_TTSModel:
    @staticmethod
    def generate_audio(text, output_path="static/output_light.wav"):
        """
        Generate speech audio from text using gTTS.
        :param text: Input text to be converted to speech.
        :param output_path: Path to save the generated audio file.
        """
        tts = gTTS(text)
        tts.save(output_path)


from TTS.api import TTS
import torch

class TTSModel:
    def __init__(self):
        """
        Initialize the TTS model with the desired pre-trained TTS model and device.
        """
        # Get device (CUDA if available, else CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Initialize the TTS model
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)

    def generate_audio(self, text, output_path, speaker_wav="/home/nim/Documents/ralph.wav"):
        """
        Generate speech audio from text using the TTS library.

        :param text: Input text to be converted to speech.
        :param output_path: File path to save the generated audio.
        :param speaker_wav: Path to the speaker reference WAV file.
        """
        # Generate speech and save it to the output file
        self.tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language="en",
            file_path=output_path
        )





