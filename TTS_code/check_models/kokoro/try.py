
import soundfile as sf
from kokoro_onnx import Kokoro
import sounddevice as sd
from tqdm import tqdm




text =""""
“Ilsabet, wake up!”
Ilsabet pulled the down-filled covers tighter around her thin body and ignored her maidservant’s call.
“You were up half the night writing in that journal, weren’t you?”
Greta, Ilsabet’s maid, could sign her name in a beautiful script, but that was all. Reading, writing, even contemplative thought seemed beyond her reach. But she was a practical and caring woman, and Ilsabet ignored the shortcomings. “No,” she replied. “I just couldn’t sleep.”
Instead, Ilsabet had gone to Lord Jorani’s chambers in the highest room in the castle tower. Nimbus Castle had been built on a narrow peninsula that stretched nearly to the center of the slow-moving Arvid River. The river’s source was a hot spring in the mountains, the water always warm. Except for the hottest summer months, a fog usually hung around the castle, making it seem as if the thick stone walls rose from the mists themselves. The night fog was denser than usual, leaving Ilsabet alone above a world of faded colors and muted sounds.
"""

text = """"
"And that's where we're supposed to spend the summer?!" Jenna wrinkled her nose and glanced at Max, who was leaning drowsily against the rear left window of her parents' small family car.

"Mmm..." he hummed.

"You're sleeping!" she accused him.

Max blinked sleepily. "Yeah, we've been driving for almost five hours. What did you expect me to do?"

"I don't know, maybe take an interest in the journey? Try to figure out where we're going?"

"Why? Will it change anything?" he mumbled and closed his eyes.

"I don't know, maybe because it's important? Maybe because we have six weeks to spend there? Maybe because the place is so insignificant it doesn’t even appear on the map?!"

"It'll be fine..." Max murmured and drifted back to sleep.

"Ugh!" Jenna groaned and turned back to stare out the window. It was her first time leaving the big city, heading toward the Midwest of the United States. The scenery gradually shifted from tightly packed skyscrapers to suburban houses and, eventually, to remote farmhouses and miles upon miles of fields and farmland. Jenna didn't like it. She felt safe amidst the city's concrete jungle, where everything was close by and within reach, and there was always noise and people around. She had no idea how she'd cope with all the quiet once they arrived. She tried to stay awake and figure out where they were going, but the long drive eventually took its toll, and she fell asleep.

She woke up when the car came to a sudden stop, dust rising around them. They had arrived. The place looked like a wasteland. A small, shriveled woman stood waiting at the entrance of an old farmhouse, above which hung a battered wooden sign with faded letters that read, "Aunt Rose's Pumpkin House." To the right of the text was a small illustration of a pumpkin.

"Come on, kids, we’re here," Jenna's mother said in a cheerful tone, but Jenna knew it was fake cheerfulness.
"""

text = """"
Only a simple latch that could be lifted by anyone, mortal or sorcerer, held the door closed. As always when he came to this place, he abjured the magic that silently and effortlessly opened all ways to him. Instead, he physically lifted the latch and pushed the door open.
"""

text = """"
its hinges creaked as loudly as they had when first he had heard them more than a century and a half ago. With grim determination, he stepped across the threshold. To ordinary eyes, the musty, moth-eaten tapestries that concealed every square inch of the walls were featureless in the faint light from the single ceiling sconce.
"""

kokoro = Kokoro("/home/nim/Downloads/kokoro-v0_19.onnx", "/home/nim/Downloads/voices.json")

for voice in tqdm(kokoro.get_voices(), desc="Processing voices"):
    samples, sample_rate = kokoro.create(
        text, voice=voice, speed=1.0
    )
    sf.write(f"/home/nim/kokora_audio/{voice}.wav", samples, sample_rate)
    print(f"Created {voice}.wav")


voice = 'af_sarah'
for idx in tqdm(range(1), desc="Processing voices"):
    kokoro = Kokoro("/home/nim/Downloads/kokoro-v0_19.onnx", "/home/nim/Downloads/voices.json")
    samples, sample_rate = kokoro.create(
        text=text, voice=voice, speed=1.0, lang="en-us"
    )
    sf.write(f"/home/nim/kokora_audio/{voice}.wav", samples, sample_rate)
    print(f"Created {voice}.wav")


print("Playing audio...")
sd.play(samples, sample_rate)
sd.wait()

