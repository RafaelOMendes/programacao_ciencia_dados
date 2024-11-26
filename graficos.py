import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo para os gráficos
sns.set(style="whitegrid")

# Caminho para o arquivo JSON único
json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'processed_music.json')

# Função para carregar os dados do JSON em um DataFrame
def load_data_from_json(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Carregar o JSON como uma lista de dicionários
        return pd.DataFrame(data)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erro ao carregar o arquivo JSON: {e}")
        return pd.DataFrame()
    

# Carregar os dados
df = load_data_from_json(json_file)

# Garantir que as colunas sejam numéricas ou de datetime
df['tempo'] = pd.to_numeric(df['tempo'], errors='coerce')
df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year

# Remover entradas inválidas
df = df.dropna(subset=['tempo', 'year'])

# Gráfico 1: Evolução do BPM ao longo dos anos
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='year', y='tempo', marker='o', color='blue')
plt.title('Evolução do BPM ao Longo dos Anos', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('BPM', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(visible=True, linestyle='--', alpha=0.7)
plt.show()

# Traduzir notas musicais para o sistema brasileiro
note_translation = {
    "C": "Dó", "D": "Ré", "E": "Mi", "F": "Fá", 
    "G": "Sol", "A": "Lá", "B": "Si", 
    "C#": "Dó#", "D#": "Ré#", "F#": "Fá#", 
    "G#": "Sol#", "A#": "Lá#"
}

# Criar uma coluna para armazenar a nota mais frequente de cada música
df['most_frequent_note'] = df['chroma_notes'].apply(
    lambda notes: note_translation.get(notes[0]['note'], notes[0]['note']) if notes and isinstance(notes, list) else None
)

# Contar a frequência de cada nota traduzida
note_frequency = df['most_frequent_note'].value_counts()

# Gráfico da frequência de aparição das notas mais frequentes
plt.figure(figsize=(10, 6))
sns.barplot(x=note_frequency.index, y=note_frequency.values, palette='coolwarm')
plt.title('Frequência de Aparição das Notas Mais Frequentes', fontsize=16)
plt.xlabel('Nota', fontsize=12)
plt.ylabel('Frequência', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(visible=True, linestyle='--', alpha=0.7)
plt.show()

# Gráfico de intensidade média das notas
# Criar um DataFrame para trabalhar com as intensidades
chroma_df = pd.json_normalize(df['chroma_notes'].explode())
if not chroma_df.empty:
    mean_chroma = chroma_df.groupby('note')['intensity'].mean().sort_values(ascending=False)
    mean_chroma.index = mean_chroma.index.map(lambda x: note_translation.get(x, x))  # Aplicar tradução aqui também
    plt.figure(figsize=(10, 6))
    sns.barplot(x=mean_chroma.index, y=mean_chroma.values, palette='viridis')
    plt.title('Intensidade Média das Notas Musicais', fontsize=16)
    plt.xlabel('Nota', fontsize=12)
    plt.ylabel('Intensidade Média', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.show()

    # Gráfico de duração média das músicas por ano
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df.groupby('year')['duration'].mean().reset_index(), x='year', y='duration', marker='o', color='green')
    plt.title('Duração Média das Músicas por Ano', fontsize=16)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Duração Média (segundos)', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.show()

    # Criar uma nova coluna que combine título e artista
    df['track_artist'] = df['title'] + " - " + df['artist']

    # Contar a frequência das combinações únicas de título e artista
    track_artist_frequency = df['track_artist'].value_counts()

    # Criar gráfico das músicas mais repetidas (considerando artista)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=track_artist_frequency.index[:10], y=track_artist_frequency.values[:10], palette='coolwarm')
    plt.title('Músicas que Mais se Repetem (Considerando Artista)', fontsize=16)
    plt.xlabel('Música e Artista', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.show()

    # Gráfico 4: Artistas com mais músicas
    if 'artist' in df.columns:
        # Contar o número de músicas por artista
        artist_counts = df['artist'].value_counts()

        # Limitar a exibição aos 20 artistas mais frequentes (opcional)
        top_artists = artist_counts.head(20)

        plt.figure(figsize=(12, 8))
        sns.barplot(y=top_artists.index, x=top_artists.values, palette='magma')
        plt.title('Artistas que Mais Aparecem')
        plt.xlabel('Número de Músicas')
        plt.ylabel('Artista')
        plt.grid(axis='x')
        plt.show()

        # Contar músicas únicas por artista
        unique_tracks_by_artist = df.groupby('artist')['title'].nunique().sort_values(ascending=False)

        # Criar gráfico para os 10 artistas com mais músicas diferentes
        plt.figure(figsize=(12, 8))
        sns.barplot(
            x=unique_tracks_by_artist.head(10).values, 
            y=unique_tracks_by_artist.head(10).index, 
            palette='viridis'
        )

        plt.title('Artistas com Mais Músicas Diferentes', fontsize=16)
        plt.xlabel('Número de Músicas Diferentes', fontsize=12)
        plt.ylabel('Artista', fontsize=12)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.show()
    else:
        print("Coluna 'artist' não encontrada nos dados.")


else:
    print("Nenhuma informação sobre notas musicais disponível para criar o gráfico.") 
