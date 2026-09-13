import os
import json
import asyncio
from pathlib import Path

from google import genai
import edge_tts


# ==============================
# CURIOX SETTINGS
# ==============================

CHANNEL_NAME = "CurioX"

TOPIC = "Why You Never Feel Like You Have Enough Money"

MODEL = "gemini-2.5-flash"

VOICE = "en-US-GuyNeural"


# ==============================
# OUTPUT FOLDER
# ==============================

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ==============================
# GENERATE AI CONTENT
# ==============================

def generate_content():

    api_key = os.environ.get("AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX")

    if not api_key:
        raise Exception(
            "GEMINI_API_KEY is missing. "
            "Add it to GitHub Secrets."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are the AI content creator for a YouTube channel called "{CHANNEL_NAME}".

Create a 45-60 second YouTube Short.

TOPIC:
{TOPIC}

STYLE:

- Modern Ideas style
- Intelligent
- Thought-provoking
- Psychological
- Simple English
- Fast-paced
- Cinematic feeling
- Strong hook in the first 2 seconds
- Keep viewers curious
- Explain the psychology behind the topic
- Use relatable examples
- Make the viewer think
- End with a powerful memorable insight
- No fake facts
- No copied content
- No unnecessary introduction
- No "Hey guys"
- No boring explanations

The script should sound natural when spoken by an AI voice.

The narration should be approximately 100-140 words.

Return ONLY valid JSON.

Use exactly this format:

{{
    "title": "YouTube Shorts title",
    "description": "YouTube description",
    "hashtags": [
        "#shorts",
        "#money",
        "#psychology",
        "#curiox"
    ],
    "script": "Complete narration script"
}}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown JSON formatting if Gemini adds it
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)


# ==============================
# CREATE AI VOICE
# ==============================

async def create_voice(text):

    voice_file = OUTPUT_DIR / "voice.mp3"

    speech = edge_tts.Communicate(
        text,
        VOICE
    )

    await speech.save(
        str(voice_file)
    )

    return voice_file


# ==============================
# MAIN PROGRAM
# ==============================

def main():

    print("================================")
    print("        CURIOX AI SYSTEM")
    print("================================")

    print("Channel:", CHANNEL_NAME)
    print("Topic:", TOPIC)

    print("\nGenerating AI script...")

    data = generate_content()

    print("\n--------------------------------")
    print("TITLE")
    print("--------------------------------")

    print(data["title"])

    print("\n--------------------------------")
    print("SCRIPT")
    print("--------------------------------")

    print(data["script"])

    print("\nCreating AI voice...")

    voice_file = asyncio.run(
        create_voice(
            data["script"]
        )
    )

    # ==============================
    # SAVE METADATA
    # ==============================

    metadata_file = OUTPUT_DIR / "metadata.json"

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

    print("\n--------------------------------")
    print("FILES CREATED")
    print("--------------------------------")

    print("Voice:")
    print(voice_file)

    print("Metadata:")
    print(metadata_file)

    print("\n================================")
    print("   CURIOX VIDEO DATA READY")
    print("================================")


# ==============================
# START
# ==============================

if __name__ == "__main__":
    main()
