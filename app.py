from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import firestore, credentials
from twilio.rest import Client
import random


## twilio auth credential
TWILIO_ACCOUNT_SID = 'ACe13f73d65b4d20704f76f70631e64c9f'
TWILIO_AUTH_TOKEN = 'f7f09156bee438719b49241279dd2fe8'
TWILIO_PHONE_NUMBER = '+17627631791'




## twilio client initializing
twilio_client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)




## initializing firebase client
cred = credentials.Certificate('admin.json') ## admin.json is out credential file for firebase account
firebase_admin.initialize_app(cred)
db = firestore.client()




## initializing flask
app = Flask(__name__)



disease_to_specialization = {
    "kidney problem":["NEPHROLOGY"],
    "kidney failure":["NEPHROLOGY"],
    "chronic kidney disease":["NEPHROLOGY"],
    "acute kidney injury":["NEPHROLOGY"],
    "kidney stones":["NEPHROLOGY"],
    "nephrotic syndrome":["NEPHROLOGY"],
    "polycystic kidney disease":["NEPHROLOGY"],
    "glomerulonephritis":["NEPHROLOGY"],
    "urinary tract infection":["NEPHROLOGY"],
    "uti":["NEPHROLOGY"],
    "blood in urine":["NEPHROLOGY"],
    "frequent urination":["NEPHROLOGY"],
    "painful urination":["NEPHROLOGY"],
    "swelling in legs or feet":["NEPHROLOGY"],
    "foamy urine":["NEPHROLOGY"],
    "high creatinine":["NEPHROLOGY"],
    "renal failure":["NEPHROLOGY"],
    "renal disease":["NEPHROLOGY"],
    "nephrology":["NEPHROLOGY"],
    "dialysis":["NEPHROLOGY"],
    "kidney pain":["NEPHROLOGY"],
    "kidney transplant":["NEPHROLOGY"],
    "kidney":["NEPHROLOGY"],

    "andrology": ["ANDROLOGY"],
    "male health": ["ANDROLOGY"],
    "testosterone therapy": ["ANDROLOGY"],
    "erectile dysfunction": ["ANDROLOGY"],
    "male fertility": ["ANDROLOGY"],
    "infertility treatment": ["ANDROLOGY"],
    "sperm count": ["ANDROLOGY"],
    "penis health": ["ANDROLOGY"],
    "prostate problems": ["ANDROLOGY"],
    "male hormone treatment": ["ANDROLOGY"],
    "sexual health": ["ANDROLOGY"],
    "low libido": ["ANDROLOGY"],
    "prostate cancer": ["ANDROLOGY","ONCOLOGY"],
    "premature ejaculation": ["ANDROLOGY"],
    "vasectomy": ["ANDROLOGY"],
    "male reproductive health": ["ANDROLOGY"],
    "testicular cancer": ["ANDROLOGY"],
    "andropause": ["ANDROLOGY"],

    "pediatrics": ["PEDIATRICS"],
    "children's health": ["PEDIATRICS"],
    "pediatrician": ["PEDIATRICS"],
    "child growth": ["PEDIATRICS"],
    "child development": ["PEDIATRICS"],
    "immunization": ["PEDIATRICS"],
    "vaccination": ["PEDIATRICS"],
    "newborn care": ["PEDIATRICS"],
    "baby doctor": ["PEDIATRICS"],
    "pediatric exam": ["PEDIATRICS"],
    "pediatric surgery": ["PEDIATRICS"],
    "adhd": ["PEDIATRICS"],
    "asthma": ["PEDIATRICS"],
    "childhood diseases": ["PEDIATRICS"],
    "autism": ["PEDIATRICS"],
    "growth hormone treatment": ["PEDIATRICS"],
    "pediatric cardiology": ["PEDIATRICS"],
    "pediatric orthopedics": ["PEDIATRICS"],
    "pediatric neurology": ["PEDIATRICS"],
    "pediatric endocrinology": ["PEDIATRICS"],
    "child obesity": ["PEDIATRICS"],
    "pediatric allergies": ["PEDIATRICS"],
    "neonatal care": ["PEDIATRICS"],
    "pediatric gastroenterology": ["PEDIATRICS"],

    "dermatology": ["DERMATOLOGY"],
    "skin care": ["DERMATOLOGY"],
    "acne treatment": ["DERMATOLOGY"],
    "eczema": ["DERMATOLOGY"],
    "psoriasis": ["DERMATOLOGY"],
    "rashes": ["DERMATOLOGY"],
    "skin cancer": ["DERMATOLOGY"],
    "dermatologist": ["DERMATOLOGY"],
    "skin rash": ["DERMATOLOGY"],
    "sunburn": ["DERMATOLOGY"],
    "moles": ["DERMATOLOGY"],
    "skin pigmentation": ["DERMATOLOGY"],
    "botox": ["DERMATOLOGY"],
    "laser hair removal": ["DERMATOLOGY"],
    "anti-aging treatments": ["DERMATOLOGY"],
    "wrinkles": ["DERMATOLOGY"],
    "stretch marks": ["DERMATOLOGY"],
    "hair loss treatment": ["DERMATOLOGY"],
    "rosacea": ["DERMATOLOGY"],
    "melasma": ["DERMATOLOGY"],
    "tattoo removal": ["DERMATOLOGY"],
    "skin infections": ["DERMATOLOGY"],
    "skin allergy": ["DERMATOLOGY"],
    "skin biopsy": ["DERMATOLOGY"],
    "nail fungus": ["DERMATOLOGY"],
    "laser treatment for scars": ["DERMATOLOGY"],

    "cardiology": ["CARDIOLOGY"],
    "heart disease": ["CARDIOLOGY"],
    "heart problems": ["CARDIOLOGY"],
    "hypertension": ["CARDIOLOGY"],
    "chest pain": ["CARDIOLOGY"],
    "ecg": ["CARDIOLOGY"],
    "arrhythmia": ["CARDIOLOGY"],
    "heart attack": ["CARDIOLOGY"],
    "heart failure": ["CARDIOLOGY"],
    "cardiologist": ["CARDIOLOGY"],
    "blood pressure": ["CARDIOLOGY","GENERAL MEDICINE"],
    "cholesterol": ["CARDIOLOGY","GENERAL MEDICINE"],
    "coronary artery disease": ["CARDIOLOGY"],
    "stroke prevention": ["CARDIOLOGY"],
    "pacemaker": ["CARDIOLOGY"],
    "cardiac surgery": ["CARDIOLOGY"],
    "valve problems": ["CARDIOLOGY"],
    "heart check-up": ["CARDIOLOGY"],
    "angina": ["CARDIOLOGY"],
    "heart murmur": ["CARDIOLOGY"],
    "cardiomyopathy": ["CARDIOLOGY"],
    "arrhythmic heart disease": ["CARDIOLOGY"],
    "peripheral artery disease": ["CARDIOLOGY"],
    "high triglycerides": ["CARDIOLOGY"],
    "cardiac rehabilitation": ["CARDIOLOGY"],
    "hypertrophic cardiomyopathy": ["CARDIOLOGY"],

    "neurology": ["NEUROLOGY"],
    "brain health": ["NEUROLOGY"],
    "headache": ["NEUROLOGY","GENERAL MEDICINE"],
    "migraine": ["NEUROLOGY"],
    "seizures": ["NEUROLOGY"],
    "neurologist": ["NEUROLOGY"],
    "stroke": ["NEUROLOGY"],
    "alzheimer's disease": ["NEUROLOGY"],
    "parkinson's disease": ["NEUROLOGY"],
    "memory problems": ["NEUROLOGY"],
    "numbness": ["NEUROLOGY"],
    "nervous system": ["NEUROLOGY"],
    "tremors": ["NEUROLOGY"],
    "dizziness": ["NEUROLOGY"],
    "spinal cord injury": ["NEUROLOGY"],
    "multiple sclerosis": ["NEUROLOGY"],
    "sleep disorders": ["NEUROLOGY"],
    "epilepsy": ["NEUROLOGY"],
    "neuropathy": ["NEUROLOGY"],
    "nerve pain": ["NEUROLOGY"],
    "dementia": ["NEUROLOGY"],
    "nervous system disorders": ["NEUROLOGY"],
    "neurodegenerative disease": ["NEUROLOGY"],
    "brain tumor": ["NEUROLOGY"],

    "hepatology": ["HEPATOLOGY"],
    "liver health": ["HEPATOLOGY"],
    "hepatitis": ["HEPATOLOGY"],
    "fatty liver": ["HEPATOLOGY"],
    "cirrhosis": ["HEPATOLOGY"],
    "liver transplant": ["HEPATOLOGY"],
    "liver disease": ["HEPATOLOGY"],
    "jaundice": ["HEPATOLOGY"],
    "liver enzymes": ["HEPATOLOGY"],
    "hepatitis b": ["HEPATOLOGY"],
    "hepatitis c": ["HEPATOLOGY"],
    "gallbladder problems": ["HEPATOLOGY"],
    "liver cancer": ["HEPATOLOGY"],
    "fatty liver treatment": ["HEPATOLOGY"],
    "liver function test": ["HEPATOLOGY"],
    "liver biopsy": ["HEPATOLOGY"],
    "hepatologist": ["HEPATOLOGY"],
    "liver cirrhosis": ["HEPATOLOGY"],
    "cholestasis": ["HEPATOLOGY"],
    "hepatitis d": ["HEPATOLOGY"],
    "hepatocellular carcinoma": ["HEPATOLOGY"],

    "oncology": ["ONCOLOGY"],
    "cancer": ["ONCOLOGY"],
    "tumor": ["ONCOLOGY"],
    "oncologist": ["ONCOLOGY"],
    "chemotherapy": ["ONCOLOGY"],
    "radiotherapy": ["ONCOLOGY"],
    "radiation therapy": ["ONCOLOGY"],
    "breast cancer": ["ONCOLOGY"],
    "lung cancer": ["ONCOLOGY"],
    "colon cancer": ["ONCOLOGY"],
    "leukemia": ["ONCOLOGY"],
    "lymphoma": ["ONCOLOGY"],
    "cancer treatment": ["ONCOLOGY"],
    "immunotherapy": ["ONCOLOGY"],
    "cancer screening": ["ONCOLOGY"],
    "cancer surgery": ["ONCOLOGY"],
    "metastasis": ["ONCOLOGY"],
    "tumor markers": ["ONCOLOGY"],
    "palliative care": ["ONCOLOGY"],
    "radiation oncology": ["ONCOLOGY"],
    "melanoma": ["ONCOLOGY"],
    "breast cancer treatment": ["ONCOLOGY"],
    "colorectal cancer": ["ONCOLOGY"],
    "cancer immunotherapy": ["ONCOLOGY"],

    "gynecology": ["GYNECOLOGY"],
    "women's health": ["GYNECOLOGY"],
    "ob": ["GYNECOLOGY"],
    "gyn": ["GYNECOLOGY"],
    "menstrual cycle": ["GYNECOLOGY"],
    "pregnancy": ["GYNECOLOGY"],
    "fertility": ["GYNECOLOGY"],
    "contraception": ["GYNECOLOGY"],
    "birth control": ["GYNECOLOGY"],
    "menopause": ["GYNECOLOGY"],
    "fibroids": ["GYNECOLOGY"],
    "polycystic ovary syndrome": ["GYNECOLOGY"],
    "pcos": ["GYNECOLOGY"],
    "vaginal infections": ["GYNECOLOGY"],
    "cervical screening": ["GYNECOLOGY"],
    "ovarian cancer": ["GYNECOLOGY"],
    "breast exam": ["GYNECOLOGY"],
    "pelvic pain": ["GYNECOLOGY"],
    "hysterectomy": ["GYNECOLOGY"],
    "pregnancy checkup": ["GYNECOLOGY"],
    "postpartum care": "GYNECOLOGY",
    "endometriosis": ["GYNECOLOGY"],
    "hpv vaccination": ["GYNECOLOGY"],
    "pregnancy complications": ["GYNECOLOGY"],
    "vaginal prolapse": ["GYNECOLOGY"],

    "ent": ["ENT"],
    "ear problems": ["ENT"],
    "nose problems": ["ENT"],
    "throat problems": ["ENT"],
    "hearing loss": ["ENT"],
    "sinusitis": ["ENT"],
    "allergy": ["ENT"],
    "tonsilitis": ["ENT"],
    "ear infection": ["ENT"],
    "sleep apnea": ["ENT"],
    "snoring": ["ENT"],
    "vertigo": ["ENT"],
    "sore throat": ["ENT"],
    "nasal congestion": ["ENT"],
    "deafness": ["ENT"],
    "sinus infection": ["ENT"],
    "ear wax removal": ["ENT"],
    "nasal surgery": ["ENT"],
    "throat cancer": ["ENT"],
    "voice disorder": ["ENT"],

    "psychology": ["PSYCHOLOGY"],
    "mental health": ["PSYCHOLOGY"],
    "therapy": ["PSYCHOLOGY"],
    "stress": ["PSYCHOLOGY"],
    "anxiety": ["PSYCHOLOGY"],
    "depression": ["PSYCHOLOGY"],
    "psychologist": ["PSYCHOLOGY"],
    "counseling": ["PSYCHOLOGY"],
    "family therapy": ["PSYCHOLOGY"],
    "addiction": ["PSYCHOLOGY"],
    "anger management": ["PSYCHOLOGY"],
    "cognitive therapy": ["PSYCHOLOGY"],
    "psychotherapy": ["PSYCHOLOGY"],
    "mental illness": ["PSYCHOLOGY"],
    "bipolar disorder": ["PSYCHOLOGY"],
    "ocd": ["PSYCHOLOGY"],
    "grief counseling": ["PSYCHOLOGY"],
    "relationship therapy": ["PSYCHOLOGY"],
    "ptsd": ["PSYCHOLOGY"],
    "child therapy": ["PSYCHOLOGY"],
    "couples therapy": ["PSYCHOLOGY"],
    "addiction therapy": ["PSYCHOLOGY"],

    "general medicine": ["GENERAL MEDICINE"],
    "primary care": ["GENERAL MEDICINE"],
    "general practitioner": ["GENERAL MEDICINE"],
    "check-up": ["GENERAL MEDICINE"],
    "health screening": ["GENERAL MEDICINE"],
    "fever": ["GENERAL MEDICINE"],
    "cold": ["GENERAL MEDICINE"],
    "stomach pain": ["GENERAL MEDICINE"],
    "fatigue": ["GENERAL MEDICINE"],
    "cough": ["GENERAL MEDICINE"],
    "diabetes": ["GENERAL MEDICINE"],
    "annual check-up": ["GENERAL MEDICINE"],
    "chronic illness": ["GENERAL MEDICINE"],
    "physical exam": ["GENERAL MEDICINE"],
    "preventative care": ["GENERAL MEDICINE"],
    "health consultation": ["GENERAL MEDICINE"],

    "ophthalmology": ["OPHTHALMOLOGY"],
    "eye problems": ["OPHTHALMOLOGY"],
    "vision": ["OPHTHALMOLOGY"],
    "glaucoma": ["OPHTHALMOLOGY"],
    "cataract": ["OPHTHALMOLOGY"],
    "eye exam": ["OPHTHALMOLOGY"],
    "lasik": ["OPHTHALMOLOGY"],
    "astigmatism": ["OPHTHALMOLOGY"],
    "macular degeneration": ["OPHTHALMOLOGY"],
    "dry eyes": ["OPHTHALMOLOGY"],
    "vision correction": ["OPHTHALMOLOGY"],
    "contact lenses": ["OPHTHALMOLOGY"],
    "retina": ["OPHTHALMOLOGY"],
    "eye surgery": ["OPHTHALMOLOGY"],
    "eye infection": ["OPHTHALMOLOGY"],
    "color blindness": ["OPHTHALMOLOGY"],
    "night blindness": ["OPHTHALMOLOGY"],
    "eye floaters": ["OPHTHALMOLOGY"],
    "diabetic retinopathy": ["OPHTHALMOLOGY"]
}

