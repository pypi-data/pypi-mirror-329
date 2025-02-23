import os
import json
import subprocess
import sys

# File to store deployed models
DEPLOYED_MODELS_FILE = "deployed_models.json"

def load_deployed_models():
    """Load deployed models from a JSON file."""
    try:
        with open(DEPLOYED_MODELS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_deployed_models(models):
    """Save deployed models to a JSON file."""
    with open(DEPLOYED_MODELS_FILE, "w") as file:
        json.dump(models, file, indent=4)


def deploy_model(real_model_name):
    """Deploy an Ollama model by pulling it via subprocess."""
    print(f"🚀 Deploying model '{real_model_name}'...\n")
    subprocess.run(["ollama", "pull", real_model_name], check=True)
    
    deployed_models = load_deployed_models()
    deployed_models[real_model_name] = real_model_name  # Store real model name
    save_deployed_models(deployed_models)
    
    print(f"\n✅ Model '{real_model_name}' deployed successfully!")


def list_models():
    """List all locally available Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True
        )

        if result.returncode != 0:
            return f"❌ Error fetching models: {result.stderr}"

        return result.stdout.strip() or "📌 No models found."
    except Exception as e:
        return f"❌ Error fetching models: {e}"

def list_deployed_models():
    """List models that were deployed using the CLI tool."""
    deployed_models = load_deployed_models()
    if not deployed_models:
        return "📌 No deployed models found."
    return "\n".join(f"{real} -> {installed}" for real, installed in deployed_models.items())

def remove_model(real_model_name):
    """Remove a deployed Ollama model from both the machine and tracking list."""
    try:
        deployed_models = load_deployed_models()

        if real_model_name not in deployed_models:
            return f"⚠️ Model '{real_model_name}' not found in tracking file."

        installed_model_name = deployed_models[real_model_name]

        # Remove the model using subprocess
        process = subprocess.Popen(
            ["ollama", "rm", installed_model_name], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)
            sys.stdout.flush()

        process.wait()

        if process.returncode != 0:
            return f"❌ Error removing model: {process.stderr.read().strip()}"

        # Remove from tracking list
        del deployed_models[real_model_name]
        save_deployed_models(deployed_models)

        return f"\n✅ Model '{real_model_name}' (stored as '{installed_model_name}') completely removed!"
    except Exception as e:
        return f"❌ Error removing model: {e}"

def run_inference(model, prompt):
    """Run inference on a deployed Ollama model."""
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            return f"❌ Error running inference: {result.stderr}"

        return result.stdout.strip()
    except Exception as e:
        return f"❌ Error running inference: {e}"
