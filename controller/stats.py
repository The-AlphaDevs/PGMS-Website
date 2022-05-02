from firebase_admin import firestore

def get_complaints():
    db = firestore.client()
    docs = db.collection('complaints').get()
    result=[]
    for doc in docs:
        complaintDict = doc.to_dict()
        complaintDict.pop("supervisorDocRef", None)
        if complaintDict["overdue"]:
            complaintDict["overdue"] = "true"
        else:
            complaintDict["overdue"] = "false"
        result.append(complaintDict)
    db.close()
    
    return result