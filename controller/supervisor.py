from firebase_admin import firestore

def get_supervisors():
    db = firestore.client()
    docs = db.collection('supervisors').get()
    result=[]
    for doc in docs:
        result.append(doc.to_dict())
    return result