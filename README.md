# CEMAN Automação — Oficiais de Justiça do TJDFT

> Sistema de automação híbrido para Oficiais de Justiça do Tribunal de Justiça do Distrito Federal e Territórios (TJDFT), integrando o portal CEMAN, Oracle APEX, n8n e Evolution API.

---

## Descrição

Este projeto visa eliminar as tarefas manuais e repetitivas dos **Oficiais de Justiça do TJDFT**, automatizando desde a captura de mandados no portal **CEMAN** (Central de Mandados) até a comunicação via **WhatsApp** e a geração automática de certidões.

O sistema realiza o seguinte fluxo de trabalho de ponta a ponta:

```
Scraping (CEMAN) → IA Parsing (Gemini) → Gestão (Oracle APEX) → Automação WhatsApp (n8n + Evolution API) → Produção das Certidões (Coleta Automática de Provas)
```

---

## Estrutura do Projeto

```
ceman-automacao/
├── docs/                          # Documentação do projeto
│   ├── requisitos.md              # Requisitos funcionais e não funcionais
│   ├── arquitetura.md             # Arquitetura e diagramas do sistema
│   └── historias_usuario.md       # Histórias de usuário (BDD)
│
├── src/
│   ├── scraper/                   # Scripts Python (Playwright) para o CEMAN
│   │   └── ceman_scraper.py       # Login, listagem e download de mandados
│   │
│   ├── backend/                   # API FastAPI (ponte entre os componentes)
│   │   └── main.py                # Endpoints REST e integração com Gemini IA
│   │
│   ├── database/                  # Scripts SQL para Oracle APEX
│   │   └── ddl_ceman.sql          # DDL: tabelas, índices e triggers
│   │
│   └── n8n/                       # Exportações de workflows do n8n (JSON)
│       └── README.md              # Instruções de importação
│
├── infra/                         # Infraestrutura (Docker)
│   ├── docker-compose.yml         # Evolution API + n8n
│   └── .env.example               # Modelo de variáveis de ambiente
│
└── README.md                      # Este arquivo
```

---

## Tecnologias Utilizadas

| Tecnologia | Papel no sistema |
|---|---|
| **Python 3.11+** | Linguagem principal do scraper e da API backend |
| **Playwright** | Automação web headless para acesso ao portal CEMAN |
| **FastAPI** | API REST que integra todos os componentes |
| **Oracle APEX** | Banco de dados e interface de gestão dos mandados |
| **n8n** | Orquestrador de workflows de automação |
| **Evolution API** | Gateway para envio e recebimento de mensagens WhatsApp |
| **Gemini IA** | Modelo de IA do Google para extração de dados dos PDFs |
| **Docker / Docker Compose** | Contêinerização da Evolution API e do n8n |

---

## Fluxo de Trabalho

```
1. SCRAPING
   O script Python (Playwright) acessa o portal CEMAN, autentica com as credenciais do Oficial,
   baixa os PDFs dos mandados pendentes e extrai informações úteis da página.

2. IA PARSING
   Os PDFs são enviados para a API Gemini (Google AI), que extrai
   automaticamente os dados estruturados: processo, partes, endereço, vara, prazo.

3. GESTÃO APEX
   Os dados extraídos são persistidos no Oracle APEX via API REST.
   O Oficial de Justiça acessa o portal APEX para visualizar gráficos de prograssão e
   gerir os mandados atuais.

4. AUTOMAÇÃO WHATSAPP VIA n8n
   Ao selecionar um mandado (ou vários), o backend dispara um webhook no n8n.
   O n8n processa o workflow e executa intimação via WhatsApp usando a Evolution API.
   O Oficial pode confirmar cumprimentos pelo WhatsApp.
```

---

## Configuração e Execução

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Acesso à rede do TJDFT (ou VPN autorizada)
- Chave de API do Gemini (Google AI Studio)

### 1. Clonar o repositório

```bash
git clone https://github.com/SAnjos3/Automa-o-CEMAN-OFJ-TJDFT-.git
cd Automa-o-CEMAN-OFJ-TJDFT-
```

### 2. Configurar variáveis de ambiente

```bash
cp infra/.env.example infra/.env
# Edite o arquivo infra/.env com suas credenciais reais
```

### 3. Subir a infraestrutura (Evolution API + n8n)

```bash
cd infra
docker compose --env-file .env up -d
```

- **n8n** estará disponível em: `http://localhost:5678`
- **Evolution API** estará disponível em: `http://localhost:8080`

### 4. Instalar dependências Python

```bash
pip install fastapi uvicorn httpx playwright
playwright install chromium
```

### 5. Iniciar a API Backend

```bash
cd src/backend
uvicorn main:app --reload --port 8000
```

A documentação interativa (Swagger) estará em: `http://localhost:8000/docs`

### 6. Executar o scraper manualmente

```bash
cd src/scraper
python ceman_scraper.py
```

### 7. Configurar o banco de dados Oracle APEX

Execute o script DDL no seu ambiente Oracle APEX:

```sql
-- No SQL Workshop do Oracle APEX, execute:
@src/database/ddl_ceman.sql
```

---

## Documentação

- [Requisitos do Sistema](docs/requisitos.md)
- [Arquitetura do Sistema](docs/arquitetura.md)
- [Histórias de Usuário](docs/historias_usuario.md)
- [Workflows n8n](src/n8n/README.md)

