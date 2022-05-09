from firebase_admin import firestore, storage

def get_wards():
    db = firestore.client()
    docs = db.collection('wards').get()
    result=[]
    for doc in docs:
        result.append(doc.to_dict())
    db.close()
    return result