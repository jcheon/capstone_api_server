# Capstone API server
REST API server that serves capstone. 

## Docs
[Firestore SDK](https://firebase.google.com/docs/firestore/quickstart)<br/>
[Uvicorn](https://www.uvicorn.org/)<br/>
[FastAPI](https://fastapi.tiangolo.com/features/)<br/>

## Getting started

### Requirements
- Python version ``` >= 3.6 ```
- pip version ```>= 9.0 ``` 
- uvicorn ``` pip install uvicorn ```
- fastapi ``` pip install fastapi ```


### Run the server
Run the server ```uvicorn main:app --reload```

Run server on specific port 

``` uvicorn main:app --reload --port <port number>```

### Access the API UI
On your browser, go to 

```http://127.0.0.1:8000/docs```

## Covered types of places
[Place Types docs](https://developers.google.com/places/web-service/supported_types)<br/>
gas_station<br/>
restaurant<br/>
supermarket<br/><br/>
the rest of the places will be covered by the 'else' attributes in the Firebase 'cards' collection. 

## REST endpoints 
/latlong/user_id <br/>
Returns stores within 500m in radius with best card recommendation for that user. <br/>
```
{
        "store_name": str,
        "card_bank": str,
        "card_name": str,
        "cashback_amount": int,
        "distance": double,
        "img" str, 
},
.
.
.
```

