from fastapi import FastAPI
from dotenv import load_dotenv
from agents import Runner
from healthcare_agent.booking_agent import booking_agent
load_dotenv()
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}   


chat_history = []
@app.post("/appointment")
async def book_appointment(chat:str):
   chat_history.append({"role":"user","content":chat})
   response = await Runner.run(booking_agent,chat_history)
   chat_history.append({"role":"assistant","content":response.final_output})
   return {"message": response.final_output}