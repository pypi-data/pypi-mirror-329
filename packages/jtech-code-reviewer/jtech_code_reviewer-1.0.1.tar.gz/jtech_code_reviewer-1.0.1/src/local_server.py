#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import os
import logging

from src.core.agents.code_review_agent import CodeReviewAgent
from src.core.generativeai.generative_ia_client import GenerativeIAClient
from src.infra.utils.extract import Extract
from src.infra.config.logging_config import get_logger

# Configuração de logging
logger = get_logger()

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar aplicação
app = FastAPI(title="Code Review Local", version="1.0.0")

# Inicializar agente de revisão
ia_client = GenerativeIAClient()
agent = CodeReviewAgent(ia_client)

class LocalReviewRequest(BaseModel):
    """Modelo para requisição de revisão local."""
    diff: str
    file_name: str | None = None

class ReviewResponse(BaseModel):
    """Modelo para resposta da revisão."""
    suggestions: str
    status: str = "success"

@app.post("/review/local", response_model=ReviewResponse)
async def review_local_changes(request: LocalReviewRequest):
    """
    Endpoint para revisar alterações locais.
    
    Args:
        request: LocalReviewRequest contendo o diff e opcionalmente o nome do arquivo
    
    Returns:
        ReviewResponse com as sugestões da revisão
    
    Raises:
        HTTPException: Se houver erro durante o processo de revisão
    """
    try:
        logger.info("Iniciando revisão de código local")
        
        # Preparar dados para revisão
        review_data = {
            "diff": request.diff,
            "new_path": request.file_name or "local_changes"
        }
        
        # Realizar revisão
        review = agent.review_code(review_data)
        
        # Extrair feedback relevante
        feedback = Extract.extract_review_content(review)
        
        logger.info("Revisão de código concluída com sucesso")
        
        return ReviewResponse(
            suggestions=feedback
        )
        
    except Exception as e:
        logger.error(f"Erro durante revisão de código: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar revisão: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Endpoint para verificar se o serviço está funcionando."""
    return {"status": "healthy"}

def start_server():
    """Inicia o servidor FastAPI."""
    port = int(os.getenv("PORT", 3000))
    host = os.getenv("HOST", "127.0.0.1")
    
    logger.info(f"Iniciando servidor na porta {port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    start_server()