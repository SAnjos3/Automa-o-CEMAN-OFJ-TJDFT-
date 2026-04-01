# Requisitos do Sistema - CEMAN Automação

## 1. Visão Geral

Este documento descreve os requisitos funcionais e não funcionais do sistema de automação para Oficiais de Justiça do TJDFT, tendo como base o portal CEMAN (Central de Mandados).

---

## 2. Requisitos Funcionais

### RF01 - Autenticação no CEMAN
- O sistema deve autenticar-se automaticamente no portal CEMAN utilizando credenciais armazenadas de forma segura.
- O sistema deve tratar falhas de autenticação e notificar o responsável.

### RF02 - Extração de Mandados (Scraping)
- O sistema deve acessar a lista de mandados pendentes do Oficial de Justiça.
- O sistema deve baixar os PDFs dos mandados automaticamente.
- O sistema deve identificar o tipo de mandado (citação, intimação, penhora, etc.).

### RF03 - Processamento com Inteligência Artificial
- O sistema deve enviar os PDFs para o modelo Gemini IA para extração estruturada das informações.
- As informações extraídas devem incluir: nome das partes, endereço, número do processo, vara, prazo e tipo de ato.

### RF04 - Gestão via Oracle APEX
- O sistema deve persistir os dados estruturados no banco de dados Oracle APEX.
- O Oficial de Justiça deve conseguir visualizar, filtrar e atualizar o status dos mandados via APEX.
- O sistema deve registrar o histórico de ações realizadas em cada mandado.

### RF05 - Automação de Comunicações via WhatsApp
- O sistema deve enviar notificações via WhatsApp (Evolution API + n8n) para partes e advogados, conforme configurado.
- O sistema deve enviar confirmações de cumprimento de mandado ao Oficial de Justiça responsável.

### RF06 - Geração de Certidões
- O sistema deve gerar automaticamente minutas de certidões com base nos dados do mandado e no resultado do cumprimento.

---

## 3. Requisitos Não Funcionais

### RNF01 - Segurança
- Credenciais de acesso ao CEMAN devem ser armazenadas em variáveis de ambiente ou cofre seguro (ex.: `.env`).
- A comunicação entre os componentes deve ser feita via HTTPS.

### RNF02 - Disponibilidade
- O sistema deve estar disponível durante o horário de expediente do TJDFT (08h às 18h, dias úteis).
- Jobs de scraping devem ser agendados de forma a não sobrecarregar o portal CEMAN.

### RNF03 - Manutenibilidade
- O código deve seguir boas práticas de Python (PEP 8) e ser documentado.
- Os workflows do n8n devem ser exportados em JSON e versionados no repositório.

### RNF04 - Desempenho
- A extração e processamento de um lote de mandados não deve ultrapassar 10 minutos.

---

## 4. Restrições

- O sistema deve operar exclusivamente dentro da rede do TJDFT ou via VPN autorizada.
- O uso da IA Gemini deve respeitar as políticas de privacidade e sigilo processual.
- O envio de mensagens via WhatsApp deve cumprir as normas internas do TJDFT.
