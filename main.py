from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def hello_world():
    return {"Hello": "World"}



#TODO: MAKE GET REQUEST TO FIRESTORE
#    - https://firebase.google.com/docs/firestore/use-rest-api
#        - using the rest api. 
#    - https://firebase.google.com/docs/admin/setup?authuser=1#python_4 
#        Add firebase admin sdk to your server? this might work. 
