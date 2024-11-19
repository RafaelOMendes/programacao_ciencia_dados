def fetch_youtube_links():
    import json
    import yt_dlp

    # Função para carregar os dados do arquivo JSON
    def load_data(filename='billboard_data.json'):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    # Função para buscar o link do YouTube baseado no título da música e nome do cantor
    def get_youtube_link(song_title, artist):
        search_query = f"{song_title} {artist}"
        print(f"Buscando link do YouTube para: {search_query}...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'default_search': 'ytsearch1',  # Pesquisa e retorna o primeiro resultado
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(search_query, download=False)
            video_url = results['entries'][0]['webpage_url']
            print(f"Link encontrado: {video_url}")
            return video_url

    # Carregar os dados salvos
    song_data = load_data()

    # Lista para armazenar os links encontrados
    song_links = []

    # Buscar links no YouTube para cada música
    for song in song_data:
        try:
            video_url = get_youtube_link(song['title'], song['artist'])
            song_links.append({"date": song['date'], "title": song['title'], "artist": song['artist'], "url": video_url})
        except Exception as e:
            print(f"Erro ao buscar link para {song['title']} - {song['artist']}: {e}")
            song_links.append({"date": song['date'], "title": song['title'], "artist": song['artist'], "url": None})

    # Salvar os links em um novo arquivo JSON
    with open('youtube_links.json', 'w', encoding='utf-8') as file:
        json.dump(song_links, file, ensure_ascii=False, indent=4)
        print("\nLinks salvos em youtube_links.json")

if __name__ == "__main__":
    fetch_youtube_links()