def get_doc_from_dep(specializations):
    result = []
    db_doc = db.collection('Department').stream()
    for specialization in specializations:
        for department in db_doc:
            if specialization in department.get("name"):
                docs = db.collection('Department').document(department.id).collection("Doctors").stream()
                for data in docs:
                    result.append(data.to_dict())
    return result


def get_specialization(disease):
    return disease_to_specialization.get(disease.lower())


def get_doctor(name):
    db_dep = db.collection('Department').stream()
    result = []
    for dep in db_dep:
        db_doc = db.collection('Department').document(dep.id).collection("Doctors").stream()
        for doctors in db_doc:
            doc = db.collection('Department').document(dep.id).collection("Doctors").document(doctors.id).get()
            doctor_data = doc.to_dict()
            if name.lower() in doctor_data.get("dname").lower():
                result.append(doctor_data)
    return result






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
@app.route('/popular_docs', methods=['POST'])
def getPopularDoctors():
    db_ref = db.collection('Department').document("0Z0REKdBoh26uztxls5O").collection("Doctors").stream()
    return jsonify(list(map(lambda doc: doc.to_dict(), db_ref)))


## route for getting department
@app.route('/Department', methods=['POST'])
def getDepartmentData():
    if request.method == 'POST':
        db_ref = db.collection('Department').stream()
        return jsonify(list(map(lambda doc: doc.to_dict(), db_ref)))
    else:
        return {"status":False}






