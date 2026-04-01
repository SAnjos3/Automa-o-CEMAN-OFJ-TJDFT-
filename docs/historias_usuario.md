# Histórias de Usuário - CEMAN Automação

## Épico 1: Extração Automática de Mandados

### HU-01 — Login Automático no CEMAN
**Como** Oficial de Justiça,
**Quero** que o sistema faça login automaticamente no portal CEMAN,
**Para que** eu não precise inserir minhas credenciais manualmente a cada sessão.

**Critérios de Aceitação:**
- [ ] O sistema lê as credenciais de uma variável de ambiente segura.
- [ ] O sistema realiza o login com sucesso e mantém a sessão ativa.
- [ ] Em caso de falha no login, o sistema registra o erro e envia uma notificação.

---

### HU-02 — Download Automático de Mandados
**Como** Oficial de Justiça,
**Quero** que o sistema baixe automaticamente os PDFs dos mandados pendentes,
**Para que** eu economize tempo e evite erros manuais.

**Critérios de Aceitação:**
- [ ] O sistema lista todos os mandados com status "Pendente" no CEMAN.
- [ ] O sistema baixa os PDFs de cada mandado para uma pasta local temporária.
- [ ] O sistema registra quais mandados foram baixados com sucesso e quais falharam.

---

## Épico 2: Processamento com Inteligência Artificial

### HU-03 — Extração de Dados do Mandado via IA
**Como** Oficial de Justiça,
**Quero** que as informações do mandado sejam extraídas automaticamente do PDF,
**Para que** eu não precise digitar manualmente os dados de cada mandado.

**Critérios de Aceitação:**
- [ ] O sistema envia o PDF ao modelo Gemini IA.
- [ ] A IA retorna um JSON com: número do processo, partes, endereço, vara, prazo e tipo de ato.
- [ ] Os dados extraídos são validados antes de serem persistidos.

---

## Épico 3: Gestão via Oracle APEX

### HU-04 — Visualização dos Mandados no APEX
**Como** Oficial de Justiça,
**Quero** visualizar todos os meus mandados em uma tela do Oracle APEX,
**Para que** eu tenha uma visão centralizada e organizada do meu trabalho.

**Critérios de Aceitação:**
- [ ] A tela APEX exibe lista de mandados com filtros por status, data e tipo.
- [ ] É possível clicar em um mandado para ver seus detalhes completos.
- [ ] O sistema exibe o histórico de ações de cada mandado.

---

### HU-05 — Atualização de Status do Mandado
**Como** Oficial de Justiça,
**Quero** atualizar o status de um mandado diretamente pelo APEX,
**Para que** o sistema reflita a situação real do cumprimento.

**Critérios de Aceitação:**
- [ ] O Oficial pode alterar o status para: Pendente, Em Cumprimento, Cumprido, Não Localizado.
- [ ] A alteração de status dispara automaticamente um workflow no n8n.
- [ ] O histórico da mudança de status é registrado com data, hora e usuário.

---

## Épico 4: Comunicação via WhatsApp

### HU-06 — Notificação de Novo Mandado via WhatsApp
**Como** Oficial de Justiça,
**Quero** receber uma notificação no WhatsApp quando um novo mandado for atribuído a mim,
**Para que** eu seja informado imediatamente, sem precisar consultar o portal.

**Critérios de Aceitação:**
- [ ] O n8n detecta a inserção de um novo mandado no APEX.
- [ ] Uma mensagem é enviada via Evolution API para o WhatsApp do Oficial de Justiça.
- [ ] A mensagem contém: número do processo, tipo de ato, nome da parte e endereço.

---

### HU-07 — Confirmação de Cumprimento de Mandado
**Como** Oficial de Justiça,
**Quero** confirmar o cumprimento de um mandado via WhatsApp,
**Para que** o sistema seja atualizado sem que eu precise acessar o APEX.

**Critérios de Aceitação:**
- [ ] O Oficial de Justiça responde à mensagem WhatsApp com um código de confirmação.
- [ ] O n8n processa a resposta e atualiza o status do mandado no APEX.
- [ ] Uma certidão de cumprimento é gerada automaticamente.

---

## Épico 5: Geração de Certidões

### HU-08 — Geração Automática de Certidão
**Como** Oficial de Justiça,
**Quero** que o sistema gere automaticamente a minuta da certidão de cumprimento,
**Para que** eu economize tempo na elaboração de documentos.

**Critérios de Aceitação:**
- [ ] Após a confirmação de cumprimento, o sistema gera uma minuta de certidão em PDF.
- [ ] A certidão contém todos os dados obrigatórios exigidos pelo TJDFT.
- [ ] O arquivo é disponibilizado no APEX para revisão e assinatura digital pelo Oficial.
