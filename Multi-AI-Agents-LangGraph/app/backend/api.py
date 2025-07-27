
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import Settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger = get_logger(__name__)

app = FastAPI(title="Multi AI Agent")


class RequestState(BaseModel):
    model_name: str 
    system_prompt: str
    messages: List[str]
    allow_search: bool


@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f"Received chat request: {request.model_name}")
    if request.model_name not in Settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name provided")
        raise HTTPException(status_code=400, detail="Invalid model name provided")

    try:
        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Response generated successfully from AI Agent: {request.model_name}")

        return {'response': response}
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, 
                            detail=str(CustomException("Failed to get AI response", 
                                                       error_detail=e)))