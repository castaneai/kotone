import os
import io
import tempfile
import slack
from flask import Flask, request, jsonify, render_template, send_file, abort
from kotone import Kotone
from credstore import get_flows, CloudDatastoreCredStore, LocalCredStore

app = Flask(__name__, template_folder='.', static_folder='./view/build', static_url_path='')
DEVICE_ID = os.environ['KOTONE_DEVICE_ID']
credstore = CloudDatastoreCredStore() if 'GAE_APPLICATION' in os.environ else LocalCredStore()


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    flow_mc, flow_mm = get_flows()
    code_mc = request.form.get('code_mc', None)
    code_mm = request.form.get('code_mm', None)
    if None in (code_mc, code_mm):
        return render_template('auth.html',
                               auth_url_mc=flow_mc.step1_get_authorize_url(),
                               auth_url_mm=flow_mm.step1_get_authorize_url())
    cred_mc = flow_mc.step2_exchange(code_mc)
    cred_mm = flow_mm.step2_exchange(code_mm)
    credstore.save_creds(cred_mc, cred_mm)

    return jsonify(status='OK', client_id_mc=cred_mc.client_id, client_id_mm=cred_mm.client_id)


@app.route('/api/songs')
def get_songs():
    cred_mc, cred_mm = credstore.get_creds()
    if None in (cred_mc, cred_mm):
        abort(401)
    kotone = Kotone(DEVICE_ID, cred_mc, cred_mm)
    return jsonify(kotone.get_songs())


@app.route('/api/stream/<song_id>')
def stream(song_id):
    cred_mc, cred_mm = credstore.get_creds()
    if None in (cred_mc, cred_mm):
        abort(401)
    kotone = Kotone(DEVICE_ID, cred_mc, cred_mm)
    try:
        stream_url = kotone.stream_url(song_id)
    except Exception as e:
        if 'Not Found' in str(e):
            abort(404)
    return jsonify(stream_url=stream_url)


@app.route('/api/download/<song_id>')
def download(song_id):
    cred_mc, cred_mm = credstore.get_creds()
    kotone = Kotone(DEVICE_ID, cred_mc, cred_mm)
    try:
        fname, data = kotone.download_song(song_id)
    except Exception as e:
        if 'Not Found' in str(e):
            return abort(404)
        else:
            raise
    return send_file(io.BytesIO(data), 'audio/mp3', as_attachment=True, attachment_filename=fname)


@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file[]' not in request.files:
        return abort(422)
    paths = []
    for f in request.files.getlist('file[]'):
        tf = tempfile.NamedTemporaryFile()
        f.save(tf.name)
        paths.append(tf.name)

    cred_mc, cred_mm = credstore.get_creds()
    kotone = Kotone(DEVICE_ID, cred_mc, cred_mm)
    uploaded, matched, not_uploaded = kotone.upload(paths)
    for file, reason in not_uploaded.items():
        print(f"not uploaded: {reason} [{file}]")
    uploaded_song_ids = list(uploaded.values())
    new_songs = [song for song in kotone.get_songs() if song['id'] in uploaded_song_ids]
    if 'KOTONE_SLACK_WEBHOOK_URL' in os.environ:
        webhook_url = os.environ['KOTONE_SLACK_WEBHOOK_URL']
        slack.notify_slack(webhook_url, new_songs)
    return 'ok'


if __name__ == '__main__':
    app.run()
