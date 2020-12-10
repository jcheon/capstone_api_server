
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from fastapi import FastAPI
import json
import requests

# test data: 
#   userid = 2nnKFsmSWQSrqP2w6eFYzXhb8Cr1
#   location = 39.7260327,-121.804

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

# looks for document with uid. 
# Returns dict of cards that user has
@app.get("/read_user_card_info")
def read_user_card_info(uid):

    user_ref = db.collection(u'user_info').document(u'{uid}'.format(uid=uid))
    docs = user_ref.get()

    if docs.exists: 
        print(f'exists')
    else: 
        print(u'No document')

    return docs.to_dict()

@app.get("/read_cc")
def read_cc():

    cc_ref = db.collection(u'credit_cards')
    credit_cards = cc_ref.stream()

    cc_json = {}

    for c in credit_cards: 
        #print(f'{c.id} = > {c.to_dict()}')
        cc_instance = {}
        cc_instance[f'{c.id}'] = c.to_dict()
        cc_json.update(cc_instance)
    return cc_json

@app.get("/best_else")
def best_else_card(uid): 
    user_cards = read_user_card_info(uid)
    cc_db = read_cc()

    best_cashback = -1
    best_cashback_card = ''
    for c in user_cards['cards']:
        if best_cashback < cc_db[c]['category']['else']: 
            best_cashback = cc_db[c]['category']['else']
            best_cashback_card = c


    return {'card': best_cashback_card, 'cash_back': best_cashback}
    

@app.get("/latlong/userid")
def main_query(latlong, userid):
    # Get all of card data from firestore
    cards_db = read_cc()

    # {'cards': ['amex_gold', ' amex_blue_preferred']}
    user_card_info = read_user_card_info(userid)

    best_else = best_else_card(userid)

    # #location = "39.7260327,-121.804"
    radius = 2000
    location = latlong
    req = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&key={key}".format(location=location, radius=radius, key=key))
    req_json = req.json()
    len_result = len(req_json['results'])

    final_json = {}
    final_list = []

    for i in range(len_result):
        curr_json = {}
        curr_json['place'] = req_json['results'][i]['name']

        for t in req_json['results'][i]['types']:
            if(t == 'restaurant'):
                max_cashback = -1
                max_cashback_card = ''
                max_cashback_bank = ''
                max_cashback_img = ''

                for c in user_card_info['cards']:
                    try: 
                        if max_cashback < cards_db[c]['category']['restaurant']: 
                            max_cashback = cards_db[c]['category']['restaurant']
                            max_cashback_card = c
                            max_cashback_bank = cards_db[c]['bank']
                            max_cashback_img = cards_db[c]['img']
                    except: 
                        print('no restaurant: ' + c)
                
                curr_json['cash_back'] = max_cashback
                curr_json['card'] = max_cashback_card
                curr_json['card_bank'] = max_cashback_bank
                curr_json['img'] = max_cashback_img
            
            elif(t == 'gas_station'):
                max_cashback = -1
                max_cashback_card = ''
                max_cashback_bank = ''
                max_cashback_img = ''
                for x in user_card_info['cards']: 
                    try: 
                        if max_cashback < cards_db[c]['category']['restaurant']:
                            max_cashback = cards_db[c]['category']['restaurant']
                            max_cashback_card = c
                            max_cashback_bank = cards_db[c]['bank']
                            max_cashback_img = cards_db[c]['img']
                    except: 
                        print('no gas station: ' + c)
                curr_json['cash_back'] = max_cashback
                curr_json['card'] = max_cashback_card
                curr_json['card_bank'] = max_cashback_bank
                curr_json['img'] = max_cashback_img

            elif(t == 'supermarket'):
                max_cashback = -1
                max_cashback_card = ''
                max_cashback_bank = ''
                max_cashback_img = ''
                for x in user_card_info['cards']: 
                    try: 
                        if max_cashback < cards_db[c]['category']['grocery']:
                            max_cashback = cards_db[c]['category']['grocery']
                            max_cashback_card = c
                            max_cashback_bank = cards_db[c]['bank']
                            max_cashback_img = cards_db[c]['img']
                    except: 
                        print('no market: ' + c)
                curr_json['cash_back'] = max_cashback
                curr_json['card'] = max_cashback_card
                curr_json['card_bank'] = max_cashback_bank
                curr_json['img'] = max_cashback_img

        if 'cash_back' in curr_json: 
            pass
        else: 
            curr_json['cash_back'] = best_else['cash_back']
            curr_json['card'] = best_else['card']

        final_list.append(curr_json)

 
    for d in range(len(final_list)): 
        final_json[d] = final_list[d]


    # print(final_json)
    return final_json