import os
from datetime import datetime
from shutil import copyfile

from flask import Flask, render_template, url_for, redirect, jsonify, make_response
import Portail.portail as portail

import google_auth

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.register_blueprint(google_auth.app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

port = int(os.environ.get('PORT', 5000))

@app.route('/predict/portail', methods=['GET', 'POST'])
def predict_portail():
    return make_response(jsonify({'fulfillmentText': 'Le portail est '+portail.predict()[0]}))


@app.route('/train/portail')
def train_portail():
    class_predicted, message, labels=portail.predict()
    return render_template("train.html.twig", predicted=class_predicted, labels=labels)


@app.route('/train/portail/<string:classe>')
def set_classe_portail(classe):
    copyfile('static/output.jpg', "Portail/camera/" + classe.lower() + datetime.now().strftime("%d%m%Y%H%M%S%f") + '.jpg')
    return redirect(url_for('train_portail'))


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=port, ssl_context=('server.crt','server.key'))
    #app.run(host='0.0.0.0', port=port)
    app.run()

