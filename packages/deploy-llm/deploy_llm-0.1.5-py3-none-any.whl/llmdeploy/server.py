import uvicorn
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()
DEPLOYED_MODELS = {}  # Stores deployed models { "source/model": (port, model_type) }

class ChatRequest(BaseModel):
    prompt: str

@app.post("/{source}/{model}/{mode}")
async def chat(source: str, model: str, mode: str, request: ChatRequest):
    """Handle both chat and text-based models."""
    model_key = f"{source}/{model}"
    if model_key not in DEPLOYED_MODELS:
        return {"error": f"Model '{model}' from '{source}' is not deployed."}

    port, model_type = DEPLOYED_MODELS[model_key]

    if mode not in ["chat", "completion"]:
        return {"error": "Invalid mode. Use 'chat' or 'completion'."}

    if mode != model_type:
        return {"error": f"Model '{model}' is a '{model_type}' model, cannot use '{mode}' mode."}

    try:
        if source == "ollama":
            response = subprocess.run(
                ["ollama", "run", model],
                input=request.prompt,
                text=True,
                capture_output=True
            )
            return {"response": response.stdout.strip()}

        elif source == "hf":
            model_path = f"hf_models/{model}"
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model_instance = AutoModelForCausalLM.from_pretrained(model_path)
            inputs = tokenizer(request.prompt, return_tensors="pt")
            outputs = model_instance.generate(**inputs)
            return {"response": tokenizer.decode(outputs[0], skip_special_tokens=True)}

    except Exception as e:
        return {"error": str(e)}

def start_server(port: int):
    """Start FastAPI server on a given port."""
    uvicorn.run(app, host="0.0.0.0", port=port)
