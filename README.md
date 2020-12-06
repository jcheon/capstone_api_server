# Capstone API server
REST API server that serves capstone. 

### Getting started

## Requirements
- Python version ``` >= 3.6 ```
- pip version ```>= 9.0 ``` 
- uvicorn ``` pip install uvicorn ```
- fastapi ``` pip install fastapi ```


## Run the server
Run the server 

```uvicorn main:app --reload```

Run server on specific port 

``` uvicorn main:app --reload --port <port number>```

## Access the API UI
On your browser, go to 

```http://127.0.0.1:8000/docs```

## REST endpoints 
/test

```{"Hello" : "World"}```

## PS: dont steal my api keys please.. just temporary for now

