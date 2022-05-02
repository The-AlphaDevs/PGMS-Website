from firebase_admin import firestore

def fetch_complaints(complaintType):
    db = firestore.client()
    docs = db.collection('complaints').get()
    result=[]
    for doc in docs:
        res = doc.to_dict()
        if(complaintType=='All Complaints'):
            result.append(res)
        if(res['status']==complaintType):
            result.append(res)
    db.close()
    return result

def fetch_single_complaint(complaintID):
    db = firestore.client()
    docs = db.collection('complaints').get()
    result=[]
    for doc in docs:
        res = doc.to_dict()
        if(res['id']==complaintID):
            result.append(res)
            break
    db.close()
    return result

def closeComplaint(complaintID):
    db = firestore.client()
    db.collection('complaints').document(complaintID).update({'status': 'Closed'})