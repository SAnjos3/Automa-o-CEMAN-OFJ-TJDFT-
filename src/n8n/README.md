# Workflows n8n — CEMAN Automação

Esta pasta contém os arquivos JSON de exportação dos workflows do **n8n** utilizados no projeto.

## Como importar um workflow no n8n

1. Acesse o painel do n8n.
2. Clique em **"Workflows"** no menu lateral.
3. Clique em **"Import from File"**.
4. Selecione o arquivo `.json` desejado desta pasta.
5. Configure as credenciais necessárias (Evolution API, APEX REST) antes de ativar.

## Workflows disponíveis

| Arquivo | Descrição |
|---|---|
| `notificacao_novo_mandado.json` | Envia WhatsApp ao Oficial quando um novo mandado é inserido. |
| `confirmacao_cumprimento.json` | Processa a resposta do Oficial via WhatsApp e atualiza o APEX. |

> **Atenção:** Os arquivos JSON **não devem conter credenciais** (chaves de API, senhas, tokens). Configure as credenciais diretamente na interface do n8n após a importação.
