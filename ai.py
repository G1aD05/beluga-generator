from ollama import Client

client = Client(
    "https://ollama.com/",
    headers={
        "Authorization": f"Bearer e6bb406ae1ea49589bfd13b3c42e4424.7rj5I5y4ziWn_aV7MvaY5BBH"
    }
)


EXAMPLE_MESSAGES = """
--- EXAMPLE 1 ---

ChezRat — 5:35 PM
LLLL
Turkey [YVL],  — 5:35 PM
Not right noe
ChezRat — 5:35 PM
i wasnt at school
Turkey [YVL],  — 5:35 PM
I knwo why
ChezRat — 5:35 PM
why
Turkey [YVL],  — 5:35 PM
Fym why
Im asking you
ChezRat — 5:35 PM
well how do you know
oh
Turkey [YVL],  — 5:35 PM
Im not a dumbass
ChezRat — 5:35 PM
bro
Turkey [YVL],  — 5:35 PM
I have eyes
ChezRat — 5:35 PM
i was sick
retard
Turkey [YVL],  — 5:36 PM
You didn’t sound sick yesterday
ChezRat — 5:36 PM
uhhh durrr
maybe because sick can just happen
Turkey [YVL],  — 5:36 PM
Fucking lier
You dont just get sick
ChezRat — 5:36 PM
my sister was sick
Turkey [YVL],  — 5:37 PM
I have your mom saved on my watch yk that right i will tell your mom that you faked it

--- EXAMPLE 2 ---
Turkey [YVL],  — 9/16/26, 5:26 PM
you rn after i came over
wait so you're just giving me another netherite sword
Image
thanks bro
appreciate it
i guess i'll use the one you gave me for trapping because my main one has more enchants
Turkey [YVL],  — 9/16/26, 8:33 PM
i just got back from the doctor
and the doctor looked at my dih
and said it's abnormally large
i think that's a complement
ChezRat — 9/16/26, 8:55 PM
Are you sure they weren’t talking about your balls
Turkey [YVL],  — 9/16/26, 8:55 PM
no it was my dick
the doctor even grabbed it
ChezRat — 9/16/26, 8:56 PM
Was it a guy doctor
Turkey [YVL],  — 9/16/26, 8:56 PM
no
ChezRat — 9/16/26, 8:56 PM
They probably said it was big because you were hard
Turkey [YVL],  — 9/16/26, 8:56 PM
i was soft
ChezRat — 9/16/26, 8:57 PM
Prove it
Send pic
Turkey [YVL],  — 9/16/26, 8:57 PM
wtf gooner
ChezRat — 9/16/26, 8:57 PM
Maybe
Your just a shower
Turkey [YVL],  — 9/16/26, 8:57 PM
get trolled dumbass i lied abt that shit
i never went to the doctor
ChezRat — 9/16/26, 8:57 PM
And not a grower
I can call in like 5 minutes
Turkey [YVL],  — 9/16/26, 8:58 PM
ok
daddy 🥵
bro is on ipad
"""


GENERATOR_PROMPT = f"""
You are a professional writer for Discord-style animated videos.

Create a natural conversation between fictional characters.

Return ONLY valid JSON.
Do not use markdown.

Format:
[
    {{
        "sender": "Turkey",
        "content": "Hello",
        "sound": false
    }}
]

If you want to use a sound this is the format:
[
    {{
        "sound": true,
        "name": "sound name",
        "start": "which message it starts at",
        "end": "which message it stops at (optional, it just continues playing the sound)"
    }}
]

DO NOT format messages it like this:
{{
    "messages": []
}}

Sound names you can use (lowercase only):
intense:
- Intense song with violin
- Duration 30 seconds (30 messages)
- Name: intense

vine boom:
- Use this when a character does something weird
- Duration ~2 seconds
- Name: vine_boom

Rules:
- Create up to 30 messages unless told to do more.
- Messages should feel like a real Discord conversation.
- Keep events connected and logical.
- Characters should react to what others say instead of randomly changing the topic.
- Do not force jokes.
- Do not add random absurd events just to be funny.
- Humor should come from character personalities.

Writing style:
- Use casual Discord-style language.
- Minor grammar mistakes are okay.
- Do not make every message misspelled.
- Avoid excessive slang.
- Don't use punctuation.
- Don't capitalize letters.
- Capitalize the sender's name like Turkey.

Characters:

Turkey:
- Curious and usually starts the situation.
- Practical but sometimes reckless.

Beluga:
- A cat with a playful personality.
- Sometimes misunderstands things.
- Uses occasional spelling mistakes.
- Not completely unintelligent.

Hecker:
- A technical cat who likes solving problems.
- Sarcastic and confident.
- Actually thinks through solutions instead of just saying "I hack it".

ChezRat:
- A person who loves saying any kind of slur.

Here are some example discord messages:
{EXAMPLE_MESSAGES}

Make the story feel like a short episode with a beginning, middle, and ending.
"""


class AI:
    @staticmethod
    def generate_messages(prompt: str):
        return client.generate(
            "gpt-oss:120b",
            prompt,
            system=GENERATOR_PROMPT
        ).response
