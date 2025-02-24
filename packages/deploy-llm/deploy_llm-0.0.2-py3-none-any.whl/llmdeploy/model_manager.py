import json
import os
from llmdeploy.ollama_manager import deploy_ollama_model, remove_ollama_model, infer_ollama

MODELS_FILE = "models.json"

def load_models():
    """Load models from JSON storage."""
    if os.path.exists(MODELS_FILE):
        with open(MODELS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_models(models):
    """Save models to JSON storage."""
    with open(MODELS_FILE, "w") as f:
        json.dump(models, f, indent=4)

def deploy_model(model_name, model_type):
    """Deploy a model using Ollama."""
    models = load_models()

    if model_name in models:
        return f"⚠️ Model '{model_name}' is already deployed."

    model_info = {
        "name": model_name,
        "source": "ollama",
        "type": model_type
    }

    deploy_status = deploy_ollama_model(model_name)
    if "❌" in deploy_status:
        return deploy_status  # Return error message if deployment fails

    models[model_name] = model_info
    save_models(models)
    
    return f"✅ Model '{model_name}' deployed successfully."

def list_models():
    """List all deployed models."""
    models = load_models()
    return json.dumps(models, indent=4) if models else "📜 No models deployed."

def remove_model(model_name):
    """Remove a deployed model."""
    models = load_models()
    if model_name not in models:
        return f"❌ Model '{model_name}' not found."

    remove_status = remove_ollama_model(model_name)
    if "❌" in remove_status:
        return remove_status  # Return error message if removal fails

    del models[model_name]
    save_models(models)
    
    return f"✅ Model '{model_name}' removed."

def run_inference(model_name, input_text=None, image_path=None):
    """Run inference on a model."""
    models = load_models()
    if model_name not in models:
        return f"❌ Model '{model_name}' not found."

    model_type = models[model_name]["type"]
    return infer_ollama(model_name, model_type, input_text, image_path)
