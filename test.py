import firebase_admin
from firebase_admin import firestore, credentials


cred = credentials.Certificate('admin.json') ## admin.json is out credential file for firebase account
firebase_admin.initialize_app(cred)
db = firestore.client()


def update_doctors_in_department(dep_id_value):
    # Reference to the Doctors subcollection under the specified department
    doctors_ref = db.collection("Department").document(dep_id_value).collection("Doctors")
    doctors = doctors_ref.stream()

    for doctor in doctors:
        doctor.reference.update({"dep_id": dep_id_value})
        print(f"✅ Updated Doctor {doctor.id} with dep_id = {dep_id_value}")



update_doctors_in_department("0Z0REKdBoh26uztxls5O")