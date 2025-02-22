from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
from bhumi.base_client import BaseLLMClient, LLMConfig
import os
import dotenv
from groq import AsyncGroq
import json

dotenv.load_dotenv()
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize clients
api_key = os.getenv("GROQ_API_KEY")
bhumi_config = LLMConfig(
    api_key=api_key,
    model="groq/mixtral-8x7b-32768",
    debug=True,
    max_retries=3,
    max_tokens=500
)
bhumi_client = BaseLLMClient(bhumi_config)
groq_client = AsyncGroq(api_key=api_key)

@app.get("/")
async def get():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws/bhumi")
async def websocket_bhumi_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        try:
            # Receive prompt from frontend
            prompt = await websocket.receive_text()
            
            # Get streaming response from Bhumi
            stream = await bhumi_client.completion([
                {"role": "user", "content": prompt}
            ], stream=True)
            
            async for chunk in stream:
                await websocket.send_text(json.dumps({
                    "type": "chunk",
                    "content": chunk
                }))
                
            await websocket.send_text(json.dumps({
                "type": "done"
            }))
            
        except Exception as e:
            print(f"Error: {e}")
            await websocket.close()
            break

@app.websocket("/ws/groq")
async def websocket_groq_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        try:
            # Receive prompt from frontend
            prompt = await websocket.receive_text()
            
            # Get streaming response from raw Groq
            completion = await groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="mixtral-8x7b-32768",
                stream=True
            )
            
            async for chunk in completion:
                if chunk.choices[0].delta.content:
                    await websocket.send_text(json.dumps({
                        "type": "chunk",
                        "content": chunk.choices[0].delta.content
                    }))
            
            await websocket.send_text(json.dumps({
                "type": "done"
            }))
            
        except Exception as e:
            print(f"Error: {e}")
            await websocket.close()
            break

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 