# -*- coding: utf-8 -*-
"""
Baixador de vídeos/aulas do YouTube.

Permite escolher a qualidade do vídeo (4K, 1080p, 720p, 480p) ou baixar
somente o áudio em MP3. Usa a biblioteca yt-dlp e o ffmpeg para juntar
os streams de vídeo e áudio na melhor qualidade possível.

Uso:
    python baixar.py
    (o programa vai pedir a URL e a qualidade de forma interativa)

Ou direto pela linha de comando:
    python baixar.py "https://youtu.be/XXXX" --qualidade 1080
    python baixar.py "https://youtu.be/XXXX" --audio
"""

import argparse
import os
import sys

try:
    from yt_dlp import YoutubeDL
except ImportError:
    print("A biblioteca 'yt-dlp' nao esta instalada.")
    print("Instale com o comando:  pip install -r requirements.txt")
    sys.exit(1)


# Pasta onde os downloads serao salvos (subpasta 'Downloads' ao lado do script)
PASTA_DOWNLOADS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Downloads")


# Opcoes de qualidade oferecidas no menu.
# A "format string" do yt-dlp escolhe o melhor video ate a altura pedida
# (ex.: 1080p) e junta com o melhor audio disponivel.
OPCOES_QUALIDADE = {
    "1": ("Melhor qualidade disponivel (4K/8K se houver)", "bestvideo+bestaudio/best"),
    "2": ("1080p (Full HD)", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
    "3": ("720p (HD)", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
    "4": ("480p (economico)", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
    "5": ("Somente audio (MP3)", "audio"),
}


def _hook_progresso(d):
    """Mostra o progresso do download de forma limpa."""
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        velocidade = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\r  Baixando... {percent}  |  {velocidade}  |  faltam {eta}   ",
              end="", flush=True)
    elif d["status"] == "finished":
        print("\r  Download concluido. Processando/convertendo...            ")


def montar_opcoes(formato):
    """Monta o dicionario de configuracoes do yt-dlp conforme a escolha."""
    opcoes = {
        "outtmpl": os.path.join(PASTA_DOWNLOADS, "%(title)s.%(ext)s"),
        "progress_hooks": [_hook_progresso],
        "noplaylist": False,      # baixa playlist inteira se a URL for de playlist
        "ignoreerrors": True,     # continua mesmo se um video da lista falhar
        "restrictfilenames": True,  # evita caracteres invalidos no Windows
    }

    if formato == "audio":
        # Extrai o audio e converte para MP3 na melhor taxa.
        opcoes["format"] = "bestaudio/best"
        opcoes["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        opcoes["format"] = formato
        # Garante saida em MP4 quando possivel (mais compativel).
        opcoes["merge_output_format"] = "mp4"

    return opcoes


def baixar(url, formato):
    """Executa o download de fato."""
    os.makedirs(PASTA_DOWNLOADS, exist_ok=True)
    opcoes = montar_opcoes(formato)

    print(f"\nSalvando em: {PASTA_DOWNLOADS}\n")
    with YoutubeDL(opcoes) as ydl:
        ydl.download([url])
    print("\nPronto! Arquivo(s) salvo(s) na pasta 'Downloads'.\n")


def menu_interativo():
    """Fluxo interativo quando o script e rodado sem argumentos."""
    print("=" * 55)
    print("     BAIXADOR DE AULAS / VIDEOS DO YOUTUBE")
    print("=" * 55)

    url = input("\nCole a URL do video (ou playlist): ").strip()
    if not url:
        print("Nenhuma URL informada. Encerrando.")
        return

    print("\nEscolha a qualidade:")
    for chave, (descricao, _) in OPCOES_QUALIDADE.items():
        print(f"  {chave}. {descricao}")

    escolha = input("\nDigite o numero da opcao (padrao = 2): ").strip() or "2"
    if escolha not in OPCOES_QUALIDADE:
        print("Opcao invalida. Usando 1080p como padrao.")
        escolha = "2"

    formato = OPCOES_QUALIDADE[escolha][1]
    baixar(url, formato)


def main():
    parser = argparse.ArgumentParser(
        description="Baixa videos/aulas do YouTube com escolha de qualidade."
    )
    parser.add_argument("url", nargs="?", help="URL do video ou playlist")
    parser.add_argument(
        "--qualidade", choices=["4k", "1080", "720", "480"],
        help="Qualidade maxima do video"
    )
    parser.add_argument(
        "--audio", action="store_true", help="Baixar somente o audio em MP3"
    )
    args = parser.parse_args()

    # Sem URL -> modo interativo (menu).
    if not args.url:
        menu_interativo()
        return

    # Com URL -> modo linha de comando.
    if args.audio:
        formato = "audio"
    else:
        mapa = {
            "4k": OPCOES_QUALIDADE["1"][1],
            "1080": OPCOES_QUALIDADE["2"][1],
            "720": OPCOES_QUALIDADE["3"][1],
            "480": OPCOES_QUALIDADE["4"][1],
        }
        formato = mapa.get(args.qualidade, OPCOES_QUALIDADE["2"][1])

    baixar(args.url, formato)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload cancelado pelo usuario.")
    except Exception as erro:
        print(f"\nOcorreu um erro: {erro}")
