import openai
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    audio_path = "podcasts/hipsters_154_testes.mp3"
    file_name = "hipsters_154_testes"
    podcast_url = "https://www.hipsters.tech/testes-de-software-e-inteligencia-artificial-hipsters-154/"

    openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == '__main__':
    main()