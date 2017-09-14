import os
import shutil

from flask import render_template, Flask, send_from_directory, request

from . import fs


app = Flask(__name__, root_path=os.getcwd())


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
    shutil.copyfile(img_file, fs.new_char_file(label_dir))


if __name__ == '__main__':
    app.run()
