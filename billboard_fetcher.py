def fetch_billboard_data():
        
    import requests
    from bs4 import BeautifulSoup
    import json

    # Lista para armazenar os dados
    song_data = []

    # Anos e meses para buscar dados
    years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013]
    months = range(1, 13)  # De Janeiro a Dezembro

    # Headers para simular um navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for year in years:
        for month in months:
            # Formatar a data no formato YYYY-MM-DD
            date = f"{year}-{month:02d}-01"
            url = f"https://www.billboard.com/charts/hot-100/{date}"
            print(f"\nObtendo dados da Billboard para {date}...")

            try:
                # Fazer requisição para o site
                response = requests.get(url, headers=headers)
                
                # Verificar se a requisição foi bem-sucedida
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Encontrar a música número 1
                    top_song_tag = soup.find('h3', class_='c-title')  # Ajuste aqui baseado no HTML inspecionado
                    if top_song_tag:
                        top_song = top_song_tag.get_text(strip=True)
                    else:
                        top_song = "Música não encontrada"

                    # Encontrar o artista da música número 1
                    artist_tag = soup.find('span', class_='a-no-trucate')  # Ajuste aqui baseado no HTML inspecionado
                    if artist_tag:
                        top_artist = artist_tag.get_text(strip=True)
                    else:
                        top_artist = "Artista não encontrado"

                    # Salvar os dados
                    song_data.append({"date": date, "title": top_song, "artist": top_artist})
                    print(f"Música número 1 em {date}: {top_song} - {top_artist}")
                else:
                    print(f"Falha ao acessar a página para {date} (status code: {response.status_code})")
            
            except Exception as e:
                print(f"Erro ao processar {date}: {e}")

    # Salvar os dados em um arquivo JSON
    with open('billboard_data.json', 'w') as file:
        json.dump(song_data, file, indent=4)

    print("\nDados salvos no arquivo 'billboard_data.json'!")

if __name__ == "__main__":
    fetch_billboard_data()