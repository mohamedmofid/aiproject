from fastapi import FastAPI
from pydantic import BaseModel
from app.model import load_model, predict
from app.questions import get_next_question
from app.utils import fill_missing_attributes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI app
app = FastAPI(title="Mushroom Edibility Predictor", version="1.2")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = [
    "http://localhost:3000",  # Or replace with the domain where your frontend is running
    "http://127.0.0.1:51754"  # Example of the frontend port
]

# Add CORSMiddleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the frontend to access the backend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load the model and encoders
model, label_encoders = load_model()

# Default values for missing inputs
DEFAULT_VALUES = {
    "gill_color": "white",
    "spore_print_color": "brown",
    "mushroom_population": "several",
    "gill_size": "narrow",
    "mushroom_odor": "none",
    "mushroom_habitat": "woods",
    "bruising_present": "no",
}

# Data model for user inputs
class MushroomFeatures(BaseModel):
    gill_color: str = None
    spore_print_color: str = None
    mushroom_population: str = None
    gill_size: str = None
    mushroom_odor: str = None
    mushroom_habitat: str = None
    bruising_present: str = None

@app.post("/predict")
def predict_edibility(features: MushroomFeatures):
    user_inputs = features.dict()
    filled_inputs = fill_missing_attributes(user_inputs, DEFAULT_VALUES)

    try:
        prediction, confidence = predict(model, label_encoders, filled_inputs)
        
        return {
            "prediction": "Edible" if prediction == 0 else "Poisonous",
            "confidence": confidence,
        }
    except ValueError as e:
        return {"error": str(e)}

# GET endpoint to ask the next question
@app.get("/ask")
def ask_question(provided_data: dict = {}):
    next_question = get_next_question(provided_data)
    if next_question:
        return {"next_question": next_question}
    return {"message": "All required attributes are provided."}
