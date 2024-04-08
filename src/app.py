from flask import Flask, request, jsonify
import requests
from models.plate_reader import PlateReader, InvalidImage

APP_HOST = '0.0.0.0'
APP_PORT = 8080

IMAGE_HOST = '178.154.220.122'
IMAGE_PORT = 7777
IMAGE_SERVER_TIMEOUT = 0.5

app = Flask(__name__)

plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


@app.route('/process_image/<int:img_id>', methods=['GET'])
def process_single_image(img_id):
    try:
        url = f'http://{IMAGE_HOST}:{IMAGE_PORT}/images/{img_id}'
        response = requests.get(url, timeout=IMAGE_SERVER_TIMEOUT)
        if response.status_code == 200:
            plate_text = plate_reader.read_text(response.content)
            return jsonify({'img_id': img_id, 'plate_text': plate_text})
        else:
            return jsonify({'error': 'Failed to download image'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/process_images', methods=['POST'])
def process_multiple_images():
    try:
        img_ids = request.json.get('img_ids', [])
        results = []

        for img_id in img_ids:
            url = f'http://{IMAGE_HOST}:{IMAGE_PORT}/images/{img_id}'
            response = requests.get(url, timeout=IMAGE_SERVER_TIMEOUT)
            if response.status_code == 200:
                plate_text = plate_reader.read_text(response.content)
                results.append({'img_id': img_id, 'plate_text': plate_text})

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT)
