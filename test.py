import requests
import firebase_admin
from firebase_admin import firestore, credentials


doc_list = []
cred = credentials.Certificate('admin.json')  ## admin.json is out credential file for firebase account
firebase_admin.initialize_app(cred)
db = firestore.client()

disease_to_specialization = {
    "nephrologist":"NEPHROLOGIST",
    "kidney problem":"NEPHROLOGIST",
    "kidney failure":"NEPHROLOGIST",
    "chronic kidney disease":"NEPHROLOGIST",
    "acute kidney injury":"NEPHROLOGIST",
    "kidney stones":"NEPHROLOGIST",
    "nephrotic syndrome":"NEPHROLOGIST",
    "polycystic kidney disease":"NEPHROLOGIST",
    "glomerulonephritis":"NEPHROLOGIST",
    "urinary tract infection":"NEPHROLOGIST",
    "UTI":"NEPHROLOGIST",
    "lower back pain":"NEPHROLOGIST",
    "blood in urine":"NEPHROLOGIST",
    "frequent urination":"NEPHROLOGIST",
    "painful urination":"NEPHROLOGIST",
    "swelling in legs or feet":"NEPHROLOGIST",
    "foamy urine":"NEPHROLOGIST",
    "high creatinine":"NEPHROLOGIST",
    "renal failure":"NEPHROLOGIST",
    "renal disease":"NEPHROLOGIST",
    "nephrology":"NEPHROLOGIST",
    "dialysis":"NEPHROLOGIST",
    "kidney pain":"NEPHROLOGIST",
    "kidney transplant":"NEPHROLOGIST",
    "kidney":"NEPHROLOGIST"
}

def get_doc_from_dep(specialization):
    db_doc = db.collection('Department').stream()
    for department in db_doc:
        if specialization.lower() in department.get("name").lower():
            docs = db.collection('Department').document(department.id).collection("Doctors").stream()
            for data in docs:
                doc_list.append(data.to_dict())
    return doc_list

def get_specialization(disease):
    return disease_to_specialization.get(disease.lower())


def get_doctor(name):
    db_dep = db.collection('Department').stream()

    for dep in db_dep:
        db_doc = db.collection('Department').document(dep.id).collection("Doctors").stream()
        for doctors in db_doc:
            doc = db.collection('Department').document(dep.id).collection("Doctors").document(doctors.id).get()
            doctor = doc.to_dict()
            if name.lower() in doctor.get("dname").lower():
                doc_list.append(doctor)
    return doc_list


userInput = "kidney"
result = get_specialization(userInput)
if result is None:
    doctors = get_doctor(userInput)
    for doctor in doctors:
        print(doctor)
else:
    doctors = get_doc_from_dep(result)
    for doctor in doctors:
        print(doctor)