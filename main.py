
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from fastapi import FastAPI
import json
import requests


#TODO: MAKE GET REQUEST TO FIRESTORE
#    - https://firebase.google.com/docs/firestore/use-rest-api
#        - using the rest api. 
#    - https://firebase.google.com/docs/admin/setup?authuser=1#python_4 
#        Add firebase admin sdk to your server? this might work. 

# connect to firebase firestore 
cred = credentials.Certificate("cc-app-29660-firebase-adminsdk-ssi40-030cc8e94c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# setup key for google places API call
open_key_file = open("keys.json")
keys_json = json.load(open_key_file);
key = keys_json["google_places"]

#start fastapi
app = FastAPI()

@app.get("/helloworld")
def hello_world():
    return {"Hello": "World"}


@app.post("/write")
def write(): 
# in mango collection, make document if not already there, then set the data as such
    doc_ref = db.collection(u'mango').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
        })
    return {"status_code": 200}

   
@app.get("/read")
def read_user_info():

    user_ref = db.collection(u'user_info')
    docs = user_ref.stream()
    for doc in docs: 
        print(f'{doc.id} => {doc.to_dict()}')

    return docs

@app.get("/read_cc")
def read_cc():
    
    cc_ref = db.collection(u'credit_cards')
    credit_cards = cc_ref.stream()

    print(f'credit cards')
    for c in credit_cards: 
        print(f'{c.id} = > {c.to_dict()}')

    return credit_cards


@app.get("/latlong/userid")
def main_query(latlong, userid):

    #location = "39.7260327,-121.804"
    radius = 2000
    location = latlong

    req = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&key={key}".format(location=location, radius=radius, key=key))

    req_json = req.json()

    len_result = len(req_json['results'])

    for i in range(len_result):
        for t in req_json['results'][i]['types']:
            if(t == 'restaurant'):
                print(req_json['results'][i]['name'] + ' is a restaurant')
            if(t == 'gas_station'):
                print(req_json['results'][i]['name'] + ' is a gas station')
            if(t == 'supermarket'):
                print(req_json['results'][i]['name'] + ' is a supermarket')
            else: 
                # recommend else category
                print("else")

    return {"status_code": 200}
