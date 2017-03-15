import os

from flask import render_template, Flask, send_from_directory, request

import fs
import gfx

app = Flask(__name__)


@app.route('/')
def index():
    return 'ok'


@app.route('/img/<int:img_id>')
def render_image(img_id):
    prev_result = request.args.get('content')
    if prev_result:
        classify_image(img_id - 1, prev_result)
    return render_template('show_image.html', img_id=img_id)


@app.route('/chars/<filename>')
def send_image(filename):
    return send_from_directory('chars', filename)


def classify_image(img_id: int, label: str) -> None:
    img_file = 'chars/{}.png'.format(img_id)
    label_dir = 'labelled-chars/{}'.format(label)
    os.makedirs(label_dir, exist_ok=True)
    gfx.Image.read_from(img_file).save_to(fs.new_char_file(label_dir))


if __name__ == '__main__':
    app.run()