##don't work with these user apis
@app.route('/createUser', methods=['POST'])
def createUser():
    if request.method == 'POST':
        uid = request.args.get('UID')
        isPhoneVerified = False
        isDetailsFilled = False
        print(uid)
        data = {"uid": uid, "isPhoneVerified": isPhoneVerified, "isDetailsFilled": isDetailsFilled}
        db.collection("Users").document(uid).set(data)
        return jsonify({"status":True}),200
    else:
        return jsonify({"status":False})


#for getting a user
@app.route('/getUser',methods=['POST'])
def getUser():
    if request.method == 'POST':
        uid = request.args.get('UID')
        user = db.collection("Users").document(uid).get()
        return jsonify(user.to_dict())
    else:
        return None



#for update a user
@app.route('/updateUser',methods=['POST'])
def updateUser():
    if request.method == "POST":
        uid = request.get_json().get('uid')
        uName = request.get_json().get('uName')
        uGender = request.get_json().get('uGender')
        DOB = request.get_json().get('DOB')
        uAddress = request.get_json().get('uAddress')
        uLat = request.get_json().get('uLat')
        uLong = request.get_json().get('uLong')
        uEmail = request.get_json().get('uEmail')
        uPhone = request.get_json().get('uPhone')
        uProfilePic = request.get_json().get('uProfilePic')
        isPhoneVerified = request.get_json().get('isPhoneVerified')
        isDetailsFilled = request.get_json().get('isDetailsFilled')

        user = db.collection("Users").document(uid)
        try:
            user.update({
                "uid":uid,
                "uName":uName,
                "uGender":uGender,
                "DOB":DOB,
                "uAddress":uAddress,
                "uLat":uLat,
                "uLong":uLong,
                "uEmail":uEmail,
                "uPhone":uPhone,
                "uProfilePic":uProfilePic,
                "isPhoneVerified":isPhoneVerified,
                "isDetailsFilled":isDetailsFilled,
            })
            return jsonify({"status":True})
        except Exception:
            return jsonify({"status":False})
    else:
        return None

