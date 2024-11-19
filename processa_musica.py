import librosa
import numpy as np
import os
import difflib
import json


class MusicProcessor:
    def __init__(self, music_data, music_dir="Music"):
        """
        Inicializa o MusicProcessor com os dados da música e o diretório dos arquivos.
        :param music_data: Dicionário contendo informações da música (JSON original).
        :param music_dir: Diretório onde os arquivos de música estão armazenados.
        """
        self.music_data = music_data
        self.music_dir = music_dir
        self.audio_file = None

    def find_audio_file(self):
        """
        Procura pelo arquivo de áudio mais próximo com base no título da música.
        """
        title = self.music_data.get("title", "").lower()
        if not title:
            raise ValueError("O título da música não foi fornecido.")

        # Listar arquivos na pasta Music
        files = os.listdir(self.music_dir)
        audio_files = [f for f in files if f.endswith(('.wav', '.mp3', '.flac'))]

        # Encontrar o arquivo com o nome mais próximo
        matches = difflib.get_close_matches(title, audio_files, n=1, cutoff=0.3)
        if matches:
            self.audio_file = os.path.join(self.music_dir, matches[0])
            print(f"Arquivo encontrado: {self.audio_file}")
        else:
            raise FileNotFoundError(f"Nenhum arquivo encontrado para o título '{title}'.")

    def extract_audio_features(self):
        """
        Extrai informações da música usando librosa.
        :return: Dicionário com os dados extraídos.
        """
        if not self.audio_file or not os.path.exists(self.audio_file):
            raise FileNotFoundError("Arquivo de áudio não encontrado para análise.")

        print(f"Analisando o arquivo: {self.audio_file}")
        y, sr = librosa.load(self.audio_file, sr=None)

        # Extrair informações com librosa
        duration = librosa.get_duration(y=y, sr=sr)  # Duração em segundos
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)  # BPM (tempo)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)  # Matriz de cromas
        mean_chroma = chroma.mean(axis=1)  # Média de intensidade por nota

        # Traduzir cromograma para notas
        chroma_notes = self.translate_chroma_to_notes(mean_chroma)

        # Retornar dados convertidos
        return {
            "duration": float(duration),  # Converter para tipo float serializável
            "tempo": float(tempo),  # Converter para tipo float serializável
            "chroma_mean": [float(val) for val in mean_chroma],  # Converter ndarray para lista de floats
            "chroma_notes": chroma_notes,  # Notas traduzidas
        }


    @staticmethod
    def translate_chroma_to_notes(chroma_mean):
        """
        Traduz o vetor chroma_mean para as notas correspondentes.
        :param chroma_mean: Vetor com as médias de intensidade das 12 notas.
        :return: Lista de notas ordenadas pela intensidade.
        """
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        # Associar notas às intensidades
        note_intensity = list(zip(notes, chroma_mean))
        # Ordenar por intensidade (maior para menor)
        sorted_notes = sorted(note_intensity, key=lambda x: x[1], reverse=True)
        # Retornar apenas as notas (ou incluir intensidades, se necessário)
        return [{"note": note, "intensity": round(intensity, 3)} for note, intensity in sorted_notes]

    def process(self):
        """
        Realiza o processamento completo da música:
        1. Encontra o arquivo de áudio.
        2. Extrai os recursos do áudio.
        3. Atualiza o JSON com os novos dados.
        """
        self.find_audio_file()
        audio_features = self.extract_audio_features()
        self.music_data.update(audio_features)
        return self.music_data


class NumpyEncoder(json.JSONEncoder):
    """Encoder customizado para converter tipos NumPy em tipos compatíveis com JSON."""
    def default(self, obj):
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        elif isinstance(obj, (np.floating, float)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def process_all_music(json_file, music_dir="Music", output_file="processed_music.json"):
    """
    Processa todas as músicas listadas em um arquivo JSON.
    :param json_file: Caminho para o arquivo JSON com os dados das músicas.
    :param music_dir: Diretório onde os arquivos de música estão armazenados.
    :param output_file: Nome do arquivo JSON de saída.
    """
    with open(json_file, "r") as f:
        music_list = json.load(f)

    processed_data = []
    for music_data in music_list:
        try:
            processor = MusicProcessor(music_data, music_dir)
            updated_data = processor.process()
            processed_data.append(updated_data)
            print(f"Processado: {music_data['title']}")
        except Exception as e:
            print(f"Erro ao processar {music_data['title']}: {e}")

    # Salvar os dados atualizados no arquivo de saída usando o encoder customizado
    with open(output_file, "w") as f:
        json.dump(processed_data, f, indent=4, cls=NumpyEncoder)
    print(f"Dados processados salvos em {output_file}")


# Exemplo de uso
if __name__ == "__main__":
    process_all_music("youtube_links.json", music_dir="Music", output_file="processed_music.json")
