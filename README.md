# Baixador de Aulas / Vídeos do YouTube

Projeto simples em Python para baixar vídeos e aulas do YouTube e assistir
depois, offline, com **escolha de qualidade** (4K, 1080p, 720p, 480p) ou
apenas o **áudio em MP3**.

## O que já está instalado na sua máquina
- Python 3.13
- ffmpeg (necessário para juntar vídeo + áudio e converter MP3)
- yt-dlp (instalado via `requirements.txt`)

## Instalação (só na primeira vez)
Abra o terminal nesta pasta e rode:

```bash
pip install -r requirements.txt
```

## Como usar

### Modo fácil (menu interativo)
Dê **duplo clique** no arquivo `Baixar.bat`, ou rode no terminal:

```bash
python baixar.py
```

O programa vai pedir a URL e mostrar o menu de qualidade:

```
  1. Melhor qualidade disponivel (4K/8K se houver)
  2. 1080p (Full HD)
  3. 720p (HD)
  4. 480p (economico)
  5. Somente audio (MP3)
```

### Modo linha de comando (mais rápido)

```bash
# 1080p (Full HD)
python baixar.py "https://youtu.be/XXXX" --qualidade 1080

# Melhor qualidade possível
python baixar.py "https://youtu.be/XXXX" --qualidade 4k

# Somente áudio em MP3
python baixar.py "https://youtu.be/XXXX" --audio
```

## Onde ficam os arquivos
Todos os downloads são salvos na subpasta **`Downloads`** (criada
automaticamente dentro desta pasta).

## Recursos
- Escolha de qualidade do vídeo ou só áudio (MP3 192kbps)
- Suporta **playlists inteiras** (basta colar a URL da playlist)
- Barra de progresso com velocidade e tempo restante
- Nomes de arquivo compatíveis com Windows
- Continua a lista mesmo se um vídeo falhar

## Atualizar o yt-dlp
O YouTube muda com frequência. Se algum download parar de funcionar,
atualize a biblioteca:

```bash
pip install -U yt-dlp
```

## Aviso
Use apenas para conteúdo que você tem direito de baixar (aulas, material
educacional, vídeos próprios ou com licença que permita). Respeite os
Termos de Serviço do YouTube e os direitos autorais dos criadores.
