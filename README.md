# Capstone API server
REST API server that serves capstone. 

## Docs
[Firestore SDK](https://firebase.google.com/docs/firestore/quickstart)

[Uvicorn](https://www.uvicorn.org/)

[FastAPI](https://fastapi.tiangolo.com/features/)

## Getting started

### Requirements
- Python version ``` >= 3.6 ```
- pip version ```>= 9.0 ``` 
- uvicorn ``` pip install uvicorn ```
- fastapi ``` pip install fastapi ```


### Run the server
Run the server 

```uvicorn main:app --reload```

Run server on specific port 

``` uvicorn main:app --reload --port <port number>```

### Access the API UI
On your browser, go to 

```http://127.0.0.1:8000/docs```

### Covered types of places
[Place Types docs](https://developers.google.com/places/web-service/supported_types)
\ngas_station
\nrestaurant
\nsupermarket
\n\nthe rest of the places will be covered by the 'else' attributes in the Firebase 'cards' collection. 

### REST endpoints 
/test

```{"Hello" : "World"}```

