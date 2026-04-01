"""
API Backend — CEMAN Automação

Ponte entre o scraper Python, a IA Gemini, o Oracle APEX e os workflows n8n.
Construída com FastAPI.
"""

import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="CEMAN Automação API",
    description="API de integração para o sistema de automação dos Oficiais de Justiça do TJDFT.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost").split(",")
        if origin.strip()
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Configurações via variáveis de ambiente
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
APEX_BASE_URL = os.getenv("APEX_BASE_URL", "")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")


# ---------------------------------------------------------------------------
# Modelos Pydantic
# ---------------------------------------------------------------------------
class MandadoStatus(BaseModel):
    status: str


class MandadoDados(BaseModel):
    id: str
    processo: str
    tipo: str
    partes: str | None = None
    endereco: str | None = None
    vara: str | None = None
    prazo: str | None = None
    status: str = "Pendente"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/", summary="Health check")
async def health_check():
    """Verifica se a API está operacional."""
    return {"status": "ok", "servico": "CEMAN Automação API"}


@app.post("/mandados/processar", summary="Processa um PDF de mandado via Gemini IA")
async def processar_mandado(arquivo: UploadFile = File(...)):
    """
    Recebe o PDF de um mandado, envia para o Gemini IA para extração de dados
    e persiste o resultado no Oracle APEX.
    """
    conteudo = await arquivo.read()

    dados_extraidos = await _extrair_dados_gemini(conteudo)

    await _persistir_apex(dados_extraidos)
    await _notificar_n8n(dados_extraidos)

    return {"mensagem": "Mandado processado com sucesso.", "dados": dados_extraidos}


@app.get("/mandados", summary="Lista todos os mandados")
async def listar_mandados():
    """Retorna a lista de mandados armazenados no Oracle APEX."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{APEX_BASE_URL}/mandados")
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao consultar o Oracle APEX.")
        return resp.json()


@app.patch("/mandados/{mandado_id}/status", summary="Atualiza o status de um mandado")
async def atualizar_status(mandado_id: str, payload: MandadoStatus):
    """Atualiza o status de um mandado no Oracle APEX e notifica o n8n."""
    async with httpx.AsyncClient() as client:
        resp = await client.patch(
            f"{APEX_BASE_URL}/mandados/{mandado_id}",
            json={"status": payload.status},
        )
        if resp.status_code not in (200, 204):
            raise HTTPException(status_code=502, detail="Erro ao atualizar o Oracle APEX.")

    await _notificar_n8n({"id": mandado_id, "status": payload.status})
    return {"mensagem": f"Status do mandado {mandado_id} atualizado para '{payload.status}'."}


@app.post("/webhook/n8n", summary="Recebe eventos do n8n")
async def webhook_n8n(payload: dict):
    """Endpoint para receber callbacks e eventos enviados pelo n8n."""
    # Processar evento recebido (ex.: confirmação de WhatsApp)
    return {"mensagem": "Evento recebido com sucesso.", "payload": payload}


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------


async def _extrair_dados_gemini(pdf_bytes: bytes) -> dict:
    """Envia o conteúdo do PDF para o Gemini IA e retorna os dados estruturados."""
    import base64

    pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Extraia do documento judicial as seguintes informações em JSON: "
                            "numero_processo, tipo_ato, nome_partes, endereco, vara, prazo."
                        )
                    },
                    {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}},
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json=body,
            timeout=60,
        )
        resp.raise_for_status()

    candidatos = resp.json().get("candidates", [])
    if not candidatos:
        raise HTTPException(status_code=502, detail="Gemini IA não retornou dados.")

    import json
    texto = candidatos[0]["content"]["parts"][0]["text"]
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return {"texto_bruto": texto}


async def _persistir_apex(dados: dict) -> None:
    """Persiste os dados extraídos no Oracle APEX via REST."""
    if not APEX_BASE_URL:
        return
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{APEX_BASE_URL}/mandados", json=dados, timeout=30)
        if resp.status_code not in (200, 201):
            raise HTTPException(
                status_code=502,
                detail=f"Falha ao persistir dados no Oracle APEX: HTTP {resp.status_code}.",
            )


async def _notificar_n8n(dados: dict) -> None:
    """Dispara um webhook no n8n com os dados do mandado."""
    if not N8N_WEBHOOK_URL:
        return
    async with httpx.AsyncClient() as client:
        resp = await client.post(N8N_WEBHOOK_URL, json=dados, timeout=30)
        if resp.status_code not in (200, 201):
            # Registra a falha mas não interrompe o fluxo principal
            import logging
            logging.getLogger(__name__).warning(
                "Falha ao notificar o n8n: HTTP %s — %s", resp.status_code, resp.text
            )