#for getting banner
@app.route("/getBanners" , methods = ['POST'])
def getBanners():
    if request.method == 'POST':
        banners = []
        banner = db.collection("Advertisement").stream()
        for data in banner:
            banners.append(data.to_dict())

        return jsonify(banners)
    else:
        print("error")
        return None




# Route for retrieving favourite doctors for specific user
@app.route('/get_fav_doctors', methods=['POST'])
def getFavDoctors ():
    if request.method == 'POST':
        user_id = request.args.get('uid')
        try:
            user_doc = db.collection('Users').document(user_id).collection('Fav Doctors').stream()
            return jsonify(list(map(lambda doc: doc.to_dict(), user_doc)))

        except Exception:
            return jsonify({"status": False})
    else:
        return None


#to add a fav doctor
@app.route("/addFavDoctor", methods = ['POST'])
def addFavDoctor():
    if request.method == 'POST':
        user_id = request.args.get('uid')
        doc_id = request.args.get('did')
        dep_id = request.args.get('id')

        fav_doc_id = db.collection('Users').document(user_id).collection('Fav Doctors').document().id

        fav_doc_data = {"id": str(fav_doc_id), "uid": str(user_id), "did": str(doc_id), "dep_id": dep_id}
        db.collection('Users').document(user_id).collection('Fav Doctors').document(fav_doc_id).set(fav_doc_data)
        return jsonify({"status": True})
    else:
        return None







