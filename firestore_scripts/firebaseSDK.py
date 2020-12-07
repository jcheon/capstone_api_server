import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("cc-app-29660-firebase-adminsdk-ssi40-030cc8e94c.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# in mango collection, make document if not already there, then set the data as such
doc_ref = db.collection(u'mango').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
    })

# READ DATA
user_ref = db.collection(u'user_info')
docs = user_ref.stream()

for doc in docs: 
    print(f'{doc.id} => {doc.to_dict()}')
    

cc_ref = db.collection(u'credit_cards')
credit_cards = cc_ref.stream()

print(f'credit cards')
for c in credit_cards: 
    print(f'{c.id} = > {c.to_dict()}')
