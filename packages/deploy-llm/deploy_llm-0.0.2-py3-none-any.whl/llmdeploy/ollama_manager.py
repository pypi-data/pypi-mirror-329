import subprocess

def deploy_ollama_model(model_name):
    """Deploy an Ollama model."""
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        return f"✅ Model '{model_name}' pulled successfully."
    except subprocess.CalledProcessError as e:
        return f"❌ Error deploying Ollama model: {e}"

def remove_ollama_model(model_name):
    """Remove an Ollama model."""
    try:
        subprocess.run(["ollama", "rm", model_name], check=True)
        return f"✅ Model '{model_name}' removed successfully."
    except subprocess.CalledProcessError as e:
        return f"❌ Error removing Ollama model: {e}"

def infer_ollama(model_name, model_type, input_text=None, image_path=None):
    """Run inference using Ollama (text or multimodal)."""
    try:
        command = ["ollama", "run", model_name]
        
        if model_type == "text" and input_text:
            command.append(input_text)
        elif model_type == "multimodal" and image_path:
            command.extend(["--image", image_path])

        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip() if result.stdout else "❌ No output received."
    
    except subprocess.CalledProcessError as e:
        return f"❌ Inference error: {e}"
