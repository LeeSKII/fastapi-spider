from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get('/spider')
async def spider():
  return {"message": "This is a spider"}