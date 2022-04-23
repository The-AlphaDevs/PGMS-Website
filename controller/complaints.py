from firebase_admin import firestore

def fetch_complaints(complaintType):
    db = firestore.client()
    docs = db.collection('complaints').get()
    result=[]
    for doc in docs:
        res = doc.to_dict()
        if(res['status']==complaintType):
            result.append(res)
    db.close()
    print("result")
    print(result)
    return result