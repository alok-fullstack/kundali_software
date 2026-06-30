"""
Chat API route.

POST /api/chat - Chat with kundali assistant about a generated kundali.
"""

import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException, status

# Ensure parent directories are in path
backend_dir = Path(__file__).resolve().parent.parent.parent
kundali_dir = backend_dir.parent
if str(kundali_dir) not in sys.path:
    sys.path.insert(0, str(kundali_dir))

from api.models import ChatRequest, ChatResponse, ErrorResponse
from src.chat_assistant import KundaliChatAssistant
from api.routes.kundali import get_kundali

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Kundali not found"}
    },
    summary="Chat with Kundali Assistant",
    description="Ask questions about a generated kundali in Hindi or English."
)
async def chat_with_kundali(request: ChatRequest) -> ChatResponse:
    """
    Chat with the Kundali AI Assistant.

    The assistant can answer questions about:
    - Career predictions
    - Marriage analysis (including Manglik dosh)
    - Children/Santan predictions
    - Health analysis
    - Wealth/Money predictions
    - Dasha analysis (current and future periods)
    - Planet effects
    - Remedies and lucky elements
    - Sade Sati, Kaal Sarp Dosh, etc.

    Questions can be asked in Hindi (Hinglish) or English.

    Example questions:
    - "Career ke baare mein batao"
    - "Shaadi kab hogi?"
    - "Health kaisi rahegi?"
    - "Shani ka prabhav kya hai?"
    - "What are my lucky colors?"
    """
    try:
        # Get kundali from store
        kundali = get_kundali(request.kundali_id)

        # Create assistant and get response
        assistant = KundaliChatAssistant(kundali)
        answer = assistant.get_response(request.question)

        return ChatResponse(
            success=True,
            answer=answer,
            kundali_id=request.kundali_id
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )
