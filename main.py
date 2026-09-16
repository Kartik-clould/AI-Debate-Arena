from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import DebateRequest
from agents import ask_ai, run_debate

app = FastAPI()

#The following code is used for connecting the front end with the Fast API because without it we are facing CORS error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "AI Debate Arena is running!"}


@app.post("/debate")
def start_debate(request: DebateRequest):
    result = run_debate(request.topic)

    return result


@app.get("/test-ai")
def test_ai():
    answer = ask_ai("Say hello to the AI Debate Arena in one sentence.")

    return {
        "answer": answer
    }