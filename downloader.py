def download_songs():
    import json
    import yt_dlp
    import os

    # Função para carregar os links do arquivo JSON
    def load_links(filename='youtube_links.json'):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    # Função para baixar os vídeos/áudios do YouTube usando yt-dlp
    def download_audio(url, title, output_dir='downloads'):
        # Verifica se o diretório de saída existe, caso contrário cria
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Caminho do arquivo esperado
        output_file = os.path.join(output_dir, f"{title}.mp3")
        
        # Verificar se o arquivo já existe
        if os.path.exists(output_file):
            print(f"Arquivo já existe: {output_file}, pulando download.")
            return

        # Configurações do yt-dlp para download de áudio
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Nome do arquivo e pasta de destino
            'quiet': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Baixa o áudio no formato MP3
                'preferredquality': '192',
            }],
        }

        # Baixar o conteúdo do URL usando yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    # Carregar os links do arquivo JSON
    song_links = load_links()

    # Baixar os áudios para cada link encontrado
    for song in song_links:
        if song['url']:
            print(f"\nBaixando: {song['title']} - {song['artist']}...")
            download_audio(song['url'], song['title'])
        else:
            print(f"Link ausente para {song['title']} - {song['artist']}, pulando...")

if __name__ == "__main__":
    download_songs()