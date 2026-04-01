# 📋 Especificação de Requisitos: Projeto CEMAN-Automação

Este documento detalha as necessidades funcionais e de qualidade para o sistema de automação destinado aos Oficiais de Justiça do TJDFT.

---

## 1. Requisitos Funcionais (RF)

### 🔑 Autenticação e Acesso
* **RF01 - Login Unificado:** O sistema deve possuir uma interface de login própria para o Oficial de Justiça no Oracle APEX.
* **RF02 - Integração MFA:** A aplicação deve solicitar o código do *Microsoft Authenticator* e replicá-lo no portal CEMAN para concluir o acesso automatizado.
* **RF03 - Persistência de Sessão:** O sistema deve gerenciar a sessão do navegador para evitar logouts durante o processamento de lotes.

### 🛰️ Captura e Processamento (Scraping & IA)
* **RF04 - Sincronização de Mesa:** Acessar a "Mesa de Trabalho" do CEMAN e listar todos os mandados pendentes.
* **RF05 - Extração de Metadados Web:** Capturar Nº do Processo, Nome da Parte, Endereço e Data de Distribuição diretamente da interface.
* **RF06 - Extração de Metadados PDF (IA):** Utilizar IA para analisar o PDF e identificar:
    * Número de Telefone (WhatsApp).
    * Natureza do Mandado (Citação, Intimação, Penhora, etc.).
    * Grau de Urgência (Baixo, Médio, Alto).
    * Resumo Executivo do objetivo do mandado.
* **RF07 - Gestão Multidestinatários:** Caso um mandado possua múltiplos alvos, o sistema deve criar trilhas de contato independentes para cada um.

### 💬 Agente de Comunicação (n8n + WhatsApp)
* **RF08 - Orquestração de Conversa:** O agente deve realizar a saudação oficial, verificar a identidade (ex: confirmação de CPF) e enviar o mandado em PDF.
* **RF09 - Fuso Horário Comercial:** Disparar novas mensagens apenas entre 08:00 e 18:00.
* **RF10 - Resposta Automática de Suporte:** Fora do horário comercial, responder mensagens recebidas informando a indisponibilidade momentânea do Oficial.
* **RF11 - Transbordo Manual:** Fornecer link direto para o chat do WhatsApp caso a IA não consiga concluir o protocolo ou o usuário peça suporte humano.

### 📄 Provas e Finalização
* **RF12 - Registro de Fé Pública (Prints):** Realizar capturas de tela automáticas da confirmação de leitura e mensagens-chave.
* **RF13 - Log de Eventos:** Salvar histórico completo da interação (texto e timestamps) no banco de dados.
* **RF14 - Geração de Certidão:** Preencher rascunho de certidão com dados da diligência para revisão do Oficial.
* **RF15 - Lista Negra (Blacklist):** Permitir o bloqueio de números específicos para evitar automações futuras.

---

## 2. Requisitos Não Funcionais (RNF)

* **RNF01 - Segurança (LGPD):** Dados sensíveis de partes processuais devem ser armazenados com criptografia e acesso restrito.
* **RNF02 - Usabilidade:** A interface no Oracle APEX deve ser otimizada para visualização rápida em desktop, com foco em ações em massa.
* **RNF03 - Desempenho:** O processamento de IA para extração de dados de cada PDF não deve exceder 15 segundos.
* **RNF04 - Disponibilidade:** O motor de comunicação (n8n/Evolution API) deve operar 24/7 para processar respostas e logs.

---

## ⚖️ Regras de Negócio (RN)

* **RN01:** O envio do mandado só deve ocorrer após a confirmação positiva de identidade pelo alvo.
* **RN02:** Mandados marcados como "Urgentes" pela IA devem aparecer no topo da lista de prioridades no Dashboard.
* **RN03:** Se um número for identificado como "Fixo" ou "Sem WhatsApp", o status deve ser alterado imediatamente para "Diligência Física Necessária".