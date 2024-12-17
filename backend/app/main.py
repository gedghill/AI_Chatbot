import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from chatbot import predict_class, get_response
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="COM727 Chatbot API", description="An API for chatbot interaction", version="1.0")

# Add this after initializing the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configure logging
logging.basicConfig(
    filename="chat.log",  # Log file name
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
)

# Define request model
class ChatRequest(BaseModel):
    message: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log incoming requests."""
    logging.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

@app.post("/api/chatbot", summary="Chat with the chatbot", tags=["Chatbot"])
def chatbot_response(chat_request: ChatRequest):
    user_message = chat_request.message
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Log the user message
    logging.info(f"User message: {user_message}")

    # Predict the intent and generate response
    intents_list = predict_class(user_message)
    if not intents_list:
        bot_response = "I didn't understand that. Can you clarify?"
    else:
        bot_response = get_response(intents_list)

    # Log the bot response
    logging.info(f"Bot response: {bot_response}")

    return {"response": bot_response}


@app.get("/api/hello", summary="Chat with the chatbot", tags=["Chatbot"])
def hello():
    return {
        "response": "hello backend is running fine."
    }