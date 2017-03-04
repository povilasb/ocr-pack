from flask import render_template, Flask, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    return 'ok'


@app.route('/img/<int:img_id>')
def render_image(img_id):
    return render_template('show_image.html', img_id=img_id)


@app.route('/chars/<filename>')
def send_image(filename):
    return send_from_directory('chars', filename)


if __name__ == '__main__':
    app.run()
