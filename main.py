from openai import OpenAI
from dotenv import load_dotenv
import os


def openai_whisper_transcribe(audio_path: str, file_name: str, whisper_model: str, openai_client: OpenAI):
    print(f"Transcrevendo com o whispers...")

    audio = open(audio_path, "rb")
    response = openai_client.audio.transcriptions.create(
        model=whisper_model,
        file=audio
    )
    trancription = response.text

    with open(f"completed_text_{file_name}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(trancription)

    return trancription

def main():
    load_dotenv()

    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")

    audio_path = "podcasts/como_seria_uma_civilização_extraterrestre_a_escala_de_kardashev.mp3"
    file_name = "hipsters_154_testes"

    whisper_model = "whisper-1"
    completed_transcription = openai_whisper_transcribe(audio_path, file_name, whisper_model, client)

if __name__ == '__main__':
    main()