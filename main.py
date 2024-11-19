from billboard_fetcher import fetch_billboard_data
from youtube_fetcher import fetch_youtube_links
from downloader import download_songs

def main():
    print("Iniciando processo completo...")
    
    # Passo 1: Coletar dados da Billboard
    #fetch_billboard_data()
    
    # Passo 2: Buscar links no YouTube
    #fetch_youtube_links()
    
    # Passo 3: Baixar músicas do YouTube
    download_songs()
    
    print("Processo completo!")

if __name__ == "__main__":
    main()
