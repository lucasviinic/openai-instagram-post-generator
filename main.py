from openai import OpenAI
from dotenv import load_dotenv
import os
import requests


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

def openai_gpt_hashtag_creator(instagram_summary: str, file_name: str, client: OpenAI) -> str:
    print("Gerando as hashtags com a OpenAI...")

    system_prompt = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.
    - A saída deve conter 5 hashtags.

    """

    user_prompt =f'Aqui está um resumo de um texto "{instagram_summary}". Por favor, gere 5 hashtags que sejam relevantes para este texto e que possam ser publicadas no Instagram.  Por favor, faça isso em português do Brasil'

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.6
    )

    hashtags = response.choices[0].message.content

    with open(f"hashtags_{file_name}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(hashtags)

    return hashtags

def openai_gpt_image_text_generator(instagram_summary: str, file_name: str, client: OpenAI):
    print("Gerando a saída de texto para criacao de imagens com GPT...")

    system_prompt = """
    - A saída deve ser uma única, do tamanho de um tweet, que seja capaz de descrever o conteúdo do texto para que possa ser transcrito como uma imagem.
    - Não inclua hashtags
    """

    user_prompt =  f'Reescreva o texto a seguir, em uma frase, para que descrever o texto abaixo em um tweet: {instagram_summary}'

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.6
    )

    text_to_image = response.choices[0].message.content

    with open(f"text_to_image_generation_{file_name}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text_to_image)

    return text_to_image

def openai_dalle_image_denerator(resolution: str, image_summary: str, file_name: str, client: OpenAI, qtt_images = 1):
    print("Criando uma imagem utilizando a API do DALL-E...")

    user_prompt = f"Uma pintura ultra futurista, textless, 3d que retrate: {image_summary}"

    response = client.images.generate(
        prompt=user_prompt,
        n=qtt_images,
        size=resolution
    )

    return response.data

def read_file_tool(file_name: str):
    try:
        with open(file_name, "r") as file:
            return file.read()
    except IOError as e:
        print(f"Erro no carregamento do arquivo: {e}")

def image_downloader_tool(file_name: str, generated_image: str, qtt_images = 1):
  image_names_list = []
  try:
    for image_counter in range(0, qtt_images):
        path = generated_image[image_counter].url
        image = requests.get(path)

        with open(f"{file_name}_{image_counter}.png", "wb") as image_file:
            image_file.write(image.content)

        image_names_list.append(f"{file_name}_{image_counter}.png")
    return image_names_list
  except:
    print("Ocorreu um erro!")
    return  None


def main():
    load_dotenv()

    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")

    audio_path = "podcasts/a_escala_de_kardashev.mp3"
    file_name = "a_escala_de_kardashev"
    resolution = "1024x1024"
    qtt_images = 4

    whisper_model = "whisper-1"

    completed_transcription = read_file_tool("completed_text_a_escala_de_kardashev.txt")
    instagram_summary = read_file_tool("instagram_summary_a_escala_de_kardashev.txt")
    hashtags = read_file_tool("hashtags_a_escala_de_kardashev.txt")
    instagram_image_summary = read_file_tool("text_to_image_generation_a_escala_de_kardashev.txt")

    generated_image = openai_dalle_image_denerator(resolution, instagram_image_summary, file_name, client, qtt_images)
    image_downloader_tool(file_name, generated_image, qtt_images)

if __name__ == '__main__':
    main()