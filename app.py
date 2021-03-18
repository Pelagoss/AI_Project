import os
from datetime import datetime
from shutil import copyfile

from flask import Flask, render_template, url_for, redirect
import portail

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/predict/portail')
def predict_portail():
    return {
  "session": {
    "id": "example_session_id",
    "params": {}
  },
  "prompt": {
    "override": False,
    "firstSimple": {
      "speech": "Le portail est "+portail.predict()[0],
      "text": ""
    }
  },
  "scene": {
    "name": "SceneName",
    "slots": {"status":"FINAL"},
    "next": {
      "name": "actions.scene.END_CONVERSATION"
    }
  }
}


@app.route('/train/portail')
def train_portail():
    class_predicted, message, labels=portail.predict()
    return render_template("train.html.twig", predicted=class_predicted, labels=labels)


@app.route('/train/portail/<string:classe>')
def set_classe_portail(classe):
    copyfile('static/output.jpg', os.path.join("camera/"+classe, datetime.now().strftime("%d%m%Y%H%M%S%f")+'.jpg'))
    return redirect(url_for('train_portail'))


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('server.crt','server.key'))