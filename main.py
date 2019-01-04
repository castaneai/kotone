import os
import io
from flask import Flask, request, jsonify, render_template, send_file, abort
from kotone import Kotone
from credstore import get_flows, CloudDatastoreCredStore, LocalCredStore

app = Flask(__name__, template_folder='.')
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
    kotone = Kotone(DEVICE_ID, cred_mc, cred_mm)
    return jsonify(kotone.get_songs())


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


if __name__ == '__main__':
    app.run()
