from dotenv import load_dotenv
import os

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import uuid

from agent import root_agent


APP_NAME = "feynman_tamagotchi_app"
USER_ID = "student_1"
SESSION_ID = str(uuid.uuid4())


session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentInput(BaseModel):
    message: str

@app.get("/")
async def home():
    return {"status": "Feynman Tamagotchi API is running"}



@app.on_event("startup")
async def startup_event():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )


@app.post("/chat")
async def chat(data: StudentInput):
    user_message = Content(
        role="user",
        parts=[Part(text=data.message)]
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    mood = "hungry"

    if "TAMAGOTCHI_MOOD: happy" in final_response:
        mood = "happy"
    elif "TAMAGOTCHI_MOOD: confused" in final_response:
        mood = "confused"
    elif "TAMAGOTCHI_MOOD: excited" in final_response:
        mood = "excited"
    elif "TAMAGOTCHI_MOOD: sick" in final_response:
        mood = "sick"

    return {
        "mood": mood,
        "feedback": final_response
    }
