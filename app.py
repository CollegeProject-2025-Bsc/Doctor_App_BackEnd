from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import firestore, credentials
from twilio.rest import Client
import random


## twilio auth credential
TWILIO_ACCOUNT_SID = 'ACe13f73d65b4d20704f76f70631e64c9f'
TWILIO_AUTH_TOKEN = '42eef7a34c4000944d424ad30f7f96da'
TWILIO_PHONE_NUMBER = '+17627631791'




## twilio client initializing
twilio_client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)




## initializing firebase client
cred = credentials.Certificate('admin.json') ## admin.json is out credential file for firebase account
firebase_admin.initialize_app(cred)
db = firestore.client()




## initializing flask
app = Flask(__name__)




## method for generating otp
def create_otp():
    return random.randint(100000,999999)



## method for sending otp to the front end
@app.route('/getOtp', methods=['POST'])
def getOtp():
    phone_number = request.get_json().get('phoneNumber')
    otp = create_otp()
    send_otp(phone_number,otp)
    return jsonify({'otp':otp}),200


## method for sending otp through msg
def send_otp(phone,otp):
    message = twilio_client.messages.create(
        from_= TWILIO_PHONE_NUMBER,
        body= f'your otp is : {otp} for HEALTH SATHI APP',
        to = phone
    )
    return message.sid



## our default route
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


## route for getting popular doctor
@app.route('/popular_docs')
def getPopularDoctors():
    db_ref = db.collection('Department').document("0Z0REKdBoh26uztxls5O").collection("Doctors").stream()
    return jsonify(list(map(lambda doc: doc.to_dict(), db_ref)))


## route for getting department
@app.route('/Department', methods = ['POST'])
def getDepartmentData():
    if request.method == 'POST':
        db_ref = db.collection('Department').stream()
        return jsonify(list(map(lambda doc: doc.to_dict(), db_ref)))
    else:
        return None




## main function
if __name__ == '__main__':
    app.run()



## last block of our app.py file
## Run the app.py using this command in terminal   ------>    python .\app.py
## then open a new terminal
## And run this command to redirect all request to our local host   ------>    ngrok http --url=safely-massive-seahorse.ngrok-free.app 5000
## backend url is ------>   https://safely-massive-seahorse.ngrok-free.app

