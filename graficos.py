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
    
#aqui começa a festa

#aqui começa a festa

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

# Gráfico 2: Distribuição de BPM por ano
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='year', y='tempo', palette='Set2')
plt.title('Distribuição de BPM por Ano', fontsize=16)
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

    # Gráfico: Músicas que mais se repetem
    # Supondo que 'track_name' seja a coluna que armazena os nomes das músicas
    track_frequency = df['title'].value_counts()

    # Criar gráfico das músicas mais repetidas
    plt.figure(figsize=(12, 6))
    sns.barplot(x=track_frequency.index[:10], y=track_frequency.values[:10], palette='coolwarm')
    plt.title('Músicas que Mais se Repetem', fontsize=16)
    plt.xlabel('Música', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(visible=True, linestyle='--', alpha=0.7)
    plt.show()


else:
    print("Nenhuma informação sobre notas musicais disponível para criar o gráfico.") 
