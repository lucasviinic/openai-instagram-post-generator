from openai import OpenAI
from dotenv import load_dotenv
import os


def openai_gpt_text_summarizer(completed_transcription: str, file_name: str, client: OpenAI) -> str:
    print("Resumindo com o gpt para um post do instagram...")

    system_prompt = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.

    """
    user_prompt = ". \nReescreva a transcrição acima para que possa ser postado como uma legenda do Instagram. Ela deve resumir o texto para chamada na rede social. Inclua hashtags"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": completed_transcription + user_prompt
            }
        ],
        temperature=0.6
    )

    instagram_summary = response.choices[0].message.content

    with open(f"instagram_summary_{file_name}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(instagram_summary)

    return instagram_summary

def openai_whisper_transcribe(audio_path: str, file_name: str, whisper_model: str, openai_client: OpenAI) -> str:
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

    instagram_summary = openai_gpt_text_summarizer(completed_transcription, file_name, client)

if __name__ == '__main__':
    main()