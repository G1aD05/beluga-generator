from generator import Generator as Gen
from ai import AI

import json

response = AI.generate_messages("Create the video about ChezRat about to say the n word (nagger) and then everyone else tells him to not do it but he does it anyways and then everyone kicks him")
print(response)
messages = json.loads(response)

sounds = []

for message in messages:
    if 'sound' not in message or message['sound']:
        print(message)
        sounds.append(message)
    else:
        Gen.create_message(message["sender"], message["content"])

Gen.generate_video(sounds, 1.5)
