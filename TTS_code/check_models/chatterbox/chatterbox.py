import torchaudio as ta
from TTS_code.check_models.chatterbox.chatterbox import ChatterboxTTS
from TTS_code.check_models.chatterbox.chatterbox import ChatterboxMultilingualTTS

# English example
model = ChatterboxTTS.from_pretrained(device="cuda")

text = "“Ilsabet, wake up!” Ilsabet pulled the down-filled covers tighter around her thin body and ignored her maidservant’s call. “You were up half the night writing in that journal, weren’t you?” Greta, Ilsabet’s maid, could sign her name in a beautiful script, but that was all. Reading, writing, even contemplative thought seemed beyond her reach. But she was a practical and caring woman, and Ilsabet ignored the shortcomings. “No,” she replied. “I just couldn’t sleep.” Instead, Ilsabet had gone to Lord Jorani’s chambers in the highest room in the castle tower. Nimbus Castle had been built on a narrow peninsula that stretched nearly to the center of the slow-moving Arvid River. The river’s source was a hot spring in the mountains, the water always warm. Except for the hottest summer months, a fog usually hung around the castle, making it seem as if the thick stone walls rose from the mists themselves. The night fog was denser than usual, leaving Ilsabet alone above a world of faded colors and"
# wav = model.generate(text)
# ta.save("/home/nim/Downloads/test-english.wav", wav, model.sr)

# # Multilingual examples
# multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")

# If you want to synthesize with a different voice, specify the audio prompt
AUDIO_PROMPT_PATH = "/home/nim/Documents/scott_brick.wav"
wav = model.generate(text, audio_prompt_path=AUDIO_PROMPT_PATH)
ta.save("/home/nim/Downloads/test2.wav", wav, model.sr)



######################
import torchaudio as ta
from TTS_code.check_models.chatterbox.chatterbox import ChatterboxTTS
from TTS_code.check_models.chatterbox.chatterbox import ChatterboxMultilingualTTS

# Multilingual examples
multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")

heb_text = "שלום, מי זה בדלת?"
wav_heb = multilingual_model.generate(heb_text, language_id="he")
wav_heb = multilingual_model.generate(heb_text, audio_prompt_path="/home/nim/Documents/תמר_עמית_מזל_של_מתחילים.wav", language_id="he")
ta.save("/home/nim/Documents/TRY..wav", wav_heb, multilingual_model.sr)
ta.save("/home/nim/Documents/תמר_עמית_מזל_של_מתחילים..wav", wav_heb, multilingual_model.sr)