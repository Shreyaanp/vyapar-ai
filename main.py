from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json
import time
from prodAI import process_prompt
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str
    description: str = None
    variation: str = None
    pricing: float = None

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Product Description API"}

@app.post("/process/")
async def process_content(request: PromptRequest):
    try:
        # Combine all the product information into a single prompt
        final_input = f"Product Name: {request.prompt}, Description: {request.description or 'N/A'}, Variation: {request.variation or 'N/A'}, Pricing: {request.pricing or 'N/A'}"
        
        start_time = time.time()
        raw_result = process_prompt(final_input)
        end_time = time.time()
        
        
        if not isinstance(raw_result, str):
            raise ValueError(f"Unexpected format: expected a string but got {type(raw_result)}")

        json_string = raw_result.replace("```json\n", "").replace("\n```", "")

        data = json.loads(json_string)
        
        return data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
