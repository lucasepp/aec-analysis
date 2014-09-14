from flask import Flask
from flask import request, render_template, send_file, logging
from flask.ext.socketio import SocketIO, emit
from flask.ext.uploads import UploadSet, configure_uploads
import os
import services


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
DEFAULT_PORT = 5000

socketio = SocketIO(app)

log = logging.getLogger('run')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

photos = UploadSet()
photos.file_allowed = lambda a, b: True

app.config['UPLOADS_DEFAULT_DEST'] = '/tmp'
configure_uploads(app, photos)

@app.route('/')
def index_demo():
    return render_template('app.html')


@app.route('/admin')
def admin():
    keys = services.get_data_keys()
    return render_template('admin.html', data_keys=keys)

@app.route('/admin/labels', methods=['POST',])
def admin_label_change():
    log.info('Form: %s' % (request.form, ))
    label = request.form['input_label']
    nodes_tag = request.form['nodes-tag']
    bars_tag = request.form['bars-tag']
    force_nodes_tag = request.form['force_nodes-tag']
    force_bars_tag = request.form['force_bars-tag']

    keys = services.get_data_keys()
    return render_template('admin.html', data_keys=keys)

@app.route('/api/<channel>', methods=['POST',])
def api_upload_channel(channel):
    services.save_and_notify_upload(socketio, photos, request.files['data'], channel)
    return 'ok'


@app.route('/socket.io')
def return_socketiojs():
    return send_file('static/js/socket.io-1.1.0.js')


@socketio.on('data', namespace='/data')
def data_message(message):
    emit('data', message, broadcast=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', str(DEFAULT_PORT)))
    if port == 0:
        port = DEFAULT_PORT
    app.debug = len(os.environ.get('DEBUG', '')) != 0
    socketio.run(app, port=port, host='0.0.0.0')
