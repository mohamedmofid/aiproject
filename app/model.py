import joblib
import numpy as np

MODEL_PATH = "models/mushroom_model.joblib"
ENCODER_PATH = "models/label_encoders.joblib"

def load_model():
    """Load the trained model and encoders."""
    model = joblib.load(MODEL_PATH)
    label_encoders = joblib.load(ENCODER_PATH)
    return model, label_encoders

def encode_inputs(inputs, label_encoders):
    """Encode categorical inputs using saved label encoders."""
    encoded_inputs = {}
    for feature, value in inputs.items():
        if feature in label_encoders:
            encoded_inputs[feature] = label_encoders[feature].transform([value])[0]
        else:
            raise ValueError(f"Unexpected feature: {feature}")
    return encoded_inputs

def predict(model, encoders, inputs):
    """Encode inputs, make a prediction, and calculate confidence."""
    encoded_inputs = encode_inputs(inputs, encoders)
    input_values = np.array(list(encoded_inputs.values())).reshape(1, -1)
    prediction = model.predict(input_values)[0]
    # probabilities = model.predict_proba(input_values)[0]
    # confidence = max(probabilities)
    # round(confidence, 2)
    
    return prediction, 0
