from flask import Flask, request, jsonify
import requests
from escpos.printer import Usb
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# epson = Usb(0x04b8, 0x0202, 0, )
epson = Usb(0x04b8, 0x0202, 0, profile="TM-T88IV")


def resized_image(unprocessed_image, max_width=512):
    width, height = unprocessed_image.size
    new_height = int((max_width / width) * height)
    return unprocessed_image.resize((max_width, new_height))


@app.route('/print-image', methods=['POST'])
def print_image():
    try:
        data = request.get_json()

        image_url = data.get('image_url')

        print("Url:", image_url)

        if not image_url:
            return jsonify({'error': 'Invalid input'}), 400

        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve image'}), 400

        image = Image.open(BytesIO(response.content))

        resized = resized_image(image)

        epson.image(resized, center=True)
        epson.cut()

        return jsonify({'message': 'Successfully printed'}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


if __name__ == '__main__':
    from waitress import serve
    print("Listening to incoming requests on port 8080")
    serve(app, host="0.0.0.0", port=8080)
