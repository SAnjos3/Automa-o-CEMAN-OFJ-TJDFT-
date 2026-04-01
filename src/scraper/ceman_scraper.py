"""
Módulo de scraping do CEMAN.

Utiliza Playwright para autenticar no portal CEMAN e baixar os PDFs dos mandados pendentes.
"""

import os
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright, Page


CEMAN_URL = os.getenv("CEMAN_URL", "https://ceman.tjdft.jus.br")
CEMAN_USUARIO = os.getenv("CEMAN_USUARIO", "")
CEMAN_SENHA = os.getenv("CEMAN_SENHA", "")
DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "/tmp/mandados"))


async def login(page: Page) -> None:
    """Realiza o login no portal CEMAN."""
    await page.goto(CEMAN_URL)
    await page.fill('input[name="usuario"]', CEMAN_USUARIO)
    await page.fill('input[name="senha"]', CEMAN_SENHA)
    await page.click('button[type="submit"]')
    await page.wait_for_load_state("networkidle")


async def listar_mandados(page: Page) -> list[dict]:
    """Retorna a lista de mandados pendentes disponíveis no portal."""
    await page.goto(f"{CEMAN_URL}/mandados/pendentes")
    await page.wait_for_load_state("networkidle")

    mandados = []
    linhas = await page.query_selector_all("table.mandados tbody tr")
    for linha in linhas:
        colunas = await linha.query_selector_all("td")
        if len(colunas) >= 3:
            mandados.append(
                {
                    "id": await colunas[0].inner_text(),
                    "processo": await colunas[1].inner_text(),
                    "tipo": await colunas[2].inner_text(),
                }
            )
    return mandados


async def baixar_pdf(page: Page, mandado_id: str) -> Path:
    """Baixa o PDF de um mandado específico e retorna o caminho do arquivo."""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    destino = DOWNLOAD_DIR / f"{mandado_id}.pdf"

    async with page.expect_download() as download_info:
        await page.goto(f"{CEMAN_URL}/mandados/{mandado_id}/pdf")
    download = await download_info.value
    await download.save_as(destino)
    return destino


async def executar_scraping() -> list[dict]:
    """
    Fluxo principal de scraping:
    1. Faz login no CEMAN.
    2. Lista mandados pendentes.
    3. Baixa o PDF de cada mandado.
    Retorna lista com metadados e caminho do PDF.
    """
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await login(page)
        mandados = await listar_mandados(page)

        for mandado in mandados:
            try:
                caminho_pdf = await baixar_pdf(page, mandado["id"])
                resultados.append({**mandado, "pdf": str(caminho_pdf), "erro": None})
            except (TimeoutError, OSError) as exc:
                resultados.append({**mandado, "pdf": None, "erro": str(exc)})

        await browser.close()

    return resultados


if __name__ == "__main__":
    resultados = asyncio.run(executar_scraping())
    for r in resultados:
        print(r)
