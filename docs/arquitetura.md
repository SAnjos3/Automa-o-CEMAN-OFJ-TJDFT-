# Arquitetura do Sistema - CEMAN Automação

## 1. Visão Geral da Arquitetura

O sistema adota uma arquitetura **híbrida**, combinando automação web com Python/Playwright, uma API intermediária em FastAPI, um banco de dados Oracle APEX e orquestração de workflows via n8n.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CEMAN (Portal Web)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Playwright (Scraping)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               src/scraper  (Python + Playwright)                │
│   - Login automático                                            │
│   - Listagem de mandados                                        │
│   - Download de PDFs                                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP POST (PDF / metadados)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               src/backend  (FastAPI)                            │
│   - Recebe PDFs do scraper                                      │
│   - Envia para Gemini IA (parsing)                              │
│   - Persiste dados no Oracle APEX                               │
│   - Expõe endpoints REST para o n8n                             │
└──────────┬───────────────────────────────┬──────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐     ┌────────────────────────────────────┐
│  Oracle APEX (DB)    │     │         n8n (Workflows)            │
│  - Tabelas DDL       │     │  - Trigger via Webhook             │
│  - Relatórios APEX   │     │  - Envia WhatsApp (Evolution API)  │
│  - Gestão de status  │     │  - Lógica de negócio adicional     │
└──────────────────────┘     └────────────────────────────────────┘
```

---

## 2. Componentes

### 2.1 Scraper (Python + Playwright)
- **Localização:** `src/scraper/`
- **Responsabilidade:** Acessar o portal CEMAN, autenticar, listar e baixar mandados em PDF.
- **Tecnologia:** Python 3.11+, Playwright (modo headless).
- **Agendamento:** Cron job ou trigger manual via API.

### 2.2 API Backend (FastAPI)
- **Localização:** `src/backend/`
- **Responsabilidade:** Intermediar a comunicação entre o scraper, a IA, o banco de dados e o n8n.
- **Endpoints principais:**
  - `POST /mandados/processar` — recebe PDF e dispara parsing via Gemini IA.
  - `GET /mandados` — lista mandados armazenados.
  - `PATCH /mandados/{id}/status` — atualiza o status de um mandado.
  - `POST /webhook/n8n` — recebe eventos do n8n.

### 2.3 Banco de Dados (Oracle APEX)
- **Localização:** `src/database/`
- **Responsabilidade:** Armazenar mandados, partes, histórico de ações e usuários.
- **Scripts:** DDL Oracle SQL para criação de tabelas e sequências.

### 2.4 Workflows n8n
- **Localização:** `src/n8n/`
- **Responsabilidade:** Orquestrar notificações WhatsApp e outros fluxos automatizados.
- **Formato:** Arquivos JSON exportados do n8n.

### 2.5 Infraestrutura (Docker)
- **Localização:** `infra/`
- **Responsabilidade:** Prover Evolution API e n8n em contêineres Docker.
- **Arquivo principal:** `docker-compose.yml`.

---

## 3. Fluxo de Dados Principal

```
1. Scraper acessa o CEMAN e baixa PDFs dos mandados.
2. Scraper envia PDF para o endpoint POST /mandados/processar do Backend.
3. Backend envia o PDF para a API Gemini IA e extrai dados estruturados (JSON).
4. Backend persiste os dados no Oracle APEX via REST ou driver Oracle.
5. Backend dispara webhook no n8n com os dados do mandado.
6. n8n processa o workflow e envia mensagem WhatsApp via Evolution API.
7. Oficial de Justiça visualiza e gerencia os mandados no portal Oracle APEX.
```

---

## 4. Segurança

- Variáveis sensíveis (senhas, chaves de API) armazenadas em `.env` (nunca versionadas).
- Comunicação interna via rede Docker isolada.
- Autenticação JWT nos endpoints da FastAPI.