# Route for booking an Appointment
@app.route('/book_appointment', methods=['POST'])
def bookAppointment():
    if request.method == 'POST':
            data = request.get_json()   # Give input in JSON format in Postman

            required_fields = ['uid', 'did', 'appointment_slot', 'appointment_date', 'payment_mode','day','payment_status','payment_id','fee']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                missed = ", ".join(missing_fields)
                return jsonify({'error': f'Missing fields: {missed}'}), 400

            try:
                appointment_id = db.collection('Appointment').document().id
                appointment_data = {
                    'appointment_id': appointment_id,
                    'payment_id':data['payment_id'],
                    'user_id': data['uid'],
                    'doctor_id': data['did'],
                    'day':data['day'],
                    'appointment_slot': data['appointment_slot'],
                    'appointment_date': data['appointment_date'],  # Expected format: "YYYY-MM-DD"
                    'payment_mode': data['payment_mode'],
                    'payment_status': data['payment_status'],
                    'fee': int(data['fee'])
                }
                db.collection('Appointment').document(appointment_id).set(appointment_data)
                return jsonify({'message': 'Appointment Successfully Booked.'}), 200

            except Exception:
                return jsonify({"status": False})
    else:
        return None



# Route for retrieving all Appointment details booked by a specific user
@app.route('/get_user_appointments', methods=['POST'])
def getUserAppointments():
    if request.method == 'POST':
            user_id = request.args.get('uid')
            if not user_id:
                return jsonify({'error': 'Missing uid parameter'}), 400

            try:
                appointments_ref = db.collection('Appointment').where('user_id', '==', user_id).stream()
                return jsonify(list(map(lambda doc: doc.to_dict(), appointments_ref))), 200

            except Exception:
                return jsonify({"status": False})
    else:
        return None




# Route for retrieving the list of all Doctors from a specific Department
@app.route('/get_department_doctors', methods=['POST'])
def getDepartmentDoctors():
    if request.method == 'POST':
          dept_id = request.args.get('id')
          if not dept_id:
                return jsonify({'error': 'Please enter the department id.'}), 400

          try:
                dept_ref = db.collection('Department').document(dept_id)
                doc_list = dept_ref.collection('Doctors').stream()
                return jsonify(list(map(lambda doc: doc.to_dict(), doc_list))), 200
          except Exception:
              return jsonify({"status": False})
    else:
          return None



# Route for searching feature in app
@app.route('/search',methods = ['POST'])
def getSearchResult():
    if request.method == 'POST':
        keyword = request.args.get('keyword')
        result = get_specialization(keyword)

        if result is None:
            result = get_doctor(keyword)
        else:
            result = get_doc_from_dep(result)

        return jsonify(result)
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