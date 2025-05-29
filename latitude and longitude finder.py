import requests
import firebase_admin
from firebase_admin import firestore, credentials


def findLatLong(address):
    url = f"https://us1.locationiq.com/v1/search?key={api_key}&q={address}&format=json"
    response = requests.get(url)
    data = response.json()
    if not data or not isinstance(data, list):

        return 0, 0

    return str(data[0]['lat']), str(data[0]['lon'])

api_key = "pk.2da019e7f8aa37bcc665172e2c375f90"

cred = credentials.Certificate('admin.json') ## admin.json is out credential file for firebase account
firebase_admin.initialize_app(cred)
db = firestore.client()

db_dep = db.collection('Department').stream()

for dep in db_dep:
    db_doc = db.collection('Department').document(dep.id).collection("Doctors").stream()
    for doctors in db_doc:
        doc = db.collection('Department').document(dep.id).collection("Doctors").document(doctors.id).get()
        doctor = doc.to_dict()
        if doctor.get("clatitude") == 0 and doctor.get("clongitude") == 0:
            lat,long = findLatLong(doctor.get("caddress"))
            print(f"{lat} , {long}")
            db.collection('Department').document(dep.id).collection("Doctors").document(doctors.id).update({"clatitude": float(lat),"clongitude": float(long)})