from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as image_type
import os
import imageio.v3 as iio
from moviepy.editor import AudioFileClip, CompositeAudioClip, ImageSequenceClip
import random
from pathlib import Path

background = 50, 51, 57
circle_mask = Image.new("L", (75, 75), 0)

index = 0

ping_file = "sounds/discord_ping.mp3"

hour = random.randint(1, 12)


def mask(image: image_type):
    draw = ImageDraw.Draw(circle_mask)
    draw.ellipse(
        (0, 0, 75, 75),
        fill=255
    )
    image.putalpha(circle_mask)


class Generator:
    @staticmethod
    def generate_video(custom_sounds: list[dict] = None, SLOWDOWN: float = 2):
        video_id = random.randint(1, 1000000)
        frames = []
        folder = "frames"

        files = sorted(
            os.listdir(folder),
            key=lambda x: int(x.split("_")[1].split(".")[0])
        )

        frame_files = []

        for file in files:
            if file.endswith(".png"):
                frame_files.append(file)
                frames.append(
                    iio.imread(os.path.join(folder, file))
                )

        sounds = []

        OUT_FPS = 30
        frames_out = []
        for f in frames:
            frames_out.extend([f] * max(1, round(SLOWDOWN * OUT_FPS)))

        for i in range(len(frame_files)):
            ping = AudioFileClip(ping_file)
            sounds.append(ping.set_start(i * SLOWDOWN))

        if custom_sounds:
            for sound in custom_sounds:
                file = AudioFileClip(f"sounds/{sound['name']}.mp3")

                start = float(sound["start"])

                if "end" in sound:
                    end = float(sound["end"])
                    duration = end - start

                    if duration > 0:
                        duration = min(duration, file.duration)
                        file = file.subclip(0, duration)

                file = file.set_start(start * SLOWDOWN)
                sounds.append(file)

        audio = CompositeAudioClip(sounds)

        # write at a real framerate, no temp round-trip needed
        video = ImageSequenceClip(frames_out, fps=OUT_FPS)
        video = video.set_audio(audio)
        video.write_videofile(f"temp/output_{video_id}.mp4", audio_codec="aac")

        video.write_videofile(
            f"videos/final_{video_id}.mp4",
            codec="libx264",
            audio_codec="aac"
        )

        # Cleanup
        images = Path("frames")
        for image in images.iterdir():
            if image.is_file():
                image.unlink()

        temp_video = Path(f"temp/output_{video_id}.mp4")
        temp_video.unlink()

    @staticmethod
    def create_message(sender: str, content: str):
        global index

        split_length = 28

        content_split = []

        while content:
            if len(content) <= split_length:
                content_split.append(content)
                break

            split_at = content.rfind(" ", 0, split_length + 1)

            if split_at == -1:
                next_space = content.find(" ")

                if next_space == -1:
                    content_split.append(content)
                    break

                content_split.append(content[:next_space])
                content = content[next_space + 1:]
                continue

            content_split.append(content[:split_at])
            content = content[split_at + 1:]

        frame = Image.new("RGBA", (1000, 1000), (0, 0, 0))

        canvas = Image.new("RGBA", (500, 100), background)

        profile = Image.open(f"profiles/{sender.lower()}.png")

        display = profile.copy()
        display.thumbnail((75, 75), Image.Resampling.LANCZOS)

        mask(display)

        x = 10
        y = (canvas.height - display.height) // 2

        draw = ImageDraw.Draw(canvas)

        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            35
        )

        draw.text(
            (100, 10),
            sender,
            font=font,
            fill="white"
        )

        username_width = draw.textbbox(
            (0, 0),
            sender,
            font=font,
        )[2]

        draw = ImageDraw.Draw(canvas)

        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            25
        )

        minute = str(round((index + 10) / 2))

        draw.text(
            (100 + username_width + 10, 18),
            f"{hour}:{'0' + minute if len(minute) == 1 else minute} PM",
            font=font,
            fill=(156, 157, 163)
        )

        new_height = 55 + (len(content_split) * 40) + 25

        new_canvas = Image.new(
            "RGBA",
            (500, new_height),
            background
        )

        new_canvas.paste(canvas, (0, 0))
        canvas = new_canvas

        draw = ImageDraw.Draw(canvas)

        for i, text in enumerate(content_split):
            draw.text(
                (100, 55 + (i * 55)),
                text,
                font=font,
                fill="white"
            )

        canvas.paste(
            display,
            (x, y),
            display.getchannel("A")
        )

        frame.paste(
            canvas,
            (250, 250)
        )

        frame.save(f"frames/frame_{index}.png")
        index += 1
