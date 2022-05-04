from firebase_admin import firestore
from sqlalchemy import true

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

def valid_invalid(value, cid, supemail):
    db = firestore.client()
    doc = db.collection('complaints').document(cid).get()
    if value=='valid':
        if doc.to_dict()['overdue'] == true:
            supdoc = db.collection('supervisors').document(supemail).get()
            score = supdoc.to_dict()['score']
            db.collection('supervisors').document(supemail).update({'score': score-15})
        else:
            supdoc = db.collection('supervisors').document(supemail).get()
            score = supdoc.to_dict()['score']
            db.collection('supervisors').document(supemail).update({'score': score-10})
    else:
        if doc.to_dict()['overdue'] == true:
            supdoc = db.collection('supervisors').document(supemail).get()
            score = supdoc.to_dict()['score']
            db.collection('supervisors').document(supemail).update({'score': score+5})
        else:
            supdoc = db.collection('supervisors').document(supemail).get()
            score = supdoc.to_dict()['score']
            db.collection('supervisors').document(supemail).update({'score': score+10})