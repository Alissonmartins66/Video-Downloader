import requests
from flask import Flask, request, send_file, render_template, jsonify
import yt_dlp
import os

app = Flask(__name__)
output_path = os.path.expanduser("~/Downloads")

@app.route('/get_thumbnail', methods=['GET'])
def get_thumbnail():
    url = request.args.get('video_url')

    if not url:
        return jsonify({'error': 'O URL do vídeo não foi fornecido.'}), 400

    ydl_opts = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        thumbnail_url = info.get('thumbnail')

    return jsonify({'thumbnail_url': thumbnail_url})

@app.route('/')
def homepage():
    video_url = request.args.get('video_url')
    return render_template('homepage.html', video_url=video_url)

def resolve_short_url(short_url):
    try:
        # Envia uma solicitação HEAD para o URL encurtado para seguir redirecionamentos
        response = requests.head(short_url, allow_redirects=True)
        full_url = response.url
        return full_url
    except Exception as e:
        print(f"Erro ao resolver URL encurtado: {str(e)}")
        return None

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('video_url')
    selected_format = request.form.get('format')

    if not url:
        return 'O URL do vídeo não foi fornecido.', 400

    # Verifica se o URL é um URL encurtado e tenta desencurtá-lo
    if "youtu.be" in url:
        full_url = resolve_short_url(url)
        if full_url:
            url = full_url
        else:
            return 'Erro ao resolver URL encurtado.', 400

    format_map = {
        'video': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'audio': 'bestaudio/best',
    }

    if selected_format in format_map:
        ydl_opts = {
            'format': format_map[selected_format],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'media')  # Nome do vídeo ou áudio
            filename = f"{title}.{'mp4' if selected_format == 'video' else 'mp3'}"
            ydl.download([url])

        media_path = os.path.join(output_path, filename)
        if os.path.exists(media_path):
            return send_file(media_path, as_attachment=True)
        else:
            return f'Arquivo baixado! Confira em sua pasta de download padrão.'
    else:
        return 'Formato selecionado não é válido.', 400


if __name__ == '__main__':
    app.run(debug=True)
