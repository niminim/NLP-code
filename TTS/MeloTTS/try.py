from melo.api import TTS

# Speed is adjustable
speed = 1.0

# CPU is sufficient for real-time inference.
# You can set it manually to 'cpu' or 'cuda' or 'cuda:0' or 'mps'
device = 'auto' # Will automatically use GPU if available

# English
text = "Did you ever hear a folk tale about a giant turtle?"

text = """
In 1962, fresh out of business school, Phil Knight borrowed $50 from his father and created a company with a simple mission:
import high-quality, low-cost athletic shoes from Japan.
"""

model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id

# American accent
output_path = '/home/nim/en-us.wav'
model.tts_to_file(text, speaker_ids['EN-US'], output_path, speed=speed)

# British accent
output_path = '/home/nim/en-br.wav'
model.tts_to_file(text, speaker_ids['EN-BR'], output_path, speed=speed)

# Indian accent
output_path = 'en-india.wav'
model.tts_to_file(text, speaker_ids['EN_INDIA'], output_path, speed=speed)

# Australian accent
output_path = 'en-au.wav'
model.tts_to_file(text, speaker_ids['EN-AU'], output_path, speed=speed)

# Default accent
output_path = 'en-default.wav'
model.tts_to_file(text, speaker_ids['EN-Default'], output_path, speed=speed)



import pkg_resources
from subprocess import check_output

# Get the list of installed packages
packages = check_output(['pip', 'list', '--format=freeze'], universal_newlines=True).splitlines()

# Iterate through packages to extract metadata
for package in packages:
    name = package.split('==')[0]
    try:
        dist = pkg_resources.get_distribution(name)
        print(f"{name} - Installed on: {dist._provider.egg_info_date()}")
    except AttributeError:
        print(f"{name} - Installation date not available")