from fastapi import FastAPI, WebSocket
import asyncio
import sys
from io import StringIO
import contextlib
import json
import logging
import traceback
from datetime import datetime
from termcolor import colored

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="QuantGPT Local Runner")

# Global namespace for code execution
GLOBALS = {
    '__name__': '__main__',
    'print': print
}

@app.get("/")
async def root():
    return {"message": "Hello from QuantGPT Local Runner"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        logger.info(colored("Client connected successfully", "green"))
        
        while True:
            try:
                data = await websocket.receive_text()
                
                try:
                    parsed_data = json.loads(data)
                    code = parsed_data["code"]
                    
                    stdout = StringIO()
                    with contextlib.redirect_stdout(stdout):
                        try:
                            compiled_code = compile(code, '<string>', 'exec')
                            exec(compiled_code, GLOBALS)
                            output = stdout.getvalue()
                            
                            await websocket.send_json({
                                "status": "completed",
                                "content": output or "Code executed successfully",
                                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                        except Exception as e:
                            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
                            await websocket.send_json({
                                "status": "failed",
                                "content": error_msg,
                                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                except json.JSONDecodeError as e:
                    await websocket.send_json({
                        "status": "failed",
                        "content": f"Invalid JSON: {str(e)}",
                        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                except KeyError:
                    await websocket.send_json({
                        "status": "failed",
                        "content": "Missing 'code' in request",
                        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")
                await websocket.send_json({
                    "status": "failed",
                    "content": f"Server error: {str(e)}",
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                break
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")