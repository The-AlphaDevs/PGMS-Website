from firebase_admin import firestore, storage
import uuid
from datetime import datetime


def get_supervisors():
    db = firestore.client()
    docs = db.collection('supervisors').get()
    result=[]
    for doc in docs:
        result.append(doc.to_dict())
    db.close()
    return result

def upload_image_and_data(file, name, email, ward, phoneno, dob):
    bucket = storage.bucket()
    uid = str(uuid.uuid4())
    blob = bucket.blob(uid + '/' + file.filename)
    ext = file.filename.split('.')[-1]
    ct = 'image/'+ext
    blob.upload_from_file(file, content_type=ct)
    blob.make_public()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data = {
        'name': name,
        'email': email,
        'ward': ward,
        'phoneno': str(phoneno),
        'dateOfBirth': dob,
        'imageUrl': blob.public_url,
        'score': 0,
        'joiningDate': str(dt_string),
        'id': uid,
        'complaintsAssigned': 0,
        'complaintsOverdue': 0,
        'complaintsResolved': 0,
        'complaintsCompleted': 0,
    }
    db = firestore.client()
    db.collection('supervisors').document(email).set(data)
    print('Hurrayyyyyyy')
    db.close()


# if profile not uploaded case and all other cases which requires validation

