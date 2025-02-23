from llmdeploy.server import start_server
import subprocess
import json
import os
import multiprocessing

DEPLOYMENT_FILE = "deployed_models.json"

def load_models():
    """Load deployed models from a file."""
    try:
        with open(DEPLOYMENT_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_models(models):
    """Save deployed models to a file."""
    with open(DEPLOYMENT_FILE, "w") as f:
        json.dump(models, f, indent=4)

def detect_model_type(source, model):
    """Detect if the model is chat-based or text-based."""
    if source == "ollama":
        chat_models = ["llama3", "mistral", "gemma"]
        return "chat" if model in chat_models else "completion"

    elif source == "hf":
        return "chat" if "chat" in model.lower() else "completion"

def deploy_model(source, model, port):
    """Deploy a model from Ollama or Hugging Face."""
    models = load_models()
    model_key = f"{source}/{model}"

    if model_key in models:
        return f"⚠️ Model '{model}' from '{source}' is already running at http://localhost:{models[model_key][0]}/{model_key}/{models[model_key][1]}"

    model_type = detect_model_type(source, model)

    if source == "ollama":
        print(f"🚀 Pulling Ollama model '{model}'...")
        subprocess.run(["ollama", "pull", model], check=True)

    elif source == "hf":
        print(f"🚀 Downloading Hugging Face model '{model}'...")
        from transformers import AutoModelForCausalLM, AutoTokenizer
        AutoModelForCausalLM.from_pretrained(model).save_pretrained(f"hf_models/{model}")
        AutoTokenizer.from_pretrained(model).save_pretrained(f"hf_models/{model}")

    # Start API server in a new process
    process = multiprocessing.Process(target=start_server, args=(port,))
    process.start()

    models[model_key] = (port, model_type)
    save_models(models)

    return f"✅ Model '{model}' ({model_type}) from '{source}' deployed at http://localhost:{port}/{model_key}/{model_type}"

def list_models():
    """List deployed models."""
    models = load_models()
    return "\n".join([
        f"{m} ({t}) -> http://localhost:{p}/{m}/{t}" for m, (p, t) in models.items()
    ]) if models else "No models deployed."

def remove_model(source, model):
    """Remove a deployed model."""
    models = load_models()
    model_key = f"{source}/{model}"
    if model_key not in models:
        return f"❌ Error: Model '{model}' from '{source}' not found."

    del models[model_key]
    save_models(models)
    return f"✅ Model '{model}' from '{source}' removed successfully."
