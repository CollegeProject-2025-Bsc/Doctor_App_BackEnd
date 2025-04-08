from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import firestore, credentials


cred = credentials.Certificate('admin.json')
firebase_admin.initialize_app(cred)
db = firestore.client()



app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/data', methods = ['POST'])
def getDepartmentData():
    if request.method == 'POST':
        db_ref = db.collection('Department').stream()
        return jsonify(list(map(lambda doc: doc.to_dict(), db_ref)))
    else:
        return None





if __name__ == '__main__':
    app.run()
